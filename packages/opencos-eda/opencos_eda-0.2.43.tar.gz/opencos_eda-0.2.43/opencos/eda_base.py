import argparse
import copy
import glob
import subprocess
import os
import queue
import re
import shutil
import shlex
import signal
import sys
import threading
import time
from pathlib import Path

import opencos
from opencos import seed, deps_helpers, util, files
from opencos import eda_config
from opencos.deps_helpers import get_deps_markup_file, deps_markup_safe_load


def print_base_help() -> None:
    '''Prints help() information from other argparsers we use, without "usage"'''
    # using bare 'print' here, since help was requested, avoids --color and --quiet
    print(util.get_argparser_short_help())
    print(eda_config.get_argparser_short_help())
    print(get_argparser_short_help())


def get_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog='eda options', add_help=False, allow_abbrev=False)
    parser.add_argument('-q', '--quit', action='store_true',
                        help='For interactive mode (eda called with no options, command, or targets)')
    parser.add_argument('--exit', action='store_true', help='same as --quit')
    parser.add_argument('-h', '--help', action='store_true')

    # Note - these top level eda.py args, that aren't from eda_config.py or util.py, need to
    # be fed back into CommandMulti or CommandSweep, since they re-invoke eda.
    parser.add_argument('--tool', type=str, default=None,
                        help='Tool to use for this command, such as: modelsim_ase, verilator,' \
                        + ' modelsim_ase=/path/to/bin/vsim, verilator=/path/to/bin/verilator')
    parser.add_argument('--eda-safe', action='store_true',
                        help='disable all DEPS file deps shell commands, overrides values from --config-yml')
    return parser


def get_argparser_short_help() -> str:
    return util.get_argparser_short_help(parser=get_argparser())


def get_eda_exec(command:str=''):
    # NOTE(drew): This is kind of flaky. 'eda multi' reinvokes 'eda'. But the executable for 'eda'
    # is one of:
    # 1. pip3 install opencos-eda
    #    -- script 'eda', installed from PyPi
    # 2. pip3 uninstall .; python3 -m build; pip3 install
    #    -- script 'eda' but installed from local.
    # 2. (opencos repo)/bin/eda - a python wrapper to link to (opencos repo)/opencos/eda.py (package)
    #    packages cannot be run standalone, they need to be called as: python3 -m opencos.eda,
    #    and do not work with relative paths. This only works if env OC_ROOT is set or can be found.
    # 3. If you ran 'source bin/addpath' then you are always using the local (opencos repo)/bin/eda
    eda_path = shutil.which('eda')
    if not eda_path:
        # Can we run from OC_ROOT/bin/eda?
        oc_root = util.get_oc_root()
        if not oc_root:
            util.error(f"Need 'eda' in our path to run 'eda {command}', could not find env OC_ROOT, {eda_path=}, {oc_root=}")
        else:
            bin_eda = os.path.join(oc_root, 'bin', 'eda')
            if not os.path.exists(bin_eda):
                util.error(f"Need 'eda' in our path to run 'eda {command}', cound not find bin/, {eda_path=}, {oc_root=}, {bin_eda=}")
            else:
                util.info(f"'eda' not in path, using {bin_eda=} for 'eda' {command} executable")
                eda_path = os.path.abspath(bin_eda)

    return eda_path


def which_tool(command, config):
    '''Returns which tool will be used for a command, given the command_handlers in config dict.'''
    from opencos import eda_tool_helper
    if config is None:
        util.error(f'which_tool({command=}) called w/out config')
    if not command in config.get('command_handler', {}):
        util.error("which_tool called with invalid command?")

    # Note: we could create a throw-away Command object using config, and check its
    # args['tool']:
    #    cmd_obj = config['command_handler'][command](config=config)
    #    return cmd_obj.args.get('tool', None)
    # But that has side effects and prints a lot of garbage, and does a lot
    # of loading and setting values to create that throw away Command object.

    # Instead, we'll directly look up at the class _TOOL w/out creating the obj.
    tool = getattr(config['command_handler'][command], '_TOOL', None)
    return tool


class Tool:
    '''opencos.eda_base.Tool is a base class used by opencos.tools.<name>.

    If you do not have a config (dict) for the contructor, please use Tool(config={})'''

    error = util.error # use that module's method
    _TOOL = '' # this is the only place a class._TOOL should be set to non-empty str
    _URL = None
    _EXE = None

    def __init__(self, config: dict):
        # Because Command child classes (CommandSimVerilator, for example), will
        # inherit both Command and Tool classes, we'd like them to reference
        # a Command object's self.args instead of the class Tool.args. Safely create it
        # if it doesn't exist:
        self._VERSION = None
        if getattr(self, 'args', None) is None:
            self.args = {}
        if getattr(self, 'args_help', None) is None:
            self.args_help = {}
        if getattr(self, 'defines', None) is None:
            self.defines = {}
        self.args.update({
            'tool':   self._TOOL, # Set for all derived classes.
        })
        self.args_help.update({
            'tool': 'Tool to use for this command, such as: verilator',
        })
        # update self._EXE if config says to:
        self.set_exe(config)
        self.get_versions()

        if getattr(self, 'set_tool_config_from_config', None):
            # Hook for classes like CommandSim that have a Tool derived class attached:
            # have the Tool constructor run set_tool_config_from_config(), otherwise
            # every derived class will have to do this.
            # Allows command handlers to make thier own customizations from --config-yaml=YAML.
            self.set_tool_config_from_config()

    def set_exe(self, config: dict) -> None:
        if self._TOOL and self._TOOL in config.get('auto_tools_order', [{}])[0]:
            exe = config.get('auto_tools_order', [{}])[0][self._TOOL].get('exe', '')
            if exe and type(exe) is list:
                exe = exe[0] # pick first
            if exe and exe != self._EXE:
                util.info(f'Override for {self._TOOL} using exe {exe}')
                self._EXE = exe

    def get_full_tool_and_versions(self) -> str:
        '''Returns tool:version, such as: verilator:5.033'''
        if not self._VERSION:
            self.get_versions()
        return str(self._TOOL) + ':' + str(self._VERSION)

    def get_versions(self) -> str:
        '''Sets and returns self._VERSION'''
        return self._VERSION

    def set_tool_defines(self) -> None:
        pass

class Command:

    command_name: str = ''

    def __init__(self, config:dict):
        if getattr(self, 'args', None) is None:
            self.args = {}
        if getattr(self, 'args_help', None) is None:
            self.args_help = {}
        self.args.update({
            "keep" : False,
            "force" : False,
            "fake" : False,
            "stop-before-compile": False,   # Usually in the self.do_it() method, stop prior to compile/elaborate/simulate
            "stop-after-compile": False,
            "stop-after-elaborate": False,  # Set to True to only run compile + elaboration (aka compile + lint)
            "lint": False, # Same as stop-after-elaborate
            "eda-dir" : "eda.work", # all eda jobs go in here
            "job-name" : "", # this is used to create a certain dir under "eda_dir"
            "work-dir" : "", # this can be used to run the job in a certain dir, else it will be <eda-dir>/<job-name> else <eda-dir>/<target>_<command>
            "sub-work-dir" : "", # this can be used to name the dir built under <eda-dir>, which seems to be same function as job-name??
            "work-dir-use-target-dir": False,
            "suffix" : "",
            "design" : "", # not sure how this relates to top
            'export':     False,
            'export-run': False,       # run from the exported location if possible, if not possible run the command in usual place.
            'export-json': False,      # generates an export.json suitable for a testrunner, if possible for self.command.
            'enable-tags': [],
            'disable-tags': [],
            'test-mode': False,
        })
        self.args_help.update({
            'stop-before-compile': ('stop this run before any compile (if possible for tool) and'
                                    ' save .sh scripts in eda-dir/'),
            'eda-dir':     'relative directory where eda logs are saved',
            'export':      'export results for these targets in eda-dir',
            'export-run':  'export, and run, results for these targets in eda-dir',
            'export-json': 'export, and save a JSON file per target',
            'work-dir':    ('Optional override for working directory, often defaults to'
                            ' ./eda.work/<top>.<command>'),
            "work-dir-use-target-dir": ('Set the work-dir to be the same as the in-place location'
                                       ' where the target (DEPS) exists'),
            'enable-tags': ('DEPS markup tag names to be force enabled for this'
                            ' command (mulitple appends to list).'),
            'diable-tags': ('DEPS markup tag names to be disabled (even if they'
                            ' match the criteria) for this command (mulitple appends to list).'
                            ' --disable-tags has higher precedence than --enable-tags.'),
            'test-mode': ('command and tool dependent, usually stops the command early without'
                          ' executing.'),
        })
        self.modified_args = {}
        self.config = copy.deepcopy(config) # avoid external modifications.
        self.target = ""
        self.target_path = ""
        self.status = 0

    def error(self, *args, **kwargs):
        '''Returns None, child classes can call self.error(..) instead of util.error, which updates their self.status.

        Please consider using Command.error(..) (or self.error(..)) in place of util.error so self.status is updated.
        '''
        self.status = util.error(*args, **kwargs)

    def status_any_error(self, report=True) -> bool:
        '''Used by derived classes process_tokens() to know an error was reached
        and to not perform the command. Necessary for pytests that use eda.main()'''
        if report and self.status > 0:
            util.error(f"command '{self.command_name}' has previous errors")
        return self.status > 0

    def which_tool(self, command:str):
        return which_tool(command, config=self.config)

    def create_work_dir(self):
        util.debug(f"create_work_dir: {self.args['eda-dir']=} {self.args['work-dir']=}")
        if self.args['work-dir-use-target-dir']:
            if not self.target_path:
                self.target_path = '.'
            util.info(f"create_work_dir: --work-dir-use-target-dir: using:",
                       f"{os.path.abspath(self.target_path)}",
                       f'target={self.target}')
            self.args['work-dir'] = self.target_path
            self.args['sub-work-dir'] = ''
            return self.args['work-dir']

        if not os.path.exists(self.args['eda-dir']):
            util.safe_mkdir(self.args['eda-dir'])
            util.info(f"create_work_dir: created {self.args['eda-dir']}")
        if self.args['design'] == "":
            if ('top' in self.args) and (self.args['top'] != ""):
                self.args['design'] = self.args['top']
                util.debug(f"create_work_dir: set {self.args['design']=} from {self.args['top']=}, since it was empty")
            else:
                self.args['design'] = "design" # generic, i.e. to create work dir "design_upload"
                util.debug(f"create_work_dir: set {self.args['design']=} to 'design', since it was empty and we have no top")
        if self.target == "":
            self.target = self.args['design']
            util.debug(f"create_work_dir: set {self.target=} from design name, since it was empty")
        if self.args['work-dir'] == '':
            if self.args['sub-work-dir'] == '':
                if self.args['job-name'] != '':
                    self.args['sub-work-dir'] = self.args['job-name']
                    util.debug(f"create_work_dir: set {self.args['sub-work-dir']=} from {self.args['job-name']=}, since it was empty")
                else:
                    self.args['sub-work-dir'] = f'{self.target}.{self.command_name}'
                    util.debug(f"create_work_dir: set {self.args['sub-work-dir']=} from {self.target=} and {self.command_name=}, since it was empty and we have no job-name")
            self.args['work-dir'] = os.path.join(self.args['eda-dir'], self.args['sub-work-dir'])
            util.debug(f"create_work_dir: set {self.args['work-dir']=}")
        keep_file = os.path.join(self.args['work-dir'], "eda.keep")
        if (os.path.exists(self.args['work-dir'])):
            if os.path.exists(keep_file) and not self.args['force']:
                self.error(f"Cannot remove old work dir due to '{keep_file}'")
            elif os.path.abspath(self.args['work-dir']) in os.getcwd():
                # This effectively checks if
                # --work-dir=.
                # --work-dir=$PWD
                # --work-dir=/some/path/almost/here
                # Allow it, but preserve the existing directory, we don't want to blow away
                # files up-heir from us.
                # Enables support for --work-dir=.
                util.info(f"Not removing existing work-dir: '{self.args['work-dir']}' is within {os.getcwd()=}")
            elif str(Path(self.args['work-dir'])).startswith(str(Path('/'))):
                # Do not allow other absolute path work dirs if it already exists.
                # This prevents you from --work-dir=~ and eda wipes out your home dir.
                self.error(f'Cannot use work-dir={self.args["work-dir"]} starting with absolute path "/"')
            elif str(Path('..')) in str(Path(self.args['work-dir'])):
                # Do not allow other ../ work dirs if it already exists.
                self.error(f'Cannot use work-dir={self.args["work-dir"]} with up-hierarchy ../ paths')
            else:
                # If we made it this far, on a directory that exists, that appears safe
                # to delete and re-create:
                util.info(f"Removing previous '{self.args['work-dir']}'")
                shutil.rmtree(self.args['work-dir'])
                util.safe_mkdir(self.args['work-dir'])
                util.debug(f'create_work_dir: created {self.args["work-dir"]}')
        else:
            util.safe_mkdir(self.args['work-dir'])
            util.debug(f'create_work_dir: created {self.args["work-dir"]}')
        if (self.args['keep']):
            open(keep_file, 'w').close()
            util.debug(f'create_work_dir: created {keep_file=}')
        return self.args['work-dir']

    def exec(self, work_dir, command_list, background=False, stop_on_error=True,
             quiet=False, tee_fpath=None, shell=False):
        if not quiet:
            util.info(f"exec: {' '.join(command_list)} (in {work_dir}, {tee_fpath=})")
        original_cwd = util.getcwd()
        os.chdir(work_dir)

        stdout, stderr, return_code = util.subprocess_run_background(
            work_dir=None, # we've already called os.chdir(work_dir).
            command_list=command_list,
            background=background,
            fake=self.args.get('fake', False),
            tee_fpath=tee_fpath,
            shell=shell
        )

        os.chdir(original_cwd)
        if return_code:
            self.status += return_code
            if stop_on_error: self.error(f"exec: returned with error (return code: {return_code})")
            else            : util.debug(f"exec: returned with error (return code: {return_code})")
        else:
            util.debug(f"exec: returned without error (return code: {return_code})")
        return stderr, stdout, return_code

    def set_arg(self, key, value):

        # Do some minimal type handling, preserving the type(self.args[key])
        if key not in self.args:
            self.error(f'set_arg, {key=} not in self.args {value=}',
                       f'({self.command_name=}, {self.__class__.__name__=})')

        cur_value = self.args[key]

        if isinstance(cur_value, dict):
            # if dict, update
            self.args[key].update(value)

        elif isinstance(cur_value, list):
            # if list, append (no duplicates)
            if isinstance(value, list):
                # new value also a list
                for x in value:
                    if x not in self.args[key]:
                        self.args[key].append(x)
            elif value not in cur_value:
                self.args[key].append(value)

        elif isinstance(cur_value, bool):
            # if bool, then attempt to convert new value string or int --> bool
            if isinstance(value, (bool, int)):
                self.args[key] = bool(value)
            elif isinstance(value, str):
                if value.lower() in ['false', '0']:
                    self.args[key] = False
                else:
                    self.args[key] = True
            else:
                raise Exception(f'set_arg({key=}, {value=}) bool, {type(cur_value)=} {type(value)=}')

        elif isinstance(cur_value, int):
            # if int, attempt to convert string or bool --> int
            if isinstance(value, (bool, int, str)):
                self.args[key] = int(value)
            else:
                raise Exception(f'set_arg({key=}, {value=}) int, {type(cur_value)=} {type(value)=}')


        else:
            # else overwrite it as-is.
            self.args[key] = value

        self.modified_args[key] = True
        util.debug(f'Set arg["{key}"]="{self.args[key]}"')


    def get_argparser(self, parser_arg_list=None) -> argparse.ArgumentParser:
        ''' Returns an argparse.ArgumentParser() based on self.args (dict)

        If parser_arg_list is not None, the ArgumentParser() is created using only the keys in
        self.args provided by the list parser_arg_list.
        '''

        # Preference is --args-with-dashes, which then become parsed.args_with_dashes, b/c
        # parsed.args-with-dashes is not legal python. Some of self.args.keys() still have - or _, so
        # this will handle both.
        # Also, preference is for self.args.keys(), to be str with - dashes
        parser = argparse.ArgumentParser(prog='eda', add_help=False, allow_abbrev=False)
        bool_action_kwargs = util.get_argparse_bool_action_kwargs()

        if not parser_arg_list:
            args = self.args
        else:
            args = {key: self.args[key] for key in parser_arg_list}

        for key,value in args.items():
            if '_' in key and '-' in key:
                assert False, f'{args=} has {key=} with both _ and -, which is not allowed'
            if '_' in key:
                util.warning(f'{key=} has _ chars, prefer -')

            keys = [key] # make a list
            if '_' in key:
                keys.append(key.replace('_', '-')) # switch to POSIX dashes for argparse
            elif '-' in key:
                keys.append(key.replace('-', '_')) # also support --some_arg_with_underscores

            arguments = [] # list supplied to parser.add_argument(..) so one liner supports both.
            for this_key in keys:
                arguments.append(f'--{this_key}')

            if self.args_help.get(key, ''):
                help_kwargs = {'help': self.args_help[key] + f' (default={value})'}
            elif value is None:
                help_kwargs = {'help': f'default={value}'}
            else:
                help_kwargs = {'help': f'{type(value).__name__} default={value}'}


            # It's important to set the default=None on these, except for list types where default is []
            # If the parsed Namespace has values set to None or [], we do not update. This means that as deps
            # are processed that have args set, they cannot override the top level args that were already set.
            # nor be overriden by defaults.
            if type(value) is bool:
                # For bool, support --key and --no-key with this action=argparse.BooleanOptionalAction.
                # Note, this means you cannot use --some-bool=True, or --some-bool=False, has to be --some-bool
                # or --no-some-bool.
                parser.add_argument(
                    *arguments, default=None, **bool_action_kwargs, **help_kwargs)
            elif type(value) is list:
                parser.add_argument(*arguments, default=value, action='append', **help_kwargs)
            elif type(value) in [int, str]:
                parser.add_argument(*arguments, default=value, type=type(value), **help_kwargs)
            elif value is None:
                parser.add_argument(*arguments, default=None, **help_kwargs)
            else:
                assert False, f'{key=} {value=} how do we do argparse for this type of value?'

        return parser


    def run_argparser_on_list(
            self, tokens: list, parser_arg_list=None, apply_parsed_args:bool=True
    ) -> (dict, list):
        ''' Creates an argparse.ArgumentParser() for all the keys in self.args, and attempts to parse
        from the provided list. Parsed args are applied to self.args.

        Returns a tuple of (parsed argparse.Namespace obj, list of unparsed args)

        If parser_arg_list is not None, the ArgumentParser() is created using only the keys in
        self.args provided by the list parser_arg_list.
        If apply_parsed_args=False, the parsed args were not applied.
        '''

        parser = self.get_argparser(parser_arg_list=parser_arg_list)
        try:
            parsed, unparsed = parser.parse_known_args(tokens + [''])
            unparsed = list(filter(None, unparsed))
        except argparse.ArgumentError:
            self.error(f'problem {command_name=} attempting to parse_known_args for {tokens=}')

        parsed_as_dict = vars(parsed)

        args_to_be_applied = {}

        for key,value in parsed_as_dict.items():
            # key should have _ instead of POSIX dashes, but we still support dashes like self.args['build-file'],
            # etc.
            if key not in self.args and '_' in key:
                # try with dashes instead of _
                key = key.replace('_', '-')
            assert key in self.args, f'{key=} not in {self.args=}'

            args_to_be_applied[key] = value

        if apply_parsed_args:
            self.apply_args_from_dict(args_to_be_applied)

        return parsed, unparsed


    def apply_args_from_dict(self, args_to_be_applied:dict) -> list:
        util.debug('apply_args_from_dict() -- called by:',
                   f'{self.command_name=}, {self.__class__.__name__=},',
                   f'{args_to_be_applied=}')
        for key, value in args_to_be_applied.items():

            if value is None:
                continue # don't update a self.args[key] to None
            if isinstance(value, list) and len(value) == 0:
                continue # don't update a self.args[key] that's a list --> to an empty list.
            if not isinstance(value, list) and self.args[key] == value:
                continue # don't update non list if the value already matches.
            if not isinstance(value, list) and self.modified_args.get(key, None):
                # For list types, we append. For all others they overwrite, so if we've already
                # modified the arg once, do not modify it again. Such as, command line set an arg,
                # but then a target tried to set it again; or a target set it, and then a dependent
                # target tried to set it again.
                util.warning(f"Command.run_argparser_on_list ({self.command_name}) -",
                             f"skipping {key=} {value=} b/c arg is already modified",
                             f"with different cur value (cur value={self.args.get(key, None)})")
                continue
            if self.args[key] != value:
                util.debug(f"Command.run_argparser_on_list - setting set_arg b/c",
                           f" argparse -- {key=} {value=} (cur value={self.args[key]})")
                self.set_arg(key, value) # Note this has special handling for lists already.
                self.modified_args[key] = True


    def process_tokens(self, tokens: list, process_all: bool = True,
                       pwd: str = os.getcwd()) -> list:
        '''Command.process_tokens(..) for all named self.args.keys() returns the
        unparsed tokens list

        Derived classes do not need to return a list of unparsed args, nor
        return self.status
        '''

        _, unparsed = self.run_argparser_on_list(tokens)
        if process_all and len(unparsed) > 0:
            self.error(f"Didn't understand argument: '{unparsed=}' in",
                       f" {self.command_name=} context")

        return unparsed

    def get_command_from_unparsed_args(
            self, tokens: list, error_if_no_command: bool = True
    ) -> str:
        '''Given a list of unparsed args, try to fish out the eda <command> value.

        This will remove the value from the tokens list.
        '''
        ret = ''
        for value in tokens:
            if value in self.config['command_handler'].keys():
                ret = value
                tokens.remove(value)
                break

        if not ret and error_if_no_command:
            self.error(f"Looking for a valid eda {self.command_name} <command>",
                       f"but didn't find one in {tokens=}")
        return ret



    def set_tool_config_from_config(self) -> None:
        '''Returns None. Hook for classes like CommandSim that have a Tool derived class attached.

        Have the Tool constructor run set_tool_config_from_config() if it exists, otherwise every
        derived class will have to call this (error-prone if the omit it but needed it).

        Allows command handlers to make thier own customizations from --config-yaml=YAML.
        '''
        pass

    def update_tool_config(self) -> None:
        '''Returns None. Hook for classes like CommandSim to make tool specific overrides.'''
        pass

    def write_eda_config_and_args(self):
        if not self.args.get('work-dir', None):
            util.warning(f'Ouput work-dir not set, saving ouput eda_config to {os.getcwd()}')
        util.write_eda_config_and_args(dirpath=self.args.get('work-dir', os.getcwd()),
                                       command_obj_ref=self)

    def is_export_enabled(self) -> bool:
        # check if any self.args['export'] is set in any way (but not set to False
        # or empty list)
        return any([arg.startswith('export') and v for arg,v in self.args.items()])

    def run(self) -> None:
        self.do_it()

    def do_it(self) -> None:
        self.write_eda_config_and_args()
        self.error(f"No tool bound to command '{self.command_name}', you",
                   " probably need to setup tool, or use '--tool <name>'")

    def command_safe_set_tool_defines(self) -> None:
        '''Safe wrapper for calling self.set_tool_defines() in case a Tool parent class is

        not yet present. If you have Tool parent, you can instead simply call:
           self.set_tool_defines()
        '''
        set_tool_defines = getattr(self, 'set_tool_defines', None)
        if set_tool_defines and callable(set_tool_defines):
            self.set_tool_defines()


    def help(self, tokens: list = []) -> None:
        '''Since we don't quite follow standard argparger help()/usage(), we'll format our own

        if self.args_help has additional help information.
        '''

        # Indent long lines (>100) to indent=56 (this is where we leave off w/ {vstr:12} below.
        def indent_me(text:str):
            return util.indent_wrap_long_text(text, width=100, indent=56)

        util.info('Help:')
        # using bare 'print' here, since help was requested, avoids --color and --quiet
        print()
        print('Usage:')
        print(f'    eda [options] {self.command_name} [options] [files|targets, ...]')
        print()

        print_base_help()
        lines = []
        if not self.args:
            print(f'Unparsed args: {tokens}')
            return

        if self.command_name:
            lines.append(f"Generic help for command='{self.command_name}'"
                         f" (using '{self.__class__.__name__}')")
        else:
            lines.append(f"Generic help (from class Command):")

        # Attempt to run argparser on args, but don't error if it fails.
        unparsed = []
        if tokens:
            try:
                _, unparsed = self.run_argparser_on_list(tokens=tokens)
            except:
                pass

        for k in sorted(self.args.keys()):
            v = self.args[k]
            vstr = str(v)
            khelp = self.args_help.get(k, '')
            if khelp:
                khelp = f'  - {khelp}'
            if type(v) == bool :
                lines.append(indent_me(f"  --{k:20} : boolean    : {vstr:12}{khelp}"))
            elif type(v) == int:
                lines.append(indent_me(f"  --{k:20} : integer    : {vstr:12}{khelp}"))
            elif type(v) == list:
                lines.append(indent_me(f"  --{k:20} : list       : {vstr:12}{khelp}"))
            elif type(v) == str:
                vstr = "'" + v + "'"
                lines.append(indent_me(f"  --{k:20} : string     : {vstr:12}{khelp}"))
            else:
                lines.append(indent_me(f"  --{k:20} : <unknown>  : {vstr:12}{khelp}"))
        lines.append('')
        for line in lines:
            print(line)

        if unparsed:
            print(f'Unparsed args: {unparsed}')


class CommandDesign(Command):

    # Used by for DEPS work_dir_add_srcs@ commands, by class methods:
    #   update_file_lists_for_work_dir(..), and resolve_target(..)
    _work_dir_add_srcs_path_string = '@EDA-WORK_DIR@'

    # Optionally error in self.process_tokens, derived classes can override.
    error_on_no_files_or_targets = False
    error_on_missing_top = False

    def __init__(self, config: dict):
        Command.__init__(self, config=config)
        self.args.update({
            'seed': seed.get_seed(style="urandom"),
            'top': '',
            'all-sv': True,
            'unprocessed-plusargs': [],
        })
        self.args_help.update({
            'seed':   'design seed, default is 31-bit non-zero urandom',
            'top':    'TOP level verilog/SV module or VHDL entity for this target',
            'all-sv': ('Maintain .sv and .v in single file list.'
                       ' False: .sv flist separate from .v flist and separate compile(s)'
                       ' True: .sv and .v files compiled together if possible'),
            'unprocessed-plusargs': 'Args that began with +, but were not +define+ or +incdir+, +<name>, ' \
            + ' or +<name>=<value>. These become tool dependent, for example "sim" commands will treat as sim-plusargs',
        })
        self.defines = {}
        self.incdirs = []
        self.files = {}
        self.files_v = []
        self.files_sv = []
        self.files_vhd = []
        self.files_cpp = []
        self.files_non_source = []
        self.files_caller_info = {}
        self.dep_shell_commands = [] # each list entry is a {}
        self.dep_work_dir_add_srcs = set() # key: tuple (target_path, target_node, filename)
        self.oc_root = util.get_oc_root()
        for (d,v) in self.config.get('defines', {}).items():
            self.defines[d] = v

        self.cached_deps = {} # key = abspath of DEPS markup file, has sub-dicts for 'data' and 'line_numbers'.
        self.targets_dict = {} # key = targets that we've already processed in DEPS files
        self.last_added_source_file_inferred_top = ''

    def run_dep_commands(self):
        # Run any shell@ commands from DEPS files
        self.run_dep_shell_commands()
        # Update any work_dir_add_srcs@ in our self.files, self.files_v, etc, b/c
        # self.args['work-dir'] now exists.
        self.update_file_lists_for_work_dir()
        # Link any non-sources to our work-dir:
        self.update_non_source_files_in_work_dir()

    def run_dep_shell_commands(self):
        # Runs from self.args['work-dir']
        all_cmds_lists = []

        log_fnames_count = {} # count per target_node.

        for iter, d in enumerate(self.dep_shell_commands):
            clist = util.ShellCommandList(d['exec_list'])
            log = clist.tee_fpath
            target_node = d["target_node"]
            if clist.tee_fpath is None:
                lognum = log_fnames_count.get(target_node, 0)
                log = f'{target_node}__shell_{lognum}.log' # auto log every shell command.
                clist.tee_fpath = log
                # In case some single target has N shell commands, give them unique log names.
                log_fnames_count.update({target_node: lognum + 1})
            all_cmds_lists += [
                [], # blank line
                # comment, where it came from, log to {node}__shell_{lognum}.log (or tee name from DEPS.yml)
                [f'# command {iter}: target: {d["target_path"]} : {target_node} --> {log}'],
                # actual command (list or util.ShellCommandList)
                clist,
            ]
            d['exec_list'] = clist # update to tee_fpath is set.

        util.write_shell_command_file(dirpath=self.args['work-dir'], filename='pre_compile_dep_shell_commands.sh',
                                      command_lists=all_cmds_lists)

        for iter,d in enumerate(self.dep_shell_commands):
            util.info(f'run_dep_shell_commands {iter=}: {d=}')
            clist = util.ShellCommandList(d['exec_list'])
            # NOTE(drew): shell=True subprocess call, can disable with self.config
            #  However, in Windows, we seem to have to run these with shell=False
            if sys.platform.startswith('win'):
                self.exec(self.args['work-dir'], clist, shell=False)
            else:
                self.exec(self.args['work-dir'], clist, tee_fpath=clist.tee_fpath,
                          shell=self.config.get('deps_subprocess_shell', False))

    def update_file_lists_for_work_dir(self):
        if len(self.dep_work_dir_add_srcs) == 0:
            return

        # If we encounter any @EDA-WORK_DIR@some_file.v in self.files, self.files_v, etc, then replace it with:
        # self.args['work-dir'] / some_file.v:
        _work_dir_add_srcs_path_string_len = len(self._work_dir_add_srcs_path_string)
        work_dir_abspath = os.path.abspath(self.args['work-dir'])
        for key in list(self.files.keys()): # list so it's not an iterator, we're updating self.files.
            if type(key) is str and key.startswith(self._work_dir_add_srcs_path_string):
                new_key = os.path.join(work_dir_abspath, key[_work_dir_add_srcs_path_string_len :])
                self.files.pop(key)
                self.files[new_key] = True

        my_file_lists_list = [self.files_v, self.files_sv, self.files_vhd, self.files_cpp]
        for my_file_list in my_file_lists_list:
            for iter,value in enumerate(my_file_list):
                if value and type(value) is str and value.startswith(self._work_dir_add_srcs_path_string):
                    new_value = os.path.join(work_dir_abspath, value[_work_dir_add_srcs_path_string_len :])
                    my_file_list[iter] = new_value
                    util.debug(f"file lists: replaced {value} with {new_value}")

    def update_non_source_files_in_work_dir(self):
        for fname in self.files_non_source:
            _, leaf_fname = os.path.split(fname)
            destfile = os.path.join(self.args['work-dir'], leaf_fname)
            relfname = os.path.relpath(fname)
            caller_info = self.files_caller_info[fname]
            if not os.path.exists(fname):
                util.info(f'{fname=} {self.files_caller_info=}')
                self.error(f'Non-source file (reqs?) {relfname=} does not exist from {caller_info}')
            elif not os.path.exists(destfile):
                util.debug(f'updating non-source file to work-dir: Linked {fname=} to {destfile=}, from {caller_info}')
                if sys.platform == "win32":
                    shutil.copyfile(fname, destfile) # On Windows, fall back to copying
                else:
                    os.symlink(src=fname, dst=destfile)

    def get_top_name(self, name):
        return os.path.splitext(os.path.basename(name))[0]

    def process_plusarg(self, plusarg: str, pwd: str = os.getcwd()):
        '''Retuns str, parses a +define+, +incdir+, +key=value str; adds to internal.

        Adds to self.defines, self.incdirs,
        Or, adds to self.args['unprocessed-plusargs'] (list) and retuns value added
        to unprocessed-plusargs.
        '''

        # Since this may be coming from a raw CLI/bash/powershell argparser, we may have
        # args that come from shlex.quote(token), such as:
        #   token = '\'+define+OC_ROOT="/foo/bar/opencos"\''
        # So we strip all outer ' or " on the plusarg:
        plusarg = util.strip_outer_quotes(plusarg)
        if not pwd:
            pwd = ''

        if plusarg.startswith('+define+'):
            plusarg = plusarg.lstrip('+define+')
            m = re.match(r'^(\w+)$', plusarg)
            if m:
                k = m.group(1)
                self.defines[k] = None
                util.debug(f"Defined {k}")
                return None
            m = re.match(r'^(\w+)\=(\S+)$', plusarg)
            if not m: m = re.match(r'^(\w+)\=(\"[^\"]*\")$', plusarg)
            if m:
                k = m.group(1)
                v = m.group(2)
                if v and type(v) is str:
                    if v.startswith('%PWD%/'):
                        v = v.replace('%PWD%', os.path.abspath(pwd))
                    if v.startswith('%SEED%'):
                        v = v.replace('%SEED%', str(self.args.get('seed', 1)))
                self.defines[k] = v
                util.debug(f"Defined {k}={v}")
                return None
            self.error(f"Didn't understand +define+: '{plusarg}'")
            return None

        if plusarg.startswith('+incdir+'):
            plusarg = plusarg.lstrip('+incdir+')
            m = re.match(r'^(\S+)$', plusarg)
            if m:
                incdir = m.group(1)
                if incdir not in self.incdirs:
                    self.incdirs.append(os.path.abspath(incdir))
                    util.debug(f"Added include dir '{os.path.abspath(incdir)}'")
                return None
            self.error(f"Didn't understand +incdir+: '{plusarg}'")
            return None

        # remaining plusargs as stored in self.args['unprocessed-plusargs'] (list)
        if plusarg.startswith('+'):
            if not self.config.get('bare_plusarg_supported', False):
                self.error(f"bare plusarg(s) are not supported: {plusarg}'")
                return None
            elif plusarg not in self.args['unprocessed-plusargs']:
                self.args['unprocessed-plusargs'].append(plusarg)
                # For anything added to unprocessed-plusarg, we have to return it, to let
                # derived classes have the option to handle it
                return plusarg
        else:
            self.error(f"Didn't understand +plusarg: '{plusarg}'")
        return None


    def append_shell_commands(self, cmds : list):
        # Each entry in cmds (list) should be a dict with keys ['target_node', 'target_path', 'exec_list']
        for entry in cmds:
            if entry is None or type(entry) is not dict:
                continue
            if entry in self.dep_shell_commands:
                # we've already run this exact command (target node, target path, exec list), don't run it
                # again
                continue

            assert 'exec_list' in entry, f'{entry=}'
            util.debug(f'adding - dep_shell_command: {entry=}')
            self.dep_shell_commands.append(entry)

    def append_work_dir_add_srcs(self, add_srcs: list, caller_info: str):
        # Each entry in add_srcs (list) should be a dict with keys ['target_node', 'target_path', 'file_list']
        for entry in add_srcs:
            if entry is None or type(entry) is not dict:
                continue

            work_dir_files = entry['file_list']
            for filename in work_dir_files:
                # Unfortunately, self.args['work-dir'] doesn't exist yet and hasn't been set, so we'll add these
                # files as '@EDA-WORK_DIR@' + filename, and have to replace the EDA-WORK_DIR@ string later in our flow.
                filename_use = self._work_dir_add_srcs_path_string + filename
                dep_key_tuple = (
                    entry['target_path'],
                    entry['target_node'],
                    filename_use
                )
                if filename_use not in self.files:
                    util.debug(f'work_dir_add_srcs@ {dep_key_tuple=} added file {filename_use=}')
                    self.add_file(filename=filename_use, use_abspath=False, caller_info=caller_info)
                    # avoid duplicate calls, and keep a paper trail of which DEPS added
                    # files from the self.args['work-dir'] using this method.
                    self.dep_work_dir_add_srcs.add(dep_key_tuple) # add to set()
                elif dep_key_tuple not in self.dep_work_dir_add_srcs:
                    # we've already added the file so this dep was skipped for this one file.
                    util.warning(f'work_dir_add_srcs@ {dep_key_tuple=} but {filename_use=}' \
                                 + 'is already in self.files (duplicate dependency on generated file?)')


    def resolve_target(self, target, no_recursion=False, caller_info=''):
        util.debug("Entered resolve_target(%s)" % (target))
        # self.target is a name we grab for the job (i.e. for naming work dir etc).  we don't want the path prefix.
        # TODO: too messy -- there's also a self.target, args['job-name'], args['work-dir'], args['design'], args['top'], args['sub-work-dir'] ...

        self.target_path, self.target = os.path.split(target)

        if target in self.targets_dict:
            # If we're encountered this target before, stop. We're not traversing again.
            return True

        self.targets_dict[target] = None
        file_exists, fpath, forced_extension = files.get_source_file(target)
        if file_exists:
            # If the target is a file (we're at the root here processing CLI arg tokens)
            # and that file exists and has an extension, then there's no reason to go looking
            # in DEPS files, add the file and return True.
            file_base, file_ext = os.path.splitext(fpath)
            if forced_extension or file_ext:
                self.add_file(fpath, caller_info=caller_info,
                              forced_extension=forced_extension)
                return True

        return self.resolve_target_core(target, no_recursion, caller_info)

    def resolve_target_core(self, target, no_recursion, caller_info=''):
        util.debug("Entered resolve_target_core(%s)" % (target))
        found_target = False
        util.debug("Starting to resolve target '%s'" % (target))
        target_path, target_node = os.path.split(target)

        deps = None
        data = None
        found_deps_file = False

        if self.config['deps_markup_supported']:
            deps = deps_helpers.DepsFile(
                command_design_ref=self, target_path=target_path, cache=self.cached_deps
            )
            deps_file = deps.deps_file
            data = deps.data
            data_only_lines = deps.line_numbers

        # Continue if we have data, otherwise look for files other than DEPS.<yml|yaml>
        if data is not None:
            found_deps_file = True
            found_target = deps.lookup(target_node=target_node, caller_info=caller_info)

        if found_deps_file and found_target:

            entry = deps.get_entry(target_node=target_node)

            # For convenience, use an external class for this DEPS.yml table/dict
            # This could be re-used for any markup DEPS.json, DEPS.toml, DEPS.py, etc.
            deps_processor = deps_helpers.DepsProcessor(
                command_design_ref = self,
                deps_entry = entry,
                target = target,
                target_path = target_path,
                target_node = target_node,
                deps_file = deps_file,
                # Update the caller_info for this DEPS.yml file's target_node, b/c we're now
                # examining this entry (target) in this deps_file.
                caller_info = deps.gen_caller_info(target_node)
            )

            # Process the target, and get new (unprocessed) deps entries list.
            # This updates self (for defines, incdirs, top, args, etc)
            # This will skip remaining deps in self.targets_dict
            deps_targets_to_resolve = deps_processor.process_deps_entry()
            util.debug(f'   ... for {target_node=} {deps_file=}, {deps_targets_to_resolve=}')

            # Recurse on the returned deps (ordered list), if they haven't already been traversed.
            for x in deps_targets_to_resolve:
                caller_info = deps.gen_caller_info(target_node)
                if x and type(x) is tuple:
                    # if deps_processor.process_deps_entry() gave us a tuple, it's an
                    # unprocessed 'command' that we kept in order until now. Append it.
                    assert len(x) == 2, f'command tuple {x=} must be len 2, {target_node=} {deps_file=}'
                    shell_commands_list, work_dir_add_srcs_list = x
                    self.append_shell_commands( cmds=shell_commands_list )
                    self.append_work_dir_add_srcs( add_srcs=work_dir_add_srcs_list,
                                                   caller_info=caller_info )

                elif x and x not in self.targets_dict:
                    self.targets_dict[x] = None # add it before processing.
                    file_exists, fpath, forced_extension = files.get_source_file(x)
                    if file_exists:
                        self.add_file(filename=fpath, caller_info=caller_info,
                                      forced_extension=forced_extension)
                    else:
                        util.debug(f'   ... Calling resolve_target_core({x=})')
                        found_target |= self.resolve_target_core( x, no_recursion, caller_info=caller_info)


        # Done with DEPS.yml if it existed.

        if not found_target:
            util.debug("Haven't been able to resolve %s via DEPS" % (target))
            known_file_extensions_for_source = []
            for x in ['verilog', 'systemverilog', 'vhdl', 'cpp']:
                known_file_extensions_for_source += self.config.get('file_extensions', {}).get(x, [])
            for e in known_file_extensions_for_source:
                try_file = target + e
                util.debug("Looking for %s" % (try_file))
                if os.path.exists(try_file):
                    self.add_file(try_file, caller_info=str('n/a::' + target + '::n/a'))
                    found_target = True
                    break # move on to the next target
            if not found_target: # if STILL not found_this_target...
                self.error("Unable to resolve target '%s'" % (target))

        # if we've found any target since being called, it means we found the one we were called for
        return found_target

    def add_file(self, filename, use_abspath=True, add_to_non_sources=False,
                 caller_info:str='', forced_extension:str=''):
        file_base, file_ext = os.path.splitext(filename)
        if use_abspath:
            file_abspath = os.path.abspath(filename)
        else:
            file_abspath = filename


        if file_abspath in self.files:
            util.debug("Not adding file %s, already have it" % (file_abspath))
            return

        known_file_ext_dict = self.config.get('file_extensions', {})
        v_file_ext_list = known_file_ext_dict.get('verilog', [])
        sv_file_ext_list = known_file_ext_dict.get('systemverilog', [])
        vhdl_file_ext_list = known_file_ext_dict.get('vhdl', [])
        cpp_file_ext_list = known_file_ext_dict.get('cpp', [])

        if forced_extension:
            # If forced_extension='systemverilog', then use the first known extension for
            # it ('.sv', from eda_config_defaults.yml), which will pick it up in the if-elif
            # below.
            file_ext = known_file_ext_dict.get(forced_extension, [''])[0]
            util.debug(f"{forced_extension=} for {filename=} as type '{file_ext}'")


        if not add_to_non_sources and \
           file_ext in known_file_ext_dict.get('inferred_top', []):
            self.last_added_source_file_inferred_top = file_abspath

        if add_to_non_sources:
            self.files_non_source.append(file_abspath)
            util.debug("Added non-source file file %s as %s" % (filename, file_abspath))
        elif file_ext in v_file_ext_list and not self.args['all-sv']:
            self.files_v.append(file_abspath)
            util.debug("Added Verilog file %s as %s" % (filename, file_abspath))
        elif file_ext in sv_file_ext_list or ((file_ext in v_file_ext_list) and self.args['all-sv']):
            self.files_sv.append(file_abspath)
            util.debug("Added SystemVerilog file %s as %s" % (filename, file_abspath))
        elif file_ext in vhdl_file_ext_list:
            self.files_vhd.append(file_abspath)
            util.debug("Added VHDL file %s as %s" % (filename, file_abspath))
        elif file_ext in cpp_file_ext_list:
            self.files_cpp.append(file_abspath)
            util.debug("Added C++ file %s as %s" % (filename, file_abspath))
        else:
            # unknown file extension. In these cases we link the file to the working directory
            # so it is available (for example, a .mem file that is expected to exist with relative path)
            self.files_non_source.append(file_abspath)
            util.debug("Added non-source file %s as %s" % (filename, file_abspath))

        self.files[file_abspath] = True
        self.files_caller_info[file_abspath] = caller_info
        return file_abspath

    def process_tokens(self, tokens: list, process_all: bool = True,
                       pwd: str = os.getcwd()) -> list:

        util.debug(f'CommandDesign - process_tokens start - {tokens=}')

        # see if it's a flag/option like --debug, --seed <n>, etc
        # This returns all unparsed args, and doesn't error out due to process_all=False
        orig_tokens = tokens.copy()
        unparsed = Command.process_tokens(self, tokens, process_all=False, pwd=pwd)
        util.debug(f'CommandDesign - after Command.process_tokens(..) {unparsed=}')

        # deal with +define+ or +incdir+, consume it and remove from unparsed
        # walk the list, remove all items after we're done.
        remove_list = []
        for token in unparsed:
            # Since this is a raw argparser, we may have args that come from shlex.quote(token), such as:
            # token = '\'+define+OC_ROOT="/foo/bar/opencos"\''
            # So we have to check for strings that have been escaped for shell with extra single quotes.
            m = re.match(r"^\'?\+\w+", token)
            if m:
                # Copy and strip all outer ' or " on the plusarg:
                plusarg = util.strip_outer_quotes(token)
                self.process_plusarg(plusarg, pwd=pwd)
                remove_list.append(token)
        for x in remove_list:
            unparsed.remove(x)

        if len(unparsed) == 0 and self.error_on_no_files_or_targets:
            # derived classes can set error_on_no_files_or_targets=True
            # For example: CommandSim will error (requires files/targets),
            # CommandWaves does not (files/targets not required)
            # A nice-to-have: if someone ran: eda sim; without a file/target,
            # check the DEPS markup file for a single target, and if so run it
            # on the one and only target.
            if self.config['deps_markup_supported']:
                deps = deps_helpers.DepsFile(
                    command_design_ref=self, target_path=os.getcwd(), cache=self.cached_deps
                )
                if deps.deps_file and deps.data:
                    all_targets = deps_helpers.deps_data_get_all_targets(deps.data)
                    if all_targets:
                        target = all_targets[-1]
                        unparsed.append(target)
                        util.warning(f"For command '{self.command_name}' no files or targets were",
                                     f"presented at the command line, so using '{target}' from",
                                     f"{deps.deps_file}")
            if len(unparsed) == 0:
                # If unparsed is still empty, then error.
                self.error(f"For command '{self.command_name}' no files or targets were",
                           f"presented at the command line: {orig_tokens}")

        # by this point hopefully this is a target ... is it a simple filename?
        remove_list = []
        last_potential_top_file = ('', '')   # (top, fpath)
        last_potential_top_target = ('', '') # (top, path/to/full-target-name)
        last_potential_top_isfile = False
        caller_info = ''
        for token in unparsed:
            file_exists, fpath, forced_extension = files.get_source_file(token)
            if file_exists:
                file_abspath = os.path.abspath(fpath)
                file_base, file_ext = os.path.splitext(file_abspath)
                if not forced_extension and not file_ext:
                    # This probably isn't a file we want to use
                    util.warning(f'looking for deps {token=}, found {file_abspath=}' \
                                 + ' but has no file extension, we will not add this file')
                    # do not consume it, it's probably a named target in DEPS.yml
                else:
                    self.add_file(filename=fpath, caller_info=caller_info,
                                  forced_extension=forced_extension)
                    if not self.args['top']:
                        known_file_ext_dict = self.config.get('file_extensions', {})
                        if forced_extension:
                            file_ext = known_file_ext_dict.get(forced_extension, [''])[0]
                        if file_ext in known_file_ext_dict.get('inferred_top', []):
                            # last cmd line arg was a filename that could have inferred top.
                            last_potential_top_isfile = True

                    remove_list.append(token)
                    continue # done with token, consume it, we added the file.

            # we appear to be dealing with a target name which needs to be resolved (usually recursively)
            if token.startswith(os.sep):
                target_name = token # if it's absolute path, don't prepend anything
            else:
                target_name = os.path.join(".", token) # prepend ./so that we always have a <path>/<file>

            util.debug(f'Calling self.resolve_target on {target_name=}')
            if self.resolve_target(target_name, caller_info=caller_info):
                if not self.args['top']:
                    # last cmd line arg was a target that we'll likely use for inferred top.
                    last_potential_top_target = (self.get_top_name(target_name), target_name)
                    last_potential_top_isfile = False

                remove_list.append(token)
                continue # done with token

        for x in remove_list:
            unparsed.remove(x)

        # we were unable to figure out what this command line token is for...
        if process_all and len(unparsed) > 0:
            self.error(f"Didn't understand command remaining tokens {unparsed=} in CommandDesign")

        # handle a missing self.args['top'] with last filepath or last target:
        if not self.args.get('top', ''):
            if not last_potential_top_isfile and last_potential_top_target[0]:
                # If we have a target name from DEPS, prefer to use that.
                self.args['top'], self.args['top-path'] = last_potential_top_target
                util.info("--top not specified, inferred from target:",
                          f"{self.args['top']} ({self.args['top-path']})")

            else:
                best_top_fname = self.last_added_source_file_inferred_top
                if best_top_fname:
                    last_potential_top_file = (self.get_top_name(best_top_fname), best_top_fname)

            if not self.args['top'] and last_potential_top_file[0]:
                # If we don't have a target name, and no top name yet, then go looking for the
                # module name in the final source file added.
                self.args['top-path'] = last_potential_top_file[1] # from tuple: (top, fpath)
                self.args['top'] = util.get_inferred_top_module_name(
                    module_guess=last_potential_top_file[0],
                    module_fpath=last_potential_top_file[1]
                )
                if self.args['top']:
                    util.info("--top not specified, inferred from final source file:",
                              f"{self.args['top']} ({self.args['top-path']})")
                    # If top wasn't set, and we're using the final command-line 'arg' filename
                    # (not from DEPS.yml) we need to override self.target if that was set. Otherwise
                    # it won't save to the correct work-dir:
                    self.target = self.args['top']

        if self.error_on_missing_top and not self.args.get('top', ''):
            self.error(f"Did not get a --top or DEPS top, required to run command",
                       f"'{self.command_name}' for tool={self.args.get('tool', None)}")

        return unparsed


    def get_command_line_args(self, remove_args:list=[], remove_args_startswith:list=[]) -> list:
        '''Returns a list of all the args if you wanted to re-run this command
        (excludes eda, command, target).'''

        # This will not set bool's that are False, does not add --no-<somearg>
        # nor --<somearg>=False
        # This will not set str's that are empty.
        # this will not set ints that are 0
        ret = []
        for k,v in self.args.items():

            # Some args cannot be extracted and work, so omit these:
            if k in ['top-path'] + remove_args:
                continue
            if any([k.startswith(x) for x in remove_args_startswith]):
                continue

            if type(v) is bool and v:
                ret.append(f'--{k}')
            elif type(v) is int and bool(v):
                ret.append(f'--{k}={v}')
            elif type(v) is str and v:
                ret.append(f'--{k}={v}')
            elif type(v) is list:
                for item in v:
                    if item or type(item) not in [bool, str]:
                        # don't print bool/str that are blank.
                        ret.append(f'--{k}={item}') # lists append

        return ret


_threads_start = 0
_threads_done = 0

class CommandParallelWorker(threading.Thread):
    def __init__(self, n, work_queue, done_queue):
        threading.Thread.__init__(self)
        self.n = n
        self.work_queue = work_queue
        self.done_queue = done_queue
        self.stop_request = False
        self.job_name = ""
        self.proc = None
        self.pid = None
        self.last_timer_debug = 0
        util.debug(f"WORKER_{n}: START")

    def run(self):
        global _threads_start
        global _threads_done
        while True:
            # Get the work from the queue and expand the tuple
            i, command_list, job_name, work_dir = self.work_queue.get()
            self.job_name = job_name
            try:
                util.debug(f"WORKER_{self.n}: Running job {i}: {job_name}")
                PIPE=subprocess.PIPE
                STDOUT=subprocess.STDOUT
                util.debug(f"WORKER_{self.n}: Calling Popen")
                proc = subprocess.Popen(command_list, stdout=PIPE, stderr=STDOUT)
                self.proc = proc
                util.debug(f"WORKER_{self.n}: Opened process, PID={proc.pid}")
                self.pid = proc.pid
                _threads_start += 1
                while proc.returncode == None:
                    try:
                        if (time.time() - self.last_timer_debug) > 10:
                            util.debug(f"WORKER_{self.n}: Calling proc.communicate")
                        stdout, stderr = proc.communicate(timeout=0.5)
                        util.debug(f"WORKER_{self.n}: got: \n*** stdout:\n{stdout}\n*** stderr:{stderr}")
                    except subprocess.TimeoutExpired:
                        if (time.time() - self.last_timer_debug) > 10:
                            util.debug(f"WORKER_{self.n}: Timer expired, stop_request={self.stop_request}")
                            self.last_timer_debug = time.time()
                        pass
                    if self.stop_request:
                        util.debug(f"WORKER_{self.n}: got stop request, issuing SIGINT")
                        proc.send_signal(signal.SIGINT)
                        util.debug(f"WORKER_{self.n}: got stop request, calling proc.wait")
                        proc.wait()
                    if False and self.stop_request:
                        util.debug(f"WORKER_{self.n}: got stop request, issuing proc.terminate")
                        proc.terminate()
                        util.debug(f"WORKER_{self.n}: proc poll returns is now {proc.poll()}")
                        try:
                            util.debug(f"WORKER_{self.n}: Calling proc.communicate")
                            stdout, stderr = proc.communicate(timeout=0.2) # for completeness, in case we ever pipe/search stdout/stderr
                            util.debug(f"WORKER_{self.n}: got: \n*** stdout:\n{stdout}\n*** stderr:{stderr}")
                        except subprocess.TimeoutExpired:
                            util.debug(f"WORKER_{self.n}: timeout waiting for comminicate after terminate")
                        except:
                            pass
                        util.debug(f"WORKER_{self.n}: proc poll returns is now {proc.poll()}")

                util.debug(f"WORKER_{self.n}: -- out of while loop")
                self.pid = None
                self.proc = None
                self.job_name = "<idle>"
                util.debug(f"WORKER_{self.n}: proc poll returns is now {proc.poll()}")
                try:
                    util.debug(f"WORKER_{self.n}: Calling proc.communicate one last time")
                    stdout, stderr = proc.communicate(timeout=0.1) # for completeness, in case we ever pipe/search stdout/stderr
                    util.debug(f"WORKER_{self.n}: got: \n*** stdout:\n{stdout}\n*** stderr:{stderr}")
                except subprocess.TimeoutExpired:
                    util.debug(f"WORKER_{self.n}: timeout waiting for communicate after loop?")
                except:
                    pass
                return_code = proc.poll()
                util.debug(f"WORKER_{self.n}: Finished job {i}: {job_name} with return code {return_code}")
                self.done_queue.put((i, job_name, return_code))
            finally:
                util.debug(f"WORKER_{self.n}: -- in finally block")
                self.work_queue.task_done()
                _threads_done += 1


class CommandParallel(Command):
    def __init__(self, config: dict):
        Command.__init__(self, config=config)
        self.jobs = []
        self.jobs_status = []
        self.args['parallel'] = 1
        self.worker_threads = []

    def __del__(self):
        util.debug(f"In Command.__del__, threads done/started: {_threads_done}/{_threads_start}")
        if _threads_start == _threads_done:
            return
        util.warning(f"Need to shut down {_threads_start-_threads_done} worker threads...")
        for w in self.worker_threads:
            if w.proc:
                util.warning(f"Requesting stop of PID {w.pid}: {w.job_name}")
                w.stop_request = True
        for i in range(10):
            util.debug(f"Threads done/started: {_threads_done}/{_threads_start}")
            if _threads_start == _threads_done:
                util.info(f"All threads done")
                return
            time.sleep(1)
        subprocess.Popen(['stty', 'sane']).wait()
        util.debug(f"Scanning workers again")
        for w in self.worker_threads:
            if w.proc:
                util.info(f"need to SIGINT WORKER_{w.n}, may need manual cleanup, check 'ps'")
                if w.pid:
                    os.kill(w.pid, signal.SIGINT)
        for i in range(5):
            util.debug(f"Threads done/started: {_threads_done}/{_threads_start}")
            if _threads_start == _threads_done:
                util.info(f"All threads done")
                return
            time.sleep(1)
        subprocess.Popen(['stty', 'sane']).wait()
        util.debug(f"Scanning workers again")
        for w in self.worker_threads:
            if w.proc:
                util.info(f"need to TERM WORKER_{w.n}, probably needs manual cleanup, check 'ps'")
                if w.pid:
                    os.kill(w.pid, signal.SIGTERM)
        for i in range(5):
            util.debug(f"Threads done/started: {_threads_done}/{_threads_start}")
            if _threads_start == _threads_done:
                util.info(f"All threads done")
                return
            time.sleep(1)
        subprocess.Popen(['stty', 'sane']).wait()
        util.debug(f"Scanning workers again")
        for w in self.worker_threads:
            if w.proc:
                util.info(f"need to KILL WORKER_{w.n}, probably needs manual cleanup, check 'ps'")
                if w.pid:
                    os.kill(w.pid, signal.SIGKILL)
        util.stop_log()
        subprocess.Popen(['stty', 'sane']).wait()

    def run_jobs(self, command):
        # this is where we actually run the jobs.  it's a messy piece of code and prob could use refactoring
        # but the goal was to share as much as possible (job start, end, pass/fail judgement, etc) while
        # supporting various mode combinations (parallel mode, verbose mode, fancy mode, etc) and keeping the
        # UI output functional and awesome sauce

        # walk targets to find the longest name, for display reasons
        longest_job_name = 0
        total_jobs = len(self.jobs)
        self.jobs_status = [None] * total_jobs
        for i in range(total_jobs):
            l = len(self.jobs[i]['name'])
            if l>longest_job_name: longest_job_name = l

        run_parallel = self.args['parallel'] > 1

        # figure out the width to print various numbers
        jobs_digits = len(f"{total_jobs}")
        jobs_fmt = "%%%dd" % jobs_digits # ugh, for printing out a number with N digits

        # run the jobs!
        running_jobs = {}
        passed_jobs = []
        failed_jobs = []
        workers = []
        jobs_complete = 0
        jobs_launched = 0
        num_parallel = min(len(self.jobs), self.args['parallel'])
        # 16 should really be the size of window or ?
        (columns,lines) = shutil.get_terminal_size()
        # we will enter fancy mode if we are parallel and we can leave 6 lines of regular scrolling output
        fancy_mode = util.args['fancy'] and (num_parallel > 1) and (num_parallel <= (lines-6))
        multi_cwd = util.getcwd() + os.sep

        self.patch_jobs_for_duplicate_target_names()

        if run_parallel:
            # we are doing this multi-threaded
            util.info(f"Parallel: Running multi-threaded, starting {num_parallel} workers")
            work_queue = queue.Queue()
            done_queue = queue.Queue()
            for x in range(num_parallel):
                worker = CommandParallelWorker(x, work_queue, done_queue)
                # Setting daemon to True will let the main thread exit even though the workers are blocking
                worker.daemon = True
                worker.start()
                self.worker_threads.append(worker)
                workers.append(x)
            if fancy_mode:
                # in fancy mode, we will take the bottom num_parallel lines to show state of workers
                util.fancy_start(fancy_lines=num_parallel)
                for x in range(num_parallel):
                    util.fancy_print(f"Starting worker {x}", x)

        while len(self.jobs) or len(running_jobs.items()):
            job_done = False
            job_done_quiet = False
            anything_done = False

            def sprint_job_line(job_number=0, job_name="", final=False, hide_stats=False):
                return (f"INFO: [EDA] " +
                        util.string_or_space(f"[job {jobs_fmt%job_number}/{jobs_fmt%total_jobs} ", final) +
                        util.string_or_space(f"| pass ", hide_stats or final) +
                        util.string_or_space(f"{jobs_fmt%len(passed_jobs)}/{jobs_fmt%jobs_complete} ", hide_stats) +
                        util.string_or_space(f"@ {(100*(jobs_complete))/total_jobs:5.1f}%", hide_stats or final) +
                        util.string_or_space(f"] ", final) +
                        f"{command} {(job_name+' ').ljust(longest_job_name+3,'.')}")

            # for any kind of run (parallel or not, fancy or not, verbose or not) ... can we launch a job?
            if len(self.jobs) and (len(running_jobs.items()) < num_parallel):
                # we are launching a job
                jobs_launched += 1
                anything_done = True
                job = self.jobs.pop(0)
                if job['name'].startswith(multi_cwd): job['name'] = job['name'][len(multi_cwd):]
                # in all but fancy mode, we will print this text at the launch of a job.  It may get a newline below
                job_text = sprint_job_line(jobs_launched, job['name'], hide_stats=run_parallel)
                command_list = job['command_list']
                cwd = util.getcwd()

                if run_parallel:
                    # multithreaded job launch: add to queue
                    worker = workers.pop(0) # we don't actually know which thread will pick up, but GUI will be consistent
                    running_jobs[str(jobs_launched)] = { 'name' : job['name'],
                                                         'number' : jobs_launched,
                                                         'worker' : worker,
                                                         'start_time' : time.time(),
                                                         'update_time' : time.time()}
                    work_queue.put((jobs_launched, command_list, job['name'], cwd))
                    suffix = "<START>"
                    if fancy_mode:
                        util.fancy_print(job_text+suffix, worker)
                    else:
                        # if we aren't in fancy mode, we will print a START line, periodic RUNNING lines, and PASS/FAIL line per-job
                        if len(failed_jobs): util.print_orange(job_text + util.string_yellow + suffix)
                        else:                util.print_yellow(job_text + util.string_yellow + suffix)
                else:
                    # single-threaded job launch, we are going to print out job info as we start each job... no newline
                    # since non-verbose silences the job and prints only <PASS>/<FAIL> after the trailing "..." we leave here
                    if len(failed_jobs): util.print_orange(job_text, end="")
                    else:                util.print_yellow(job_text, end="")
                    job_done_number = jobs_launched
                    job_done_name = job['name']
                    job_start_time = time.time()
                    if util.args['verbose']:
                        # previous status line gets a \n, then job is run passing
                        # stdout/err, then print 'job_text' again with pass/fail
                        util.print_green("")
                        # run job, sending output to the console
                        _, _, job_done_return_code = self.exec(
                            cwd, command_list, background=False, stop_on_error=False, quiet=False
                        )
                        # reprint the job text previously printed before running job(and given "\n" after the trailing "...")
                    else:
                        # run job, swallowing output (hope you have a logfile)
                        _, _, job_done_return_code = self.exec(
                            cwd, command_list, background=True, stop_on_error=False, quiet=True
                        )
                        job_done_quiet = True # in this case, we have the job start text (trailing "...", no newline) printed
                    job_done = True
                    job_done_run_time = time.time() - job_start_time
                    # Since we consumed the job, use the job['index'] to track the per-job status:

            if run_parallel:
                # parallel run, check for completed job
                if done_queue.qsize():
                    # we're collecting a finished job from a worker thread.  note we will only reap one job per iter of the big
                    # loop, so as to share job completion code at the bottom
                    anything_done = True
                    job_done = True
                    job_done_number, job_done_name, job_done_return_code = done_queue.get()
                    t = running_jobs[str(job_done_number)]
                    # in fancy mode, we need to clear the worker line related to this job.
                    if fancy_mode:
                        util.fancy_print(f"INFO: [EDA] Parallel: Worker Idle ...", t['worker'])
                    job_done_run_time = time.time() - t['start_time']
                    util.debug(f"removing job #{job_done_number} from running jobs")
                    del running_jobs[str(job_done_number)]
                    workers.append(t['worker'])

            if run_parallel:
                # parallel run, update the UI on job status
                for _,t in running_jobs.items():
                    if (fancy_mode or (time.time() - t['update_time']) > 30):
                        t['update_time'] = time.time()
                        job_text = sprint_job_line(t['number'], t['name'], hide_stats=True)
                        suffix = f"<RUNNING: {util.sprint_time(time.time() - t['start_time'])}>"
                        if fancy_mode:
                            util.fancy_print(f"{job_text}{suffix}", t['worker'])
                        else:
                            if len(failed_jobs): util.print_orange(job_text+util.string_yellow+suffix)
                            else:                util.print_yellow(job_text+util.string_yellow+suffix)

            # shared job completion code
            # single or multi-threaded, we can arrive here to harvest <= 1 jobs, and need {job, return_code} valid, and
            # we expect the start of a status line to have been printed, ready for pass/fail
            if job_done:
                jobs_complete += 1
                if job_done_return_code is None or job_done_return_code:
                    # embed the color code, to change color of pass/fail during the util.print_orange/yellow below
                    if job_done_return_code == 124:
                        # bash uses 124 for bash timeout errors, if that was preprended to the command list.
                        suffix = f"{util.string_red}<TOUT: {util.sprint_time(job_done_run_time)}>"
                    else:
                        suffix = f"{util.string_red}<FAIL: {util.sprint_time(job_done_run_time)}>"
                    failed_jobs.append(job_done_name)
                else:
                    suffix = f"{util.string_green}<PASS: {util.sprint_time(job_done_run_time)}>"
                    passed_jobs.append(job_done_name)
                # we want to print in one shot, because in fancy modes that's all that we're allowed
                job_done_text = "" if job_done_quiet else sprint_job_line(job_done_number, job_done_name)
                if len(failed_jobs): util.print_orange(f"{job_done_text}{suffix}")
                else:                util.print_yellow(f"{job_done_text}{suffix}")
                self.jobs_status[job_done_number-1] = job_done_return_code

            if not anything_done:
                time.sleep(0.25) # if nothing happens for an iteration, chill out a bit

        if total_jobs:
            emoji = "< :) >" if (len(passed_jobs) == total_jobs) else "< :( >"
            util.info(sprint_job_line(final=True,job_name="jobs passed")+emoji, start="")
        else:
            util.info(f"Parallel: <No jobs found>")
        # Make sure all jobs have a set status:
        for iter,rc in enumerate(self.jobs_status):
            if rc is None or type(rc) != int:
                self.error(f'job {iter=} {rc=} did not return a proper return code')
                jobs_status[iter] = 1

        # if self.status > 0, then keep it non-zero, else set it if we still have running jobs.
        if self.status == 0:
            self.status = 0 if len(self.jobs_status) == 0 else max(self.jobs_status)
        util.fancy_stop()

    @staticmethod
    def get_name_from_target(target: str) -> str:
        return target.replace('../', '').lstrip('./')


    def update_args_list(self, args: list, tool: str) -> None:
        '''Modfies list args, using allow-listed known top-level args:

        --config-yml
        --eda-safe
        --tool

        Many args were consumed by eda before CommandParallel saw them
        (for commands like 'multi' or 'sweep'). Some are in self.config.
         We need to apply those eda level args to each single exec-command
        '''
        if any(a.startswith('--config-yml') for a in self.config['eda_original_args']):
            cfg_yml_fname = self.config.get('config-yml', None)
            if cfg_yml_fname:
                args.append(f'--config-yml={cfg_yml_fname}')
        if '--eda-safe' in self.config['eda_original_args']:
            args.append('--eda-safe')
        if tool:
            # tool can be None, if so we won't add it to the command (assumes default from
            # config-yml auto load order)
            args.append('--tool=' + tool)


    def get_unparsed_args_on_single_command(self, command: str, tokens: list) -> list:
        '''Returns a list of args that the single (non-multi) command cannot parse

        This will error on bad --args or -arg, such as:
          eda multi sim --seeeed=1
        is not a valid arg in CommandSim

        +arg=value, +arg+value will not be included in the return list, those are
        intended to be consumed by the single/job command downstream (anything starting
        with '+')

        Used by CommandMulti and CommandSweep.
        '''
        single_cmd_handler = self.config['command_handler'][command](config=self.config)
        single_cmd_parsed, single_cmd_unparsed = single_cmd_handler.run_argparser_on_list(
            tokens=tokens.copy(),
            apply_parsed_args=False,
        )
        util.debug(f'{self.command_name}: {single_cmd_unparsed=}')

        # There should not be any single_cmd_unparsed args starting with '-'
        bad_remaining_args = [x for x in single_cmd_unparsed if x.startswith('-')]
        if bad_remaining_args:
            self.error(f'for {self.command_name} {command=} the following args are unknown',
                       f'{bad_remaining_args}')

        # Remove unparsed args starting with '+', since those are commonly sent downstream to
        # single job (example, CommandSim plusargs).
        return [x for x in single_cmd_unparsed if not x.startswith('+')]


    def patch_jobs_for_duplicate_target_names(self) -> None:
        '''Examines list self.jobs, and if leaf target names are duplicate will
        patch each command's job-name to:
            --job-name=path.leaf.command[.tool]
        '''

        def get_job_name(job_dict: dict) -> str:
            '''Fishes the job-name out of an entry in self.jobs'''
            for i, item in enumerate(job_dict['command_list']):
                if item.startswith('--job-name='):
                    _, name = item.split('--job-name=')
                    return name
                elif item == '--job-name':
                    return job_dict['command_list'][i + 1]
            return ''

        def replace_job_name(job_dict: dict, new_job_name: str) -> dict:
            '''Replaces the job-name in an entry in self.jobs'''
            for i, item in enumerate(job_dict['command_list']):
                if item.startswith('--job-name='):
                    job_dict['command_list'][i] = '--job-name=' + new_job_name
                    return job_dict
                elif item == '--job-name':
                    job_dict['command_list'][i + 1] = new_job_name
                    return job_dict
            return job_dict


        job_names_count_dict = {}
        for job_dict in self.jobs:

            key = get_job_name(job_dict)
            if not key:
                self.error(f'{job_dict=} needs to have a --job-name= arg attached')
            if key not in job_names_count_dict:
                job_names_count_dict[key] = 1
            else:
                job_names_count_dict[key] += 1

        for i, job_dict in enumerate(self.jobs):
            key = get_job_name(job_dict)
            if job_names_count_dict[key] < 2:
                continue

            tpath, _ = os.path.split(job_dict['target'])

            # prepend path information to job-name:
            patched_sub_work_dir = False
            patched_target_path = os.path.relpath(tpath).replace(os.sep, '_')
            new_job_name = f'{patched_target_path}.{key}'
            new_job_dict = replace_job_name(job_dict, new_job_name)
            self.jobs[i] = new_job_dict
            util.debug(f'Patched job {job_dict["name"]}: --job-name={new_job_name}')

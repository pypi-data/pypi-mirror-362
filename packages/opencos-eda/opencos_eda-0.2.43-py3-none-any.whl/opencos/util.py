
# SPDX-License-Identifier: MPL-2.0

import sys
import subprocess
import datetime
import os
import time
import atexit
import shutil
import traceback
import argparse
import yaml
import re
import textwrap

from opencos import eda_config

global_exit_allowed = False
progname = "UNKNOWN"
progname_in_message = True
logfile = None
loglast = 0
debug_level = 0

args = {
    'color' : False,
    'quiet' : False,
    'verbose' : False,
    'debug' : False,
    'fancy' : sys.stdout.isatty(),
    'warnings' : 0,
    'errors' : 0,
}


def strip_all_quotes(s:str):
    return s.replace("'", '').replace('"', '')

def strip_outer_quotes(s:str):
    ret = str(s)
    while (ret.startswith("'") and ret.endswith("'")) or \
          (ret.startswith('"') and ret.endswith('"')):
        ret = ret[1:-1]
    return ret


def yaml_load_only_root_line_numbers(filepath:str):
    '''Returns a dict of {key: int line number}, very crude'''
    # Other solutions aren't as attractive, require a lot of mappers to get
    # line numbers on returned values that aren't dict
    data = None
    with open(filepath) as f:
        try:
            # Try to do a very lazy parse of root level keys only, returns dict{key:lineno}
            data = dict()
            for lineno,line in enumerate(f.readlines()):
                m = re.match(r'^(\w+):', line)
                if m:
                    key = m.group(1)
                    data[key] = lineno + 1
        except Exception as e:
            error(f"Error loading YAML {filepath=}:", e)
    return data


def toml_load_only_root_line_numbers(filepath:str):
    '''Returns a dict of {key: int line number}, very crude'''
    data = None
    with open(filepath) as f:
        try:
            data = dict()
            for lineno, line in enumerate(f.readlines()):
                m = re.match(r'^\[(\w+)\]', line)
                if m:
                    key = m.group(1)
                    data[key] = lineno + 1
        except Exception as e:
            error(f'Error loading TOML {filepath=}', e)
    return data


def yaml_safe_load(filepath:str, only_root_line_numbers=False):
    '''Returns dict or None from filepath (str), errors if return type not in assert_return_types.

    (assert_return_types can be empty list to avoid check.)

    only_root_line_numbers -- if True, will return a dict of {key: line number (int)} for
                              all the root level keys. Used for debugging DEPS.yml in
                              eda.CommandDesign.resolve_target_core
    '''

    data = None

    if only_root_line_numbers:
        return yaml_load_only_root_line_numbers(filepath)

    with open(filepath) as f:
        debug(f'Opening {filepath=}')
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as e:

            # if yamllint is installed, then use it to get all errors in the .yml|.yaml
            # file, instead of the single exception.
            if shutil.which('yamllint'):
                try:
                    sp_out = subprocess.run(
                        f'yamllint -d relaxed --no-warnings {filepath}'.split(),
                        capture_output=True, text=True )
                    for x in sp_out.stdout.split('\n'):
                        if x:
                            info('yamllint: ' + x)
                except:
                    pass

            if hasattr(e, 'problem_mark'):
                mark = e.problem_mark
                error(f"Error parsing {filepath=}: line {mark.line + 1},",
                      f"column {mark.column +1}: {e.problem}")
            else:
                error(f"Error loading YAML {filepath=}:", e)
        except Exception as e:
            error(f"Error loading YAML {filepath=}:", e)

    return data


def yaml_safe_writer(data:dict, filepath:str) -> None:

    if filepath.endswith('.yml') or filepath.endswith('.yaml'):
        with open(filepath, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True,
                      default_flow_style=False, sort_keys=False, encoding=('utf-8'))
    else:
        warning(f'{filepath=} to be written for this extension not implemented.')



def start_log(filename, force=False):
    global logfile, loglast
    if os.path.exists(filename):
        if force:
            info(f"Overwriting '{filename}', which exists, due to --force-logfile.")
        else:
            error(f"The --logfile path '{filename}' exists.  Use --force-logfile (vs --logfile) to override.")
    try:
        logfile = open( filename, 'w')
        debug(f"Opened logfile '{filename}' for writing")
    except Exception as e:
        error(f"Error opening '{filename}' for writing!")

def write_log(text, end):
    global logfile, loglast
    sw = text.startswith(f"INFO: [{progname}]")
    if (((time.time() - loglast) > 10) and
        (text.startswith(f"DEBUG: [{progname}]") or
         text.startswith(f"INFO: [{progname}]") or
         text.startswith(f"WARNING: [{progname}]") or
         text.startswith(f"ERROR: [{progname}]"))):
        dt = datetime.datetime.now().ctime()
        print(f"INFO: [{progname}] Time: {dt}", file=logfile)
        loglast = time.time()
    print(text, end=end, file=logfile)
    logfile.flush()
    os.fsync(logfile)

def stop_log():
    global logfile, loglast
    if logfile:
        debug(f"Closing logfile")
        logfile.close()
    logfile = None
    loglast = 0

atexit.register(stop_log)

def get_argparse_bool_action_kwargs() -> dict:
    bool_kwargs = dict()
    x = getattr(argparse, 'BooleanOptionalAction', None)
    if x is not None:
        bool_kwargs['action'] = x
    else:
        bool_kwargs['action'] = 'store_true'
    return bool_kwargs

def get_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog='opencos common options', add_help=False, allow_abbrev=False)
    # We set allow_abbrev=False so --force-logfile won't try to attempt parsing shorter similarly
    # named args like --force, we want those to go to unparsed list.
    # For bools, support --color and --no-color with this action=argparse.BooleanOptionalAction
    # -- however Python3.8 and older does not support this, so as a workaround, use kwargs for
    #    boolean actions:
    bool_action_kwargs = get_argparse_bool_action_kwargs()

    parser.add_argument('--version', default=False, action='store_true')
    parser.add_argument('--color', **bool_action_kwargs, default=True,
                        help='Use shell colors for info/warning/error messaging')
    parser.add_argument('--quiet', **bool_action_kwargs, help='Do not display info messaging')
    parser.add_argument('--verbose', **bool_action_kwargs,
                        help='Display additional messaging level 2 or higher')
    parser.add_argument('--fancy', **bool_action_kwargs)
    parser.add_argument('--debug', **bool_action_kwargs,
                        help='Display additional debug messaging level 1 or higher')
    parser.add_argument('--debug-level', type=int, default=0,
                        help='Set debug level messaging (default: 0)')
    parser.add_argument('--logfile', type=str, default='',
                        help='Write eda messaging to logfile (default disabled)')
    parser.add_argument('--force-logfile', type=str, default='',
                        help='Set to force overwrite the logfile')
    parser.add_argument('--no-respawn', action='store_true',
                        help='Legacy mode (default respawn disabled) for respawning eda.py using $OC_ROOT/bin')
    return parser

def get_argparser_short_help(parser=None) -> str:
    if not parser:
        parser = get_argparser()
    full_lines = parser.format_help().split('\n')
    lineno = 0
    for lineno, line in enumerate(full_lines):
        if line.startswith('options:'):
            break
    # skip the line that says 'options:', repalce with the progname:
    return f'{parser.prog}:\n' + '\n'.join(full_lines[lineno + 1:])


def process_token(arg:str) -> bool:
    # This is legacy holdover for oc_cli.py, that would process one token at a time.
    # Simply run through our full argparser.
    parsed, unparsed = process_tokens(tokens[arg])
    if len(unparsed) == 0:
        debug(f"Processed command: {arg}")
        return True
    return False


def process_tokens(tokens:list) -> (argparse.Namespace, list):
    global debug_level

    parser = get_argparser()
    try:
        parsed, unparsed = parser.parse_known_args(tokens + [''])
        unparsed = list(filter(None, unparsed))
    except argparse.ArgumentError:
        error(f'problem attempting to parse_known_args for {tokens=}')

    if parsed.debug_level: set_debug_level(parsed.debug_level)
    elif parsed.debug:     set_debug_level(1)
    else:                  debug_level = 0

    debug(f'util.process_tokens: {parsed=} {unparsed=}  from {tokens=}')

    if parsed.force_logfile != '':
        start_log(parsed.force_logfile, force=True)
    elif parsed.logfile != '':
        start_log(parsed.logfile, force=False)

    parsed_as_dict = vars(parsed)
    for key,value in parsed_as_dict.items():
        if value is not None:
            args[key] = value # only update with non-None values to our global 'args' dict
    return parsed, unparsed

def indent_wrap_long_text(text, width=80, initial_indent=0, indent=4):
    """Returns str, wraps text to a specified width and indents subsequent lines."""
    wrapped_lines = textwrap.wrap(text, width=width,
                                  initial_indent=' ' * initial_indent,
                                  subsequent_indent=' ' * indent)
    return '\n'.join(wrapped_lines)

# ********************
# fancy support
# In fancy mode, we take the bottom fancy_lines_ lines of the screen to be written using fancy_print,
# while the lines above that show regular scrolling content (via info, debug, warning, error above).
# User should not use print() when in fancy mode

fancy_lines_ = []

def fancy_start(fancy_lines = 4, min_vanilla_lines = 4):
    global fancy_lines_
    (columns,lines) = shutil.get_terminal_size()
    if (fancy_lines < 2):
        error(f"Fancy mode requires at least 2 fancy lines")
    if (fancy_lines > (lines-min_vanilla_lines)):
        error(f"Fancy mode supports at most {(lines-min_vanilla_lines)} fancy lines, given {min_vanilla_lines} non-fancy lines")
    if len(fancy_lines_): error(f"We are already in fancy line mode??")
    for _ in range(fancy_lines-1):
        print("") # create the requisite number of blank lines
        fancy_lines_.append("")
    print("", end="") # the last line has no "\n" because we don't want ANOTHER blank line below
    fancy_lines_.append("")
    # the cursor remains at the leftmost character of the bottom line of the screen

def fancy_stop():
    global fancy_lines_
    if len(fancy_lines_): # don't do anything if we aren't in fancy mode
        # user is expected to have painted something into the fancy lines, we can't "pull down" the regular
        # lines above, and we don't want fancy_lines_ blank or garbage lines either, that's not pretty
        fancy_lines_ = []
        # since cursor is always left at the leftmost character of the bottom line of the screen, which was
        # one of the fancy lines which now has the above-mentioned "something", we want to move one lower
        print("")

def fancy_print(text, line):
    global fancy_lines_
    # strip any newline, we don't want to print that
    if text.endswith("\n"): text.rstrip()
    lines_above = len(fancy_lines_) - line - 1
    if lines_above:
        print(f"\033[{lines_above}A"+ # move cursor up
              text+f"\033[1G"+ # desired text, then move cursor to the first character of the line
              f"\033[{lines_above}B", # move the cursor down
              end="", flush=True)
    else:
        print(text+f"\033[1G", # desired text, then move cursor to the first character of the line
              end="", flush=True)
    fancy_lines_[line] = text

def print_pre():
    # stuff we do before printing any line
    if len(fancy_lines_):
        # Also, note that in fancy mode we don't allow the "above lines" to be partially written, they
        # are assumed to be full lines ending in "\n"
        # As always, we expect the cursor was left in the leftmost character of bottom line of screen
        print(f"\033[{len(fancy_lines_)-1}A"+ # move the cursor up to where the first fancy line is drawn
              f"\033[0K", # clear the old fancy line 0
              end="",flush=True)

def print_post(text, end):
    # stuff we do after printing any line
    if len(fancy_lines_):
        #time.sleep(1)
        # we just printed a line, including a new line, on top of where fancy line 0 used to be, so cursor
        # is now at the start of fancy line 1.
        # move cursor down to the beginning of the final fancy line (i.e. standard fancy cursor resting place)
        for x in range(len(fancy_lines_)):
            print("\033[0K",end="") # erase the line to the right
            print(fancy_lines_[x],flush=True,end=('' if x==(len(fancy_lines_)-1) else '\n'))
            #time.sleep(1)
        print("\033[1G", end="", flush=True)
    if logfile: write_log(text, end=end)

string_red = f"\x1B[31m"
string_green = f"\x1B[32m"
string_orange = f"\x1B[33m"
string_yellow = f"\x1B[39m"
string_normal = f"\x1B[0m"

def print_red(text, end='\n'):
    print_pre()
    print(f"{string_red}{text}{string_normal}" if args['color'] else f"{text}", end=end, flush=True)
    print_post(text, end)

def print_green(text, end='\n'):
    print_pre()
    print(f"{string_green}{text}{string_normal}" if args['color'] else f"{text}", end=end, flush=True)
    print_post(text, end)

def print_orange(text, end='\n'):
    print_pre()
    print(f"{string_orange}{text}{string_normal}" if args['color'] else f"{text}", end=end, flush=True)
    print_post(text, end)

def print_yellow(text, end='\n'):
    print_pre()
    print(f"{string_yellow}{text}{string_normal}" if args['color'] else f"{text}", end=end, flush=True)
    print_post(text, end)

def set_debug_level(level):
    global debug_level
    debug_level = level
    args['debug'] = (level > 0)
    args['verbose'] = (level > 1)
    info(f"Set debug level to {debug_level}")

# the <<d>> stuff is because we change progname after this is read in.  if we instead infer progname or
# get it passed somehow, we can avoid this ugliness / performance impact (lots of calls to debug happen)
def debug(*text, level=1, start='<<d>>', end='\n'):
    if start=='<<d>>': start = f"DEBUG: " + (f"[{progname}] " if progname_in_message else "")
    if args['debug'] and (((level==1) and args['verbose']) or (debug_level >= level)):
        print_yellow(f"{start}{' '.join(list(text))}", end=end)

def info(*text, start='<<d>>', end='\n'):
    if start=='<<d>>': start = f"INFO: " + (f"[{progname}] " if progname_in_message else "")
    if not args['quiet']:
        print_green(f"{start}{' '.join(list(text))}", end=end)

def warning(*text, start='<<d>>', end='\n'):
    if start=='<<d>>': start = f"WARNING: " + (f"[{progname}] " if progname_in_message else "")
    args['warnings'] += 1
    print_orange(f"{start}{' '.join(list(text))}", end=end)

def error(*text, error_code=-1, do_exit=True, start='<<d>>', end='\n') -> int:
    if start=='<<d>>': start = f"ERROR: " + (f"[{progname}] " if progname_in_message else "")
    args['errors'] += 1
    print_red(f"{start}{' '.join(list(text))}", end=end)
    if do_exit:
        if args['debug']: print(traceback.print_stack())
        return exit(error_code)
    else:
        if error_code is None:
            return 0
        else:
            return abs(int(error_code))

def exit(error_code=0, quiet=False):
    if global_exit_allowed:
        if not quiet: info(f"Exiting with {args['warnings']} warnings, {args['errors']} errors")
        sys.exit(error_code)

    if error_code is None:
        return 0
    else:
        return abs(int(error_code))

def getcwd():
    try:
        cc = os.getcwd()
    except Exception as e:
        error("Unable to getcwd(), did it get deleted from under us?")
    return cc

_oc_root=None
_oc_root_set=False
def get_oc_root(error_on_fail:bool=False):
    global _oc_root
    global _oc_root_set
    '''Returns a str or False for the root directory of *this* repo.

    If environment variable OC_ROOT is set, that is used instead, otherwise attempts to use
    `git rev-parse`
    '''
    # if we've already run through here once, just return the memorized result
    if _oc_root_set: return _oc_root

    # try looking for an env var
    s = os.environ.get('OC_ROOT')
    if s:
        debug(f'get_oc_root() -- returning from env: {s=}')
        _oc_root = s.strip()
    else:
        # try asking GIT
        cp = subprocess.run('git rev-parse --show-toplevel', stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                            shell=True, universal_newlines=True)
        if cp.returncode != 0:
            # TODO(drew): at some point, address the fact that not all repos are oc_root.  Is this function asking for
            # the repo we are in?  or a pointer to the oc_root which maybe elsewhere on the system?
            print_didnt_find_it = debug
            if error_on_fail:
                print_didnt_find_it = error
            print_didnt_find_it(f'Unable to get a OC_ROOT directory using git rev-parse')
        else:
            _oc_root = cp.stdout.strip()
            if sys.platform == 'win32':
                _oc_root = _oc_root.replace('/', '\\') # git gives us /, but we need \

    # there is no sense running through this code more than once
    _oc_root_set = True
    return _oc_root

def string_or_space(text, whitespace=False):
    if whitespace:
        return " " * len(text)
    else:
        return text

def sprint_time(s):
    s = int(s)
    txt = ""
    do_all = False
    # days
    if (s >= (24*60*60)): # greater than 24h, we show days
        d = int(s/(24*60*60))
        txt += f"{d}d:"
        s -= (d*24*60*60)
        do_all = True
    # hours
    if do_all or (s >= (60*60)):
        d = int(s/(60*60))
        txt += f"{d:2}:"
        s -= (d*60*60)
        do_all = True
    # minutes
    d = int(s/(60))
    txt += f"{d:02}:"
    s -= (d*60)
    # seconds
    txt += f"{s:02}"
    return txt

def safe_cp(source:str, destination:str, create_dirs:bool=False):
    try:
        # Infer if destination is a directory
        if destination.endswith('/') or os.path.isdir(destination):
            if not os.path.exists(destination) and create_dirs:
                os.makedirs(destination, exist_ok=True)
            destination = os.path.join(destination, os.path.basename(source))
        else:
            # Ensure parent directory exists if needed
            parent_dir = os.path.dirname(destination)
            if create_dirs and parent_dir and not os.path.exists(parent_dir):
                os.makedirs(parent_dir, exist_ok=True)
        # actually copy the file
        shutil.copy2(source, destination)
    except Exception as e:
        print(f"Error copying file from '{source}' to '{destination}': {e}")
    info(f"Copied {source} to {destination}")

def safe_rmdir(path):
    """Safely and reliably remove a non-empty directory."""
    try:
        # Ensure the path exists
        if os.path.exists(path):
            shutil.rmtree(path)
            info(f"Directory '{path}' has been removed successfully.")
        else:
            debug(f"Directory '{path}' does not exist.")
    except Exception as e:
        error(f"An error occurred while removing the directory '{path}': {e}")

def safe_mkdir(path : str):
    try:
        os.mkdir(path)
    except FileExistsError:
        pass
    except:
        try:
            os.system(f'mkdir -p {path}')
        except Exception as e:
            error(f'unable to mkdir {path=}, exception {e=}')

def safe_mkdirs(base : str, new_dirs : list):
    for p in new_dirs:
        safe_mkdir( os.path.join(base, p) )


def import_class_from_string(full_class_name):
    """
    Imports a class given its full name as a string.

    Args:
        full_class_name: The full name of the class,
                         e.g., "module.submodule.ClassName".

    Returns:
        The imported class, or None if an error occurs.
    """
    from importlib import import_module
    try:
        module_path, class_name = full_class_name.rsplit(".", 1)
        module = import_module(module_path)
        return getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        print(f"Error importing class {full_class_name=}: {e=}")
        return None


class ShellCommandList(list):
    def __init__(self, obj=None, tee_fpath=None):
        super().__init__(obj)
        for k in ['tee_fpath']:
            setattr(self, k, getattr(obj, k, None))
        if tee_fpath:
            self.tee_fpath = tee_fpath


def write_shell_command_file(dirpath : str, filename : str, command_lists : list, line_breaks : bool = False):
    ''' Writes new file at {dirpath}/{filename} as a bash shell command, using command_lists (list of lists)

    -- dirpath (str)        -- directory where file is written (usually eda.work/{target}_sim
    -- filename (str)       -- filename, for example compile_only.sh
    -- command_lists (list) -- list of (list or ShellCommandList), each item in the list is a list of commands (aka, how
                               subprocess.run(args) uses a list of commands.
    -- line_breaks (bool)   -- Set to True to have 1 word per line in the file followed by a line break.
                               Default False has an entry in command_lists all on a single line.

    Returns None, writes the file and chmod's it to 0x755.

    '''
    # command_lists should be a list-of-lists.
    bash_path = shutil.which('bash')
    assert type(command_lists) is list, f'{command_lists=}'
    fullpath = os.path.join(dirpath, filename)
    with open(fullpath, 'w') as f:
        if not bash_path:
            bash_path = "/bin/bash" # we may not get far, but we'll try
        f.write('#!' + bash_path + '\n\n')
        for obj in command_lists:
            assert isinstance(obj, list), f'{obj=} (obj must be list/ShellCommandList) {command_lists=}'
            clist = list(obj).copy()
            tee_fpath = getattr(obj, 'tee_fpath', None)
            if tee_fpath:
                # Note the | tee foo.log will ruin bash error codes, so if we're bash is
                # available, we'll check that ${PIPESTATUS} is 0 to percolate the
                # a non-zero on the first command (sim.exe).
                if shutil.which('bash'):
                    clist.append(f'2>&1 | tee {tee_fpath}' + ' && test ${PIPESTATUS} -eq 0')
                else:
                    clist.append(f'2>&1 | tee {tee_fpath}')

            if len(clist) > 0:
                if line_breaks:
                    # line_breaks=True - have 1 word per line, followed by \ and \n
                    sep = " \\" + "\n"
                    f.write(sep.join(clist))
                    f.write(" \n")
                else:
                    # line_break=False (default) - all words on 1 line.
                    f.write(' '.join(clist))
                    f.write(" \n")
            else:
                f.write("\n")
        f.write("\n")
        f.close()
        os.chmod(fullpath, 0o755)


def write_eda_config_and_args(dirpath : str, filename='eda_output_config.yml', command_obj_ref=None):
    import copy
    if command_obj_ref is None:
        return
    fullpath = os.path.join(dirpath, filename)
    data = dict()
    for x in ['command_name', 'config', 'target', 'args', 'modified_args', 'defines',
              'incdirs', 'files_v', 'files_sv', 'files_vhd']:
        # Use deep copy b/c otherwise these are references to opencos.eda.
        data[x] = copy.deepcopy(getattr(command_obj_ref, x, ''))

    # fix some burried class references in command_obj_ref.config,
    # otherwise we won't be able to safe load this yaml, so cast as str repr.
    for k, v in command_obj_ref.config.items():
        if k == 'command_handler':
            data['config'][k] = str(v)

    yaml_safe_writer(data=data, filepath=fullpath)


def get_inferred_top_module_name(module_guess: str, module_fpath: str) -> str:
    '''Returns the best guess as the 'top' module name name, given a fpath where

    module_fpath = /some/path/to/module_guess.[v|sv]

    Use the module_guess if it exists in the file as: module <module_guess>
    Otherwise use the last observed: module <best_guess>
    Otherwise use blank str
    '''

    best_guess = ''
    if not os.path.isfile(module_fpath):
        return ''
    with open(module_fpath, encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip()
            if line.startswith('module '):
                parts = line.split()
                module_name = parts[1]
                rstrip_nonword_pattern = r'\W+$'
                module_name = re.sub(rstrip_nonword_pattern, '', module_name)
                if bool(re.fullmatch(r'^\w+$', module_name)):
                    if module_name == module_guess:
                        return module_guess
                    elif module_name:
                        best_guess = module_name
    if best_guess:
        return best_guess
    else:
        return ''


def subprocess_run(work_dir, command_list, fake:bool=False, shell=False) -> int:
    ''' Run command_list in the foreground, with preference to use bash if shell=True.'''

    if work_dir is not None:
        os.chdir(work_dir)

    proc_kwargs = {'shell': shell}
    bash_exec = shutil.which('bash')
    if shell and bash_exec:
        proc_kwargs.update({'executable': bash_exec})

    if shell:
        c = ' '.join(command_list)
    else:
        c = command_list

    if fake:
        info(f"util.subprocess_run FAKE: would have called subprocess.run({c}, **{proc_kwargs}")
        return 0
    else:
        debug(f"util.subprocess_run: About to call subprocess.run({c}, **{proc_kwargs}")
        proc = subprocess.run(c, **proc_kwargs)
        return proc.returncode


def subprocess_run_background(work_dir, command_list, background=True, fake:bool=False,
                              shell=False, tee_fpath=None) -> (str, str, int):
    ''' Run command_list in the background, with preference to use bash if shell=True

    tee_fpath is relative to work_dir.
    '''

    debug(f'util.subprocess_run_background: {background=} {tee_fpath=} {shell=}')

    if fake or (not background and not tee_fpath):
        # If tee_fpath is set, we're going to "background" but with it also
        # printed out (stdout and tee_fpath).
        rc = subprocess_run(work_dir, command_list, fake=fake, shell=shell)
        return '', '', rc

    if work_dir is not None:
        os.chdir(work_dir)

    proc_kwargs = {'shell': shell,
                   'stdout': subprocess.PIPE,
                   'stderr': subprocess.STDOUT,
                   }

    bash_exec = shutil.which('bash')
    if shell and bash_exec:
        proc_kwargs.update({'executable': bash_exec})

    if shell:
        c = ' '.join(command_list)
    else:
        c = command_list # leave as list.

    debug(f"util.subprocess_run_background: about to call subprocess.Popen({c}, **{proc_kwargs})")
    proc = subprocess.Popen(c, **proc_kwargs)

    if tee_fpath:
        stdout = ''
        stderr = ''
        with open(tee_fpath, 'w') as f:
            for line in iter(proc.stdout.readline, b''):
                line = line.rstrip().decode("utf-8")
                if not background:
                    print(line)
                f.write(line + '\n')
                stdout += line + '\n'

        proc.communicate()
        rc = proc.returncode
        info('util.subprocess_run_background: wrote: ' + os.path.abspath(tee_fpath))


    else:

        debug(f"util.subprocess_run_background: about to call proc.communicate()")
        stdout, stderr = proc.communicate()
        rc = proc.returncode

        stdout = stdout.decode('utf-8') if stdout else ""
        stderr = stderr.decode('utf-8') if stderr else ""
        debug(f"shell_run_background: {rc=}")
        if stdout:
            for lineno, line in enumerate(stdout.strip().split('\n')):
                debug(f"stdout:{lineno+1}: {line}")
        if stderr:
            for lineno, line in enumerate(stdout.strip().split('\n')):
                debug(f"stderr:{lineno+1}: {line}")

    return stdout, stderr, rc


def sanitize_defines_for_sh(value):
    # Need to sanitize this for shell in case someone sends a +define+foo+1'b0,
    # which needs to be escaped as +define+foo+1\'b0, otherwise bash or sh will
    # think this is an unterminated string.
    # TODO(drew): decide if we should instead us shlex.quote('+define+key=value')
    # instead of this function.
    if type(value) is str:
        value = value.replace("'", "\\" + "'")
    return value

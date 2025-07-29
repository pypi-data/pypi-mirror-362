''' opencos.tools.yosys - base class for slang_yosys.py, invio_yosys.py, tabbycad_yosys.py

Contains classes for ToolYosys
'''

# pylint: disable=R0801 # (calling functions with same arguments)

import os
import shutil
import subprocess

from opencos import util
from opencos.eda_base import Tool
from opencos.commands import CommandSynth

class ToolYosys(Tool):
    '''Parent class for ToolTabbyCadYosys, ToolInvioYosys, ToolSlangYosys'''

    _TOOL = 'yosys'
    _EXE = 'yosys'
    _URL = 'https://yosyshq.readthedocs.io/en/latest/'

    yosys_exe = ''
    sta_exe = ''
    sta_version = ''

    def get_versions(self) -> str:
        if self._VERSION:
            return self._VERSION

        path = shutil.which(self._EXE)
        if not path:
            self.error(f'"{self._EXE}" not in path or not installed, see {self._URL}')
        else:
            self.yosys_exe = path

        # Unforunately we don't have a non-PATH friendly support on self._EXE to set
        # where standalone 'sta' is. Even though Yosys has 'sta' internally, Yosys does
        # not fully support timing constraints or .sdc files, so we have to run 'sta'
        # standalone.
        sta_path = shutil.which('sta')
        if sta_path:
            util.debug(f'Also located "sta" via {sta_path}')
            self.sta_exe = sta_path
            sta_version_ret = subprocess.run(
                [self.sta_exe, '-version'], capture_output=True, check=False
            )
            util.debug(f'{self.yosys_exe} {sta_version_ret=}')
            sta_ver = sta_version_ret.stdout.decode('utf-8').split()[0]
            if sta_ver:
                self.sta_version = sta_ver

        version_ret = subprocess.run(
            [self.yosys_exe, '--version'], capture_output=True, check=False
        )
        util.debug(f'{self.yosys_exe} {version_ret=}')

        # Yosys 0.48 (git sha1 aaa534749, clang++ 14.0.0-1ubuntu1.1 -fPIC -O3)
        words = version_ret.stdout.decode('utf-8').split()

        if len(words) < 2:
            self.error(f'{self.yosys_exe} --version: returned unexpected str {version_ret=}')
        self._VERSION = words[1]
        return self._VERSION

    def set_tool_defines(self):
        self.defines.update({
            'OC_TOOL_YOSYS': None
        })
        if 'OC_LIBRARY' not in self.defines:
            self.defines.update({
                'OC_LIBRARY_BEHAVIORAL': None,
                'OC_LIBRARY': "0"
            })


class CommonSynthYosys(CommandSynth, ToolYosys):
    '''Common parent class used by invio_yosys and tabbycad_yosys

    for child classes: CommandSynthInvioYosys and tabbycad_yosys.CommandSynthTabbyCadYosys
    '''

    def __init__(self, config:dict):
        CommandSynth.__init__(self, config=config)
        ToolYosys.__init__(self, config=self.config)

        self.args.update({
            'sta': False,
            'liberty-file': '',
            'sdc-file': '',
            'yosys-synth': 'synth',              # synth_xilinx, synth_altera, etc (see: yosys help)
            'yosys-pre-synth': ['prep', 'proc'], # command run in yosys prior to yosys-synth.
            'yosys-blackbox': [],                # list of modules that yosys will blackbox.
        })
        self.args_help.update({
            'sta': 'After running Yosys, run "sta" with --liberty-file.' \
            + ' sta can be installed via: https://github.com/The-OpenROAD-Project/OpenSTA',
            'sdc-file': '.sdc file to use with --sta, if not present will use auto constraints',
            'liberty-file': 'Single liberty file for synthesis and sta,' \
            + ' for example: github/OpenSTA/examples/nangate45_slow.lib.gz',
            'yosys-synth': 'The synth command provided to Yosys, see: yosys help.',
            'yosys-pre-synth': 'Yosys commands performed prior to running "synth"' \
            + ' (or eda arg value for --yosys-synth)',
            'yosys-blackbox': 'List of modules that yosys will blackbox, likely will need these' \
            + ' in Verilog-2001 for yosys to read outside of slang and synth',
        })

        self.yosys_out_dir = ''
        self.yosys_v_path = ''
        self.full_work_dir = ''
        self.blackbox_list = []

    def do_it(self) -> None:
        self.set_tool_defines()
        self.write_eda_config_and_args()

        # Set up some dirs and filenames.
        self.full_work_dir = self.args.get('work-dir', '')
        if not self.full_work_dir:
            self.error(f'work_dir={self.full_work_dir} is not set')
        self.full_work_dir = os.path.abspath(self.full_work_dir)
        self.yosys_out_dir = os.path.join(self.full_work_dir, 'yosys')
        util.safe_mkdir(self.yosys_out_dir)
        self.yosys_v_path = os.path.join(self.yosys_out_dir, f'{self.args["top"]}.v')

        if self.is_export_enabled():
            self.do_export()
            return

        self.write_and_run_yosys_f_files()

    def write_and_run_yosys_f_files(self, **kwargs) -> None:
        '''Derived classes must define, to run remainder of do_it() steps'''
        raise NotImplementedError


    def create_yosys_synth_f(self) -> util.ShellCommandList:
        '''Derived classes may define, if they wish to get a list of yosys commands'''
        return util.ShellCommandList([])


    def get_synth_command_lines(self) -> list:
        '''Common yosys tcl after all blackbox and read_verilog commands'''

        lines = []
        lines += self.args.get('yosys-pre-synth', [])

        synth_command = self.args.get('yosys-synth', 'synth')
        if self.args['flatten-all']:
            synth_command += ' -flatten'

        lines.append(synth_command)


        # TODO(drew): I need a blackbox flow here? Or a memory_libmap?
        #   --> https://yosyshq.readthedocs.io/projects/yosys/en/latest/cmd/memory_libmap.html
        # TODO(drew): can I run multiple liberty files?
        if self.args['liberty-file']:
            lines += [
                'dfflibmap -liberty ' + self.args['liberty-file'],
                #'memory_libmap -lib ' + self.args['liberty-file'], # Has to be unzipped?
                'abc -liberty  ' + self.args['liberty-file'],
            ]
        lines += [
            'opt_clean',
            f'write_verilog {self.yosys_v_path}',
            f'write_json {self.yosys_v_path}.json',
        ]
        return lines


    def create_sta_f(self) -> util.ShellCommandList:
        '''Returns command list, for running 'sta' on sta.f'''

        if not self.args['sta']:
            return []

        if not self.args['liberty-file']:
            self.error('--sta is set, but need to also set --liberty-file=<file>')

        if self.args['sdc-file']:
            if not os.path.exists(self.args['sdc-file']):
                self.error(f'--sdc-file={self.args["sdc-file"]} file does not exist')

        if not self.sta_exe:
            self.error(f'--sta is set, but "sta" was not found in PATH, see: {self._URL}')

        sta_command_list = util.ShellCommandList(
            [ self.sta_exe, '-no_init', '-exit', 'sta.f' ],
            tee_fpath = 'sta.log'
        )

        # Need to create sta.f:
        if self.args['sdc-file']:
            sdc_path = self.args['sdc-file']
        else:
            # Need to create sdc.f:
            sdc_path = 'sdc.f'
            self.create_sdc_f()

        with open(os.path.join(self.args['work-dir'], 'sta.f'), 'w',
                  encoding='utf-8') as f:
            lines = [
                'read_liberty ' + self.args['liberty-file'],
                'read_verilog ' + self.yosys_v_path,
                'link_design ' + self.args['top'],
                'read_sdc ' + sdc_path,
                'report_checks',
            ]
            f.write('\n'.join(lines))

        return util.ShellCommandList(
            sta_command_list,
            tee_fpath = 'sta.log'
        )


    def create_sdc_f(self) -> None:
        '''Returns None, creates sdc.f'''

        if self.args['sdc-file']:
            # already exists from args, return b/c nothing to create.
            return

        with open(os.path.join(self.args['work-dir'], 'sdc.f'), 'w',
                  encoding='utf-8') as f:
            clock_name = self.args['clock-name']
            period = self.args['clock-ns']
            name_not_equal_clocks_str = f'NAME !~ "{clock_name}"'
            lines = [
                f'create_clock -add -name {clock_name} -period {period} [get_ports ' \
                + '{' + clock_name + '}];',
                f'set_input_delay -max {self.args["idelay-ns"]} -clock {clock_name}' \
                + ' [get_ports * -filter {DIRECTION == IN && ' \
                + name_not_equal_clocks_str + '}];',
                f'set_output_delay -max {self.args["odelay-ns"]} -clock {clock_name}' \
                + ' [get_ports * -filter {DIRECTION == OUT}];',
            ]
            f.write('\n'.join(lines))

'''pytests for: eda [multi|tools-multi] synth [args] <target(s)>'''

import os
import pytest

from opencos import eda, eda_tool_helper
from opencos.tests import helpers


thispath = os.path.dirname(__file__)

def chdir_remove_work_dir(relpath):
    '''Changes dir to relpath, removes the work directories (eda.work, eda.export*)'''
    return helpers.chdir_remove_work_dir(thispath, relpath)

# Figure out what tools the system has available, without calling eda.main(..)
config, tools_loaded = eda_tool_helper.get_config_and_tools_loaded()

# list of tools we'd like to try:
list_of_synth_tools = [
    'invio_yosys',
    'tabbycad_yosys',
    'slang_yosys'
]

list_of_elab_tools = [
    'invio_yosys',
    'slang_yosys'
]

def skip_it(tool, command) -> bool:
    '''skip_it: returns True if we should skip due to lack of tool existence'''
    return bool( tool not in tools_loaded or
                 (command == 'elab' and tool not in list_of_elab_tools) or
                 (command == 'synth' and tool not in list_of_synth_tools) )


@pytest.mark.parametrize("tool", list_of_synth_tools)
@pytest.mark.parametrize("command", ['elab', 'synth'])
class Tests:
    '''skippable (via pytest parameters) class holder for pytest methods'''

    def test_args_multi_synth_bad_target_should_fail(self, tool, command):
        '''Tests: eda mulit <elab|synth>, and this test should fail.'''
        if skip_it(tool, command):
            pytest.skip(f"{tool=} {command=} skipped, {tools_loaded=}")
            return # skip/pass
        chdir_remove_work_dir('../../lib')
        cmdlist = (f'multi {command} --debug --fail-if-no-targets --tool {tool}'
                   ' target_doesnt_exist*').split()
        rc = eda.main(*cmdlist)
        print(f'{rc=}')
        assert rc != 0

    def test_args_multi_synth_oclib_fifos(self, tool, command):
        '''This should be 4 jobs and takes ~15 seconds for synth.'''
        if skip_it(tool, command):
            pytest.skip(f"{tool=} {command=} skipped, {tools_loaded=}")
            return # skip/pass
        chdir_remove_work_dir('../../lib')
        cmdlist = (f'multi {command} --debug --fail-if-no-targets --tool {tool}'
                   ' --yosys-synth=synth_xilinx oclib_fifo*').split()
        rc = eda.main(*cmdlist)
        print(f'{rc=}')
        assert rc == 0

    def test_args_multi_synth_oclib_rams(self, tool, command):
        '''This should be 4 jobs and takes ~15 seconds for synth.'''
        if skip_it(tool, command):
            pytest.skip(f"{tool=} {command=} skipped, {tools_loaded=}")
            return # skip/pass
        chdir_remove_work_dir('../../lib')
        cmdlist = (f'multi {command} --debug --fail-if-no-targets --tool {tool}'
                   ' --yosys-synth=synth_xilinx rams/oclib_ram*').split()
        rc = eda.main(*cmdlist)
        print(f'{rc=}')
        assert rc == 0

'''pytests for opencos.deps_helpers'''

# TODO(drew): these need to be refactored if we cleanup deps_helpers.py, this still
# uses the old DEPS (non-markup) command format, such as 'shell@some bash command'

# TODO(drew): for now, ignore long lines and docstrings
# pylint: disable=line-too-long,missing-function-docstring

from pathlib import Path
import os
import pytest

from opencos import eda_tool_helper, deps_helpers

THISPATH = os.path.dirname(__file__)

# Figure out what tools the system has available, without calling eda.main(..)
config, tools_loaded = eda_tool_helper.get_config_and_tools_loaded()


def test_get_all_targets():
    '''Makes sure that deps_helpers.get_all_targets(filter_str:str) works'''

    targets = deps_helpers.get_all_targets(
        dirs=[
            str(Path('../../lib/tests')),
            str(Path('../../lib/rams/tests')),
        ],
        base_path=str(Path(THISPATH)),
        filter_str='*test',
    )
    print(f'{targets=}')
    assert str(Path('../../lib/rams/tests/oclib_ram2rw_test')) in targets
    assert str(Path('../../lib/tests/oclib_fifo_test')) in targets
    for t in targets:
        assert t.endswith('test'), f'target {t} filter did not work *test'


@pytest.mark.skipif(
    not('vivado' in tools_loaded or
        'verilator' in tools_loaded),
    reason="requires vivado or verilator"
)
def test_get_all_targets_eda_multi():
    '''Makes sure that deps_helpers.get_all_targets(filter_using_mult:str) works'''

    targets = deps_helpers.get_all_targets(
        base_path=THISPATH,
        filter_using_multi='sim ../../lib/tests/*test ../../lib/rams/tests/*test',
    )
    print(f'{targets=}')
    assert '../../lib/rams/tests/oclib_ram2rw_test' in targets
    assert '../../lib/tests/oclib_fifo_test' in targets
    for t in targets:
        assert t.endswith('test'), f'target {t} filter did not work *test'


def test_parse_deps_shell_str__no_parse():
    line = 'some_file.sv'
    d = deps_helpers.parse_deps_shell_str(line, '', '')
    assert d is None, f'{d=}'

    line = 'some_target:'
    d = deps_helpers.parse_deps_shell_str(line, '', '')
    assert d is None, f'{d=}'

    line = '   csr@some_file.sv'
    d = deps_helpers.parse_deps_shell_str(line, '', '')
    assert d is None, f'{d=}'

def test_parse_deps_shell_str__cp():
    line = '    shell@ cp ./oclib_fifo_test.sv oclib_fifo_test_COPY.sv ;'
    d = deps_helpers.parse_deps_shell_str(line, '', '')
    assert d is not None, f'{d=}'
    assert d['exec_list'] == ['cp', './oclib_fifo_test.sv', 'oclib_fifo_test_COPY.sv', ';'], f'{d=}'

def test_parse_deps_shell_str__echo():
    line = '    shell@echo "hello world"'
    d = deps_helpers.parse_deps_shell_str(line, '', '')
    assert d is not None, f'{d=}'
    assert d['exec_list'] == ['echo', '"hello', 'world"'], f'{d=}'

def test_parse_deps_shell_str__path_replacement():
    # Dealing w/ relative paths, change the current working directory to the module directory
    module_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(module_dir)
    line = 'shell@cp ../deps_helpers.py foo.py'
    d = deps_helpers.parse_deps_shell_str(line, target_path='./', target_node='foo_target')
    assert d is not None, f'{d=}'
    assert d['exec_list'] == ['cp', os.path.abspath('../deps_helpers.py'), 'foo.py'], f'{d=}'
    assert d['target_node'] == 'foo_target'
    assert d['target_path'] == os.path.abspath('./')


def test_parse_deps_work_dir_add_srcs__no_parse():
    line = 'some_file.sv'
    d = deps_helpers.parse_deps_work_dir_add_srcs(line, '', '')
    assert d is None, f'{d=}'

    line = 'some_target:'
    d = deps_helpers.parse_deps_work_dir_add_srcs(line, '', '')
    assert d is None, f'{d=}'

    line = '   csr@some_file.sv'
    d = deps_helpers.parse_deps_work_dir_add_srcs(line, '', '')
    assert d is None, f'{d=}'

def test_parse_deps_work_dir_add_srcs__single_file():
    line = '    work_dir_add_srcs@ single_file.txt'
    d = deps_helpers.parse_deps_work_dir_add_srcs(line, '', '')
    assert d is not None, f'{d=}'
    assert d['file_list'] == ['single_file.txt']

def test_parse_deps_work_dir_add_srcs__several_file():
    line = '    work_dir_add_srcs@ single_file.txt another.sv  gen-verilog/mine.v ./gen-vhdl/wordy.vhdl'
    d = deps_helpers.parse_deps_work_dir_add_srcs(line, '', '')
    assert d is not None, f'{d=}'
    assert d['file_list'] == [
        'single_file.txt', 'another.sv', 'gen-verilog/mine.v', './gen-vhdl/wordy.vhdl'
    ]


def test_parse_deps_peakrdl__no_parse():
    line = 'some_file.sv'
    d = deps_helpers.parse_deps_peakrdl(line, '', '')
    assert d is None, f'{d=}'

    line = 'some_target:'
    d = deps_helpers.parse_deps_peakrdl(line, '', '')
    assert d is None, f'{d=}'

    line = '   csr@some_file.sv'
    d = deps_helpers.parse_deps_peakrdl(line, '', '')
    assert d is None, f'{d=}'

def test_parse_deps_peakrdl__with_top():
    line = '    peakrdl@ --cpuif axi4-lite-flat --top   my_fancy_csrs ./my_csrs.rdl'
    d = deps_helpers.parse_deps_peakrdl(line, '', '')
    assert d is not None, f'{d=}'
    assert len(d['shell_commands_list']) > 0
    assert d['work_dir_add_srcs']['file_list'] == ['peakrdl/my_fancy_csrs_pkg.sv', 'peakrdl/my_fancy_csrs.sv']

def test_parse_deps_peakrdl__with_top2():
    line = '    peakrdl@ --cpuif axi4-lite-flat --top=my_fancy_csrs ./my_csrs.rdl'
    d = deps_helpers.parse_deps_peakrdl(line, '', '')
    assert d is not None, f'{d=}'
    assert len(d['shell_commands_list']) > 0
    assert d['work_dir_add_srcs']['file_list'] == ['peakrdl/my_fancy_csrs_pkg.sv', 'peakrdl/my_fancy_csrs.sv']

def test_parse_deps_peakrdl__infer_top():
    line = '    peakrdl@ --cpuif axi4-lite-flat ./my_csrs.rdl'
    d = deps_helpers.parse_deps_peakrdl(line, '', '')
    assert d is not None, f'{d=}'
    assert len(d['shell_commands_list']) > 0
    assert d['work_dir_add_srcs']['file_list'] == ['peakrdl/my_csrs_pkg.sv', 'peakrdl/my_csrs.sv']

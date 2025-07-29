
import os
import sys

from opencos import eda, eda_config, util

# Used by pytest, so we can skip tests if tools aren't present.

def get_config_and_tools_loaded(quiet=False, args=[]):
    # We have to figure out what tools are avaiable w/out calling eda.main,
    # so we can get some of these using eda_config.get_eda_config()
    config, _ = eda_config.get_eda_config(args=args, quiet=quiet)
    config = eda.init_config(config=config, quiet=quiet)
    tools_loaded = config.get('tools_loaded', set()).copy()
    return config, tools_loaded

def get_all_handler_commands(config=None, tools_loaded=None) -> dict:
    all_handler_commands = dict()

    if config is None or tools_loaded is None:
        config, tools_loaded = get_config_and_tools_loaded()

    assert type(config) is dict
    assert type(tools_loaded) is set

    # Let's re-walk auto_tools_order to get this ordered per eda command:
    for tool, table in config.get('auto_tools_order', [{}])[0].items():
        if tool not in tools_loaded:
            continue

        if table.get('disable-tools-multi', False):
            # Flagged as do-not-add when running eda command: tools-multi
            util.debug(f'eda_tool_helper.py -- skipping {tool=} it is set with flag',
                       'disable-tools-multi in config')
            continue

        for command, handler in table.get('handlers', {}).items():
            if command not in all_handler_commands:
                # create ordered list from config.
                all_handler_commands[command] = list([tool])
            else:
                all_handler_commands[command].append(tool)

    return all_handler_commands

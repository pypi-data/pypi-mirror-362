from typing import List

from bluer_options.terminal import show_usage, xtra
from bluer_ai.help.generic import help_functions as generic_help_functions

from bluer_ugv import ALIAS
from bluer_ugv.help.swallow import help_functions as help_swallow
from bluer_ugv.help.socket import help_functions as help_socket


help_functions = generic_help_functions(plugin_name=ALIAS)

help_functions.update(
    {
        "socket": help_socket,
        "swallow": help_swallow,
    }
)

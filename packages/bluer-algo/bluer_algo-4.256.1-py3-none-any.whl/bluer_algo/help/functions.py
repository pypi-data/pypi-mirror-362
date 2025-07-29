from bluer_ai.help.generic import help_functions as generic_help_functions

from bluer_algo import ALIAS
from bluer_algo.help.image_classifier import help_functions as help_image_classifier


help_functions = generic_help_functions(plugin_name=ALIAS)

help_functions.update(
    {
        "image_classifier": help_image_classifier,
    }
)

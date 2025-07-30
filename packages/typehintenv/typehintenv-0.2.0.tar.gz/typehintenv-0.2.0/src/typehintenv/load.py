import sys
import os
import logging
from typing import Callable, Optional
from types import ModuleType

from .converters import DEFAULT_CONVERTERS

def load_env(
        converters : dict[type, Callable[[str], object]] = DEFAULT_CONVERTERS, 
        module_to_insert_in : Optional[ModuleType] = None) -> None:
    """
        Sets the values of the constants in the caller module using environment variables
        If no module is given, it is extracted from the "caller frame"

        # Parameters
            - converters : a dict of types T, and a function str -> T. Those function must raise ValueError in case the conversion fails
            - module_to_insert_in : the module (file) in which the constants are declared

        # Side Effects
        Can change the values of the constants in the `module_to_insert_in` if given, else to the function caller's module

    """

    converters = {**DEFAULT_CONVERTERS, **converters} # the default ones with the overrides given
    if module_to_insert_in is None:
        # Default to caller's module
        module_to_insert_in = sys._getframe(1).f_globals.get('__name__')
        module_to_insert_in = sys.modules[module_to_insert_in]
    
    annotations = getattr(module_to_insert_in, '__annotations__', {})
    for var_name, var_type in annotations.items():
        # Edge-cases
        if var_name.startswith('_'):
            logging.debug(f"Skipping {var_name} because it starts with a '_'")
            continue
        env_value = os.environ.get(var_name)

        # Getting that value
        if env_value is None:
            logging.error(f"Variable {var_name} is not set in the environment")
            continue
        
        # Getting the converter
        converter = converters.get(var_type, var_type)
        if converter is None:
            # this error is critical as it's the developer that missed something
            logging.error(f"No converter defined for type {var_type}")
            raise KeyError(f"No converter defined for type {var_type}")
        
        # Converting the value
        try:
            value = converter(env_value)
        except ValueError as e:
            logging.error(f"Error converting {var_name}: {e}, it's value is not accepted by the converter function.")
            raise ValueError("Error converting {var_name}: {e}, it's value is not accepted by the converter function.")
        except Exception as e:
            logging.error(f"Error converting {var_name}, this error is not expected. See the stacktrace for more informations.")
            raise e 
        
        # Setting the value
        setattr(module_to_insert_in, var_name, value)
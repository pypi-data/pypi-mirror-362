'''
This is the package for `typeenv`, a simple system to load environment variables into python constants and enjoy type-hinting on them.

Put your constants in a file (like env.py) with the types you want to use in your code, and **then** call `load_env`.

This file is a stupid env loader I made while bored
Define constants and their type at the root of the file, they will be loaded from your environment
The names must match

If you define a type, you must define a converter in _CONVERTERS
Define all yout logic with a _ at the start (or else it will be considered an env variable)
'''

from .load import load_env
from .converters import DEFAULT_CONVERTERS

load_env
DEFAULT_CONVERTERS
# Typehintenv - Env loading using type annotations

The idea is simple : in one file (like an env.py), you define your constants, with the same name as your env variables and you give them a type. At the end of this file, you call the loader (as you would do with python-dotenv for example).

After that, all the constants in the env.py file are loaded, and you can import them from other modules, with your IDE knowing they exist, and what their type is.

# Example

## The most basic one

You have those variables in your environment

```bash
A=1.2
B=5
C=toto
D=true
```

You declare a file like **env.py** with

```python
from typehintenv import load_env

A : float
B : int
C : str
D : bool

load_env()
```

And then, from the rest of your code, just use it like this

```python
from .env import A, D

if D:
    print(type(A))

# this code will show 'float'
```

## With a dotenv

You can use `python-dotenv` to load a environment file, just ensure doing it before calling `load_env`, as you will need the os.environ loaded before the call.

## Extending the converters

In the environment, everything is a string. When loading those into python, functions are used to changed from strings to the types you want. 

`load_env` takes as a first argument a dictionary of converters : the keys are the types (T) and the values are functions that convert from strings to T.

This function can also perform validation, as they can raise `ValueError` if the values are not correct.

There is a small set of converters for the basic types of the language, you can override them.

```python
from typing import Literal

from typehintenv import load_env

A : bool
ENV : Litteral["env", "prod"]

def parse_env(s : string) -> Litteral["env", "prod"]:
    if s not in ("env", "prod"):
        raise ValueError("Not a correct environment")
    return s

load_env({
    bool : lambda s: s in ("oui", "vrai"), # can't help wanting my booleans to be in french
    Litteral["env", "prod"] : parse_env # now we have more of a validator
})
```

# Acknowledgments

The work from (typenv)[https://pypi.org/project/typenv/] is quite the same, exclusing the fact that it does not use type annotations but rather uses it's own model.

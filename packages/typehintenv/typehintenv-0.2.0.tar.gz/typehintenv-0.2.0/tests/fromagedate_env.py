from typing import Literal, TypeVar, Type, Callable

_ENVIRONMENT_VALUES = Literal["production", "dev"]

# Explicitly define constants with type annotations
DB_PORT: int
DB_HOST: str
DB_NAME: str
DB_USER: str
DB_PASSWD: str
SECRET_KEY: str
ENVIRONMENT: _ENVIRONMENT_VALUES
HOSTNAME: str
EMAIL_PASSWD: str
EMAIL_USER: str
EMAIL_HOST: str
EMAIL_PORT: int
EMAIL_USE_TLS: bool

def _convert_env_values(env : str) -> str:
    allowed_choices = ["production", "dev"]
    if env not in allowed_choices:
        raise Exception(f"Environment '{env}' not in {allowed_choices}")
    return env

_T = TypeVar("T")
_CONVERTERS : dict[Type, Callable[[str], _T]] = {
    str : str,
    int : int,
    bool : lambda x : x.lower() in ('true', 'yes', '1'),
    _ENVIRONMENT_VALUES: _convert_env_values
}

from typehintenv import load_env

load_env(_CONVERTERS)

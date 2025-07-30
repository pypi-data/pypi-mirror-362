def to_bool(s : str) -> bool:
    return s.lower() in ("1", "yes", "true")

DEFAULT_CONVERTERS = {
    str:str,
    int:int,
    float:float,
    bool:to_bool,
}
from typing import Type, Dict, Protocol
from src.models import ParseResult

class ExerciseHandler(Protocol):
    def __init__(self, exercise: str): ...
    def initial_load(self) -> ParseResult: ...
    def parse_content(self) -> ParseResult: ...

_REGISTRY: Dict[str, Type[ExerciseHandler]] = {}

def register_type(name: str):
    def deco(cls: Type[ExerciseHandler]):
        _REGISTRY[name.lower()] = cls
        return cls
    return deco

def get_handler(name: str) -> Type[ExerciseHandler]:
    try:
        return _REGISTRY[name.lower()]
    except KeyError:
        raise ValueError(f"Unknown exercise type: {name}. Registered: {list(_REGISTRY)}")

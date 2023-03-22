from typing import Any, Union


def loads(content: str) -> Any:
    ...


def load(fp: Union[str, bytes]) -> Any:
    loads(fp.read())


def dumps(content: str) -> str:
    ...


def dump(fp: Union[str, bytes]) -> str:
    dumps(fp.read())

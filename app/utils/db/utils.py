import typing

from app.services.repository.base import Model

T = typing.TypeVar("T")
Dictionary = typing.TypeVar("Dictionary", bound=typing.Dict[typing.Any, typing.Any])


@typing.overload
def manual_cast(result: typing.Any) -> "Model": ...


@typing.overload
def manual_cast(result: typing.Any, cast_type: typing.Type[T]) -> T: ...


# noinspection PyUnusedLocal
def manual_cast(result, cast_type=None):
    return result


def filter_payload(payload):
    return {k: v for k, v in payload.items() if k not in ['cls', 'self'] and v is not None}

from contextlib import contextmanager
from functools import wraps
from typing import Callable, Self, List, Tuple

from google.protobuf.message import Message
from grpc import ServicerContext
from loguru import logger


def form_metadata(request_id: str | None) -> List[Tuple[str, str]]:
    metadata = []
    if request_id:
        metadata.append(("request_id", request_id))

    return metadata


@contextmanager
def _contextualize(context: ServicerContext):
    metadata = dict(context.invocation_metadata())
    request_id = metadata.get("request_id", "SYSTEM_LOG")
    with logger.contextualize(request_id=request_id):
        yield


def logging_decorator(func: Callable[[Self, Message, ServicerContext], Message]):
    @wraps(func)
    def wrapper(self: Self, request: Message, context: ServicerContext) -> Message:
        with _contextualize(context):
            return func(self, request, context)

    return wrapper


def exception_decorator(func: Callable[[Self, Message, ServicerContext], Message]):
    @wraps(func)
    def wrapper(self: Self, request: Message, context: ServicerContext) -> Message:
        try:
            return func(self, request, context)
        except Exception as e:
            logger.exception(e)
            raise e

    return wrapper


def exception_logging_decorator(func: Callable[[Self, Message, ServicerContext], Message]):
    @wraps(func)
    def wrapper(self: Self, request: Message, context: ServicerContext) -> Message:
        with _contextualize(context):
            try:
                return func(self, request, context)
            except Exception as e:
                logger.exception(e)
                raise e

    return wrapper

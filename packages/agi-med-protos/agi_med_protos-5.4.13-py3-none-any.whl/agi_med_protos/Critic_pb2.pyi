from agi_med_protos import commons_pb2 as _commons_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CriticRequest(_message.Message):
    __slots__ = ("Text", "Chat")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    CHAT_FIELD_NUMBER: _ClassVar[int]
    Text: str
    Chat: _commons_pb2.ChatItem
    def __init__(self, Text: _Optional[str] = ..., Chat: _Optional[_Union[_commons_pb2.ChatItem, _Mapping]] = ...) -> None: ...

class CriticResponse(_message.Message):
    __slots__ = ("Score",)
    SCORE_FIELD_NUMBER: _ClassVar[int]
    Score: float
    def __init__(self, Score: _Optional[float] = ...) -> None: ...

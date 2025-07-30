from agi_med_protos import commons_pb2 as _commons_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ContentInterpreterRequest(_message.Message):
    __slots__ = ("Kind", "Query", "Resource", "ResourceId", "Chat")
    KIND_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    RESOURCEID_FIELD_NUMBER: _ClassVar[int]
    CHAT_FIELD_NUMBER: _ClassVar[int]
    Kind: str
    Query: str
    Resource: bytes
    ResourceId: str
    Chat: _commons_pb2.ChatItem
    def __init__(self, Kind: _Optional[str] = ..., Query: _Optional[str] = ..., Resource: _Optional[bytes] = ..., ResourceId: _Optional[str] = ..., Chat: _Optional[_Union[_commons_pb2.ChatItem, _Mapping]] = ...) -> None: ...

class ContentInterpreterResponse(_message.Message):
    __slots__ = ("Interpretation", "Resource", "ResourceId")
    INTERPRETATION_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    RESOURCEID_FIELD_NUMBER: _ClassVar[int]
    Interpretation: str
    Resource: bytes
    ResourceId: str
    def __init__(self, Interpretation: _Optional[str] = ..., Resource: _Optional[bytes] = ..., ResourceId: _Optional[str] = ...) -> None: ...

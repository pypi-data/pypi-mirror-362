from agi_med_protos import commons_pb2 as _commons_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ContentRouterRequest(_message.Message):
    __slots__ = ("OuterContext", "ResourceId", "Kind", "Query")
    OUTERCONTEXT_FIELD_NUMBER: _ClassVar[int]
    RESOURCEID_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    OuterContext: _commons_pb2.OuterContextItem
    ResourceId: str
    Kind: str
    Query: str
    def __init__(self, OuterContext: _Optional[_Union[_commons_pb2.OuterContextItem, _Mapping]] = ..., ResourceId: _Optional[str] = ..., Kind: _Optional[str] = ..., Query: _Optional[str] = ...) -> None: ...

class ContentRouterResponse(_message.Message):
    __slots__ = ("Interpretation", "ResourceId")
    INTERPRETATION_FIELD_NUMBER: _ClassVar[int]
    RESOURCEID_FIELD_NUMBER: _ClassVar[int]
    Interpretation: str
    ResourceId: str
    def __init__(self, Interpretation: _Optional[str] = ..., ResourceId: _Optional[str] = ...) -> None: ...

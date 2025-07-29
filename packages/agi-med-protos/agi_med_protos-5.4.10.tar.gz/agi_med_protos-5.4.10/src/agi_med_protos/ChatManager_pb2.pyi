from agi_med_protos import commons_pb2 as _commons_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ChatManagerRequest(_message.Message):
    __slots__ = ("Text", "OuterContext", "ResourceId", "Command")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    OUTERCONTEXT_FIELD_NUMBER: _ClassVar[int]
    RESOURCEID_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    Text: str
    OuterContext: _commons_pb2.OuterContextItem
    ResourceId: str
    Command: str
    def __init__(self, Text: _Optional[str] = ..., OuterContext: _Optional[_Union[_commons_pb2.OuterContextItem, _Mapping]] = ..., ResourceId: _Optional[str] = ..., Command: _Optional[str] = ...) -> None: ...

class ChatManagerResponse(_message.Message):
    __slots__ = ("Text", "State", "Action", "ResourceId", "Widget", "Command")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    RESOURCEID_FIELD_NUMBER: _ClassVar[int]
    WIDGET_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    Text: str
    State: str
    Action: str
    ResourceId: str
    Widget: str
    Command: str
    def __init__(self, Text: _Optional[str] = ..., State: _Optional[str] = ..., Action: _Optional[str] = ..., ResourceId: _Optional[str] = ..., Widget: _Optional[str] = ..., Command: _Optional[str] = ...) -> None: ...

class DomainInfo(_message.Message):
    __slots__ = ("DomainId", "Name")
    DOMAINID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DomainId: str
    Name: str
    def __init__(self, DomainId: _Optional[str] = ..., Name: _Optional[str] = ...) -> None: ...

class DomainsRequest(_message.Message):
    __slots__ = ("LanguageCode",)
    LANGUAGECODE_FIELD_NUMBER: _ClassVar[int]
    LanguageCode: str
    def __init__(self, LanguageCode: _Optional[str] = ...) -> None: ...

class DomainsResponse(_message.Message):
    __slots__ = ("Domains",)
    DOMAINS_FIELD_NUMBER: _ClassVar[int]
    Domains: _containers.RepeatedCompositeFieldContainer[DomainInfo]
    def __init__(self, Domains: _Optional[_Iterable[_Union[DomainInfo, _Mapping]]] = ...) -> None: ...

class TrackInfo(_message.Message):
    __slots__ = ("TrackId", "Name", "DomainId")
    TRACKID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DOMAINID_FIELD_NUMBER: _ClassVar[int]
    TrackId: str
    Name: str
    DomainId: str
    def __init__(self, TrackId: _Optional[str] = ..., Name: _Optional[str] = ..., DomainId: _Optional[str] = ...) -> None: ...

class TracksRequest(_message.Message):
    __slots__ = ("LanguageCode",)
    LANGUAGECODE_FIELD_NUMBER: _ClassVar[int]
    LanguageCode: str
    def __init__(self, LanguageCode: _Optional[str] = ...) -> None: ...

class TracksResponse(_message.Message):
    __slots__ = ("Tracks",)
    TRACKS_FIELD_NUMBER: _ClassVar[int]
    Tracks: _containers.RepeatedCompositeFieldContainer[TrackInfo]
    def __init__(self, Tracks: _Optional[_Iterable[_Union[TrackInfo, _Mapping]]] = ...) -> None: ...

class EntrypointInfo(_message.Message):
    __slots__ = ("EntrypointKey", "Caption")
    ENTRYPOINTKEY_FIELD_NUMBER: _ClassVar[int]
    CAPTION_FIELD_NUMBER: _ClassVar[int]
    EntrypointKey: str
    Caption: str
    def __init__(self, EntrypointKey: _Optional[str] = ..., Caption: _Optional[str] = ...) -> None: ...

class EntrypointsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class EntrypointsResponse(_message.Message):
    __slots__ = ("Entrypoints", "DefaultEntrypointKey")
    ENTRYPOINTS_FIELD_NUMBER: _ClassVar[int]
    DEFAULTENTRYPOINTKEY_FIELD_NUMBER: _ClassVar[int]
    Entrypoints: _containers.RepeatedCompositeFieldContainer[EntrypointInfo]
    DefaultEntrypointKey: str
    def __init__(self, Entrypoints: _Optional[_Iterable[_Union[EntrypointInfo, _Mapping]]] = ..., DefaultEntrypointKey: _Optional[str] = ...) -> None: ...

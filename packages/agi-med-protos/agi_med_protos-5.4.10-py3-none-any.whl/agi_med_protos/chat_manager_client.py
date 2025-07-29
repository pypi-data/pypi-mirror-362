import json
from typing import Any, Dict, List

from .abstract_client import AbstractClient
from .commons_pb2 import OuterContextItem
from .ChatManager_pb2 import (
    ChatManagerRequest,
    ChatManagerResponse,
    DomainsRequest,
    DomainsResponse,
    DomainInfo,
    TracksRequest,
    TracksResponse,
    TrackInfo,
    EntrypointsRequest,
    EntrypointsResponse,
    EntrypointInfo,
)
from .ChatManager_pb2_grpc import ChatManagerStub
from .converters import convert_outer_context
from .log_error_handlers import form_metadata


from typing import Tuple


DictStr = Dict[str, str]


class ChatManagerClient(AbstractClient):
    def __init__(self, address) -> None:
        super().__init__(address)
        self._stub = ChatManagerStub(self._channel)

    def __call__(
        self, text: str, dict_outer_context: dict, resource_id: str = "", request_id: str = "", command: dict | None = None
    ) -> DictStr:
        outer_context: OuterContextItem = convert_outer_context(dict_outer_context)
        command_str = json.dumps(command) if command else ""

        request = ChatManagerRequest(
            Text=text,
            OuterContext=outer_context,
            ResourceId=resource_id,
            Command=command_str,
        )

        response: ChatManagerResponse = self._stub.GetChatResponse(request, metadata=form_metadata(request_id))
        replica: dict[str, Any] = {
            "Text": response.Text,
            "ResourceId": response.ResourceId,
            "State": response.State,
            "Action": response.Action,
            "Widget": response.Widget,
            "Command": response.Command,
        }
        return replica

    def get_domains(self, request_id: str = "") -> List[DictStr]:
        request = DomainsRequest()
        response: DomainsResponse = self._stub.GetDomains(request, metadata=form_metadata(request_id))
        domains: List[DomainInfo] = response.Domains
        res = [{"DomainId": di.DomainId, "Name": di.Name} for di in domains]
        return res

    def get_tracks(self, request_id: str = "") -> List[DictStr]:
        request = TracksRequest()
        response: TracksResponse = self._stub.GetTracks(request, metadata=form_metadata(request_id))
        tracks: List[TrackInfo] = response.Tracks
        res = [{"TrackId": ti.TrackId, "Name": ti.Name, "DomainId": ti.DomainId} for ti in tracks]
        return res

    def get_entrypoints(self, request_id: str = "") -> Tuple[List[DictStr], str]:
        request = EntrypointsRequest()
        response: EntrypointsResponse = self._stub.GetEntrypoints(request, metadata=form_metadata(request_id))
        entrypoints_raw: List[EntrypointInfo] = response.Entrypoints
        entrypoints = [{"EntrypointKey": ei.EntrypointKey, "Caption": ei.Caption} for ei in entrypoints_raw]
        default_entrypoint_key: str = response.DefaultEntrypointKey
        res = entrypoints, default_entrypoint_key
        return res

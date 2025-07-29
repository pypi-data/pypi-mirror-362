from typing import Tuple

from .commons_pb2 import (
    OuterContextItem,
)
from .ContentRouter_pb2_grpc import ContentRouterStub
from .ContentRouter_pb2 import (
    ContentRouterRequest,
    ContentRouterResponse,
)
from .abstract_client import AbstractClient
from .converters import convert_outer_context
from .log_error_handlers import form_metadata


ResourceId = str
Interpretation = str


class ContentRouterClient(AbstractClient):
    def __init__(self, address):
        super().__init__(address)
        self._stub = ContentRouterStub(self._channel)

    def interpret(
        self, resource_id: str, kind: str, query: str, dict_outer_context: dict | None, request_id: str = ""
    ) -> Tuple[Interpretation, ResourceId]:
        outer_context: OuterContextItem = convert_outer_context(dict_outer_context)

        request = ContentRouterRequest(
            OuterContext=outer_context,
            ResourceId=resource_id,
            Kind=kind,
            Query=query,
        )

        response: ContentRouterResponse = self._stub.Interpret(request, metadata=form_metadata(request_id))
        return response.Interpretation, response.ResourceId

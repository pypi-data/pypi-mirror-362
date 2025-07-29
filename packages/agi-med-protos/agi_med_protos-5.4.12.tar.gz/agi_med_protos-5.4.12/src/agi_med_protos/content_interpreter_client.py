from .abstract_client import AbstractClient
from .commons_pb2 import ChatItem
from .ContentInterpreter_pb2 import (
    ContentInterpreterRequest,
    ContentInterpreterResponse,
)
from .ContentInterpreter_pb2_grpc import ContentInterpreterStub
from .converters import convert_chat
from .log_error_handlers import form_metadata


class ContentInterpreterClient(AbstractClient):
    def __init__(self, address):
        super().__init__(address)
        self._stub = ContentInterpreterStub(self._channel)

    def interpret(
        self,
        kind: str,
        query: str = "",
        resource: bytes = None,
        resource_id: str = None,
        request_id: str = "",
        chat_dict: dict | None = None,
    ) -> ContentInterpreterResponse:
        chat: ChatItem = convert_chat(chat_dict)
        request = ContentInterpreterRequest(
            Kind=kind,
            Query=query,
            Resource=resource,
            ResourceId=resource_id,
            Chat=chat,
        )

        response: ContentInterpreterResponse = self._stub.Interpret(request, metadata=form_metadata(request_id))
        return response

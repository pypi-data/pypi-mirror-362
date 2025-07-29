from .abstract_client import AbstractClient
from .commons_pb2 import (
    ChatItem,
)
from .Critic_pb2 import (
    CriticRequest,
    CriticResponse,
)
from .Critic_pb2_grpc import CriticStub
from .converters import convert_chat
from .log_error_handlers import form_metadata


class CriticClient(AbstractClient):
    def __init__(self, address) -> None:
        super().__init__(address)
        self._stub = CriticStub(self._channel)

    def __call__(self, text: str, chat_dict: dict, request_id: str = "") -> str:
        chat: ChatItem = convert_chat(chat_dict)
        request = CriticRequest(Text=text, Chat=chat)

        response: CriticResponse = self._stub.GetCriticResponse(request, metadata=form_metadata(request_id))
        return response.Score

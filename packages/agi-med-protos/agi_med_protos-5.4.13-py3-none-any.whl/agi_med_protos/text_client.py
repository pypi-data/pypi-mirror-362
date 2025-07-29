from .abstract_client import AbstractClient
from .commons_pb2 import (
    ChatItem,
)
from .Text_pb2 import (
    TextRequest,
    TextResponse,
)
from .Text_pb2_grpc import TextStub
from .converters import convert_chat
from .log_error_handlers import form_metadata


class TextClient(AbstractClient):
    def __init__(self, address) -> None:
        super().__init__(address)
        self._stub = TextStub(self._channel)

    def __call__(self, text: str, chat_dict: dict, request_id: str = "") -> str:
        chat: ChatItem = convert_chat(chat_dict)
        request = TextRequest(Text=text, Chat=chat)

        response: TextResponse = self._stub.GetTextResponse(request, metadata=form_metadata(request_id))
        return response.Text

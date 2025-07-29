from .commons_pb2 import (
    ChatItem,
    InnerContextItem,
    OuterContextItem,
    ReplicaItem,
)


def convert_chat(chat_dict: dict) -> ChatItem:
    if chat_dict is None:
        return None
    dict_outer_context = chat_dict["OuterContext"]
    outer_context: OuterContextItem = convert_outer_context(dict_outer_context)

    dict_inner_context = chat_dict["InnerContext"]
    inner_context: InnerContextItem = convert_inner_context(dict_inner_context)

    chat = ChatItem(OuterContext=outer_context, InnerContext=inner_context)
    return chat


def convert_outer_context(dict_outer_context: dict | None) -> OuterContextItem:
    if dict_outer_context is None:
        return None
    outer_context = OuterContextItem(
        Sex=dict_outer_context["Sex"],
        Age=dict_outer_context["Age"],
        UserId=dict_outer_context["UserId"],
        SessionId=dict_outer_context["SessionId"],
        ClientId=dict_outer_context["ClientId"],
        TrackId=dict_outer_context["TrackId"],
        EntrypointKey=dict_outer_context["EntrypointKey"],
        LanguageCode=dict_outer_context["LanguageCode"],
    )
    return outer_context


def convert_inner_context(dict_inner_context: dict | None) -> InnerContextItem:
    if dict_inner_context is None:
        return None
    dict_replicas = dict_inner_context["Replicas"]
    replicas = [
        ReplicaItem(
            Body=dict_replica["Body"],
            Role=dict_replica["Role"],
            DateTime=dict_replica["DateTime"],
            ResourceId=dict_replica["ResourceId"],
        )
        for dict_replica in dict_replicas
    ]
    inner_context = InnerContextItem(Replicas=replicas)
    return inner_context

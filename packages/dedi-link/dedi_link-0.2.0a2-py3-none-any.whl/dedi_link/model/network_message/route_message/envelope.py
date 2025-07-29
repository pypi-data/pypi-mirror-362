from dedi_link.etc.enums import MessageType
from ..message_metadata import MessageMetadata
from ..network_message import NetworkMessage


@NetworkMessage.register_child(MessageType.ROUTE_ENVELOPE)
class RouteEnvelope(NetworkMessage):
    """
    A message to envelope another message for proxy routing.
    """
    message_type: MessageType = MessageType.ROUTE_ENVELOPE

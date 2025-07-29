from typing import Mapping, Any

from .base_model import BaseModel


class Node(BaseModel):
    """
    A node in a network

    A Node object represents a node in the network, a basic
    unit of operation and communication.
    """
    def __init__(self,
                 node_id: str,
                 node_name: str,
                 url: str,
                 description: str,
                 *,
                 public_key: str | None = None,
                 data_index: dict = None,
                 score: float = 0.0,
                 approved: bool = False,
                 ):
        """
        A node in a network

        A Node object represents a node in the network, a basic
        unit of operation and communication.
        :param node_id: The unique ID of the node
        :param node_name: The name of the node
        :param url: The URL of the node
        :param description: A description of the node
        require authentication. If disabled, all users will be mapped to the
        same static user with the same permissions.
        :param public_key: The public key of the node
        :param data_index: The data index of the node
        :param score: The score of the node
        :param approved: Whether the node is approved for message exchange
        """
        self.node_id = node_id
        self.node_name = node_name
        self.url = url
        self.public_key = public_key
        self.description = description
        self.data_index = data_index or {}
        self.score = score
        self.approved = approved

    def __eq__(self, other) -> bool:
        if not isinstance(other, Node):
            return NotImplemented

        return all([
            self.node_id == other.node_id,
            self.node_name == other.node_name,
            self.url == other.url,
            self.public_key == other.public_key,
            self.description == other.description,
        ])

    def __hash__(self) -> int:
        return hash((
            self.node_id,
            self.node_name,
            self.url,
            self.public_key,
            self.description,
        ))

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> 'Node':
        """
        Build a node object from a dictionary
        :param payload: Dictionary containing the node information
        :return: Node object
        """
        return cls(
            node_id=payload['nodeId'],
            node_name=payload['nodeName'],
            url=payload['nodeUrl'],
            description=payload.get('nodeDescription', ''),
            public_key=payload.get('publicKey', None),
            data_index=payload.get('dataIndex', {}),
            score=payload.get('score', 0.0),
            approved=payload.get('approved', False),
        )

    def to_dict(self) -> dict:
        """
        Serialise the Node object to a dictionary.
        :return: Dictionary containing node data
        """
        payload: dict = {
            'nodeId': self.node_id,
            'nodeName': self.node_name,
            'nodeUrl': self.url,
            'nodeDescription': self.description,
            'score': self.score,
            'approved': self.approved,
        }

        if self.public_key:
            payload['publicKey'] = self.public_key
        if self.data_index:
            payload['dataIndex'] = self.data_index

        return payload

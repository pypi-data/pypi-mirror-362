from typing import Mapping, Any

from .base_model import BaseModel


class User(BaseModel):
    def __init__(self,
                 user_id: str,
                 public_key: str,
                 ):
        self.user_id = user_id
        self.public_key = public_key

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the User to a dictionary representation.

        :return: Dictionary representation of the User.
        """
        return {
            'userId': self.user_id,
            'publicKey': self.public_key,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> 'User':
        """
        Create a User instance from a dictionary.

        :param data: Dictionary containing 'userId' and 'identities'.
        :return: User instance.
        """
        return cls(
            user_id=data['userId'],
            public_key=data['publicKey'],
        )

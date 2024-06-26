"""

This file contains partial objects related to Roblox users.

"""

from typing import Optional, List

from ..bases.baseuser import BaseUser
from ..utilities.shared import ClientSharedObject


class PartialUser(BaseUser):
    """
    Represents partial user information.

    Attributes:
        _shared: The shared object, which is passed to all objects this client generates.
        id: The user's ID.
        name: The user's name.
        display_name: The user's display name.
    """

    def __init__(self, shared: ClientSharedObject, data: dict):
        """
        Arguments:
            shared: The ClientSharedObject.
            data: The data from the endpoint.
        """
        self._shared: ClientSharedObject = shared

        self.id: int = data.get("id") or data.get("userId") or data.get("Id")

        super().__init__(shared=shared, user_id=self.id)

        self.name: str = data.get("name") or data.get("Name") or data.get("username") or data.get("Username")
        self.display_name: str = data.get("displayName")

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id} name={self.name!r} display_name={self.display_name!r}>"


class RequestedUsernamePartialUser(PartialUser):
    """
    Represents a partial user in the context of a search where the requested username is present.

    Attributes:
        requested_username: The requested username.
    """

    def __init__(self, shared: ClientSharedObject, data: dict):
        """
        Arguments:
            shared: The ClientSharedObject.
            data: The data from the endpoint.
        """
        super().__init__(shared=shared, data=data)

        self.requested_username: Optional[str] = data.get("requestedUsername")


class PreviousUsernamesPartialUser(PartialUser):
    """
    Represents a partial user in the context of a search where the user's previous usernames are present.
    Attributes:
        previous_usernames: A list of the user's previous usernames.
    """

    def __init__(self, shared: ClientSharedObject, data: dict):
        """
        Arguments:
            shared: The ClientSharedObject.
            data: The data from the endpoint.
        """
        super().__init__(shared=shared, data=data)

        self.previous_usernames: List[str] = data["previousUsernames"]

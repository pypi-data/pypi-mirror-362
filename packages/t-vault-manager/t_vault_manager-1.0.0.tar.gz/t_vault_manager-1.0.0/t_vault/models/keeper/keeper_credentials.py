from pydantic import Field
from t_object import ThoughtfulObject


class KeeperCredentials(ThoughtfulObject):
    """Object for keeper credentials."""

    username: str = Field(default="", alias="user")
    password: str = ""
    totp_key: str = ""

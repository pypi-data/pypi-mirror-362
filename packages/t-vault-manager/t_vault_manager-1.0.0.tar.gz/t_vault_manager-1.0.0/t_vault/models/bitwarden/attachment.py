from t_object import ThoughtfulObject


class Attachment(ThoughtfulObject):
    """A class representing an attachment with a name, item ID, and URL."""

    name: str
    item_id: str
    url: str

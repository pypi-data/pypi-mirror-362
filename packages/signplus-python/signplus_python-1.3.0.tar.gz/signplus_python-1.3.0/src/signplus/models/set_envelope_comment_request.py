from .utils.json_map import JsonMap
from .utils.base_model import BaseModel


@JsonMap({})
class SetEnvelopeCommentRequest(BaseModel):
    """SetEnvelopeCommentRequest

    :param comment: Comment for the envelope
    :type comment: str
    """

    def __init__(self, comment: str, **kwargs):
        """SetEnvelopeCommentRequest

        :param comment: Comment for the envelope
        :type comment: str
        """
        self.comment = comment
        self._kwargs = kwargs

from .utils.json_map import JsonMap
from .utils.base_model import BaseModel


@JsonMap({})
class SetEnvelopeExpirationRequest(BaseModel):
    """SetEnvelopeExpirationRequest

    :param expires_at: Unix timestamp of the expiration date
    :type expires_at: int
    """

    def __init__(self, expires_at: int, **kwargs):
        """SetEnvelopeExpirationRequest

        :param expires_at: Unix timestamp of the expiration date
        :type expires_at: int
        """
        self.expires_at = expires_at
        self._kwargs = kwargs

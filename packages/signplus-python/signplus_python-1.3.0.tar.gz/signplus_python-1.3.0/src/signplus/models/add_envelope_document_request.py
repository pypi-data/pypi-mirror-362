from .utils.json_map import JsonMap
from .utils.base_model import BaseModel
from .utils.sentinel import SENTINEL


@JsonMap({})
class AddEnvelopeDocumentRequest(BaseModel):
    """AddEnvelopeDocumentRequest

    :param file: File to upload in binary format, defaults to None
    :type file: bytes, optional
    """

    def __init__(self, file: bytes = SENTINEL, **kwargs):
        """AddEnvelopeDocumentRequest

        :param file: File to upload in binary format, defaults to None
        :type file: bytes, optional
        """
        if file is not SENTINEL:
            self.file = file
        self._kwargs = kwargs

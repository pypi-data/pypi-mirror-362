from .utils.json_map import JsonMap
from .utils.base_model import BaseModel


@JsonMap({})
class AddTemplateDocumentRequest(BaseModel):
    """AddTemplateDocumentRequest

    :param file: File to upload in binary format
    :type file: bytes
    """

    def __init__(self, file: bytes, **kwargs):
        """AddTemplateDocumentRequest

        :param file: File to upload in binary format
        :type file: bytes
        """
        self.file = file
        self._kwargs = kwargs

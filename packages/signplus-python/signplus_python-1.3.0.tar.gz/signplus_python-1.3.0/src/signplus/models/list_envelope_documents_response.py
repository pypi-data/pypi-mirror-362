from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .utils.base_model import BaseModel
from .utils.sentinel import SENTINEL
from .document import Document


@JsonMap({})
class ListEnvelopeDocumentsResponse(BaseModel):
    """ListEnvelopeDocumentsResponse

    :param documents: documents, defaults to None
    :type documents: List[Document], optional
    """

    def __init__(self, documents: List[Document] = SENTINEL, **kwargs):
        """ListEnvelopeDocumentsResponse

        :param documents: documents, defaults to None
        :type documents: List[Document], optional
        """
        if documents is not SENTINEL:
            self.documents = self._define_list(documents, Document)
        self._kwargs = kwargs

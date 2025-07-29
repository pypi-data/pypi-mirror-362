from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .utils.base_model import BaseModel
from .utils.sentinel import SENTINEL
from .annotation import Annotation


@JsonMap({})
class ListTemplateDocumentAnnotationsResponse(BaseModel):
    """ListTemplateDocumentAnnotationsResponse

    :param annotations: annotations, defaults to None
    :type annotations: List[Annotation], optional
    """

    def __init__(self, annotations: List[Annotation] = SENTINEL, **kwargs):
        """ListTemplateDocumentAnnotationsResponse

        :param annotations: annotations, defaults to None
        :type annotations: List[Annotation], optional
        """
        if annotations is not SENTINEL:
            self.annotations = self._define_list(annotations, Annotation)
        self._kwargs = kwargs

from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .utils.base_model import BaseModel
from .utils.sentinel import SENTINEL
from .page import Page


@JsonMap({"id_": "id"})
class Document(BaseModel):
    """Document

    :param id_: Unique identifier of the document, defaults to None
    :type id_: str, optional
    :param name: Name of the document, defaults to None
    :type name: str, optional
    :param filename: Filename of the document, defaults to None
    :type filename: str, optional
    :param page_count: Number of pages in the document, defaults to None
    :type page_count: int, optional
    :param pages: List of pages in the document, defaults to None
    :type pages: List[Page], optional
    """

    def __init__(
        self,
        id_: str = SENTINEL,
        name: str = SENTINEL,
        filename: str = SENTINEL,
        page_count: int = SENTINEL,
        pages: List[Page] = SENTINEL,
        **kwargs,
    ):
        """Document

        :param id_: Unique identifier of the document, defaults to None
        :type id_: str, optional
        :param name: Name of the document, defaults to None
        :type name: str, optional
        :param filename: Filename of the document, defaults to None
        :type filename: str, optional
        :param page_count: Number of pages in the document, defaults to None
        :type page_count: int, optional
        :param pages: List of pages in the document, defaults to None
        :type pages: List[Page], optional
        """
        if id_ is not SENTINEL:
            self.id_ = id_
        if name is not SENTINEL:
            self.name = name
        if filename is not SENTINEL:
            self.filename = filename
        if page_count is not SENTINEL:
            self.page_count = page_count
        if pages is not SENTINEL:
            self.pages = self._define_list(pages, Page)
        self._kwargs = kwargs

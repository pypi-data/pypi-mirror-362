from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .utils.base_model import BaseModel
from .utils.sentinel import SENTINEL
from .template import Template


@JsonMap({})
class ListTemplatesResponse(BaseModel):
    """ListTemplatesResponse

    :param has_next_page: Whether there is a next page, defaults to None
    :type has_next_page: bool, optional
    :param has_previous_page: Whether there is a previous page, defaults to None
    :type has_previous_page: bool, optional
    :param templates: templates, defaults to None
    :type templates: List[Template], optional
    """

    def __init__(
        self,
        has_next_page: bool = SENTINEL,
        has_previous_page: bool = SENTINEL,
        templates: List[Template] = SENTINEL,
        **kwargs,
    ):
        """ListTemplatesResponse

        :param has_next_page: Whether there is a next page, defaults to None
        :type has_next_page: bool, optional
        :param has_previous_page: Whether there is a previous page, defaults to None
        :type has_previous_page: bool, optional
        :param templates: templates, defaults to None
        :type templates: List[Template], optional
        """
        if has_next_page is not SENTINEL:
            self.has_next_page = has_next_page
        if has_previous_page is not SENTINEL:
            self.has_previous_page = has_previous_page
        if templates is not SENTINEL:
            self.templates = self._define_list(templates, Template)
        self._kwargs = kwargs

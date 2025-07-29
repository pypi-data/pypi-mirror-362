from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .utils.base_model import BaseModel
from .utils.sentinel import SENTINEL
from .envelope import Envelope


@JsonMap({})
class ListEnvelopesResponse(BaseModel):
    """ListEnvelopesResponse

    :param has_next_page: Whether there is a next page, defaults to None
    :type has_next_page: bool, optional
    :param has_previous_page: Whether there is a previous page, defaults to None
    :type has_previous_page: bool, optional
    :param envelopes: envelopes, defaults to None
    :type envelopes: List[Envelope], optional
    """

    def __init__(
        self,
        has_next_page: bool = SENTINEL,
        has_previous_page: bool = SENTINEL,
        envelopes: List[Envelope] = SENTINEL,
        **kwargs,
    ):
        """ListEnvelopesResponse

        :param has_next_page: Whether there is a next page, defaults to None
        :type has_next_page: bool, optional
        :param has_previous_page: Whether there is a previous page, defaults to None
        :type has_previous_page: bool, optional
        :param envelopes: envelopes, defaults to None
        :type envelopes: List[Envelope], optional
        """
        if has_next_page is not SENTINEL:
            self.has_next_page = has_next_page
        if has_previous_page is not SENTINEL:
            self.has_previous_page = has_previous_page
        if envelopes is not SENTINEL:
            self.envelopes = self._define_list(envelopes, Envelope)
        self._kwargs = kwargs

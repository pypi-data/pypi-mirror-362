from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .utils.base_model import BaseModel
from .utils.sentinel import SENTINEL
from .webhook import Webhook


@JsonMap({})
class ListWebhooksResponse(BaseModel):
    """ListWebhooksResponse

    :param webhooks: webhooks, defaults to None
    :type webhooks: List[Webhook], optional
    """

    def __init__(self, webhooks: List[Webhook] = SENTINEL, **kwargs):
        """ListWebhooksResponse

        :param webhooks: webhooks, defaults to None
        :type webhooks: List[Webhook], optional
        """
        if webhooks is not SENTINEL:
            self.webhooks = self._define_list(webhooks, Webhook)
        self._kwargs = kwargs

from __future__ import annotations
from .utils.json_map import JsonMap
from .utils.base_model import BaseModel
from .utils.sentinel import SENTINEL
from .webhook_event import WebhookEvent


@JsonMap({})
class ListWebhooksRequest(BaseModel):
    """ListWebhooksRequest

    :param webhook_id: ID of the webhook, defaults to None
    :type webhook_id: str, optional
    :param event: Event of the webhook, defaults to None
    :type event: WebhookEvent, optional
    """

    def __init__(
        self, webhook_id: str = SENTINEL, event: WebhookEvent = SENTINEL, **kwargs
    ):
        """ListWebhooksRequest

        :param webhook_id: ID of the webhook, defaults to None
        :type webhook_id: str, optional
        :param event: Event of the webhook, defaults to None
        :type event: WebhookEvent, optional
        """
        if webhook_id is not SENTINEL:
            self.webhook_id = webhook_id
        if event is not SENTINEL:
            self.event = self._enum_matching(event, WebhookEvent.list(), "event")
        self._kwargs = kwargs

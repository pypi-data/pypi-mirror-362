from __future__ import annotations
from .utils.json_map import JsonMap
from .utils.base_model import BaseModel
from .webhook_event import WebhookEvent


@JsonMap({})
class CreateWebhookRequest(BaseModel):
    """CreateWebhookRequest

    :param event: Event of the webhook
    :type event: WebhookEvent
    :param target: URL of the webhook target
    :type target: str
    """

    def __init__(self, event: WebhookEvent, target: str, **kwargs):
        """CreateWebhookRequest

        :param event: Event of the webhook
        :type event: WebhookEvent
        :param target: URL of the webhook target
        :type target: str
        """
        self.event = self._enum_matching(event, WebhookEvent.list(), "event")
        self.target = target
        self._kwargs = kwargs

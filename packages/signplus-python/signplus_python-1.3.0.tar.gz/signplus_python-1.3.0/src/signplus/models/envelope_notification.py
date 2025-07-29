from .utils.json_map import JsonMap
from .utils.base_model import BaseModel
from .utils.sentinel import SENTINEL


@JsonMap({})
class EnvelopeNotification(BaseModel):
    """EnvelopeNotification

    :param subject: Subject of the notification, defaults to None
    :type subject: str, optional
    :param message: Message of the notification, defaults to None
    :type message: str, optional
    :param reminder_interval: Interval in days to send reminder, defaults to None
    :type reminder_interval: int, optional
    """

    def __init__(
        self,
        subject: str = SENTINEL,
        message: str = SENTINEL,
        reminder_interval: int = SENTINEL,
        **kwargs
    ):
        """EnvelopeNotification

        :param subject: Subject of the notification, defaults to None
        :type subject: str, optional
        :param message: Message of the notification, defaults to None
        :type message: str, optional
        :param reminder_interval: Interval in days to send reminder, defaults to None
        :type reminder_interval: int, optional
        """
        if subject is not SENTINEL:
            self.subject = subject
        if message is not SENTINEL:
            self.message = message
        if reminder_interval is not SENTINEL:
            self.reminder_interval = reminder_interval
        self._kwargs = kwargs

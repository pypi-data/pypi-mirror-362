from .utils.json_map import JsonMap
from .utils.base_model import BaseModel
from .utils.sentinel import SENTINEL


@JsonMap({})
class CreateEnvelopeFromTemplateRequest(BaseModel):
    """CreateEnvelopeFromTemplateRequest

    :param name: Name of the envelope
    :type name: str
    :param comment: Comment for the envelope, defaults to None
    :type comment: str, optional
    :param sandbox: Whether the envelope is created in sandbox mode, defaults to None
    :type sandbox: bool, optional
    """

    def __init__(
        self, name: str, comment: str = SENTINEL, sandbox: bool = SENTINEL, **kwargs
    ):
        """CreateEnvelopeFromTemplateRequest

        :param name: Name of the envelope
        :type name: str
        :param comment: Comment for the envelope, defaults to None
        :type comment: str, optional
        :param sandbox: Whether the envelope is created in sandbox mode, defaults to None
        :type sandbox: bool, optional
        """
        self.name = self._define_str(
            "name",
            name,
            pattern="^[a-zA-Z0-9][a-zA-Z0-9 ]*[a-zA-Z0-9]$",
            min_length=2,
            max_length=256,
        )
        if comment is not SENTINEL:
            self.comment = comment
        if sandbox is not SENTINEL:
            self.sandbox = sandbox
        self._kwargs = kwargs

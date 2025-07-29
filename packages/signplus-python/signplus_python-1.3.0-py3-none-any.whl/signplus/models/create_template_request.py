from .utils.json_map import JsonMap
from .utils.base_model import BaseModel


@JsonMap({})
class CreateTemplateRequest(BaseModel):
    """CreateTemplateRequest

    :param name: name
    :type name: str
    """

    def __init__(self, name: str, **kwargs):
        """CreateTemplateRequest

        :param name: name
        :type name: str
        """
        self.name = self._define_str(
            "name",
            name,
            pattern="^[a-zA-Z0-9][a-zA-Z0-9 ]*[a-zA-Z0-9]$",
            min_length=2,
            max_length=256,
        )
        self._kwargs = kwargs

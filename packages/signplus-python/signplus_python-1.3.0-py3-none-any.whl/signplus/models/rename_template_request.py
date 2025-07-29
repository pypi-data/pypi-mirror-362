from .utils.json_map import JsonMap
from .utils.base_model import BaseModel


@JsonMap({})
class RenameTemplateRequest(BaseModel):
    """RenameTemplateRequest

    :param name: Name of the template
    :type name: str
    """

    def __init__(self, name: str, **kwargs):
        """RenameTemplateRequest

        :param name: Name of the template
        :type name: str
        """
        self.name = name
        self._kwargs = kwargs

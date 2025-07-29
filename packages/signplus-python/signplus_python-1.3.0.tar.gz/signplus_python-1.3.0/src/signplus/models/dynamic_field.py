from .utils.json_map import JsonMap
from .utils.base_model import BaseModel
from .utils.sentinel import SENTINEL


@JsonMap({})
class DynamicField(BaseModel):
    """DynamicField

    :param name: Name of the dynamic field, defaults to None
    :type name: str, optional
    :param value: Value of the dynamic field, defaults to None
    :type value: str, optional
    """

    def __init__(self, name: str = SENTINEL, value: str = SENTINEL, **kwargs):
        """DynamicField

        :param name: Name of the dynamic field, defaults to None
        :type name: str, optional
        :param value: Value of the dynamic field, defaults to None
        :type value: str, optional
        """
        if name is not SENTINEL:
            self.name = name
        if value is not SENTINEL:
            self.value = value
        self._kwargs = kwargs

from .utils.json_map import JsonMap
from .utils.base_model import BaseModel
from .utils.sentinel import SENTINEL


@JsonMap({})
class Page(BaseModel):
    """Page

    :param width: Width of the page in pixels, defaults to None
    :type width: int, optional
    :param height: Height of the page in pixels, defaults to None
    :type height: int, optional
    """

    def __init__(self, width: int = SENTINEL, height: int = SENTINEL, **kwargs):
        """Page

        :param width: Width of the page in pixels, defaults to None
        :type width: int, optional
        :param height: Height of the page in pixels, defaults to None
        :type height: int, optional
        """
        if width is not SENTINEL:
            self.width = width
        if height is not SENTINEL:
            self.height = height
        self._kwargs = kwargs

from typing import Union
from .net.environment import Environment
from .sdk import Signplus
from .services.async_.signplus import SignplusServiceAsync


class SignplusAsync(Signplus):
    """
    SignplusAsync is the asynchronous version of the Signplus SDK Client.
    """

    def __init__(
        self,
        access_token: str = None,
        base_url: Union[Environment, str, None] = None,
        timeout: int = 60000,
    ):
        super().__init__(access_token=access_token, base_url=base_url, timeout=timeout)

        self.signplus = SignplusServiceAsync(base_url=self._base_url)

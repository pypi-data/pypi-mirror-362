import os
from .dict_of_dict import DictOfDict


class EnvironmentVariableProvider(DictOfDict):
    """
    Environment Variable Provider for Configuration
    
    Environment variables must be prepended with "AEA__" to be recognized.

    If 'AEA__Setting__SubSetting' = 123 then config["Setting:SubSetting"] = 123
    """
    def __init__(self):
        super().__init__()
        self.my_dict = DictOfDict()
        for key, val in dict(os.environ).items():
            self._process(key, val)

    def _process(self, key: str, val: str):
        if key.startswith("AEA__"):
            super().__setitem__(key[5:], val)

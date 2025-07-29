import sys
from .dict_of_dict import DictOfDict


class CommandLineProvider(DictOfDict):
    """
    CommandLineProvide deals with inclusion of Command Line parameters
    into the setting.  Currently it is required to use like this

    python app.py -dSetting__SubSetting=Value
    """
    def __init__(self):
        super().__init__()
        for arg in sys.argv:
            self._processArg(arg)

    # private methods

    def _processArg(self, arg: str):
        if arg.startswith("-d") and len(arg) > 2:
            first_equals = arg.find("=")
            if first_equals != -1:
                key = arg[2:first_equals]
                val = arg[first_equals+1:]
                super().__setitem__(key, val)

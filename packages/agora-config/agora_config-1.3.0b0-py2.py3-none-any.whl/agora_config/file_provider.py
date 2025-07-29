import json
import pathlib
from agora_logging import logger
from .dict_of_dict import DictOfDict
import os
import __main__


class FileProvider(DictOfDict):
    """
    Provides configuration settings using a specific file.  Internally the file is 'AEA.json'
    which is either the primary config file or the alternate config file.  Contents of the
    file must be valid json.
    """
    def __init__(self, filename):
        super().__init__()
        try:
           main_stript_path = __main__.__file__
           base_directory = os.path.dirname(os.path.abspath(main_stript_path))
        except:
           main_stript_path = "."
           base_directory = os.path.abspath(main_stript_path)
        self.config_file = os.path.abspath(base_directory + '/' + filename)
        if filename == "AEA.json":
            self.primary = True
        else:
            self.primary = False
        self.last_modified_time = 0
        self.__check_time()

    def check_for_updates(self) -> bool:
        """
        Checks if the file has been changed,added, or deleted.
        """
        return self.__check_time()

    def get_config_file_type(self) -> str:
        """
        Returns whether the FileProvider is the 'PRIMARY' configuration or the 'ALTERNATE'.
        """
        if self.primary:
            return 'PRIMARY'
        return 'ALTERNATE'

    # private methods

    def __read_config(self) -> dict:
        """
        Reads the configuration file
        """
        self.clear()
        file_path = pathlib.Path(self.config_file)
        if file_path.exists():
            data = file_path.read_text()
            try:
                self.merge(json.loads(data))
            except Exception as e:
                logger.exception(
                    e, f"Could not load {self.get_config_file_type()} config file '{file_path}' : {str(e)}")
                self.clear()

    def __check_time(self) -> bool:
        """
        Checks if the time on the configuration file has changed
        """
        mtime = 0
        file_path = pathlib.Path(self.config_file)
        if file_path.exists():
            try:
                mtime = file_path.stat().st_mtime
            except Exception as e:
                logger.exception(
                    e, f"Could not get {self.get_config_file_type()} config file time. (config_file = '{file_path}')")
                return False
            if mtime != self.last_modified_time:
                self.__read_config()
                self.last_modified_time = mtime
                return True
        else:
            # print( f"file = '{self.config_file.absolute()}' - does not exist")
            super().clear()
        return False

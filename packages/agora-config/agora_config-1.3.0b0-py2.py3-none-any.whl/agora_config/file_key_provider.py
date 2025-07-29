import pathlib
from agora_logging import logger
from .dict_of_dict import DictOfDict
import os
import __main__


class FileKeyProvider(DictOfDict):
    """
    Provides configuration settings using Files where the filename is the 'key' and the 'value'
    is the contents of the file - precisely.  This does not mean the value in the file is JSON... 
    The entire contents of the file becomes the 'value'.

    If file 'Setting__SubSetting' contains '123' then config["Setting:SubSetting"] == 123
    """
    def __init__(self):
        super().__init__()
        try:
           main_stript_path = __main__.__file__
           base_directory = os.path.dirname(os.path.abspath(main_stript_path))
        except:
           main_stript_path = "."
           base_directory = os.path.abspath(main_stript_path)
           
        self.key_folder = os.path.abspath(base_directory + '/config/keys')
        self.last_modified_time = 0
        self.__check_time()

    def check_for_updates(self) -> bool:
        """
        Checks if any of the 'key' files has changed, been added, or has been removed.
        """
        return self.__check_time()

    # private methods

    def __read_config(self) -> dict:
        super().clear()
        key_path = pathlib.Path(self.key_folder)
        if key_path.exists() and key_path.is_dir():
            for file_path in key_path.iterdir():
                if file_path.is_file():
                    try:
                        with file_path.open() as f:
                            contents = f.read()
                            if len(contents) > 0 and contents[-1] == '\n':
                                contents = contents[:-1]
                        # print(f"contents of '{file_path.name}' is '{contents}'")
                        self.__set(file_path.name, contents)
                    except Exception as e:
                        logger.exception(
                            e, f"Could not load config file '{file_path}' : {str(e)}")

    def __set(self, key, value):
        new_dict = dict()
        current_dict = new_dict
        parts = key.split("__")
        if len(parts) > 0:
            for element in parts[:-1]:
                current_dict[element] = {}
                current_dict = current_dict[element]
            current_dict[parts[-1]] = value
        super().merge(new_dict)

    def __check_time(self) -> bool:
        """
        Checks if the times of any of the key-files or the key folder itself (i.e. a file create or delete) has changed 
        """
        mtime = 0
        modified = False
        key_path = pathlib.Path(self.key_folder)
        if key_path.exists() and key_path.is_dir():
            try:
                mtime = key_path.stat().st_mtime
                if mtime > self.last_modified_time:
                    # print( "key_folder modified" )
                    self.last_modified_time = mtime
                    modified = True
            except Exception as e:
                logger.exception(
                    e, "Could not get key folder time. 'config/keys'")

            for file_path in key_path.iterdir():
                if file_path.is_file():
                    try:
                        mtime = file_path.stat().st_mtime
                        # if file_path.name == "DEF":
                        # print( f"DEF mtime = {mtime}")
                        if mtime > self.last_modified_time:
                            # print( f"file '{file_path.name}' modified" )
                            self.last_modified_time = mtime
                            modified = True
                    except Exception as e:
                        logger.exception(
                            e, f"Could not get config file time. (config_file = '{self.key_folder}')")

            if modified == True:
                self.__read_config()
                return True
        return False

class DictOfDict(dict):
    """
    Provides dictionary with ability to access sub-items if the 'key' contains
    '__' or ':' as separators of sub-keys.  For example,

    dict["Setting__SubSetting"] == dict["Setting:SubSetting"] == dict["Setting"]["SubSetting"]
    """
    def __getitem__(self, key: str):
        key = key.replace("__", ":")
        if isinstance(key, str) and ':' in key:
            keys = key.split(':')
            try:
                value = super().__getitem__(keys[0])
                for k in keys[1:]:
                    if isinstance(value, dict):
                        value = value[k]
                    else:
                        return ""
            except KeyError:
                return ""
            return value
        else:
            try:
                value = super().__getitem__(key)
                return value
            except KeyError:
                return ""

    def __setitem__(self, key: str, value: str):
        key = key.replace("__", ":")
        if isinstance(key, str) and ':' in key:
            keys=key.split(':')
            nested_dict = self
            for k in keys[:-1]:
                if k not in nested_dict:
                    nested_dict[k] = DictOfDict()
                elif not isinstance(nested_dict[k], dict):
                    nested_dict[k] = DictOfDict()
                nested_dict = nested_dict[k]
            nested_dict[keys[-1]] = value
        else:
            super().__setitem__(key,value)
        return

    def __delitem__(self, key):
        key = key.replace("__", ":")
        if isinstance(key, str) and ":" in key:
            key1, key2 = key.split(":", 1)
            if key1 in self and isinstance(self[key1], DictOfDict):
                del self[key1][key2]
                if not bool(self[key1]):
                    super().__delitem__(key1)
        else:
            if key in self:
                super().__delitem__(key)


    def merge(self, other: dict):
        merge_nested_dicts(self, other)

def merge_nested_dicts(dict1: dict, dict2: dict):
    """
    Merges dictionary 'dict2' into 'dict1'.
    """
    for key, value in dict2.items():
        if key in dict1 and isinstance(dict1[key], dict) \
            and isinstance(value, dict):
            merge_nested_dicts(dict1[key], value)
        else:
            if isinstance(value, dict):
                dict1[key] = DictOfDict()
                merge_nested_dicts(dict1[key], value)
            else:
                dict1[key] = value
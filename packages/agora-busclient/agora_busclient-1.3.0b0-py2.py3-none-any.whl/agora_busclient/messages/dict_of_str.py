
class DictOfStr(dict):
    """
    Provides dictionary with ability to store key and value of type string.  For example,

    dict["Setting__SubSetting"] = "ABC"
    """    
    def __getitem__(self,key):
        return dict.__getitem__(self,key)
    def __setitem__(self, key, value):
        if not isinstance(key, str) or not isinstance(value, str):
            raise TypeError("key and value in Dictionary must be strings")        
        dict.__setitem__(self,key,value)

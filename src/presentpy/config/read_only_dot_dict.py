class ReadOnlyDotDict:
    def __init__(self, dictionary):
        self.internal_dicts = {}
        for key, value in dictionary.items():
            if isinstance(value, dict):
                self.internal_dicts[key] = ReadOnlyDotDict(value)
            else:
                self.internal_dicts[key] = value

    def __getattr__(self, name):
        if name in self.internal_dicts:
            return self.internal_dicts[name]
        else:
            name_ = name.replace("_", "-")
            if name_ in self.internal_dicts:
                return self.internal_dicts[name_]
        raise KeyError(f"Attribute {name} not found")

    def __getitem__(self, name):
        return self.__getattr__(name)

    def get(self, name, default=None):
        try:
            return self.__getattr__(name)
        except KeyError:
            return default

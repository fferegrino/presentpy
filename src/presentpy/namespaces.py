from collections import UserDict


class Namespaces(UserDict):
    def __call__(self, tag, *args, **kwargs):
        return self.resolve(tag)

    def resolve(self, tag):
        ns, _, tag = tag.rpartition(":")
        if ns == "":
            return tag
        return f"{{{self[ns]}}}{tag}"

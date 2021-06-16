class DictCache:
    def __init__(self, data={}, max_length=100):
        self._dict = data
        self.max_length = max_length

    def __len__(self):
        return len(self._dict)

    def __getitem__(self, key):
        return self._dict[key]

    def __setitem__(self, key, value):
        if len(self._dict) == self.max_length:
            del self._dict[list(self.keys())[0]]
        self._dict[key] = value

    def __delitem__(self, key):
        del self._dict[key]

    def __str__(self):
        return str(self._dict)

    def __iter__(self):
        for key in self._dict:
            yield key

    def copy(self):
        return dict(self._dict)

    def get(self, key, backup):
        return self._dict.get(key, backup)

    def clear(self):
        self._dict.clear()

    def values(self):
        return self._dict.values()

    def keys(self):
        return self._dict.keys()

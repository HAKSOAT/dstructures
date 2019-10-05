class Array:
    def __init__(self, size):
        self.alloc_size = size
        self.array = [None] * size

    def __iter__(self):
        self.pointer = 0
        return self

    def __next__(self):
        if self.pointer < self.alloc_size:
            result = self.array[self.pointer]
            self.pointer += 1
            return result
        else:
            raise StopIteration

    def _check_index(self, key):
        if type(key) != int:
            raise TypeError("Array indices must be an integer or a slice")
        if key < 0 or self.alloc_size <= key:
            raise IndexError("Array index out of range")

    def __getitem__(self, key):
        self._check_index(key)
        result = self.array[key]
        return result

    def __setitem__(self, key, value):
        self._check_index(key)
        self.array[key] = value

    def __repr__(self):
        return "{}".format(self.array)


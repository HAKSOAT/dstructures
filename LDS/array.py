class Array:
    def __init__(self, size, data_type):
        self.alloc_size = size
        self.data_type = data_type
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

    def _check_value(self, value):
        if type(value) != self.data_type:
            raise ValueError("Value for this array must be of {} type".format(self.data_type))

    def __getitem__(self, key):
        self._check_index(key)
        result = self.array[key]
        return result

    def __setitem__(self, key, value):
        self._check_index(key)
        self._check_value(value)
        self.array[key] = value

    def __repr__(self):
        return "{}".format(self.array)


class BitArray(Array):
    def __init__(self, size):
        super().__init__(size, data_type=bool)

    def __setitem__(self, key, value):
        self._check_index(key)
        self._check_value(value)
        self.array[key] = value

    def __invert__(self):
        for index, value in enumerate(self.array):
            if value is None:
                continue
            self.array[index] = False if value is True else True

    def _apply_operator(self, other, operator):
        if type(other) == type(self):
            zipped_array = list(zip(other.array, self.array))
            zipped_array_length = len(zipped_array)
            resulting_array = BitArray(zipped_array_length)
            for index, node in enumerate(zipped_array):
                if node[0] is None or node[1] is None:
                    continue
                if operator == "and":
                    resulting_array[index] = node[0] & node[1]
                elif operator == "or":
                    resulting_array[index] = node[0] | node[1]
                elif operator == "xor":
                    resulting_array[index] = node[0] ^ node[1]
            return resulting_array
        else:
            raise TypeError("Array is not of {} type".format(type(self)))

    def __and__(self, other):
        return self._apply_operator(other, "and")

    def __or__(self, other):
        return self._apply_operator(other, "or")

    def __xor__(self, other):
        return self._apply_operator(other, "xor")

    def set_all(self, value):
        self._check_value(value)
        for i in range(self.alloc_size):
            self.array[i] = value

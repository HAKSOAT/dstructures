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


class Bitboard:
    """ A  Bitboard is a 64-bit integer.
        The Bitboard implementation here is unsigned. Hence, negative values are not allowed.
    """
    def __init__(self, value=None, bit_type=None):
        self.max_value = (2 ** 64) - 1
        self.min_value = 0
        self.binary_prefix = '0b'
        if value is None and bit_type == "ones":
            self._value = bin(self.max_value)
        elif value is None and bit_type == "zeros":
            self._value = bin(self.min_value)
        elif value is None and bit_type not in ["ones", "zeros"]:
            raise ValueError("The bit_type argument must be 'ones' or 'zeros'")
        else:
            temp_value = int("{}".format(value), 2)
            if not self.min_value <= temp_value <= self.max_value:
                raise ValueError("Must be a valid 64 bit value")
            self._value = bin(temp_value)

    def __repr__(self):
        number_of_bits = 64
        result = self._value.replace(self.binary_prefix, '')
        return result.zfill(number_of_bits)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        temp_value = int("{}".format(v), 2)
        if not self.min_value <= temp_value <= self.max_value:
            raise ValueError("Must be a valid 64 bit value")
        self._value = bin(temp_value)

    def __setitem__(self, key, value):
        if type(key) is not int:
            raise ValueError("Key must be an integer")
        if value not in [0, 1, "0", "1"]:
            raise ValueError("Value must be a bit")
        if not self.min_value <= key <= self.max_value:
            raise IndexError("Index is out of range")
        binary_prefix_count = 2
        pre_index = self.value[:key+binary_prefix_count]
        post_index = self.value[key+binary_prefix_count+1:]
        self._value = "{}{}{}".format(pre_index, value, post_index)

    def _apply_operator(self, guest, operator):
        temp_value = self._value.replace(self.binary_prefix, '')
        host_value = int(temp_value, 2)
        guest_value = int(guest.value, 2)
        # The choice of an all-one BitBoard below has no effect on the results.
        # An all-zero BitBoard will have the same effect.
        resulting_bitboard = Bitboard(bit_type="ones")
        if operator == "and":
            resulting_bitboard.value = bin(host_value & guest_value)
        elif operator == "or":
            resulting_bitboard.value = bin(host_value | guest_value)
        elif operator == "xor":
            resulting_bitboard.value = bin(host_value ^ guest_value)
        return resulting_bitboard

    def __and__(self, guest):
        return self._apply_operator(guest, "and")

    def __or__(self, guest):
        return self._apply_operator(guest, "or")

    def __xor__(self, guest):
        return self._apply_operator(guest, "xor")

    def __lshift__(self, shift_value):
        if type(shift_value) is not int:
            raise ValueError("Must left shift using integers.")
        decimal_equivalent = int(self._value, 2)
        self._value = bin(decimal_equivalent << shift_value)
        return self

    def __rshift__(self, shift_value):
        if type(shift_value) is not int:
            raise ValueError("Must right shift using integers.")
        decimal_equivalent = int(self._value, 2)
        self._value = bin(decimal_equivalent >> shift_value)
        return self

    def first_bit(self):
        temp_value = self._value.replace(self.binary_prefix, '')
        reversed_value = temp_value[::-1]
        result = reversed_value.find("1")
        if result == -1:
            return None
        return result

    def last_bit(self):
        value = self._value.replace(self.binary_prefix, '')
        result = value.find("1")
        if result == -1:
            return None
        return result

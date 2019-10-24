class Array:
    def __init__(self, size, data_type):
        self.alloc_size = size
        self.data_type = data_type
        self._array = [None] * size

    def __iter__(self):
        self.pointer = 0
        return self

    def __next__(self):
        if self.pointer < self.alloc_size:
            result = self._array[self.pointer]
            self.pointer += 1
            return result
        else:
            raise StopIteration

    @property
    def array(self):
        return self._array

    @array.setter
    def array(self, v):
        if type(v) is not list:
            raise ValueError("Must be a Python list")
        for each in v:
            self._check_value(each)
        self._array = v

    def _check_index(self, key):
        if type(key) != int:
            raise TypeError("Array indices must be an integer or a slice")
        if key < 0 or self.alloc_size <= key:
            raise IndexError("Array index out of range")

    def _check_value(self, value):
        if type(value) != self.data_type:
            raise ValueError("Values for this array must be of {} type".format(self.data_type))

    def __getitem__(self, key):
        self._check_index(key)
        result = self._array[key]
        return result

    def __setitem__(self, key, value):
        self._check_index(key)
        self._check_value(value)
        self._array[key] = value

    def __repr__(self):
        return "{}".format(self._array)


class BitArray(Array):
    def __init__(self, size):
        super().__init__(size, data_type=bool)

    def __setitem__(self, key, value):
        self._check_index(key)
        self._check_value(value)
        self._array[key] = value

    def __invert__(self):
        for index, value in enumerate(self._array):
            if value is None:
                continue
            self._array[index] = False if value is True else True

    def _apply_operator(self, other, operator):
        if type(other) == type(self):
            zipped_array = list(zip(other.array, self._array))
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
            self._array[i] = value


class Bitboard:
    """ A  Bitboard is a 64-bit integer.
        The Bitboard implementation here is unsigned. Hence, negative values are not allowed.
    """
    def __init__(self, value=None, bit_type=None):
        self.number_of_bits = 64
        self.max_value = (2 ** self.number_of_bits) - 1
        self.min_value = 0
        self.binary_prefix = '0b'
        if value is None and bit_type == "ones":
            self._value = bin(self.max_value).replace(self.binary_prefix, '')
        elif value is None and bit_type == "zeros":
            temp_value = bin(self.min_value).replace(self.binary_prefix, '')
            self._value = temp_value.zfill(self.number_of_bits)
        elif value is None and bit_type not in ["ones", "zeros"]:
            raise ValueError("The bit_type argument must be 'ones' or 'zeros'")
        else:
            temp_value = int("{}".format(value), 2)
            if not self.min_value <= temp_value <= self.max_value:
                raise ValueError("Must be a valid 64 bit value")
            temp_value = bin(temp_value).replace(self.binary_prefix, '')
            self._value = temp_value.zfill(self.number_of_bits)

    def __repr__(self):
        result = self._value.replace(self.binary_prefix, '')
        return result.zfill(self.number_of_bits)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        temp_value = int("{}".format(v), 2)
        if not self.min_value <= temp_value <= self.max_value:
            raise ValueError("Must be a valid 64 bit value")
        temp_value = bin(temp_value).replace(self.binary_prefix, '')
        self._value = temp_value.zfill(self.number_of_bits)

    def __setitem__(self, key, value):
        if type(key) is not int:
            raise ValueError("Key must be an integer")
        if value not in [0, 1, "0", "1"]:
            raise ValueError("Value must be a bit")
        if not self.min_value <= key <= self.max_value:
            raise IndexError("Index is out of range")
        pre_index = self._value[:key]
        post_index = self._value[key+1:]
        self._value = "{}{}{}".format(pre_index, value, post_index)

    def _apply_operator(self, guest, operator):
        temp_value = self._value.replace(self.binary_prefix, '')
        host_decimal_value = int(temp_value, 2)
        guest_decimal_value = int(guest.value, 2)
        # The choice of an all-one BitBoard below has no effect on the results.
        # An all-zero BitBoard will have the same effect.
        resulting_bitboard = Bitboard(bit_type="ones")
        if operator == "and":
            temp_value = bin(host_decimal_value & guest_decimal_value).replace(self.binary_prefix, '')
            resulting_bitboard.value = temp_value.zfill(self.number_of_bits)
        elif operator == "or":
            temp_value = bin(host_decimal_value | guest_decimal_value).replace(self.binary_prefix, '')
            resulting_bitboard.value = temp_value.zfill(self.number_of_bits)
        elif operator == "xor":
            temp_value = bin(host_decimal_value ^ guest_decimal_value).replace(self.binary_prefix, '')
            resulting_bitboard.value = temp_value.zfill(self.number_of_bits)
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
        decimal_value = int(self._value, 2)
        temp_value = bin(decimal_value << shift_value)
        self._value = temp_value.zfill(self.number_of_bits)
        return self

    def __rshift__(self, shift_value):
        if type(shift_value) is not int:
            raise ValueError("Must right shift using integers.")
        decimal_value = int(self._value, 2)
        temp_value = bin(decimal_value >> shift_value)
        self._value = temp_value.zfill(self.number_of_bits)
        return self

    def first_bit(self):
        reversed_value = self._value[::-1]
        result = reversed_value.find("1")
        if result == -1:
            return None
        return result

    def last_bit(self):
        result = self._value.find("1")
        if result == -1:
            return None
        return result


class CircularBuffer:
    def __init__(self, length):
        self.buffer_length = length
        self._buffer = [None] * self.buffer_length
        # Value of -1 is chosen because:
        # the logic used involves incrementing the index before the write operation
        self.write_start_index = -1
        self.read_start_index = 0
        self.write_pointer = self.write_start_index
        self.read_pointer = self.read_start_index

    def increment_pointer(self, pointer_type):
        if pointer_type == "write":
            self.write_pointer += 1
            # Handles cases of buffer overwrite
            # Where the read pointer needs to shift based on how much data is overwritten
            if self.get_index("read") == self.get_index("write"):
                self.read_pointer += 1
        elif pointer_type == "read":
            self.read_pointer += 1
        else:
            raise ValueError("Pointer type must be read or write")

    def get_index(self, pointer_type):
        if pointer_type == "write":
            if self.write_pointer < self.buffer_length:
                index = self.write_pointer
            else:
                index = self.write_pointer % self.buffer_length
            return index
        elif pointer_type == "read":
            if self.read_pointer < self.buffer_length:
                index = self.read_pointer
            else:
                index = self.read_pointer % self.buffer_length
            return index
        else:
            raise ValueError("Pointer type must be read or write")

    def add(self, value):
        self.increment_pointer("write")
        write_index = self.get_index("write")
        self._buffer[write_index] = value

    def pop(self):
        # Prevents read operation if no write operation has been done
        if self.write_pointer == self.write_start_index:
            return None
        read_index = self.get_index("read")
        popped = self._buffer[read_index]
        self._buffer[read_index] = None
        self.increment_pointer("read")
        return popped

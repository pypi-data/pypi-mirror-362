class Int8:
    def __init__(self, value=0):
        self.value = self.to_int8(value)

    def to_int8(self, value):
        value &= 0xFF
        if value & 0x80:
            value -= 0x100
        return value

    def set(self, value):
        self.value = self.to_int8(value)

    def get(self):
        return self.value

    def __int__(self):
        return self.value

    def __repr__(self):
        return f"Int8({self.value})"

    def __add__(self, other):
        if isinstance(other, Int8):
            other = other.value
        return Int8(self.value + other)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, Int8):
            other = other.value
        return Int8(self.value - other)

    def __eq__(self, other):
        if isinstance(other, Int8):
            return self.value == other.value
        return self.value == other


class Int16:
    def __init__(self, value=0):
        self.value = self.to_int16(value)

    def to_int16(self, value):
        value &= 0xFFFF
        if value & 0x8000:
            value -= 0x10000
        return value

    def set(self, value):
        self.value = self.to_int16(value)

    def get(self):
        return self.value

    def __int__(self):
        return self.value

    def __repr__(self):
        return f"Int16({self.value})"

    def __add__(self, other):
        if isinstance(other, Int16):
            other = other.value
        return Int16(self.value + other)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, Int16):
            other = other.value
        return Int16(self.value - other)

    def __eq__(self, other):
        if isinstance(other, Int16):
            return self.value == other.value
        return self.value == other


class Int32:
    def __init__(self, value=0):
        self.value = self.to_int32(value)

    def to_int32(self, value):
        value &= 0xFFFFFFFF
        if value & 0x80000000:
            value -= 0x100000000
        return value

    def set(self, value):
        self.value = self.to_int32(value)

    def get(self):
        return self.value

    def __int__(self):
        return self.value

    def __repr__(self):
        return f"Int32({self.value})"

    def __add__(self, other):
        if isinstance(other, Int32):
            other = other.value
        return Int32(self.value + other)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, Int32):
            other = other.value
        return Int32(self.value - other)

    def __eq__(self, other):
        if isinstance(other, Int32):
            return self.value == other.value
        return self.value == other


class Int64:
    def __init__(self, value=0):
        self.value = self.to_int64(value)

    def to_int64(self, value):
        value &= 0xFFFFFFFFFFFFFFFF
        if value & 0x8000000000000000:
            value -= 0x10000000000000000
        return value

    def set(self, value):
        self.value = self.to_int64(value)

    def get(self):
        return self.value

    def __int__(self):
        return self.value

    def __repr__(self):
        return f"Int64({self.value})"

    def __add__(self, other):
        if isinstance(other, Int64):
            other = other.value
        return Int64(self.value + other)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, Int64):
            other = other.value
        return Int64(self.value - other)

    def __eq__(self, other):
        if isinstance(other, Int64):
            return self.value == other.value
        return self.value == other

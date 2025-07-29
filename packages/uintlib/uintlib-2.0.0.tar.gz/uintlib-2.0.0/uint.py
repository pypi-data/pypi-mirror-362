class UInt8:
    def __init__(self, value=0):
        self.value = value & 0xFF

    def set(self, value):
        self.value = value & 0xFF

    def get(self):
        return self.value

    def __int__(self):
        return self.value

    def __repr__(self):
        return f"UInt8({self.value})"

    def __add__(self, other):
        if isinstance(other, UInt8):
            other = other.value
        return UInt8((self.value + other) & 0xFF)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, UInt8):
            other = other.value
        return UInt8((self.value - other) & 0xFF)

    def __eq__(self, other):
        if isinstance(other, UInt8):
            return self.value == other.value
        return self.value == other


class UInt16:
    def __init__(self, value=0):
        self.value = value & 0xFFFF

    def set(self, value):
        self.value = value & 0xFFFF

    def get(self):
        return self.value

    def __int__(self):
        return self.value

    def __repr__(self):
        return f"UInt16({self.value})"

    def __add__(self, other):
        if isinstance(other, UInt16):
            other = other.value
        return UInt16((self.value + other) & 0xFFFF)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, UInt16):
            other = other.value
        return UInt16((self.value - other) & 0xFFFF)

    def __eq__(self, other):
        if isinstance(other, UInt16):
            return self.value == other.value
        return self.value == other


class UInt32:
    def __init__(self, value=0):
        self.value = value & 0xFFFFFFFF

    def set(self, value):
        self.value = value & 0xFFFFFFFF

    def get(self):
        return self.value

    def __int__(self):
        return self.value

    def __repr__(self):
        return f"UInt32({self.value})"

    def __add__(self, other):
        if isinstance(other, UInt32):
            other = other.value
        return UInt32((self.value + other) & 0xFFFFFFFF)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, UInt32):
            other = other.value
        return UInt32((self.value - other) & 0xFFFFFFFF)

    def __eq__(self, other):
        if isinstance(other, UInt32):
            return self.value == other.value
        return self.value == other


class UInt64:
    def __init__(self, value=0):
        self.value = value & 0xFFFFFFFFFFFFFFFF

    def set(self, value):
        self.value = value & 0xFFFFFFFFFFFFFFFF

    def get(self):
        return self.value

    def __int__(self):
        return self.value

    def __repr__(self):
        return f"UInt64({self.value})"

    def __add__(self, other):
        if isinstance(other, UInt64):
            other = other.value
        return UInt64((self.value + other) & 0xFFFFFFFFFFFFFFFF)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, UInt64):
            other = other.value
        return UInt64((self.value - other) & 0xFFFFFFFFFFFFFFFF)

    def __eq__(self, other):
        if isinstance(other, UInt64):
            return self.value == other.value
        return self.value == other

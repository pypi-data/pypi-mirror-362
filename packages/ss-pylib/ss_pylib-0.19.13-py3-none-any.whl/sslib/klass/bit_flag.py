class BitFlag8:
    def __init__(self, value: int = 0) -> None:
        self.value = value

    def less(self, flag: int) -> bool:
        return self.value < flag

    def set_flag(self, flag: int) -> None:
        self.value |= flag

    def clear_flag(self, flag: int) -> None:
        self.value &= ~flag

    def is_set(self, flag: int) -> bool:
        return (self.value & flag) == flag

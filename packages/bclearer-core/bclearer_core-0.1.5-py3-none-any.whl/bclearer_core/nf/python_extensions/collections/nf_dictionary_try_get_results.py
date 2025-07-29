class NfDictionaryTryGetResults:
    def __init__(self):
        self.__key_exists = False

        self.__value = None

    def __get_key_exists(self) -> bool:
        key_exists = self.__key_exists

        return key_exists

    def __set_key_exists(
        self,
        key_exists: bool,
    ):
        self.__key_exists = key_exists

    def __get_value(self):
        value = self.__value

        return value

    def __set_value(self, value):
        self.__value = value

    key_exists = property(
        fget=__get_key_exists,
        fset=__set_key_exists,
    )

    value = property(
        fget=__get_value,
        fset=__set_value,
    )

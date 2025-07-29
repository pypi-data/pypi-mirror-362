from bclearer_core.nf.python_extensions.collections.nf_dictionaries import (
    NfDictionaries,
)


class NfBimappings:
    def __init__(self, map: dict):
        NfBimappings.__populate_internal_dictionaries(
            self,
            map=map,
        )

    def try_get_range_using_domain(
        self,
        domain_key,
    ):
        range_value = self.__range_keyed_on_domain.try_get_value(
            key=domain_key,
        )

        return range_value

    def try_get_domain_using_range(
        self,
        range_key,
    ):
        domain_value = self.__domain_keyed_on_range.try_get_value(
            key=range_key,
        )

        return domain_value

    def get_range(self):
        range = (
            self.__domain_keyed_on_range.keys()
        )

        return range

    def get_domain(self):
        domain = (
            self.__range_keyed_on_domain.keys()
        )

        return domain

    def get_range_keyed_on_domain(self):
        range_keyed_on_domain = (
            self.__range_keyed_on_domain
        )

        return range_keyed_on_domain

    def get_domain_keyed_on_range(self):
        domain_keyed_on_range = (
            self.__domain_keyed_on_range
        )

        return domain_keyed_on_range

    def __populate_internal_dictionaries(
        self,
        map: dict,
    ):
        self.__domain_keyed_on_range = (
            NfDictionaries()
        )

        self.__range_keyed_on_domain = (
            NfDictionaries()
        )

        for (
            domain_value,
            range_value,
        ) in map.items():
            self.add_mapping(
                domain_value=domain_value,
                range_value=range_value,
            )

    def add_mapping(
        self,
        domain_value,
        range_value,
    ):
        self.__domain_keyed_on_range[
            range_value
        ] = domain_value

        self.__range_keyed_on_domain[
            domain_value
        ] = range_value

    @staticmethod
    def __populate_range_keyed_on_range(
        map: NfDictionaries,
    ) -> NfDictionaries:
        domain_keyed_on_range = (
            NfDictionaries()
        )

        for (
            domain_value,
            range_value,
        ) in map:
            domain_keyed_on_range[
                range_value
            ] = domain_value

        return domain_keyed_on_range

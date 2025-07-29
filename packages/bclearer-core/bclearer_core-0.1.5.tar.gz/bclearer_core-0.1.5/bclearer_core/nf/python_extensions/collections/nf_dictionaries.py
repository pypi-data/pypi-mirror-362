from bclearer_core.nf.python_extensions.collections.nf_dictionary_try_get_results import (
    NfDictionaryTryGetResults,
)


class NfDictionaries(dict):
    def __init__(self):
        dict.__init__(self)

    def try_get_value(
        self,
        key,
    ) -> NfDictionaryTryGetResults:
        nf_dictionary_try_get_result = (
            NfDictionaryTryGetResults()
        )

        nf_dictionary_try_get_result.key_exists = (
            key in self.keys()
        )

        if (
            nf_dictionary_try_get_result.key_exists
        ):
            nf_dictionary_try_get_result.value = self.get(
                key,
            )
        else:
            nf_dictionary_try_get_result.value = (
                None
            )

        return (
            nf_dictionary_try_get_result
        )

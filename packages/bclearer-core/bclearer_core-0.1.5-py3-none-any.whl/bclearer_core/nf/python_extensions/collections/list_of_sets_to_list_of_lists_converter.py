def convert_list_of_sets_to_list_of_lists(
    list_of_sets: list,
) -> list:
    list_of_lists = []

    for set_1 in list_of_sets:
        __convert_set_to_list_and_append(
            list_of_lists,
            set_1,
        )

    return list_of_lists


def __convert_set_to_list_and_append(
    list_of_lists: list,
    set_1: set,
):
    set_as_list = []

    for element in set_1:
        set_as_list.append(element)

    list_of_lists.append(set_as_list)

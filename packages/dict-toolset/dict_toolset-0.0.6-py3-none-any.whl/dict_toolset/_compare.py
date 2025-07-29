from typing import Callable, Literal, Generator

from ._key_extractor import default_dict_key_extractor
from ._basic import extend_list, list_to_dict_primitives, seperate_list


DifferenceType = Literal["TYPE", "MISSING", "NOT_EQUAL"]
DifferenceGenerator = Generator["Difference", None, None]
TypeComparer = Callable[
    ["Comparer", any, any, list[str]],
    Generator["Difference", None, None]
]


class Difference:

    __slots__ = (
        "key", "type", "pointer", "value_a", "value_b", "references"
    )

    def __init__(
        self,
        key: list[str],
        type: DifferenceType,
        value_a = None,
        value_b = None,
        references: list = None
    ) -> None:
        self.key = key
        self.type = type
        self.value_a = value_a
        self.value_b = value_b
        self.references = references

    @property
    def key_str(self):
        return ".".join(self.key).replace(".[", "[")

    def __repr__(self) -> str:
        rtn = f"{self.type} {self.key_str}"
        if self.type == "MISSING":
            if self.value_a is not None:
                return f"{rtn} IN B: {self.value_a}"
            if self.value_b is not None:
                return f"{rtn} IN A: {self.value_b}"
        if self.value_a or self.value_b:
            return f"{rtn} {self.value_a}!={self.value_b}"
        return rtn

    def __eq__(self, other) -> bool:
        if isinstance(other, str):
            return repr(self) == other
        return (
            type(self) == type(other)
            and repr(self) == repr(other)
        )

    def build_dict(self) -> dict:
        current = {"type": self.type}
        if self.value_a: current["value_a"] = self.value_a
        if self.value_b: current["value_b"] = self.value_b

        for key in reversed(self.key):
            if key.startswith("[") and key.endswith("]"):
                rtn = []
                index = key[1:-1]
                if index.isnumeric():
                    index = int(index)
                    extend_list(rtn, index)
                    rtn[index] = current
                else:
                    key, value = index.split(":")
                    rtn.append({key: value} | (current or {}))
                current = rtn
            else:
                current = {key: current}
        return current
                
def get_index(entry: dict, *index_keys) -> str:
    for index_key in index_keys:
        if index := entry.get(index_key):
            return index

class Comparer:

    def __init__(
        self,
        key_extractors: list[Callable] = None,
        type_comparers: dict[type, TypeComparer] = None,
        ignore_keys: list[list[str]] = None
    ):
        self.key_extractors = key_extractors or [default_dict_key_extractor]
        self.type_comparers = type_comparers or default_type_comparers
        self.ignore_keys = ignore_keys

    def compare(
        self,
        data_a: any,
        data_b: any,
        current_key: list[str] = None,
    ) -> DifferenceGenerator:
        if current_key and self.ignore_keys and current_key in self.ignore_keys:
            return

        if not current_key:
            current_key = []

        type_a = type(data_a)
        type_b = type(data_b)

        if type_a != type_b:
            yield Difference(
                current_key,
                "NOT_EQUAL",
                value_a=data_a,
                value_b=data_b
            )
            return

        if type_comparer := self.type_comparers.get(type_a):
            yield from type_comparer(self, data_a, data_b, current_key)
            return

        if data_a == data_b:
            return

        yield Difference(
            current_key,
            "NOT_EQUAL",
            value_a = data_a,
            value_b = data_b
        )

def dict_compare(
    comparer: Comparer,
    data_a: dict,
    data_b: dict,
    current_key: list[str] = None,
) -> DifferenceGenerator:
    if data_a == data_b:
        return

    keys_a = data_a.keys()
    keys_b = data_b.keys()

    for key in keys_a:
        if not key in keys_b:
            yield Difference(
                current_key + [key],
                "MISSING",
                value_a=data_a[key],
            )

    for key in keys_b:
        if not key in keys_a:
            yield Difference(
                current_key + [key],
                "MISSING",
                value_b=data_b[key],
            )
        else:
            yield from comparer.compare(
                data_a[key], data_b[key], current_key + [key])

def primitive_list_compare(
    list_a: list,
    list_b: list,
    current_key: list[str],
) -> DifferenceGenerator:
    dict_a = list_to_dict_primitives(list_a)
    dict_b = list_to_dict_primitives(list_b)

    for value, indexes_a in dict_a.items():
        indexes_b = dict_b.get(value, [])
        if len(indexes_a) > len(indexes_b):
            for index in indexes_a[len(indexes_b):]:
                yield Difference(
                    current_key + [f"[{index}]"],
                    "MISSING",
                    value_a=value
                )

    for value, indexes_b in dict_b.items():
        indexes_a = dict_a.get(value, [])
        if len(indexes_b) > len(indexes_a):
            for index in indexes_b[len(indexes_a):]:
                yield Difference(
                    current_key + [f"[{index}]"],
                    "MISSING",
                    value_b=value
                )

def list_compare(
    comparer: Comparer,
    data_a: list,
    data_b: list,
    current_key: list[str] = None,
) -> DifferenceGenerator:
    """Compare two lists and yield differences

    :param comparer: the comparer instance
    :type comparer: Comparer
    :param data_a: the first list to compare
    :type data_a: list
    :param data_b: the second list to compare
    :type data_b: list
    :param current_key: the current key path, defaults to None
    :type current_key: list[str], optional
    :return: a generator yielding differences
    :rtype: DifferenceGenerator
    """
    


    if data_a == data_b:
        return
    
    primitves_a, extended_a = seperate_list(data_a, comparer.key_extractors)
    primitves_b, extended_b = seperate_list(data_b, comparer.key_extractors)

    yield from primitive_list_compare(primitves_a, primitves_b, current_key)
    yield from comparer.compare(extended_a, extended_b, current_key)


default_type_comparers = {
    dict: dict_compare,
    list: list_compare,
    tuple: list_compare
}

default_comparer = Comparer()

def compare(data_a: any, data_b: any) -> DifferenceGenerator:
    yield from default_comparer.compare(data_a, data_b)

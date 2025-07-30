import math
import sys
from collections.abc import Callable, Mapping, MutableMapping, MutableSequence, Sequence, Set
from typing import Any, SupportsFloat, SupportsInt, TypeAlias

if sys.version_info < (3, 12):
    from typing_extensions import TypeAliasType
else:
    from typing import TypeAliasType

from iker.common.utils.numutils import is_normal_real

__all__ = [
    "JsonKey",
    "JsonValue",
    "JsonArray",
    "JsonObject",
    "JsonType",
    "JsonKeyCompatible",
    "JsonValueCompatible",
    "JsonArrayCompatible",
    "JsonObjectCompatible",
    "JsonTypeCompatible",
    "NodeAsterisk",
    "Node",
    "NodePath",
    "asterisk",
    "json_get",
    "json_set",
    "json_traverse",
    "json_reformat",
    "json_sanitize",
    "json_compare",
]

JsonKey = str
JsonValue = str | bool | float | int | None
JsonObject: TypeAlias = TypeAliasType("JsonObject", "dict[JsonKey, JsonType]")
JsonArray: TypeAlias = TypeAliasType("JsonArray", "list[JsonType]")
JsonType: TypeAlias = TypeAliasType("JsonType", "JsonValue | JsonObject | JsonArray")
JsonKeyCompatible = str
JsonValueCompatible = str | bool | SupportsFloat | SupportsInt | None
JsonObjectCompatible: TypeAlias = TypeAliasType("JsonObjectCompatible",
                                                "Mapping[JsonKeyCompatible, JsonTypeCompatible]")
JsonArrayCompatible: TypeAlias = TypeAliasType("JsonArrayCompatible",
                                               "Sequence[JsonTypeCompatible]")
JsonTypeCompatible: TypeAlias = TypeAliasType("JsonTypeCompatible",
                                              "JsonValueCompatible | JsonObjectCompatible | JsonArrayCompatible")


class NodeAsterisk(object):
    pass


Node = str | int | NodeAsterisk
NodePath: TypeAlias = TypeAliasType("NodePath", "list[Node]")

asterisk = NodeAsterisk()


def json_get(
    obj: JsonTypeCompatible,
    *nodes: Node,
    fallback: JsonTypeCompatible | None = None,
) -> JsonTypeCompatible | None:
    """
    Retrieves a value from a nested JSON-like structure by traversing the specified node path. Returns the fallback
    value if the path does not exist.

    :param obj: The JSON-compatible object to traverse.
    :param nodes: The path of nodes (keys or indices) to traverse.
    :param fallback: The value to return if the path does not exist.
    :return: The value at the specified path, or the ``fallback`` if not found.
    """
    if obj is None or isinstance(obj, (JsonValue | JsonValueCompatible)):
        if len(nodes) == 0:
            return obj
        return fallback

    if isinstance(obj, Mapping):
        if len(nodes) == 0:
            return obj
        head, *rest = nodes
        if not isinstance(head, str):
            return fallback
        return json_get(obj[head], *rest) if head in obj else fallback

    if isinstance(obj, Sequence):
        if len(nodes) == 0:
            return obj
        head, *rest = nodes
        if not isinstance(head, int):
            return fallback
        return json_get(obj[head], *rest) if -len(obj) <= head < len(obj) else fallback

    raise ValueError(f"unregistered type '{type(obj)}' encountered")


def json_set(obj: JsonTypeCompatible, value: JsonTypeCompatible, *nodes: Node) -> bool:
    """
    Sets a value in a nested JSON-like structure at the specified node path, creating intermediate structures as needed.

    :param obj: The JSON-compatible object to modify.
    :param value: The value to set at the specified path.
    :param nodes: The path of nodes (keys or indices) where the value should be set.
    :return: ``True`` if the value was set successfully, ``False`` otherwise.
    """
    if len(nodes) == 0:
        return False

    if isinstance(obj, Mapping):
        if not isinstance(obj, MutableMapping):
            raise ValueError(f"immutable mapping type '{type(obj)}' encountered")

        head, *rest = nodes
        if not isinstance(head, str):
            return False
        if head not in obj:
            obj[head] = None

        if len(rest) == 0:
            obj[head] = value
            return True
        rest_head, *rest_rest = rest
        if isinstance(rest_head, int) or isinstance(rest_head, NodeAsterisk):
            if not isinstance(obj[head], MutableSequence):
                obj[head] = []
            return json_set(obj[head], value, *rest)
        if isinstance(rest_head, str):
            if not isinstance(obj[head], MutableMapping):
                obj[head] = {}
            return json_set(obj[head], value, *rest)

    if isinstance(obj, Sequence):
        if not isinstance(obj, MutableSequence):
            raise ValueError(f"immutable sequence type '{type(obj)}' encountered")

        head, *rest = nodes
        if not isinstance(head, int) and not isinstance(head, NodeAsterisk):
            return False
        if isinstance(head, NodeAsterisk):
            head = len(obj)
        while not -len(obj) <= head < len(obj):
            if head < 0:
                obj.reverse()
            obj.append(None)
            if head < 0:
                obj.reverse()

        if len(rest) == 0:
            obj[head] = value
            return True
        rest_head, *rest_rest = rest
        if isinstance(rest_head, int) or isinstance(rest_head, NodeAsterisk):
            if not isinstance(obj[head], MutableSequence):
                obj[head] = []
            return json_set(obj[head], value, *rest)
        if isinstance(rest_head, str):
            if not isinstance(obj[head], MutableMapping):
                obj[head] = {}
            return json_set(obj[head], value, *rest)

    return False


def default_key_visitor(node_path: NodePath, key: JsonKeyCompatible) -> JsonKey:
    """
    Default visitor function for formatting JSON object keys during traversal.

    :param node_path: The path to the current node.
    :param key: The key to format.
    :return: The formatted key as a string.
    """
    return str(key)


def default_value_visitor(node_path: NodePath, value: JsonValueCompatible) -> JsonValue:
    """
    Default visitor function for formatting JSON values during traversal.

    :param node_path: The path to the current node.
    :param value: The value to format.
    :return: The formatted value.
    """
    if value is None or isinstance(value, JsonValue):
        return value
    if isinstance(value, SupportsFloat):
        return float(value)
    if isinstance(value, SupportsInt):
        return int(value)
    raise ValueError(f"unsupported type '{type(value)}' encountered")


def default_object_visitor(node_path: NodePath, old_object: JsonObjectCompatible, new_object: JsonObject) -> JsonType:
    """
    Default visitor function for formatting JSON objects during traversal.

    :param node_path: The path to the current node.
    :param old_object: The original object being traversed.
    :param new_object: The new object being constructed.
    :return: The formatted object.
    """
    return new_object


def default_array_visitor(node_path: NodePath, old_array: JsonArrayCompatible, new_array: JsonArray) -> JsonType:
    """
    Default visitor function for formatting JSON arrays during traversal.

    :param node_path: The path to the current node.
    :param old_array: The original array being traversed.
    :param new_array: The new array being constructed.
    :return: The formatted array.
    """
    return new_array


def json_traverse(
    obj: Any,
    key_visitor: Callable[[NodePath, JsonKeyCompatible], JsonKey] = default_key_visitor,
    value_visitor: Callable[[NodePath, JsonValueCompatible], JsonType] = default_value_visitor,
    object_visitor: Callable[[NodePath, JsonObjectCompatible, JsonObject], JsonType] = default_object_visitor,
    array_visitor: Callable[[NodePath, JsonArrayCompatible, JsonArray], JsonType] = default_array_visitor,
    stop_func: Callable[[NodePath], bool] = lambda x: False,
    *,
    raise_if_unregistered: bool = True,
    unregistered_visitor: Callable[[NodePath, Any], JsonType] | None = None,
) -> JsonType:
    """
    Recursively traverses a JSON-like structure, applying visitor functions to keys, values, objects, and arrays. Allows
    custom handling for unregistered types and stopping traversal at specific paths.

    :param obj: The JSON-compatible object to traverse.
    :param key_visitor: Function to format or process keys during traversal.
    :param value_visitor: Function to format or process values during traversal.
    :param object_visitor: Function to process objects during traversal.
    :param array_visitor: Function to process arrays during traversal.
    :param stop_func: Function to determine whether to stop traversal at a given node path.
    :param raise_if_unregistered: Whether to raise an error for unregistered types.
    :param unregistered_visitor: Function to handle unregistered types if not raising an error.
    :return: The traversed and possibly transformed JSON structure.
    """

    def func(obj: Any, node_path: NodePath):
        if stop_func(node_path):
            return None
        if obj is None or isinstance(obj, (JsonValue | JsonValueCompatible)):
            return value_visitor(node_path, obj)
        if isinstance(obj, Mapping):
            return object_visitor(
                node_path,
                obj,
                {key_visitor(node_path, key): func(value, node_path + [key]) for key, value in obj.items()},
            )
        if isinstance(obj, Sequence):
            return array_visitor(
                node_path,
                obj,
                [func(item, node_path + [index]) for index, item in enumerate(obj)],
            )
        if raise_if_unregistered or unregistered_visitor is None:
            raise ValueError(f"unregistered type '{type(obj)}' encountered")
        return unregistered_visitor(node_path, obj)

    return func(obj, [])


def default_key_formatter(key: JsonKeyCompatible) -> JsonKey:
    """
    Default formatter for JSON object keys.

    :param key: The key to format.
    :return: The formatted key as a string.
    """
    return str(key)


def default_value_formatter(value: JsonValueCompatible) -> JsonValue:
    """
    Default formatter for JSON values.

    :param value: The value to format.
    :return: The formatted value.
    """
    if value is None or isinstance(value, JsonValue):
        return value
    if isinstance(value, SupportsFloat):
        return float(value)
    if isinstance(value, SupportsInt):
        return int(value)
    raise ValueError(f"unsupported type '{type(value)}' encountered")


def json_reformat(
    obj: Any,
    key_formatter: Callable[[JsonKeyCompatible], JsonKey] = default_key_formatter,
    value_formatter: Callable[[JsonValueCompatible], JsonType] = default_value_formatter,
    *,
    raise_if_unregistered: bool = True,
    unregistered_formatter: Callable[[Any], JsonType] | None = None,
) -> JsonType:
    """
    Reformats a JSON-like structure by applying custom formatters to keys and values. Handles unregistered types if
    specified.

    :param obj: The JSON-compatible object to reformat.
    :param key_formatter: Function to format keys.
    :param value_formatter: Function to format values.
    :param raise_if_unregistered: Whether to raise an error for unregistered types.
    :param unregistered_formatter: Function to handle unregistered types if not raising an error.
    :return: The reformatted JSON structure.
    """

    def key_visitor(node_path: NodePath, key: JsonKeyCompatible) -> JsonKey:
        return key_formatter(key)

    def value_visitor(node_path: NodePath, value: JsonValueCompatible) -> JsonType:
        return value_formatter(value)

    def unregistered_visitor(node_path: NodePath, obj: Any) -> JsonType:
        return unregistered_formatter(obj) if unregistered_formatter is not None else None

    return json_traverse(obj,
                         key_visitor=key_visitor,
                         value_visitor=value_visitor,
                         raise_if_unregistered=raise_if_unregistered,
                         unregistered_visitor=unregistered_visitor)


def json_sanitize(obj: Any, *, str_inf_nan: bool = True, str_unregistered: bool = True) -> JsonType:
    """
    Sanitizes a JSON-like structure by converting non-normal floats and unregistered types to strings or ``None``, as
    specified.

    :param obj: The JSON-compatible object to sanitize.
    :param str_inf_nan: Whether to convert inf/nan floats to strings.
    :param str_unregistered: Whether to convert unregistered types to strings.
    :return: The sanitized JSON structure.
    """

    def value_formatter(value: JsonValue) -> JsonValue:
        if isinstance(value, float) and not is_normal_real(value):
            return str(value) if str_inf_nan else None
        return default_value_formatter(value)

    def unregistered_formatter(unregistered: Any) -> JsonType:
        if isinstance(unregistered, Set):
            return [json_sanitize(item, str_inf_nan=str_inf_nan, str_unregistered=str_unregistered)
                    for item in unregistered]
        return str(unregistered) if str_unregistered else None

    return json_reformat(obj,
                         value_formatter=value_formatter,
                         raise_if_unregistered=False,
                         unregistered_formatter=unregistered_formatter)


def json_compare(
    a: JsonTypeCompatible,
    b: JsonTypeCompatible,
    *,
    int_strict: bool = False,
    float_tol: float = 1e-5,
    list_order: bool = True,
    dict_extra: bool = False,
) -> bool:
    """
    Compares two JSON-like structures for equality, with options for integer strictness, float tolerance, list order,
    and dictionary key matching.

    :param a: The first JSON-compatible object to compare.
    :param b: The second JSON-compatible object to compare.
    :param int_strict: Whether to require strict integer type matching.
    :param float_tol: The tolerance for comparing float values.
    :param list_order: Whether to require list order to match.
    :param dict_extra: Whether to allow extra keys in dictionaries.
    :return: ``True`` if the structures are considered equal, ``False`` otherwise.
    """
    if a is None or b is None:
        return a is None and b is None

    if isinstance(a, (str, bool)):
        if type(a) != type(b):
            return False
        return a == b

    if isinstance(a, (SupportsFloat, SupportsInt)) and isinstance(b, (SupportsFloat, SupportsInt)):
        isint_a = isinstance(a, int) or not isinstance(a, SupportsFloat)
        isint_b = isinstance(b, int) or not isinstance(b, SupportsFloat)
        if isint_a and isint_b:
            return int(a) == int(b)
        if int_strict and (isint_a or isint_b):
            return False
        va = int(a) if isint_a else float(a)
        vb = int(b) if isint_b else float(b)
        if math.isnan(va) and math.isnan(vb):
            return True
        if math.isinf(va) and math.isinf(vb):
            return va == vb
        return abs(va - vb) <= float_tol

    if isinstance(a, Mapping) and isinstance(b, Mapping):
        if not dict_extra and set(a.keys()) != set(b.keys()):
            return False
        return all(json_compare(a[k],
                                b[k],
                                int_strict=int_strict,
                                float_tol=float_tol,
                                list_order=list_order,
                                dict_extra=dict_extra)
                   for k in set(a.keys()) & set(b.keys()))

    if isinstance(a, Sequence) and isinstance(b, Sequence):
        if len(a) != len(b):
            return False
        if list_order:
            return all(json_compare(va,
                                    vb,
                                    int_strict=int_strict,
                                    float_tol=float_tol,
                                    list_order=list_order,
                                    dict_extra=dict_extra)
                       for va, vb in zip(a, b))
        else:
            return all(json_compare(va,
                                    vb,
                                    int_strict=int_strict,
                                    float_tol=float_tol,
                                    list_order=list_order,
                                    dict_extra=dict_extra)
                       for va, vb in zip(sorted(a), sorted(b)))

    raise ValueError(f"incompatible type '{type(a)}' and '{type(b)}'")

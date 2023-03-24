from types import MappingProxyType
from collections import OrderedDict
from array import array
from frozendict import frozendict


def isIterableNotString(o):
    from collections import abc
    
    return (
        isinstance(o, abc.Iterable) and 
        not isinstance(o, memoryview) and 
        not hasattr(o, "isalpha")
    )


def getItems(o):
    from collections import abc
    
    if not isinstance(o, abc.Iterable):
        raise TypeError("object must be an iterable")
    
    if isinstance(o, abc.Mapping):
        return dict.items
    
    return enumerate


_deepfreeze_conversion_map = frozendict({
    dict: frozendict, 
    OrderedDict: frozendict, 
    list: tuple, 
    array: tuple, 
    set: frozenset, 
    bytearray: bytes, 
})

_deepfreeze_conversion_map_custom = {}


def getDeepfreezeConversionMap():
    return _deepfreeze_conversion_map | _deepfreeze_conversion_map_custom


_deepfreeze_conversion_inverse_map = frozendict({
    frozendict: dict, 
    MappingProxyType: dict, 
    tuple: list, 
})

_deepfreeze_conversion_inverse_map_custom = {}


def getDeepfreezeConversionInverseMap():
    return _deepfreeze_conversion_inverse_map | _deepfreeze_conversion_inverse_map_custom


_deepfreeze_unhashable_types = (MappingProxyType, )
_deepfreeze_unhashable_types_custom = []


def getDeepfreezeUnhashableTypes():
    return _deepfreeze_unhashable_types + _deepfreeze_unhashable_types_custom


_deepfreeze_types = (
    frozenset({x for x in _deepfreeze_conversion_map if isinstance(x, type)}) |
    {x for x in _deepfreeze_conversion_inverse_map if isinstance(x, type)}
)


def getDeepfreezeTypes():
    return (
        _deepfreeze_types | 
        {x for x in _deepfreeze_conversion_map_custom if isinstance(x, type)} | 
        {x for x in _deepfreeze_conversion_inverse_map_custom if isinstance(x, type)}
    )

_deepfreeze_types_plain = (set, bytearray, array)


def deepfreeze(o):
    try:
        hash(o)
        return o
    except TypeError:
        pass
    
    type_o = type(o)
    
    deepfreeze_types = getDeepfreezeTypes()
    
    if type_o not in deepfreeze_types:
        supported_types = ", ".join((x.__name__ for x in deepfreeze_types))
        err = f"type {type_o} is not hashable or is not one of the supported types: {supported_types}"
        raise TypeError(err)
    
    deepfreeze_conversion_map = getDeepfreezeConversionMap()
    
    if type_o in _deepfreeze_types_plain:
        return deepfreeze_conversion_map[type_o](o)
    
    if not isIterableNotString(o):
        return deepfreeze_conversion_map[type_o](o)
    
    deepfreeze_conversion_inverse_map = getDeepfreezeConversionInverseMap()
    
    frozen_type = type_o in deepfreeze_conversion_inverse_map
    
    if frozen_type:
        o = deepfreeze_conversion_inverse_map[type_o](o)
    
    from copy import copy
    
    o_copy = copy(o)
    
    for k, v in getItems(o)(o_copy):
        o[k] = deepfreeze(v)
    
    if frozen_type and not type_o in getDeepfreezeUnhashableTypes():
        return type_o(o)
    
    return deepfreeze_conversion_map[type(o)](o)


__all__ = (deepfreeze.__name__, )

del MappingProxyType
del OrderedDict
del array
del frozendict

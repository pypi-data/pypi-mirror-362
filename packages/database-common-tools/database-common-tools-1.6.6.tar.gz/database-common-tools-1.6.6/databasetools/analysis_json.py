# -*- coding: utf-8 -*-

import jsonpath
import json


##################################################
# functions field resolution
##################################################

def dump_doc_field_array(doc, path, value):
    values = jsonpath.jsonpath(doc, path)
    status = False
    if isinstance(values, list):
        _values = set()
        for _value in values:
            if isinstance(_value, int) or \
                    isinstance(_value, str) or \
                    isinstance(_value, dict):
                _values.add(str(_value))
        status = True if 0 < len(_values) else False
        return status, json.dumps(list(_values), ensure_ascii=False)
    return status, value


def dump_doc_field_value_max(doc, path, value):
    values = jsonpath.jsonpath(doc, path)
    if isinstance(values, list):
        _max = 0
        for _value in values:
            if isinstance(_value, float) or \
                    isinstance(_value, int):
                _max = _value if _max < _value else _max
        return str(_max)
    return value


def dump_doc_field_str(doc, path, value):
    values = jsonpath.jsonpath(doc, path)
    status = False
    if isinstance(values, list) and 1 == len(values):
        if isinstance(values[0], float) or \
                isinstance(values[0], int) or \
                isinstance(values[0], str):
            status = True if 0 < len(values) else False
            return status, str(values[0])
    return status, value


# object_to_list
def dump_doc_field_object_to_list(doc, path, value, key):
    values = jsonpath.jsonpath(doc, path)
    status = False
    if isinstance(values, list):
        if isinstance(values[0], dict):
            _values = list()
            for _key, doc in values[0].items():
                doc[key] = _key
                _values.append(doc)
        status = True if 0 < len(_values) else False
        return status, json.dumps(list(_values), ensure_ascii=False)
    return status, value

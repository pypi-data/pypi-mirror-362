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
        values = json.dumps(list(values), ensure_ascii=False)
        status = True
        return status, values
    return status, value


def dump_doc_field_object(doc, path, value):
    values = jsonpath.jsonpath(doc, path)
    status = False
    if isinstance(values, list):
        values = values[0]
        if isinstance(values, dict):
            status = True
            return status, values
    return status, value


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


def dump_doc_field_type(doc, path, value, toType):
    values = jsonpath.jsonpath(doc, path)
    status = False
    if isinstance(values, list) and 1 == len(values):
        if isinstance(values[0], float) or \
                isinstance(values[0], int) or \
                isinstance(values[0], str):
            status = True if 0 < len(values) else False
            return status, toType(values[0])
    return status, value


def dump_doc_field_type2array(doc, path, value,toType):
    values = jsonpath.jsonpath(doc, path)
    status = False
    if isinstance(values, list) and 1 == len(values):
        if isinstance(values[0], float) or \
                isinstance(values[0], int) or \
                isinstance(values[0], str):
            array = [toType(x) for x in values[0].split(',')]
            status = True if 0 < len(values) else False
            return status, array
    return status, value

# -*- coding: utf-8 -*-

import databasetools.analysis_json_v3 as analysis_json_v3

##################################################
# fld config
##################################################
FLD = dict()
FLD['names'] = list()
FLD['names'].append('necessity')    # 0
FLD['names'].append('path')         # 1
FLD['names'].append('type')         # 2
FLD['names'].append('default')      # 3
FLD['names'].append('toType')       # 4
FLD['names'].append('true_values')  # 5

FLD['types'] = list()
FLD['types'].append('string')         # 0
FLD['types'].append('array')          # 1
FLD['types'].append('object')         # 2
FLD['types'].append('type2array')     # 3
FLD['types'].append('toType')         # 4
FLD['types'].append('bool')           # 5

FLD['value'] = list()
FLD['value'].append('')      # 0
FLD['value'].append(list())  # 1
FLD['value'].append(dict())  # 2
FLD['value'].append(False)   # 3

FLD['data_type'] = list()
FLD['data_type'].append(int)         # 0
FLD['data_type'].append(float)       # 1
FLD['data_type'].append(str)         # 2
FLD['data_type'].append(list)        # 3
FLD['data_type'].append(bool)        # 4


##################################################
# common function
##################################################
def getDataType(_type):
    if isinstance(_type, str):
        if _type == 'int':
            return FLD['data_type'][0]
        if _type == 'float':
            return FLD['data_type'][1]
        if _type == 'str':
            return FLD['data_type'][2]
        if _type == 'list':
            return FLD['data_type'][3]
        if _type == 'bool':
            return FLD['data_type'][4]
        

##################################################
# src to dest doc analysis
##################################################
# mapConfigFlag mapping配置标志 false 错误
# fieldError 数据传输错误，缺少必要字段  true 错误
def doc_fields_analysis(srcDoc, destDoc, _mapping):
    mapConfigFlag = False
    errorKeys = list()
    fieldError = False
    for _field, _map in _mapping.items():
        mapConfigFlag = True
        keyError = False
        necessity = _map.get(FLD['names'][0], False)
        if isinstance(_map, dict):
            path = _map.get(FLD['names'][1], None)
            _type = _map.get(FLD['names'][2], FLD['types'][0])
            _toType = _map.get(FLD['names'][4], FLD['data_type'][2])
            _toType = getDataType(_toType)
            true_values = _map.get(FLD['names'][5], None)
            if path:
                if FLD['types'][0] == _type:
                    # init string
                    default_value = _map.get(FLD['names'][3], FLD['value'][0])
                    status, fieldValue = analysis_json_v3.dump_doc_field_str(srcDoc, path, default_value)
                    destDoc[_field] = fieldValue
                    if not status:
                        keyError = True
                elif FLD['types'][1] == _type:
                    # init field array
                    default_value = _map.get(FLD['names'][3], FLD['value'][1])
                    status, fieldValue = analysis_json_v3.dump_doc_field_array(srcDoc, path, default_value)
                    destDoc[_field] = fieldValue
                    if not status:
                        keyError = True
                elif FLD['types'][2] == _type:
                    # init field object
                    default_value = _map.get(FLD['names'][3], FLD['value'][2])
                    status, fieldValue = analysis_json_v3.dump_doc_field_object(srcDoc, path, default_value)
                    destDoc[_field] = fieldValue
                    if not status:
                        keyError = True
                elif FLD['types'][3] == _type:
                    # init field type2array
                    default_value = _map.get(FLD['names'][3], FLD['value'][1])
                    status, fieldValue = analysis_json_v3.dump_doc_field_type2array(srcDoc, path, default_value, _toType)
                    destDoc[_field] = fieldValue
                    if not status:
                        keyError = True
                elif FLD['types'][4] == _type:
                    # init field toType
                    default_value = _map.get(FLD['names'][3], FLD['value'][0])
                    status, fieldValue = analysis_json_v3.dump_doc_field_type(srcDoc, path, default_value, _toType)
                    destDoc[_field] = fieldValue
                    if not status:
                        keyError = True
                elif FLD['types'][5] == _type:
                    # init field bool
                    default_value = _map.get(FLD['names'][3], FLD['value'][3])
                    status, fieldValue = analysis_json_v3.dump_doc_field_bool(srcDoc, path, default_value, true_values)
                    destDoc[_field] = fieldValue
                    if not status:
                        keyError = True
            else:
                mapConfigFlag = False
        if not necessity and keyError:
            errorKeys.append(_field)
        if necessity and keyError:
            fieldError = keyError
            break
    return mapConfigFlag, fieldError, errorKeys, destDoc

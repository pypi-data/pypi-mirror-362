# -*- coding: utf-8 -*-

import analysis_json

##################################################
# fld config
##################################################
FLD = dict()
FLD['names'] = list()
FLD['names'].append('necessity')  # 0
FLD['names'].append('path')  # 1
FLD['names'].append('type')  # 2
FLD['names'].append('default')  # 3
FLD['names'].append('func')  # 4
FLD['names'].append('key')  # 5
FLD['names'].append('filter')  # 6

FLD['types'] = list()
FLD['types'].append('string')  # 0
FLD['types'].append('array')  # 1
FLD['types'].append('object')  # 2

FLD['value'] = list()
FLD['value'].append('')  # 0

FLD['funcs'] = list()
FLD['funcs'].append('object_to_list')  # 0


##################################################
# src to dest doc analysis
##################################################
# mapConfigFlag mapping配置标志 false 错误
# fieldError 数据传输错误，缺少必要字段  true 错误
def doc_fields_analysis(srcDoc, destDoc, _mapping):
    errorKeys = list()
    fieldError = False
    fieldFilter = False
    for _field, _map in _mapping.items():
        mapConfigFlag = True
        keyError = False
        necessity = _map.get(FLD['names'][0], False)
        if isinstance(_map, dict):
            path = _map.get(FLD['names'][1], None)
            _type = _map.get(FLD['names'][2], FLD['types'][0])
            default_value = _map.get(FLD['names'][3], FLD['value'][0])
            func = _map.get(FLD['names'][4], FLD['value'][0])
            key = _map.get(FLD['names'][5], FLD['value'][0])
            _filter = _map.get(FLD['names'][6], FLD['value'][0])
            if path:
                if FLD['types'][0] == _type:
                    # init string
                    status, fieldValue = analysis_json.dump_doc_field_str(srcDoc, path, default_value)
                    destDoc[_field] = fieldValue
                    if _filter:
                        if fieldValue not in _filter:
                            fieldFilter = True
                            break
                    if not status:
                        keyError = True
                elif FLD['types'][1] == _type:
                    # init field array
                    status, fieldValue = analysis_json.dump_doc_field_array(srcDoc, path, default_value)
                    destDoc[_field] = fieldValue
                    if not status:
                        keyError = True
                elif FLD['types'][2] == _type:
                    if FLD['funcs'][0] == func:
                        # init field array
                        status, fieldValue = analysis_json.dump_doc_field_object_to_list(srcDoc, path, default_value,
                                                                                         key)
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
    return mapConfigFlag, fieldError, errorKeys, fieldFilter, destDoc

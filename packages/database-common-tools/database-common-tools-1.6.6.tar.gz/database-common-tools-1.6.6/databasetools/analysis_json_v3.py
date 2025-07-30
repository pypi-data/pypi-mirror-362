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
        status = True if 0 < len(values) else False
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
        if isinstance(values[0], (float,int,str,dict,list,bool)):
            status = True if 0 < len(values) else False
            return status, str(values[0])
    return status, value


def dump_doc_field_type(doc, path, value, toType):
    values = jsonpath.jsonpath(doc, path)
    status = False
    if isinstance(values, list) and 1 == len(values):
        if isinstance(values[0], (float,int,str,dict,list,bool)):
            status = True if 0 < len(values) else False
            try:
                return status, toType(values[0])
            except Exception as e:
                return status, value
    return status, value

# 针对是一行的数据 转换为数组存储情况
def dump_doc_field_type2array(doc, path, value,toType):
    values = jsonpath.jsonpath(doc, path)
    status = False
    if isinstance(values, list) and 1 == len(values):
        if isinstance(values[0], (float,int,str,dict,list,bool)):
            array = [toType(x) for x in values[0].split(',') if x.strip()]
            status = True if 0 < len(values) else False
            return status, array
    return status, value

def dump_doc_field_bool(doc, path, default, true_values=None):
    """
    提取文档中指定路径的布尔字段值，并根据设定判断非布尔类型的字段。

    :param doc: 文档对象（字典格式）。
    :param path: 字段路径，支持 JSONPath 表达式。
    :param default: 如果字段不存在时的默认值。
    :param true_values: 定义哪些值视为 True 的列表（可选）。其余值视为 False。
    :return: (status, value) 元组。
             status: True 表示成功提取字段值并进行了判断，False 表示字段不存在。
             value: 提取的布尔值或默认值。
    """
    # 默认将 ["true", "1", "yes"] 视为 True 的值
    if true_values is None:
        true_values = [True, "true", "1", "yes", 1]

    values = jsonpath.jsonpath(doc, path)
    if isinstance(values, list) and len(values) == 1:
        field_value = values[0]
        # 判断字段是否在 true_values 中
        is_true = field_value in true_values
        return True, is_true
    return False, default




if __name__ == '__main__':
    doc = {
		"id" : "hi2234586312",
        "__delete": True,
		"aspect" : "0.67",
		"width" : 3840,
		"height" : 5760,
		"image_type" : "photo",
		"race" : [],
		"person_num" : 1,
		"age" : ["20s"],
		"gender" : "female",
		"category_ids" : "",
		"preview260_url" : "provider_image/preview260/2234586312.jpg",
		"id" : 949735,
		"real_name" : "赵旭"
	}
    # print(dump_doc_field_type2array(doc,'$.category_ids',[],int))
    # print(jsonpath.jsonpath(doc, '$.category_ids'))
    print(dump_doc_field_type(doc, '$.__delete', False))

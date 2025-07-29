
import json
from secmind.rpa_v2.entity.exception_enum import exception_map

def exception_to_json(exception, local_map):
    """
    将异常信息转换为JSON格式字符串。

    该函数接收一个异常对象作为输入，将其转换为预定义格式的JSON字符串。
    JSON字符串包含异常的英文和中文错误信息，以及一个表示是否进行了翻译的标志。

    参数:
    exception: 异常对象，可以是任何内置或自定义异常。
    local_map：

    返回值:
    返回一个JSON格式的字符串，包含异常信息和翻译标志。
    """
    # local_map优先级高会覆盖掉默认的exception_map
    merge_exception_map = exception_map.copy()
    merge_exception_map.update(local_map)
    # 将异常对象转换为字符串形式
    if isinstance(exception, Exception):
        str_exception = str(exception)
    else:
        str_exception = exception
    en_msg = str_exception
    ch_msg = str_exception
    is_translate = False
    # 使用模糊匹配遍历异常是否在映射中
    for key, value in merge_exception_map.items():
        if key in str_exception:
            en_msg = value["en"]
            ch_msg = value["ch"]
            is_translate = True
            break
    # 构建字典，然后使用json模块转换为JSON字符串
    result_dict = {
        "enErrorMessage": en_msg,
        "chErrorMessage": ch_msg,
        "isTranslate": is_translate
    }
    json_output = json.dumps(result_dict, indent=4, ensure_ascii=False)
    return json_output

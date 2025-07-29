import base64
import getopt
import json
import sys
import traceback

from secmind.rpa_v2.entity.task_execution_result import TaskExecutionResult
from secmind.rpa_v2.utils.log import LogWrapper
from secmind.rpa_v2.entity.exception_enum import exception_map

logger = LogWrapper().get_logger()


def base64_to_string(base64_string):
    # 解码base64字符串
    bytes_data = base64.b64decode(base64_string)
    # 将字节转换为字符串
    return bytes_data.decode('utf-8')


def string_to_base64(input_string):
    # 将字符串转换为字节
    string_bytes = input_string.encode('utf-8')

    # 使用base64进行编码
    base64_bytes = base64.b64encode(string_bytes)

    # 将base64字节转换回字符串
    base64_string = base64_bytes.decode('utf-8')

    return base64_string


# def get_data_map():
#     stack = inspect.stack()
#     caller_frame = stack[1].frame
#     return caller_frame.f_globals

def get_data_map():
    args = sys.argv
    if len(args) < 2:
        task_execution_result = TaskExecutionResult()
        task_execution_result.msg = "启动参数丢失"
        raise ValueError("启动参数丢失")
    try:
        argv = args[1:]
        params_base64 = ""
        opts, args = getopt.getopt(argv, "d:")
        for opt, arg in opts:
            if opt in ['-d']:
                params_base64 = arg

        decoded_string = base64_to_string(params_base64)
        return json.loads(decoded_string)
    except Exception as e:
        raise e


def go(func):
    task_execution_result = TaskExecutionResult()
    try:
        data_map = get_data_map()
        logger.info("资产IP：%s，用户名：%s", data_map['location'], data_map['user'])
        task_execution_result.data = func(data_map)
        task_execution_result.success = True
    except Exception as e:
        task_execution_result.stack = traceback.format_exc()
        import re
        if check_global_variable("pop_error_msg") and bool(re.search(r'[\u4e00-\u9fff]', pop_error_msg)):
            task_execution_result.msg = pop_error_msg
        else:
            task_execution_result.msg = str(e)
    finally:
        task_execution_result.log = logger.get_log_text_with_close()
        print(json.dumps(task_execution_result.__dict__, ensure_ascii=False))


def custom_exception_handler_class(cls):
    for attr_name, attr_value in cls.__dict__.items():
        if callable(attr_value):
            setattr(cls, attr_name, custom_exception_handler(attr_value))
    return cls


def custom_exception_handler(func):
    def wrapper(*args, **kwargs):
        custom_message = kwargs.pop('error_message', None)
        try:
            return func(*args, **kwargs)
        except Exception as e:
            global pop_error_msg
            if custom_message is None:
                pop_error_msg = repr(e)
            else:
                pop_error_msg = f"{custom_message}"
            raise e

    return wrapper


def check_global_variable(variable_name):
    return variable_name in globals()

# def class_exception_handler(cls):
#     for name, method in cls.__dict__.items():
#         if callable(method):
#             setattr(cls, name, method_exception_handler(method))
#     return cls
#
# def method_exception_handler(method):
#     @functools.wraps(method)
#     def wrapper(self, *args, error_message=None, **kwargs):
#         try:
#             return method(self, *args, **kwargs)
#         except Exception as e:
#             if error_message:
#                 print(f"{method.__name__} 出错: {error_message}")
#             else:
#                 print(f"{method.__name__} 出现未知错误")
#             # raise  e
#     return wrapper


def exception_to_json(exception):
    """
    将异常信息转换为JSON格式字符串。

    该函数接收一个异常对象作为输入，将其转换为预定义格式的JSON字符串。
    JSON字符串包含异常的英文和中文错误信息，以及一个表示是否进行了翻译的标志。

    参数:
    exception: 异常对象，可以是任何内置或自定义异常。

    返回值:
    返回一个JSON格式的字符串，包含异常信息和翻译标志。
    """
    # 将异常对象转换为字符串形式
    if isinstance(exception, Exception):
        str_exception = str(exception)
    else:
        str_exception = exception
    en_msg = str_exception
    ch_msg = str_exception
    is_translate = False
    # 使用模糊匹配遍历异常是否在映射中
    for key, value in exception_map.items():
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

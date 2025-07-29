from secmind.rpa_v2 import WinRMWrapper
from secmind.rpa_v2 import common


def do_task(data_map):
    winrm_wrapper = WinRMWrapper(data_map['location'], data_map['user'], data_map['pwd'])
    try:
        winrm_wrapper.connect()
        # winrm_wrapper.change_password("xxx", "xxx")
        return True
    except Exception as ex:
        common.logger.error(repr(ex))
        raise ex


common.go(do_task)

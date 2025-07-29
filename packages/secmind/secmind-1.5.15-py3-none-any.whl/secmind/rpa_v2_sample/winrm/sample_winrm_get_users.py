from secmind.rpa_v2 import WinRMWrapper
from secmind.rpa_v2 import common


def do_task(data_map):
    winrm_wrapper = WinRMWrapper(data_map['location'], data_map['user'], data_map['pwd'])
    try:
        winrm_wrapper.connect()
        result = winrm_wrapper.execute_command("net user administrator")
        return winrm_wrapper.get_users()
    except Exception as ex:
        common.logger.error(repr(ex))
        raise ex


common.go(do_task)

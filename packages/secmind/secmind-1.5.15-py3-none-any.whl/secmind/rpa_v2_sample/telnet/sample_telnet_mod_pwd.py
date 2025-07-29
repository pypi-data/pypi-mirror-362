from secmind.rpa_v2 import TelnetWrapper
from secmind.rpa_v2 import common


def do_task(data_map):
    telnet_wrapper = TelnetWrapper(data_map['location'], data_map['user'], data_map['pwd'], data_map['port'])
    try:
        telnet_wrapper.connect()
        # telnet_wrapper.change_password_another("xxx", "hahahaha")
        # telnet_wrapper.change_password("1xxx")
        return True
    except Exception as ex:
        common.logger.error(repr(ex))
        raise ex
    finally:
        telnet_wrapper.exit()


common.go(do_task)

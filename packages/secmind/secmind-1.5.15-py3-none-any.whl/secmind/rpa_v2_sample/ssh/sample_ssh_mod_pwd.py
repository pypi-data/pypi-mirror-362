from secmind.rpa_v2 import SSHWrapper
from secmind.rpa_v2 import common


def do_task(data_map):
    ssh_wrapper = SSHWrapper(data_map['location'], data_map['user'], data_map['pwd'], data_map['port'])
    try:
        ssh_wrapper.connect()
        # ssh_wrapper.change_password("xxx")
        # ssh_wrapper.change_password_another("xx","xxx")
        return True
    except Exception as ex:
        common.logger.error(repr(ex))
        raise ex
    finally:
        ssh_wrapper.exit()


common.go(do_task)

from secmind.rpa_v2 import SSHWrapper
from secmind.rpa_v2 import common


def do_task(data_map):
    ssh_wrapper = SSHWrapper(data_map['location'], data_map['user'], data_map['pwd'], data_map['port'])
    try:
        ssh_wrapper.connect()
        return ssh_wrapper.get_users()
    except Exception as ex:
        common.logger.error(repr(ex))
        raise ex
    finally:
        ssh_wrapper.exit()


common.go(do_task)

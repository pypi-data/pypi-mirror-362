from secmind.rpa_v2 import common
from secmind.rpa_v2.samba.samba_wrapper import SambaWrapper


def do_task(data_map):
    samba_wrapper = SambaWrapper(data_map['location'], data_map['user'], data_map['pwd'])
    try:
        samba_wrapper.connect()
        return True
    except Exception as ex:
        common.logger.error(repr(ex))
        raise ex


common.go(do_task)

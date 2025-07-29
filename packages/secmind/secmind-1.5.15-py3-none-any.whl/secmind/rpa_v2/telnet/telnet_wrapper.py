import telnetlib
import time
from typing import Optional, List

from secmind.rpa_v2.utils.common import custom_exception_handler_class
from secmind.rpa_v2.utils.invoke import ChainCommand


# 如需自定义异常提示语，只需要在调用方法参数中添加error_message="xxxxxxx"即可
@custom_exception_handler_class
class TelnetWrapper(ChainCommand):

    def _wait(self):
        time.sleep(self.command_timeout)

    def __init__(self, host, username, password, port=23, timeout=None, command_timeout=1):
        super().__init__()
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.timeout = timeout
        self.telnet: Optional[telnetlib.Telnet] = None
        self.command_timeout = command_timeout

    # 连接
    def connect(self, read_timeout=3, expectations: Optional[List] = None, regex: bool = False):
        if expectations is None:
            expectations = [r'\[(\w+)@(\w+) ~\]']
            regex = True

        self.telnet = telnetlib.Telnet(self.host, self.port, self.timeout)
        self.telnet.read_until(b"login: ", timeout=read_timeout)
        self.telnet.write(self.username.encode('utf-8') + b"\n")
        self.telnet.read_until(b"Password: ", timeout=read_timeout)
        self.telnet.write(self.password.encode('utf-8') + b"\n")
        self._wait()
        response = self.telnet.read_until(b"$", timeout=read_timeout)

        if not self.is_hit_target(response.decode('utf-8'), expectations, regex):
            raise Exception(f"Error: login result: {response}")

    # 修改自己密码
    def change_password(self, new_password, expectations: Optional[List] = None, regex: bool = False):
        try:
            if expectations is None:
                expectations = ["successfully", "成功"]
                regex = False

            self.telnet.write(b"passwd\n")
            self._wait()
            self.telnet.write(self.password.encode('utf-8') + b"\n")
            self._wait()
            self.telnet.write(new_password.encode('utf-8') + b"\n")
            self._wait()
            self.telnet.write(new_password.encode('utf-8') + b"\n")
            self._wait()
            result = self.telnet.read_very_eager().decode('utf-8')
            if not self.is_hit_target(result, expectations, regex):
                raise Exception(f"Error: change_password result: {result}")
        except Exception as ex:
            raise ex

    # 修改指定用户密码
    def change_password_another(self, username, new_password, expectations: Optional[List] = None, regex: bool = False):
        try:
            if expectations is None:
                expectations = ["successfully", "成功"]
                regex = False

            command = f"passwd {username}\n"
            self.telnet.write(command.encode('utf-8'))
            self._wait()
            self.telnet.write(new_password.encode('utf-8') + b"\n")
            self._wait()
            self.telnet.write(new_password.encode('utf-8') + b"\n")
            self._wait()
            result = self.telnet.read_very_eager().decode('utf-8')
            if not self.is_hit_target(result, expectations, regex):
                raise Exception(f"Error: change_password result: {result}")
        except Exception as ex:
            raise ex

    # 账号发现
    def get_users(self):
        try:
            self.telnet.write(b"cat /etc/passwd\n")
            self._wait()
            result = self.telnet.read_very_eager().decode('utf-8')

            users = []
            for line in result.split('\r\n'):
                if ':' in line:
                    parts = line.split(':')
                    user = {
                        "username": parts[0],
                        "password": parts[1],
                        "uid": parts[2],
                        "gid": parts[3],
                        "description": parts[4],
                        "home_directory": parts[5],
                        "shell": parts[6]
                    }
                    users.append(user)
            return users
        except Exception as ex:
            raise ex

    # 执行命令
    def execute_command(self, command, delay=1):
        self.telnet.write(command.encode('utf-8') + b"\n")
        time.sleep(delay)
        return self.telnet.read_very_eager().decode('utf-8')

    # 批量处理命令(将需要执行的多条命令放入数组中)
    def execute_multiple_commands(self, commands, delay=1):
        results = []
        for command in commands:
            result = self.execute_command(command, delay)
            results.append(result)
        return results

    def _flush_channel(self):
        self.telnet.read_very_eager()

    # 开始链式调用
    def start_chain(self, delay=1):
        time.sleep(delay)
        self._flush_channel()
        return self

    # 结束链式调用
    def end_chain(self):
        self.output = ""
        return self

    # 执行链式调用命令
    def execute_command_chain(self, command, delay=1):
        self.telnet.write(command.encode('utf-8') + b"\n")
        time.sleep(delay)
        output = self.telnet.read_very_eager().decode('utf-8')
        self.output = output
        return self

    # 关闭
    def exit(self):
        if self.telnet:
            self.telnet.close()

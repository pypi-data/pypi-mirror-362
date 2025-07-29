import time
from typing import Optional

import paramiko
from paramiko import SSHException
from paramiko.channel import Channel
from paramiko.client import SSHClient

from secmind.rpa_v2.utils.common import custom_exception_handler_class
from secmind.rpa_v2.utils.invoke import ChainCommand


# 如需自定义异常提示语，只需要在调用方法参数中添加error_message="xxxxxxx"即可
@custom_exception_handler_class
class SSHWrapper(ChainCommand):
    def __init__(self, hostname, username, password, port, timeout=None, allow_agent=False, look_for_keys=False):
        super().__init__()
        self.client: Optional[SSHClient] = None
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self.timeout = timeout
        self.allow_agent = allow_agent
        self.look_for_keys = look_for_keys
        self.channel: Optional[Channel] = None

    # 连接
    def connect(self):
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=self.hostname, port=self.port, username=self.username,
                           password=self.password, timeout=self.timeout, allow_agent=self.allow_agent,
                           look_for_keys=self.look_for_keys)
            self.client = client
        except SSHException as e:
            raise e

    # 修改自己密码
    def change_password(self, new_password):
        stdin, stdout, stderr = self.client.exec_command(f'passwd')
        stdin.write(f'{self.password}\n{new_password}\n{new_password}\n')
        stdin.flush()
        if stderr.channel.recv_exit_status() != 0:
            raise Exception(stderr.read().decode())

    # 修改指定用户密码
    def change_password_another(self, username, new_password):
        stdin, stdout, stderr = self.client.exec_command(f'passwd {username}')
        stdin.write(f'{new_password}\n{new_password}\n')
        stdin.flush()
        if stderr.channel.recv_exit_status() != 0:
            raise Exception(stderr.read().decode())

    # 账号发现
    def get_users(self):
        try:
            stdin, stdout, stderr = self.client.exec_command("cat /etc/passwd")
            user_lines = stdout.read().decode().splitlines()
            error = stderr.read().decode()
            if error:
                raise Exception(f"Error retrieving user details: {error}")
            users = []
            for line in user_lines:
                parts = line.split(":")
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
    def execute_command(self, command):
        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            output = stdout.read().decode('utf-8')
            error = stderr.read().decode('utf-8')
            return output, error
        except Exception as e:
            raise e

    # 批量处理命令(将需要执行的多条命令放入数组中)
    def execute_multi_step_command(self, commands, delay=1, byte_len=4096):
        try:
            shell = self.client.invoke_shell()
            time.sleep(delay)
            self._flush_channel(shell)
            output = []

            for command in commands:
                shell.send(command + "\n")
                time.sleep(delay)
                temp_output = ""
                while shell.recv_ready():
                    temp_output += shell.recv(byte_len).decode('utf-8')

                output.append(temp_output)

            shell.close()
            return output
        except Exception as e:
            raise e

    # 批量处理命令(执行前一个命令，会对结果进行确认，再进行一下条命令)
    def execute_interactive_command(self, command, prompts_and_next_commands, delay=1, byte_len=4096):
        try:
            shell = self.client.invoke_shell()
            time.sleep(delay)
            self._flush_channel(shell)
            output = ""

            shell.send(command + "\n")

            for prompt, next_command in prompts_and_next_commands:
                while prompt not in output:
                    if shell.recv_ready():
                        output += shell.recv(byte_len).decode('utf-8')
                    time.sleep(0.1)

                shell.send(next_command + "\n")
                time.sleep(delay)

            while shell.recv_ready():
                output += shell.recv(byte_len).decode('utf-8')

            shell.close()
            return output
        except Exception as e:
            raise e

    def _flush_channel(self, channel, buffer_size=4096):
        while channel.recv_ready():
            channel.recv(buffer_size)
        while channel.recv_stderr_ready():
            channel.recv_stderr(buffer_size)

    # 开始链式调用
    def start_chain(self, delay=1):
        self.channel = self.client.invoke_shell()
        time.sleep(delay)
        self._flush_channel(self.channel)
        return self

    # 结束链式调用
    def end_chain(self):
        self.channel.close()
        self.output = ""
        return self

    # 执行链式调用命令
    def execute_command_chain(self, command, delay=1, byte_len=4096):
        self.channel.send(command + '\n')
        time.sleep(delay)
        output = ""
        error = ""
        while self.channel.recv_ready():
            output += self.channel.recv(byte_len).decode('utf-8')
        while self.channel.recv_stderr_ready():
            error += self.channel.recv(byte_len).decode('utf-8')
        self.output = output

        if len(error) > 0:
            raise Exception(error)
        return self

    # 关闭
    def exit(self):
        if self.channel:
            self.channel.close()
        if self.client:
            self.client.close()
        # 日志混乱输出
        time.sleep(5)

import subprocess
from typing import List, Dict, Union, Optional

from secmind.rpa_v2.utils.common import custom_exception_handler_class
from secmind.rpa_v2.utils.invoke import ChainCommand


# 如需自定义异常提示语，只需要在调用方法参数中添加error_message="xxxxxxx"即可
@custom_exception_handler_class
class SambaWrapper(ChainCommand):
    def __init__(self, server: str, username: str, password: str, domain: str = ''):
        super().__init__()
        self.session: Optional[subprocess.Popen] = None
        self.server = server
        self.username = username
        self.password = password
        self.domain = domain

    # 连接
    def connect(self):
        result = self._run_rpc_command("quit")

    # 执行命令
    def execute_command(self, command):
        return self._run_rpc_command(command)

    # 批量处理命令(将需要执行的多条命令放入数组中)
    def execute_multiple_commands(self, commands):
        results = []
        for command in commands:
            result = self.execute_command(command)
            results.append(result)
        return results

    def _run_rpc_command(self, command: str) -> Union[str, None]:
        auth_cmd = [
            'rpcclient',
            '-U', f'{self.domain}\\{self.username}',
            self.server,
            '-c', command
        ]
        try:
            result = subprocess.run(auth_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    input=f'{self.password}\n', text=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise Exception(f"Command failed: {e.stderr.strip()}")

    # 修改指定用户密码
    def change_password(self, username: str, new_password: str, expectations: Optional[List] = None,
                        regex: bool = False):
        if expectations is None:
            expectations = ["NT_STATUS"]
            regex = False
        auth_cmd = [
            'rpcclient',
            '-U', f'{self.domain}\\{self.username}',
            self.server,
        ]
        session = subprocess.Popen(auth_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   text=True)
        session.stdin.write(f"{self.password}\n")
        command = f'setuserinfo2 {username} 23 {new_password}'
        session.stdin.write(f"{command}\n")
        session.stdin.flush()

        output, error = session.communicate(timeout=10)
        return_code = session.returncode
        if return_code != 0:
            if error is not None:
                raise Exception(f"return_code != 0 error: {error}")
            raise Exception(f"return_code != 0 output: {output}")

        if self.is_hit_target(output, expectations, regex):
            raise Exception(f"Command failed output: {output}")
        if self.is_hit_target(error, expectations, regex):
            raise Exception(f"Command failed error: {error}")

    def _get_user_list(self) -> List[Dict[str, str]]:
        command = 'enumdomusers'
        result = self._run_rpc_command(command)
        if not result:
            return []

        users = []
        lines = result.splitlines()
        for line in lines:
            if 'user:' in line:
                user_info = self._parse_user_info(line)
                if user_info:
                    users.append(user_info)
        return users

    def _parse_user_info(self, line: str) -> Dict[str, str]:
        user_info = {}
        parts = line.split()
        for part in parts:
            key, value = part.split(':')
            user_info[key.strip()] = value.strip('[]')
        return user_info

    def _get_user_details(self, username: str) -> Dict[str, str]:
        command = f'queryuser {username}'
        result = self._run_rpc_command(command)
        if not result:
            return {}

        user_details = {}
        lines = result.splitlines()
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                user_details[key.strip()] = value.strip()
        return user_details

    # 账号发现
    def get_users(self):
        users = self._get_user_list()
        user_details_list = []
        for user in users:
            user_details = self._get_user_details(user['user'])
            user_details_list.append(user_details)
        return user_details_list

    # 开始链式调用
    def start_chain(self, delay=1):
        return self

    # 结束链式调用
    def end_chain(self):
        self.output = ""
        return self

    # 执行链式调用命令
    def execute_command_chain(self, command):
        self.output = self._run_rpc_command(command)
        return self

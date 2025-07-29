import chardet
import winrm

from secmind.rpa_v2.utils.common import custom_exception_handler_class
from secmind.rpa_v2.utils.invoke import ChainCommand

TRANSPORT_NTLM = "ntlm"
TRANSPORT_BASIC = "basic"
TRANSPORT_CERTIFICATE = "certificate"
TRANSPORT_KERBEROS = "kerberos"
TRANSPORT_CREDSSP = "credssp"
TRANSPORT_PLAINTEXT = "plaintext"
TRANSPORT_SSL = "ssl"


# 如需自定义异常提示语，只需要在调用方法参数中添加error_message="xxxxxxx"即可
@custom_exception_handler_class
class WinRMWrapper(ChainCommand):
    def __init__(self, host, username, password, protocol='http', port=5985, transport=TRANSPORT_NTLM, path='/wsman'):
        super().__init__()
        self.use_powershell = None
        self.session = None
        self.host = host
        self.username = username
        self.password = password
        self.protocol = protocol
        self.port = port
        self.transport = transport
        self.path = path

    # 连接
    def connect(self):
        endpoint = f'{self.protocol}://{self.host}:{self.port}{self.path}'
        self.session = winrm.Session(endpoint, auth=(self.username, self.password), transport=self.transport)
        result = self.session.run_cmd('whoami')
        if result.status_code != 0:
            raise Exception(result.std_err.decode('utf-8'))

    # 修改指定用户密码
    def change_password(self, user, new_password):
        cmd = f'net user {user} {new_password}'
        result = self.session.run_cmd(cmd)
        if result.status_code != 0:
            raise Exception(result.std_err.decode('utf-8'))

    # 账号发现
    def get_users(self):
        cmd = 'wmic useraccount get /all /format:list'
        result = self.session.run_cmd(cmd)
        if result.status_code == 0:
            return self._parse_user_list(result.std_out)
        raise Exception(result.std_err.decode('utf-8'))

    def _parse_user_list(self, output):
        encoding = chardet.detect(output)['encoding']
        decoded_output = output.decode(encoding)
        users = []
        current_user = {}
        for line in decoded_output.split('\n'):
            if line.strip():
                parts = line.split('=', 1)
                if len(parts) == 2:
                    key, value = parts
                    current_user[key.strip().lower()] = value.strip()
            else:
                if current_user:
                    users.append(self._create_user_object(current_user))
                    current_user = {}
        if current_user:
            users.append(self._create_user_object(current_user))
        return users

    def _create_user_object(self, user_dict):
        return user_dict
        # return WindowsUser(
        #     name=user_dict.get('name', ''),
        #     full_name=user_dict.get('fullname'),
        #     description=user_dict.get('description'),
        #     sid=user_dict.get('sid'),
        #     domain=user_dict.get('domain'),
        #     account_type=user_dict.get('accounttype'),
        #     status=user_dict.get('status'),
        #     password_expires=user_dict.get('passwordexpires'),
        #     password_changeable=user_dict.get('passwordchangeable'),
        #     password_required=user_dict.get('passwordrequired'),
        #     password_last_change=user_dict.get('passwordlastchanged'),
        #     last_logon=user_dict.get('lastlogon'),
        #     bad_password_count=int(user_dict.get('badpasswordcount', 0)),
        #     number_of_logons=int(user_dict.get('numberoflogons', 0)),
        #     user_may_change_password=user_dict.get('usermaychangepassword') == 'TRUE',
        #     account_expires=user_dict.get('accountexpires'),
        #     primary_group_id=user_dict.get('primarygroupid'),
        #     profile=user_dict.get('profile'),
        #     home_directory=user_dict.get('homedirectory'),
        #     script_path=user_dict.get('scriptpath')
        # )

    # 执行命令
    def execute_command(self, command):
        result = self.session.run_cmd(command)
        return {
            'status_code': result.status_code,
            'std_out': self.get_decode_data(result.std_out),
            'std_err': self.get_decode_data(result.std_err)
        }

    # 执行命令
    def execute_powershell(self, script):
        result = self.session.run_ps(script)
        return {
            'status_code': result.status_code,
            'std_out': self.get_decode_data(result.std_out),
            'std_err': self.get_decode_data(result.std_err),
        }

    # 批量处理命令(将需要执行的多条命令放入数组中)
    def run_multiple_commands(self, commands, use_powershell=False):
        results = []
        for command in commands:
            if use_powershell:
                result = self.execute_powershell(command)
            else:
                result = self.execute_command(command)
            results.append(result)
        return results

    # 开始链式调用
    def start_chain(self, use_powershell=False):
        self.use_powershell = use_powershell
        return self

    # 结束链式调用
    def end_chain(self):
        self.use_powershell = None
        return self

    # 执行链式调用命令
    def execute_command_chain(self, command):
        if self.use_powershell:
            result = self.execute_powershell(command)
        else:
            result = self.execute_command(command)

        if result['status_code'] == 0:
            self.output = result['std_out']
        else:
            raise Exception(result['std_err'])

        return self

    # 反序列化输出数据
    def get_decode_data(self, data):
        if len(data) == 0:
            std_encoding = 'utf-8'
        else:
            std_encoding = chardet.detect(data)['encoding']

        return data.decode(std_encoding)

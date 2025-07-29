import copy
import json
from datetime import datetime

import pymysql
from secmind.rpa_v2 import common

def do_analysis(data_map, monitor_queue):
    special_user_data_list = data_map['specialUserList']
    global analysis_account_array
    analysis_account_array = data_map.get('analysisAccountList')
    if analysis_account_array is None:
        analysis_account_array = []
    try:
        connect = pymysql.connect(
            host=data_map['location'],
            port=int(data_map['port']),
            db=data_map['database'],
            user=data_map['user'],
            password=data_map['pwd'])
        cursor = connect.cursor()

    except Exception as ex:
        common.logger.error("mysql连接失败，请检查账号密码是否正确且该账号授予远程登录权限" + repr(ex))
        raise ex

    specialList = []
    #特殊账号
    if special_user_data_list == "null":
        special_user_data_list = []
    if special_user_data_list:
        for user_sp in special_user_data_list.split(","):
            specialList.append(user_sp)
    # 配置连接参数
    # config = {
    #     'user': user,        # 使用外部传入的用户名
    #     'password': passwd,  # 使用外部传入的密码
    #     'host': host,        # 使用外部传入的主机地址
    #     'port': int(port),        # MySQL 默认端口
    # }
    return safetyInspection(connect, cursor, specialList)


class HuntMySql:
    def __init__(self):
        super().__init__()
        self.bl0040_1 = True
        self.bl0040_2 = True
        self.bl0041 = True
        self.bl0051 = False

        #统计已经记录的登录日志数量
        self.log_count = 0
        #报表导出自定义字段
        self.isPrivilege = '0'
        self.isPrivilegeExport = '否'
        self.passwordStrategyExport = ''
        self.lastLoginTime = '-'
        self.accountActive = '-'
        self.lastPwdsetTime = None
        self.lastLog = None
        self.loginLog = ''

    def to_dict(self):
        """ 将对象转换为字典 """
        return {
            "userName": self.userName,  # 可能未赋值，需用 getattr 处理
            "bl0040_1": self.bl0040_1,
            "bl0040_2": self.bl0040_2,
            "bl0041": self.bl0041,
            "bl0051": self.bl0051,
            "bl2007": self.bl2007,

            # 报表导出自定义字段
            "isPrivilegeExport": self.isPrivilegeExport,
            "lastLoginTime": self.lastLoginTime,
            "lastPwdsetTime": self.lastPwdsetTime,
            "isWeakStrategy": self.isWeakStrategy,
            "passwordStrategyExport": self.passwordStrategyExport,
            "longUnusedExport": self.longUnusedExport,
            "longUnchangeExport": self.longUnchangeExport,
            "loginLogExport": self.loginLog,
            "accountActive": self.accountActive,
            "isPrivilege": self.isPrivilege,
        }

def safetyInspection(connect, cursor, specialList):
    # 初始化连接对象
    try:
        login_user_list = []
        hunt_mysql = HuntMySql()
        hunt_mysql.bl0040_1, hunt_mysql.bl0040_2 = bl0040(cursor, hunt_mysql)
        userHuntList = selectUser(cursor, hunt_mysql, specialList)
        # 是否有匿名用户 true 有 false 无
        bl0041(cursor, userHuntList)
        # root用户登录权限 true 只允许本地登录 false 不局限于本地登录
        bl0042(cursor, userHuntList)
        select_login_user_List(cursor, login_user_list, userHuntList)
        # 报表导出判断是否是特权账号
        isRoot(cursor, userHuntList)
        # 报表导出判断是否长期未改密
        islongtimeUchangePWd(cursor, userHuntList)
        # 报表导出密码策略
        for huntUser in userHuntList:
            if (not huntUser.bl0040_1 or not huntUser.bl0040_2):
                huntUser.isWeakStrategy = "是"
                updatePasswordStrategyExport(huntUser)
            else:
                huntUser.isWeakStrategy = "否"
        for user_hunt in userHuntList:
            # if user_hunt.userName == "":
                #匿名用户处理
                # user_hunt.userName = "匿名用户"
            #长期未登录
            if user_hunt.bl0051:
                user_hunt.longUnusedExport = '否'
            else:
                user_hunt.longUnusedExport = '是'

        json_output = json.dumps([user.to_dict() for user in userHuntList], indent=4, ensure_ascii=False)
    finally:
        # 确保关闭数据库连接
        if connect:
            connect.close()
    authority = []
    if len(login_user_list) > 100:
        login_user_list = login_user_list[:100]
    print(f'{json_output} + "#@#" + {json.dumps(authority)} + "#@#" + {json.dumps(login_user_list)}')
    return userHuntList, authority, login_user_list

def updatePasswordStrategyExport(huntUser):
    if not huntUser.bl0040_1:
        huntUser.passwordStrategyExport += ''' 检查MySQLvalidate_password插件状态：SHOW VARIABLES LIKE 'validate_password%';
 确保以下参数已配置：validate_password_policy 至少为 MEDIUM。
        '''
    if not huntUser.bl0040_2:
        huntUser.passwordStrategyExport += ''' 检查MySQLvalidate_password插件状态：SHOW VARIABLES LIKE 'validate_password%';
 确保以下参数已配置：validate_password_length 至少为 8。
           '''
def islongtimeUchangePWd(cursor, userHuntList):
    now = datetime.now()
    sql = '''
SELECT User, Host, password_last_changed ,account_locked
FROM mysql.user;'''
    cursor.execute(sql)
    results = cursor.fetchall()
    for huntUser in userHuntList:
        for row in results:
            if huntUser.userName == row[0]:
                if row[2]:
                    lastChangePwdTime = row[2]
                    huntUser.lastPwdsetTime = lastChangePwdTime.strftime('%Y-%m-%d %H:%M:%S')
                    if isinstance(lastChangePwdTime, datetime) and (now - lastChangePwdTime).days > 90:
                        huntUser.longUnchangeExport = '是'
                        huntUser.bl2007 = False
                    else:
                        huntUser.longUnchangeExport = '否'
                        huntUser.bl2007 = True
                if row[3]:
                    if row[3] == "N":
                        huntUser.accountActive = "启用"
                    elif row[3] == "Y":
                        huntUser.accountActive = "禁用"


def isRoot(cursor, userHuntList):
    sql = '''
    SELECT 
  User, Host,
  Super_priv, Grant_priv, Create_user_priv, Shutdown_priv, File_priv 
FROM 
  mysql.user
WHERE 
  Super_priv = 'Y' OR 
  Grant_priv = 'Y' OR 
  Create_user_priv = 'Y' OR 
  Shutdown_priv = 'Y' OR 
  File_priv = 'Y';
    '''
    cursor.execute(sql)
    results = cursor.fetchall()
    for user in userHuntList:
        for row in results:
            if user.userName == row[0]:
                user.isPrivilegeExport = '是'
                user.isPrivilege = '1'

def select_login_user_List(cursor, login_user_list, userHuntList):
    try:
        sql = "SHOW VARIABLES LIKE 'general_log%';"
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            if row[1] == "ON":
                sql = '''
                SELECT event_time, user_host
    FROM (
        SELECT 
            event_time, user_host,
            ROW_NUMBER() OVER (PARTITION BY user_host ORDER BY event_time DESC) AS rn
        FROM (
            SELECT * 
            FROM mysql.general_log
            WHERE command_type = 'Connect'
            ORDER BY event_time DESC
            LIMIT 100000
        ) AS temp
    ) AS ranked
    WHERE rn = 1;'''
                cursor.execute(sql)
                results = cursor.fetchall()
                for row in results:
                    time = row[0]
                    if isinstance(time, datetime):
                        time_str = time.strftime("%Y-%m-%d %H:%M:%S")
                        now = datetime.now()
                        #bl0051 长期未登录
                        trueUserList = []
                        user = row[1].split('@')[0].split("[")[1].split("]")[0]
                        if user not in trueUserList and (now-time).days < 90:
                            for hunt_user in userHuntList:
                                if user == hunt_user.userName:
                                    hunt_user.bl0051 = True
                                    trueUserList.append(hunt_user.userName)
                    else:
                        time_str = ''
                    user = row[1].split('@')[0].split("[")[1].split("]")[0]
                    ip = row[1].split('@')[1].split("[")[1].split("]")[0]
                    if not ip:
                        ip = "-"
                    login_user_list.append(f"{user},{ip},{time_str}")
                    for hunt_user in userHuntList:
                        if hunt_user.userName == user:
                            if hunt_user.lastLoginTime == "-":
                                hunt_user.lastLoginTime = f"{time_str}"
                            if hunt_user.log_count <= 10:
                                if hunt_user.loginLog == '':
                                    hunt_user.loginLog += f"{user},{ip},{time_str}"
                                else:
                                    hunt_user.loginLog += '\n' + f"{user},{ip},{time_str}"
                                hunt_user.log_count += 1
                return login_user_list
            elif row[1] == "OFF":
                # 未开启审计功能则默认所有用户都为登录
                for hunt_user in userHuntList:
                    hunt_user.bl0051 = True
        return None
    except Exception as e:
        common.logger.error( e)
        for hunt_user in userHuntList:
            hunt_user.bl0051 = True

def selectUser(cursor, hunt_mysql, specialList):
    userHuntList = []
    query = "SELECT user from mysql.user;"
    cursor.execute(query)
    results = cursor.fetchall()
    if len(results) > 0:
        for user in results:
            if user[0] in specialList or user[0].lower() in specialList:
                continue
            #=========上线取消注释==============
            if user[0].lower() not in analysis_account_array and user[0] not in analysis_account_array:
                continue
            user_hunter = copy.deepcopy(hunt_mysql)
            user_hunter.userName = user[0]
            userHuntList.append(user_hunter)
    return userHuntList

def bl0040(cursor, hunt_mysql):
    bl0040_p = False
    bl0040_l = False
    query = "SHOW VARIABLES LIKE 'validate_password%';"
    cursor.execute(query)
    results = cursor.fetchall()
    if len(results) > 0:
        for variable in results:
            if variable[0] == 'validate_password_policy':  # 检查变量名
                if "LOW" == variable[1]:
                    bl0040_p = False
                else:
                    bl0040_p = True
            if variable[0] == 'validate_password_length':
                if int(variable[1]) < 8:
                    bl0040_l = False
                else:
                    bl0040_l = True
    return bl0040_p, bl0040_l


def bl0041(cursor, userHuntList):
    for user_hunt in userHuntList:
        if user_hunt.userName == "":
            user_hunt.bl0041 = False


def bl0042(cursor, userHuntList):
    query = "SELECT Host FROM mysql.user WHERE User='root';"
    cursor.execute(query)
    results = cursor.fetchall()
    for host in results:
        if host[0] != bytearray(b'localhost'):
            for user_hunt in userHuntList:
                if user_hunt.userName == "root":
                    user_hunt.bl0042 = False

data_map = {
    "location": "10.10.10.226",
    "user": "root",
    "pwd": "1234",
    "protocol": "SSH",
    "port": "3306",
    "remote": "http://pam-selenium:4444/wd/hub",
    "loginAccount": "",
    "loginAccountPwd": "",
    "database": "mysql",
    "taskId": "132132-DASDAS",
    "discoverEnable": 1,
    "analysisEnable": 1,
    "userDatalist": "",
    "specialUserList": "",
    "analysisAccountList": []
}
if __name__ == '__main__':
    do_analysis(data_map)
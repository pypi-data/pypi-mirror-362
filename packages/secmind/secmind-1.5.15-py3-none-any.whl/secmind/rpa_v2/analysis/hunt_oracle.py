import json
import sys
from datetime import datetime

import cx_Oracle
from secmind.rpa_v2 import common
def do_analysis(data_map):
    user = data_map['user']
    passwd = data_map['pwd']
    special_user_data_list = data_map['specialUserList']
    global analysis_account_array
    analysis_account_array = data_map.get('analysisAccountList')
    if analysis_account_array is None:
        analysis_account_array = []
    #/orcl
    # 配置数据库连接信息

    mode = None
    user = data_map['user']
    if ' ' in user:
        split = user.split(' ')
        user = split[0]
        role = split[2]
        if 'SYSDBA' in role:
            mode = cx_Oracle.SYSDBA
        elif 'SYSOPER' in role:
            mode = cx_Oracle.SYSOPER
    url = "{0}/{1}@{2}:{3}/{4}".format(user, data_map['pwd'], data_map['location'], data_map['port'],
                                       data_map['database'])
    if mode:
        connect = cx_Oracle.connect(url, mode=mode)
    else:
        connect = cx_Oracle.connect(url)
    cursor = connect.cursor()


    # dsn = f'{host}:{port}/{SERVICE_NAME}'  # 数据库连接字符串，例如 "localhost:1521/xe"
    #python hunt_oracle.py system 123456 10.10.10.226 'null' 1521 orcl
    # username = 'system'  # 数据库用户名
    # password = '123456'  # 数据库密码
    # dsn = '10.10.10.226:1521/orcl'
    # special_user_data_list = []

    specialList = []
    #特殊账号
    if special_user_data_list == "null":
        special_user_data_list = []
    if special_user_data_list:
        for user_sp in special_user_data_list.split(","):
            specialList.append(user_sp)
    return safetyInspection(connect, cursor, specialList)

class HuntOracle:
    def __init__(self):
        super().__init__()
        self.bl0045 = True
        self.bl0046 = True
        self.bl0055 = False

        #统计已经记录的登录日志数量
        self.log_count = 0
        #报表导出自定义字段
        self.ugroup = ''
        self.isPrivilegeExport = '否'
        self.longUnusedExport = '是'
        self.accountActive = ''
        self.accountExpires = ''
        self.passwordStrategyExport = ''
        self.lastLoginTime = '从未登录'
        self.lastPwdsetTime = None
        self.lastLog = None
        self.createTime = '-'
        self.permission = ''
        self.loginLog = ''
        self.isWeakStrategy = None
        self.assetVersion = None
    def to_dict(self):
        """ 将对象转换为字典 """
        return {
            "userName": self.userName,  # 可能未赋值，需用 getattr 处理
            "bl0045": self.bl0045,
            "bl0046": self.bl0046,
            "bl0055": self.bl0055,

            # 报表导出自定义字段
            "accountActive": self.accountActive,
            "accountExpires": self.accountExpires,
            "createTime": self.createTime,
            "lastLoginTime": self.lastLoginTime,
            "isWeakStrategy": self.isWeakStrategy,
            "passwordStrategyExport": self.passwordStrategyExport,
            "longUnusedExport": self.longUnusedExport,
            "loginLogExport": self.loginLog,

        }

def safetyInspection(connect, cursor, specialList):
    try:
        user_hunt_list = []
        hunt = HuntOracle()

        sql_query = "SELECT USERNAME FROM DBA_USERS"  # 查询前10行数据
        cursor.execute(sql_query)
        result_userList = cursor.fetchall()
        for user in result_userList:
            if user[0] in specialList or user[0].lower() in specialList:
                continue
            #上线需要去掉注释
            if user[0] not in analysis_account_array and user[0].lower() not in analysis_account_array:
                continue
            user_hunt = HuntOracle()
            user_hunt.userName = user[0]
            user_hunt_list.append(user_hunt)

        sql_query = "SELECT USERNAME, ACCOUNT_STATUS FROM DBA_USERS WHERE USERNAME IN ('HR', 'SCOTT')"
        cursor.execute(sql_query)
        result = cursor.fetchall()
        for row in result:
            if row[1] == 'OPEN':
                for hunt_user in user_hunt_list:
                    if row[0] == hunt_user.userName:
                        hunt_user.bl0045 = False

        sql_query = "SELECT * FROM DBA_PROFILES WHERE RESOURCE_NAME='PASSWORD_VERIFY_FUNCTION'"
        cursor.execute(sql_query)
        result_passwd = cursor.fetchall()
        for row in result_passwd:
            if row[3] == 'NULL':
                for hunt_user in user_hunt_list:
                    hunt_user.bl0046 = False
        login_user_list = []
        try:
            sql_query = '''
    SELECT username, timestamp, action_name, returncode
    FROM (
        SELECT username, timestamp, action_name, returncode,
               ROW_NUMBER() OVER (PARTITION BY username ORDER BY timestamp DESC) AS rn
        FROM (
            SELECT * FROM dba_audit_trail
            WHERE action_name = 'LOGON'
              AND returncode = 0
              AND timestamp >= SYSDATE - 90
              AND ROWNUM <= 100000
        )
    ) t
    WHERE rn = 1;'''
            cursor.execute(sql_query)
            target_format = "%Y-%m-%d %H:%M:%S"
            result_login = cursor.fetchall()
            now = datetime.now()
            for row in result_login:
                if isinstance(row[1], datetime):
                    login_user_list.append(f"{row[0]},-,{row[1].strftime(target_format)}")
                    str_logon_log = f"{row[0]},-,{row[1].strftime(target_format)}"
                    trueUserList = []
                    for hunt_user in user_hunt_list:
                        if row[0] == hunt_user.userName:
                            # 报告导出- 上次登录时间
                            if hunt_user.lastLoginTime == '从未登录':
                                # 首次检测到登录时，记录时间为上次登录时间
                                hunt_user.lastLoginTime = row[1].strftime('%Y-%m-%d %H:%M:%S')
                            if hunt_user.log_count <= 10:
                                if hunt_user.loginLog == '':
                                    hunt_user.loginLog += str_logon_log
                                else:
                                    hunt_user.loginLog += '\n' + str_logon_log
                                hunt_user.log_count += 1
                        if user not in trueUserList and (now - row[1]).days < 90:
                            hunt_user.bl0055 = True
                            trueUserList.append(hunt_user.userName)
        except Exception as e:
            common.logger.error(f"检查长期未登录发生错误: {repr(e)}")
            for hunt_user in user_hunt_list:
                hunt_user.bl0055 = True
        getExportData(cursor, user_hunt_list)
        # 将用户名转小写，与账号发现统一
        for user in user_hunt_list:
            user.userName = user.userName.lower()
        json_output = json.dumps([user.to_dict() for user in user_hunt_list], indent=4, ensure_ascii=False)
        print(json_output)
        cursor.close()
        authority = []
        if len(login_user_list) > 100:
            login_user_list = login_user_list[:100]
        return user_hunt_list, authority, login_user_list
    except Exception as e:
        # 捕获数据库异常
        raise Exception(e)
    finally:
        # 关闭连接
        if connect:
            connect.close()
            print("[INFO] 数据库连接已关闭")

def getExportData(cursor, user_hunt_list):

    #报告导出- 账号状态
    sql_getStatus = '''SELECT
    USERNAME,
    ACCOUNT_STATUS,
    LOCK_DATE,
    EXPIRY_DATE,
    CREATED
    FROM
    DBA_USERS'''
    cursor.execute(sql_getStatus)
    result_status = cursor.fetchall()
    for hunt_user in user_hunt_list:
        for row in result_status:
            if row[0] == hunt_user.userName:
                hunt_user.accountActive = row[1]
                if row[4] and isinstance(row[4], datetime):
                    hunt_user.createTime = row[4].strftime('%Y-%m-%d %H:%M:%S')
                if row[2] and isinstance(row[2], datetime):
                    hunt_user.accountExpires = row[2].strftime('%Y-%m-%d %H:%M:%S')
                elif row[2] == '':
                    hunt_user.accountExpires = "从不"



    # 报告导出-密码策略
    for hunt_user in user_hunt_list:
        if not hunt_user.bl0046:
            hunt_user.passwordStrategyExport += '''检测是否启用密码验证函数SELECT * FROM DBA_PROFILES WHERE RESOURCE_NAME='PASSWORD_VERIFY_FUNCTION';
            '''
            hunt_user.isWeakStrategy = "是"
        else:
            hunt_user.isWeakStrategy = "否"


#H03102800201D
data_map = {
    "location": "10.10.10.142",
    "user": "system as Default",
    "pwd": "system",
    "protocol": "SSH",
    "port": "1521",
    "remote": "http://pam-selenium:4444/wd/hub",
    "loginAccount": "",
    "loginAccountPwd": "",
    "database": "helowin",
    "taskId": "132132-DASDAS",
    "discoverEnable": 1,
    "analysisEnable": 1,
    "userDatalist": "",
    "specialUserList": "",
    "analysisAccountList": []
}
if __name__ == '__main__':
    do_analysis(data_map)
import json
import sys
from datetime import datetime
from venv import logger

import dmPython
from secmind.rpa_v2 import common

# 配置达梦数据库连接信息
# host = '10.10.10.226'  # 数据库地址，通常是 IP
# port = 5236         # 达梦数据库默认端口
# user = 'SYSDBA'     # 数据库用户名
# password = 'SYSDBA_dm001' # 数据库密码
# special_user_data_list = ''
# python hunt_DaMeng.py SYSDBA SYSDBA_dm001 10.10.10.226 'null' 5236

def do_analysis(data_map):
    user = data_map['user']
    password = data_map['pwd']
    host = data_map['location']
    special_user_data_list = data_map['specialUserList']
    global analysis_account_array
    analysis_account_array = data_map.get('analysisAccountList')
    if analysis_account_array is None:
        analysis_account_array = []
    port = data_map['port']
    specialList = []
    #特殊账号
    if special_user_data_list == "null":
        special_user_data_list = []
    if special_user_data_list:
        for user_sp in special_user_data_list.split(","):
            specialList.append(user_sp)
    return safetyInspection(user, password, host, port, specialList)
class HuntDaMeng:
    def __init__(self):
        super().__init__()
        self.bl0049 = True
        self.bl0050 = True
        self.bl0057 = False


        #统计已经记录的登录日志数量
        self.log_count = 0
        #报表导出自定义字段
        self.ugroup = ''
        self.isPrivilegeExport = '否'
        self.longUnusedExport = '是'
        self.accountActive =''
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
            "userName": self.name,  # 可能未赋值，需用 getattr 处理
            "bl0049": self.bl0049,
            "bl0050": self.bl0050,
            "bl0057": self.bl0057,

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

def safetyInspection(user, password, host, port, specialList):
    try:
        # 创建连接
        connection = dmPython.connect(
            user=user,
            password=password,
            server=f'{host}:{port}',
        )
        hunt = HuntDaMeng()
        print("[INFO] 成功连接到达梦数据库")
        user_hunt_list = []
        # 创建游标
        cursor = connection.cursor()

        # 执行查询
        query = "SELECT USERNAME, ACCOUNT_STATUS FROM DBA_USERS"
        cursor.execute(query)

        # 获取结果
        result = cursor.fetchall()
        for row in result:
            if row[0] in specialList or row[0].lower() in specialList:
                continue
            #上线需要去掉注释
            if row[0] not in analysis_account_array and row[0].lower() not in analysis_account_array:
                continue
            hunt = HuntDaMeng()
            hunt.name = row[0]
            if (hunt.name == "TEST" or hunt.name == "TEST123") and "OPEN" in row[1]:
                hunt.bl0049 = False
            user_hunt_list.append(hunt)


        query = "SELECT PARA_NAME,PARA_VALUE FROM v$dm_ini WHERE PARA_NAME = 'PWD_POLICY';"
        cursor.execute(query)
        # 获取结果
        result_policy = cursor.fetchall()
        for row in result_policy:
            for param in row:
                if not param or param == "NULL":
                    for hunt in user_hunt_list:
                        hunt.bl0050 = False
                if param != 'PWD_POLICY':
                    binData = bin(int(param))[2:]
                    if len(binData) < 4:
                        for hunt in user_hunt_list:
                            hunt.bl0050 = False
                    else:
                        for i in range(4):
                            bit = binData[i]
                            if bit != "1":
                                for hunt in user_hunt_list:
                                    hunt.bl0050 = False
        query = '''
        SELECT 
        USER_NAME,create_time
        FROM V$SESSIONS;'''
        cursor.execute(query)
        login_user_list = []
        trueUserList = []
        # 获取结果
        result_login = cursor.fetchall()
        target_format = "%Y-%m-%d %H:%M:%S"
        now = datetime.now()
        for row in result_login:
            if isinstance(row[1],datetime):
                login_user_list.append(f"{row[0]},-,{row[1].strftime(target_format)}")
                str_logon_log = f"{row[0]},-,{row[1].strftime(target_format)}"
                for hunt_user in user_hunt_list:
                    if row[0] == hunt_user.name:
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
                    for hunt_user in user_hunt_list:
                        if row[0] == hunt_user.name:
                            hunt_user.bl0057 = True
                            trueUserList.append(hunt_user.name)
        getExportData(cursor, user_hunt_list)
        # 将用户名转小写，与账号发现统一
        for user in user_hunt_list:
            user.name = user.name.lower()
        cursor.close()
        json_output = json.dumps([user.to_dict() for user in user_hunt_list], indent=4, ensure_ascii=False)
        print(json_output)
        authority = []
        if len(login_user_list) > 100:
            login_user_list = login_user_list[:100]
        return user_hunt_list, authority, login_user_list

    except dmPython.Error as e:
        logger.exception(f"达梦数据库异常：{e}")
        raise e

    finally:
        # 关闭连接
        if 'connection' in locals() and connection:
            connection.close()
            print("[INFO] 数据库连接已关闭")


def getExportData(cursor, user_hunt_list):

    #报告导出- 账号状态
    sql_getStatus = '''    SELECT
    USERNAME,
    ACCOUNT_STATUS,
    LOCK_DATE,
    EXPIRY_DATE,
    CREATED
    FROM
    DBA_USERS;'''
    cursor.execute(sql_getStatus)
    result_status = cursor.fetchall()
    for hunt_user in user_hunt_list:
        for row in result_status:
            if row[0] == hunt_user.name:
                hunt_user.accountActive = row[1]
                if row[4] and isinstance(row[4], datetime):
                    hunt_user.createTime = row[4].strftime('%Y-%m-%d %H:%M:%S')
                if row[2] and isinstance(row[2], datetime):
                    hunt_user.accountExpires = row[2].strftime('%Y-%m-%d %H:%M:%S')
                elif row[2] == '':
                    hunt_user.accountExpires = "从不"



    # 报告导出-密码策略
    for hunt_user in user_hunt_list:
        if not hunt_user.bl0050:
            hunt_user.passwordStrategyExport += '''检测是否在用户创建时依据密码策略设置复杂密码
CREATE USER 用户名 IDENTIFIED BY '复杂密码';
            '''
            hunt_user.isWeakStrategy = "是"
        else:
            hunt_user.isWeakStrategy = "否"




# H05106400101D
data_map = {
    "location": "10.10.10.142",
    "user": "sysdba",
    "pwd": "Zc7UAGVHdjMow",
    "protocol": "dm",
    "port": "30236",
    "remote": "http://pam-selenium:4444/wd/hub",
    "loginAccount": "",
    "loginAccountPwd": "",
    "database": "PAM",
    "taskId": "132132-DASDAS",
    "discoverEnable": 1,
    "analysisEnable": 1,
    "userDatalist": "",
    "specialUserList": "",
    "analysisAccountList": []
}
if __name__ == '__main__':
    do_analysis(data_map)

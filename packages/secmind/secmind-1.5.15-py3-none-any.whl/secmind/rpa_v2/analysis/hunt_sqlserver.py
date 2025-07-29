import json
import sys
from datetime import datetime

import pymssql
import pyodbc
from secmind.rpa_v2 import common
# 配置数据库连接信息
# server = '10.10.10.226'  # SQL Server 地址，例如 'localhost' 或 '192.168.1.100'
# username = 'SA'  # 数据库用户名
# password = '123jkluio!@#'  # 数据库密码
# special_user_data_list = ''
def do_analysis(data_map):
    user = data_map['user']
    pwd = data_map['pwd']
    special_user_data_list = data_map['specialUserList']
    global analysis_account_array
    analysis_account_array = data_map.get('analysisAccountList')
    if analysis_account_array is None:
        analysis_account_array = []
    #  python hunt_sqlserver.py SA 123jkluio!@# 10.10.10.226 'null'
    specialList = []
    user_hunt_list =[]
    if special_user_data_list == "null":
        special_user_data_list = []
    if special_user_data_list:
        for user_sp in special_user_data_list.split(","):
            specialList.append(user_sp)
    try:
        connect = pymssql.connect(
            host=data_map['location'],
            port=str(data_map['port']),
            database=data_map['database'],
            user=user,
            password=pwd)
    except Exception as e:
        print("脚本登录失败" + e)

    return safetyInspection(connect, specialList)

class HuntSQLServer:
    def __init__(self):
        super().__init__()
        self.bl0047 = False
        self.bl0048 = True
        self.bl0056 = False
        self.bl2009 = True

        #统计已经记录的登录日志数量
        self.log_count = 0
        #报表导出自定义字段
        self.ugroup = ''
        self.isPrivilege = '0'
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
            "bl0047": self.bl0047,
            "bl0048": self.bl0048,
            "bl0056": self.bl0056,
            "bl2009": self.bl2009,

            # 报表导出自定义字段
            "ugroup": self.ugroup,
            "isPrivilegeExport": self.isPrivilegeExport,
            "createTime": self.createTime,
            "lastLoginTime": self.lastLoginTime,
            "isWeakStrategy": self.isWeakStrategy,
            "passwordStrategyExport": self.passwordStrategyExport,
            "longUnusedExport": self.longUnusedExport,
            "permission": self.permission,
            "assetVersion": self.assetVersion,
            "loginLogExport": self.loginLog,
            "isPrivilege": self.isPrivilege,

        }

def safetyInspection(connect, specialList):
    try:
        # 创建数据库连接
        print("[INFO] 成功连接到 SQL Server 数据库")

        # 创建游标对象
        cursor = connect.cursor()
        huntSQLServer = HuntSQLServer()
        user_hunt_list = []

        sql_query = """
        SELECT * from sys.server_principals
        """
        cursor.execute(sql_query)
        result_user = cursor.fetchall()
        for row in result_user:
            if row[0] in specialList or row[0].lower() in specialList:
                continue
            #上线需取消注释
            if row[0] not in analysis_account_array and row[0].lower() not in analysis_account_array:
                continue
            hunt_user = HuntSQLServer()
            hunt_user.name = row[0]
            user_hunt_list.append(hunt_user)

        # 执行 SQL 查询
        sql_query = "SELECT name, is_policy_checked FROM sys.sql_logins;"
        cursor.execute(sql_query)
        # 获取查询结果
        result_passwd = cursor.fetchall()
        for row in result_passwd:
            for user_hunt in user_hunt_list:
                if user_hunt.name == row[0]:
                    if row[1]:
                        user_hunt.bl0047 = True
                    else:
                        user_hunt.bl0047 = False

        #长期未改密
        now = datetime.now()
        sql = "select sp.name as usename,sl.modify_date as lastPwdsetTime from sys.server_principals sp left join sys.sql_logins sl on sp.principal_id = sl.principal_id where sp.type not in ('G', 'R') order by sp.name;"
        cursor.execute(sql)
        result_change_passwd = cursor.fetchall()
        for result in result_change_passwd:
            if result[1]:
                for user_hunt in user_hunt_list:
                    if user_hunt.name == result[0]:
                        lastChangePwdTime = result[1]
                        user_hunt.lastPwdSetTime = lastChangePwdTime.strftime('%Y-%m-%d %H:%M:%S')
                        if (now - lastChangePwdTime).days > 90:
                            user_hunt.bl2009 = False
                        else:
                            user_hunt.bl2009 = True



        sql_query = "SELECT name, is_disabled FROM sys.server_principals WHERE name = 'sa';"
        cursor.execute(sql_query)

        # 获取查询结果
        result_sa = cursor.fetchall()
        for row in result_sa:
            if not row[1]:
                for user_hunt in user_hunt_list:
                    if user_hunt.name == 'sa':
                        user_hunt.bl0048 = False

        sql_query = '''SELECT DISTINCT login_name,login_time
        FROM sys.dm_exec_sessions 
        ORDER BY login_time DESC;'''
        cursor.execute(sql_query)

        # 获取查询结果
        login_user_list = []
        result_loginUser = cursor.fetchall()
        now = datetime.now()
        for row in result_loginUser:
            if isinstance(row[1], datetime):
                login_user_list.append(f"{row[0]},-,{row[1].strftime('%Y-%m-%d %H:%M:%S')}")
                str_logon_log = f"{row[0]},-,{row[1].strftime('%Y-%m-%d %H:%M:%S')}"
                trueUserList = []
                time = row[1]
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
                        if row[0] not in trueUserList and (now - time).days < 90:
                            hunt_user.bl0056 = True
                            hunt_user.longUnusedExport = "否"
                        trueUserList.append(hunt_user.name)
        login_user_list = list(set(login_user_list))
        getExportData(cursor, user_hunt_list)

        # 关闭游标
        cursor.close()

        json_output = json.dumps([user.to_dict() for user in user_hunt_list], indent=4, ensure_ascii=False)
        print(json_output)
        authority = []
        if len(login_user_list) > 100:
            login_user_list = login_user_list[:100]
        return user_hunt_list, authority, login_user_list

    except Exception as e:
        # 捕获并处理数据库异常
        common.logger.error(f"脚本错误: {repr(e)}")
        raise e
    except TypeError as e:
        common.logger.error(f"TypeError: {repr(e)}")
        raise e

    finally:
        # 关闭连接
        if connect:
            connect.close()
            print("[INFO] 数据库连接已关闭")

def getExportData(cursor, user_hunt_list):
    # 报表导出-资产版本
    sql_getVersion = '''SELECT @@VERSION;'''
    cursor.execute(sql_getVersion)
    result_version = cursor.fetchall()
    for hunt_user in user_hunt_list:
        hunt_user.assetVersion = result_version[0][0]

    # 报告导出-角色
    sql_getRole = '''SELECT
    spr.name AS ServerRoleName,
    spp.name AS PrincipalName
FROM sys.server_role_members srm
JOIN sys.server_principals spr
    ON srm.role_principal_id = spr.principal_id
JOIN sys.server_principals spp
    ON srm.member_principal_id = spp.principal_id
WHERE spr.type_desc = 'SERVER_ROLE'
ORDER BY spp.name, spr.name;'''
    cursor.execute(sql_getRole)
    result_role = cursor.fetchall()
    for hunt_user in user_hunt_list:
        for row in result_role:
            if row[1] == hunt_user.name:
                hunt_user.ugroup = row[0]
                # 报告导出-特权账号
                if row[0] == 'sysadmin':
                    hunt_user.isPrivilegeExport = "是"
                    hunt_user.isPrivilege = '1'
                    hunt_user.permission = 'sysadmin'

    # 报告导出- 账号创建时间
    sql_getAccountBirth = '''SELECT
    name AS LoginName,
    create_date AS CreationTime
FROM sys.sql_logins
ORDER BY name;'''
    cursor.execute(sql_getAccountBirth)
    result_accountCreateTime = cursor.fetchall()
    for hunt_user in user_hunt_list:
        for row in result_accountCreateTime:
            if row[0] == hunt_user.name:
                if isinstance(row[1], datetime):
                    hunt_user.createTime = row[1].strftime('%Y-%m-%d %H:%M:%S')
                elif isinstance(row[1], str):
                    hunt_user.createTime = row[1]

    # 报告导出-密码策略
    for hunt_user in user_hunt_list:
        if not hunt_user.bl0047:
            hunt_user.passwordStrategyExport += '''检测是否启用了密码复杂策略，SELECT name, is_policy_checked FROM sys.sql_logins;
            '''
            hunt_user.isWeakStrategy = "是"
        else:
            hunt_user.isWeakStrategy = "否"




#H04105900101D
data_map = {
    "location": "10.10.10.142",
    "user": "sa",
    "pwd": "888@limiaomiao",
    "protocol": "sqlserver",
    "port": "1433",
    "remote": "http://pam-selenium:4444/wd/hub",
    "loginAccount": "",
    "loginAccountPwd": "",
    "database": "master",
    "taskId": "132132-DASDAS",
    "discoverEnable": 1,
    "analysisEnable": 1,
    "userDatalist": "",
    "specialUserList": "",
    "analysisAccountList": []
}
if __name__ == '__main__':
    do_analysis(data_map)
import concurrent
import copy
import ipaddress
import json
import logging
import math
import os
import queue
import re
import sys
import time
from asyncio import futures
from datetime import datetime, timedelta
from multiprocessing import Queue
from random import random
from threading import Thread

from secmind.rpa_v2 import WinRMWrapper, SambaWrapper
from secmind.rpa_v2 import common


class HuntWindows:
    def __init__(self):
        super().__init__()
        self.checkUserAuthority = True
        self.authorityChangeDetail = None
        self.guestAccount = True
        self.adminAccount = True
        self.bl1029 = True
        self.bl1030 = True
        self.bl1031 = True
        self.bl1032 = True
        self.bl1034 = False
        self.enbededAccount = ""
        #检查子项
        self.bl0005_1 = False
        self.bl0005_2 = False
        self.bl1026_1 = False
        self.bl1026_2 = False
        self.bl1026_3 = False
        self.bl1026_4 = False
        self.bl1026_5 = False
        self.bl1027_1 = True
        self.bl1027_2 = True
        self.bl1027_3 = True
        self.bl1027_4 = True
        self.bl1028_1 = True
        self.bl1028_2 = True
        #统计已经记录的登录日志数量
        self.log_count = 0
        #报表导出自定义字段
        self.ugroup = ''
        self.accountActive =''
        self.accountExpires = ''
        self.passwordStrategyExport = ''
        self.lastLoginTime = '-'
        self.lastPwdsetTime = None
        self.lastLog = None
        self.createTime = '-'
        self.permission = ''
        self.loginLog = ''

    def to_dict(self):
        return {
            "userName": self.userName,
            "bl0001": self.passwordComplexity,
            "bl0002": self.minimumPasswordLength,
            "bl0003": self.minimumPasswordAge,
            "bl0004": self.passwordHistorySize,
            "bl0006": self.guestAccount,
            "bl0007": self.adminAccount,
            "bl0008": self.longUnUsed,
            "authorityChangeDetail": self.authorityChangeDetail,
            "bl0009": self.checkUserAuthority,
            "bl0010": self.checkUAC,
            "bl0011": self.checkRemoteDesktop,
            "bl0012": self.checkNLA,
            "bl0013": self.checkIsRecordLoginEvents,
            "bl0014": self.checkIsAllowEnumerateResources,
            "bl1029": self.bl1029,
            "bl1030": self.bl1030,
            "bl1031": self.bl1031,
            "bl1032": self.bl1032,
            "bl1034": self.bl1034,
            "enbededAccount": self.enbededAccount,

            "isHighPermission": (self.bl1028_1 and self.bl1028_1 and self.bl1027_2 and self.bl1027_3),
            #检查子项
            "bl0005_1": self.bl0005_1,
            "bl0005_2": self.bl0005_2,
            "bl1026_1": self.bl1026_1,
            "bl1026_2": self.bl1026_2,
            "bl1026_3": self.bl1026_3,
            "bl1026_4": self.bl1026_4,
            "bl1026_5": self.bl1026_5,
            "bl1027_1": self.bl1027_1,
            "bl1027_2": self.bl1027_2,
            "bl1027_3": self.bl1027_3,
            "bl1027_4": self.bl1027_4,
            "bl1028_1": self.bl1028_1,
            "bl1028_2": self.bl1028_2,

            # 报表导出自定义字段
            "ugroup": self.ugroup,
            "isPrivilegeExport": self.isPrivilegeExport,
            "accountActive": self.accountActive,
            "createTime": self.createTime,
            "accountExpires": self.accountExpires,
            "lastLoginTime": self.lastLoginTime,
            "lastPwdsetTime": self.lastPwdsetTime,
            "isWeakStrategy": self.isWeakStrategy,
            "passwordStrategyExport": self.passwordStrategyExport,
            "longUnusedExport": self.longUnusedExport,
            "longUnchangeExport": self.longUnchangeExport,
            "permission": self.permission,
            "assetVersion":self.assetVersion,
            "loginLogExport":self.loginLog,
        }


class User:
    def __init__(self):
        super().__init__()
        self.name = None
        self.homeDirectory = None
        self.authority = None
        self.localGroup = None
        self.globalGroup = None
        self.lastLogon = False
        self.active = None
        self.logonTime_detail = None

    def to_dict(self):
        return {
            "name": self.name,
            "homeDirectory": self.homeDirectory,
            "localGroup": self.localGroup,
            "globalGroup": self.globalGroup,
            "authority": self.authority
        }


class log:
    def __init__(self):
        super().__init__()
        self.event_id = None
        self.time_generated = None
        self.source_name = None
        self.message = []
        self.keywords = None
        self.accountName = ''
        self.ip = ''


class link:
    def __init__(self):
        super().__init__()
        self.host = None
        self.passwd = None
        self.userName = None
        self.lastUserList = None


def safetyInspection(login_user_list, specialAccountList, lastUserList, link, data_map, result_queue):
    try:
        winrm_wrapper = WinRMWrapper(host=link.host, username=link.userName, password=link.passwd)
        winrm_wrapper.connect()
    except Exception as e:
        logging.error("windows资产连接失败" , e)
        raise Exception(f"资产连接失败，请检查winrm协议是否开启、账号密码是否正确")
    # 设置脚本执行速度
    global work_thread_num
    if speed == 0:
        work_thread_num = int(1)
    else:
        # 查询当前系统核心数，设置工作线程数。
        result =  winrm_wrapper.execute_powershell("$logicalProcessors = (Get-WmiObject Win32_ComputerSystem).NumberOfLogicalProcessors; Write-Output $logicalProcessors")
        if result.get('std_out'):
            # 向上取整
            work_thread_num = math.ceil(int(result.get('std_out'))/3)
            if work_thread_num > 5 :
                work_thread_num = 5
    # 为线程池创建连接对象
    global winrmList
    # 为每个线程新建连接对象保证线程安全
    winrmList = new_connections(link)
    try:
        hunter = HuntWindows()
        hunter.assetVersion = getVersion(winrm_wrapper)
        value = bl01ToBl05AndBl013(winrm_wrapper)
        # (bl0001) true：已开启密码必须符合复杂性要求 false：未开启 -1：执行异常未找到数据
        hunter.passwordComplexity = value[0]
        # (bl0002) true：最小密码长度不小于14位 false：不满足 -1：执行异常未找到数据
        hunter.minimumPasswordLength = value[1]
        # (bl0003) true：密码最短使用期限大于等于1天  -1：执行异常未找到数据
        hunter.minimumPasswordAge = value[2]
        # true:密码最大使用期限不超过90 -1：执行异常未找到数据
        hunter.maxPasswordAge = value[7]
        # (bl0004) true：强制密码历史记录不小于5  -1：执行异常未找到数据
        hunter.passwordHistorySize = value[3]
        # true：账户锁定阈值小于等于3 -1：执行异常未找到数据
        hunter.LockoutBadCount = value[4]
        # true：锁定时间不小于15分钟 -1：账户锁定阈值未启用或执行异常未找到数据
        hunter.LockoutDuration = value[5]
        if hunter.LockoutBadCount:
            hunter.bl0005_1 = True
            if hunter.LockoutDuration:
                hunter.bl0005_2 = True
        else:
            hunter.bl0005_1 = False
            hunter.bl0005_2 = False

        # (bl0006) true ：guest账户已禁用 false: guest账户启用
        hunter.guestAccount = bl0006(winrm_wrapper)
        # (bl0010) true：uac符合要求 false：不符合要求  UAC等级（4： 最高等级 3：默认等级 2：第二级 1：关闭UAC -1：查询异常）
        hunter.checkUAC = bl0010(winrm_wrapper)
        # （bl10011）true : 启用远程桌面 false ：未启用远程桌面  -1 ：查询异常
        hunter.checkRemoteDesktop = bl0011(winrm_wrapper)
        # (bl10012)true : 启用NLA false ：未启用NLA -1 ：查询异常
        hunter.checkNLA = bl0012(winrm_wrapper)
        # (bl10013)true：已开启登录审计 false：未开启 1,2 : 未全部启用了记录账户登录事件的审计（false） 3 ：启用记录账户登录事件的审计（true） 0：未启用记录账户登录事件的审计（false）
        hunter.checkIsRecordLoginEvents = bl01ToBl05AndBl013(winrm_wrapper)[6]
        # (bl10014)true: 已禁止用户匿名枚举 false ：未禁止
        hunter.checkIsAllowEnumerateResources = bl0014(winrm_wrapper)
        # 巡检所有用户（bl006,007， 008,bl1034）
        hunter.userList, user_hunter_List, login_user_list = selectAuthority(login_user_list, specialAccountList, winrm_wrapper,
                                                            hunter, value[8])
        # # (bl0007) true ：管理员账户名不为administrator false：为administrator
        admin, adminGroup = bl0007(winrm_wrapper)
        # (bl0008) true：无未使用用户 false：存在未使用用户
        # hunter.longUnUsed = bl0008(specialAccountList, winrm_wrapper)
        # (bl0009) true:权限无变化 false：发生变化
        checkUserAuthority = True
        if lastUserList:
            checkUserAuthority = bl0009(lastUserList, hunter.userList)
        if not checkUserAuthority and lastUserList:
            # (权限变更详情)
            user_hunter_List = selectAuthorityChanges(lastUserList, hunter.userList, user_hunter_List)
        # ===========log=============
        # 查看指定事件id的日志
        hunter.Logs, result_login_dict = checkLogs(winrm_wrapper, result_queue)
        # ===========log============
        # BL1026检查结果
        bl1026(hunter.Logs, hunter.passwordComplexity, hunter.minimumPasswordLength,
               hunter.minimumPasswordAge, hunter.maxPasswordAge, user_hunter_List)
        # 使用空密码的本地账户只允许进行控制台登录  true:已启用  false：已禁用
        # nullPasswordAccount = bl1027(winrm_wrapper)
        # #true:用户都有主目录 false：存在用户缺失主目录
        # hunter.userDirectory = bl1027_userDirectory(specialAccountList, winrm_wrapper)
        # BL1027检查结果
        login_user_list = checkBl1027(login_user_list, winrm_wrapper, hunter.userList, hunter.Logs, user_hunter_List, data_map, result_login_dict)
        login_user_list = deduplicate_keep_order(login_user_list)
        # bl1028检查结果
        bl1028(winrm_wrapper, admin, adminGroup, hunter.userList, hunter.Logs, user_hunter_List)
        # # BL1029检查结果
        # bl1029(winrm_wrapper, hunter.Logs, user_hunter_List)
        # # BL1030检查结果
        # bl1030(winrm_wrapper, nullPasswordAccount, hunter.Logs, specialAccountList, user_hunter_List, hunter.userList)
        # # BL1031检查结果
        # bl1031(hunter.Logs, user_hunter_List)
        # bl1032(hunter.Logs, user_hunter_List)
        print("=========账号安全检查执行完毕，即将返回数据")
        if len(login_user_list) > 100:
            login_user_list = login_user_list[:100]
        return user_hunter_List, hunter.userList, login_user_list
    except Exception as ex:
        common.logger.error("程序执行异常" , ex)
        raise ex

def getVersion(winrm_wrapper):
    result = winrm_wrapper.execute_powershell("Get-WmiObject -Class Win32_OperatingSystem | Select-Object Caption,Version")
    if result.get('std_out'):
        for line in result.get('std_out').splitlines():
            if "Windows" in line:
                return line
            else:
                return "-"
    else:
        return "-"

def bl1026(logs, passwordComplexity, minimumPasswordLength, minimumPasswordAge, maxPasswordAge, user_hunter_List):
    if passwordComplexity:
        for user_hunter in user_hunter_List:
            user_hunter.bl1026_1 = True
    if minimumPasswordLength:
        for user_hunter in user_hunter_List:
            user_hunter.bl1026_2 = True
    if minimumPasswordAge:
        for user_hunter in user_hunter_List:
            user_hunter.bl1026_4 = True
    if maxPasswordAge:
        for user_hunter in user_hunter_List:
            user_hunter.bl1026_3 = True
    for log in logs:
        if log.event_id in ['4724', '4723']:
            for user_hunter in user_hunter_List:
                if user_hunter.userName == log.accountName:
                    user_hunter.bl1026_5 = True


def checkLogs(winrm, result_queue):
    """
    4723 : 尝试修改密码
    4724 ：尝试重置密码
    4670 ：权限更改
    4732 ：添加安全组
    4625 ：登录失败
    4769 ：通过Kerberos身份验证请求的失败
    4648 ：显式凭据登录
    4724 ：重置密码
    4624 : 账户登录
    4625 ：登录失败
    4647 : 用户主动注销
    4634 ： 账户退出
    """

    try:
        ps_script = '''
 $startTime = (Get-Date).AddDays(-30)
 Get-WinEvent -FilterHashtable @{LogName='Security'; Id=@(4723, 4724, 4624); StartTime=$startTime} -MaxEvents 10000 |
Select-Object @{Name='EventID'; Expression={$_.Id}},
              @{Name='TimeGenerated'; Expression={$_.TimeCreated}},
              @{Name='SourceName'; Expression={$_.ProviderName}},
              @{Name='Message'; Expression={$_.Message}},
              @{Name='Keywords'; Expression={$_.Keywords}}
        '''
        scripts_list = split_logs_by_time()
        events = []
        futures = []
        result_login_dict = {}
        lines = ''
        reconnect(winrmList)
        with concurrent.futures.ThreadPoolExecutor(max_workers=work_thread_num) as executor:
            # 多线程获取日志
            for i in range(work_thread_num):
                if speed == 1:
                    futures.append(executor.submit(thread_get_logs, scripts_list[i], winrmList[i]))
                else:
                    futures.append(executor.submit(thread_get_logs, scripts_list[i], winrmList[0]))
            for future in concurrent.futures.as_completed(futures):
                lines += future.result()

            futures.clear()
            # 将单个日志封装为list，再将全部日志分隔为n份,分为n个进程进行执行
            result = split_into_n(lines.split('Keywords'), work_thread_num)
            # 检测是否超时
            check_overtime(result_queue, "日志分析中")

            # 多线程解析日志
            for i in range(work_thread_num):
                futures.append(executor.submit(analystLog, result[i]))
            for future in concurrent.futures.as_completed(futures):
                # 获取每个线程的返回值
                result_from_thread, log_dict = future.result()
                events.extend(result_from_thread)
                result_login_dict.update(log_dict)
    except Exception as ex:
        raise ex
    # for i in events:
    #     print(i.event_id +" "+ i.accountName +"  " +i.ip)
    return events, result_login_dict

def analystLog(logs):
    lines = 'Keywords'.join(logs)
    events = []
    logger = None
    message_flag = False
    get_flag = False
    log_dict = {}
    for line in lines.splitlines():
        # 保存日志基本信息
        if "EventID" in line:
            logger = log()
            logger.event_id = line.split(":")[1].strip()
            continue
        if "TimeGenerated" in line:
            logger.time_generated = ":".join(line.split(":")[1:]).strip()
            continue
        if "SourceName" in line:
            logger.source_name = line.split(":")[1]
            continue
        if "An account was successfully logged on" in line or "Message       :" in line:
            message_flag = True
        # 4624 登录日志分析
        if "New Logon:" in line and message_flag and int(logger.event_id) == 4624:
            get_flag = True
            continue
        if logger and int(logger.event_id) == 4624 and get_flag and message_flag:
            if "Account Name" in line and line.split(":")[1].strip() and "Network Account Name" not in line:
                logger.accountName = line.split(":")[1].strip()
                continue
            if "Source Network Address" in line and line.split(":")[1].strip():
                logger.ip = line.split(":")[1].strip()
                get_flag = False
                continue
        # 4724，4723 改密日志分析
        if "Target Account:" in line and message_flag and (
                int(logger.event_id) == 4724 or int(logger.event_id) == 4723):
            get_flag = True
            continue
        if logger and (int(logger.event_id) == 4724 or int(logger.event_id) == 4723) and get_flag and message_flag:
            if "Account Name" in line and line.split(":")[1].strip():
                logger.accountName = line.split(":")[1].strip()
                get_flag = False
                continue
        # 结束标识
        if "Keywords" in line:
            message_flag = False
            get_flag = False
            logger.keywords = line.split(":")[1]
            events.append(logger)
            # 创建登录字典，用于快速判断登录账户
            if logger.accountName not in log_dict and int(logger.event_id) == 4624:
                log_dict[logger.accountName] = logger
            logger = None
            continue
        if message_flag:
            # logger.message.append(line.strip())
            continue
    return events, log_dict


"""
list去重（不改变原顺序）
"""
def deduplicate_keep_order(lst):
    seen = set()
    result = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

"""
将数组分为n份
"""
def split_into_n(arr, n):
    length = len(arr)
    k, r = divmod(length, n)
    result = []
    start = 0
    for i in range(n):
        end = start + k + (1 if i < r else 0)
        result.append(arr[start:end])
        start = end
    return result

def split_into_two(arr):
    n = len(arr)
    k, r = divmod(n, 2)
    result = []
    start = 0
    for i in range(2):
        end = start + k + (1 if i < r else 0)
        result.append(arr[start:end])
        start = end
    return result

def checkBl1027(login_user_list, winrm, userList, logs, user_hunter_List, data_map, result_login_dict):
    # 测试账户关键词
    test_keywords = ["test", "temp", "dev", "debug", "qa", "demo", "guest"]
    try:
        time = winrm.execute_powershell(f"get-Date -Format 'yyyy/MM/dd'")
        if not time.get('std_out'):
            raise RuntimeError(f"Bl1027 get Date error: {time['std_err']}")
        now = datetime.strptime(time['std_out'].strip(), "%Y/%m/%d")
    except Exception as ex:
        common.logger.error(f"checkBl1027 Error occurred: {repr(ex)}")
        raise ex
    try:
        for user in userList:
            if re.search(r'(' + '|'.join(test_keywords) + r')', user.name, re.IGNORECASE) and user.active:
                for user_hunter in user_hunter_List:
                    if user_hunter.userName == user.name:
                        user_hunter.bl1027_2 = False
                        continue
                continue
            if user.lastLogon == "Never" or "从" in user.lastLogon:
                for user_hunter in user_hunter_List:
                    if user_hunter.userName == user.name:
                        user_hunter.bl1027_1 = False
                        continue
                continue
            if "Never" in user.lastLogon:
                for user_hunter in user_hunter_List:
                    if user_hunter.userName == user.name:
                        user_hunter.bl1027_1 = False
                        continue
            else:
                lastLogonTime = datetime.strptime(user.lastLogon, "%Y/%m/%d %H:%M:%S")
                if (now - lastLogonTime).days > 90:
                    for user_hunter in user_hunter_List:
                        if user_hunter.userName == user.name:
                            user_hunter.bl1027_1 = False
                            continue
                    continue
    except Exception as ex:
        common.logger.error(f"Bl1027处理异常: {repr(ex)}")
        raise ex
    # 检测最近是否有过登录记录
    log_loginUserInfo = []
    original_format = "%Y/%m/%d %H:%M:%S"
    target_format = "%Y-%m-%d %H:%M:%S"
    for log in logs:
        #SYSTEM是系统、具有最高权限的账号，排除在外
        if log.event_id in ['4624'] and log.accountName and log.accountName != 'SYSTEM':
            if log.ip == "-":
                continue
            # 解析原始字符串为 datetime 对象
            if log.time_generated:
                datetime_object = datetime.strptime(log.time_generated, original_format)
                # 格式化 datetime 对象为目标格式的字符串
                log.time_generated = datetime_object.strftime(target_format)
                log_loginUserInfo.append(f"{log.accountName},{log.ip},{log.time_generated}")
    for user_hunter in user_hunter_List:
        if user_hunter.userName not in result_login_dict:
            user_hunter.bl1027_4 = False
    login_user_list = login_user_list + log_loginUserInfo
    return login_user_list


def bl1027_userDirectory(specialAccountList, winrm):
    try:
        userList = SelectUserNameList(specialAccountList, winrm)
        for user in userList:
            try:
                result = winrm.execute_powershell(f'net user "{user}"')
                if result.get('std_err') not in ['', None]:
                    raise RuntimeError(f"select {user} info error: {result['std_err']}")
                for line in result['std_out'].splitlines():
                    if "主目录" in line or "Home directory" in line:
                        if line.strip() == "主目录" or line.strip() == "Home directory":
                            return False
            except Exception as ex:
                common.logger.error(f"bl1027_userDirectory Error occurred: {repr(ex)}")
                raise ex
        return True
    except Exception as ex:
        common.logger.error(f"Error occurred: {repr(ex)}")
        raise ex


def bl1027(winrm):
    try:
        result = winrm.execute_powershell(
            "reg query HKLM\SYSTEM\CurrentControlSet\Control\Lsa /v LimitBlankPasswordUse")
        if result.get('std_err') not in ['', None]:
            raise RuntimeError(f"select Guest Account error: {result['std_err']}")
        if result.get('std_out') not in ['', None]:
            for line in result['std_out'].splitlines():
                if "LimitBlankPasswordUse" in line:
                    if "0x1" in line:
                        return True
                    elif "0x0" in line:
                        return False
    except Exception as ex:
        common.logger.error(f"Error occurred: {repr(ex)}")
        raise ex


def bl1028(winrm, admin, adminGroup, userList, logs, user_hunter_List):
    try:
        # 检查管理员组内是否有普通账户
        result = winrm.execute_powershell(f'net localgroup {adminGroup}')
        flag = 0
        if not result.get('std_out'):
            raise RuntimeError(f"select local Group error in bl1028: {result['std_err']}")
        if result.get('std_out'):
            for line in result['std_out'].splitlines():
                if "---------" in line:
                    flag = 1
                    continue
                if "命令成功完成" in line or "The command completed successfully" in line:
                    flag = 0
                if flag == 1:
                    for user_hunter in user_hunter_List:
                        if user_hunter.userName in line:
                            user_hunter.bl1028_1 = False
        # 检查用户工作目录权限是否仅管理员组，系统账户，用户自己有读写权限，其余用户只拥有读、执行权限
        for user in userList:
            if user.authority:
                for line in user.authority.split():
                    if adminGroup in line.strip() or user.name in line.strip() or "AUTHORITY\SYSTEM" in line.strip():
                        continue
                    # 避免users组拥有过高权限
                    if "\\Users" in line.strip() and not any(
                            rights in line.strip() for rights in ["(F)", "(M)", "(WO)", "(WDAC)", "(D)"]):
                        for user_hunter in user_hunter_List:
                            if user_hunter.userName == user.name:
                                user_hunter.bl1028_2 = False
                    # 避免Authenticated Users组拥有过高权限
                    if "Authenticated Users" in line.strip() and not any(
                            rights in line.strip() for rights in ["(F)", "(M)", "(WO)", "(WDAC)", "(D)"]):
                        for user_hunter in user_hunter_List:
                            if user_hunter.userName == user.name:
                                user_hunter.bl1028_2 = False
    except Exception as ex:
        common.logger.error(f"Error occurred: {repr(ex)}")
        raise ex


def bl1029(winrm, logs, user_hunter_List):
    ip_user = {}
    login_fail_count = {}
    lastLoginTime = None
    lastLoginTime_k = None
    targetUser = None
    flag = 0
    loginIp = None
    for log in logs:
        # 检查是否五分钟内连续两次登录失败
        if str(log.event_id) in ['4625']:
            if log.accountName not in login_fail_count:
                login_fail_count[log.accountName] = 1
            else:
                login_fail_count[log.accountName] += 1
            if login_fail_count[log.accountName] > 3:
                for user_hunter in user_hunter_List:
                    if user_hunter.userName == log.accountName:
                        user_hunter.bl1029 = False
            # loginTime = datetime.strptime(log.time_generated, "%Y/%m/%d %H:%M:%S")
            # if not lastLoginTime and lastLoginTime - loginTime < timedelta(minutes=5):
            #     return False
            # lastLoginTime = loginTime

        # 检查是否存在一个ip登录多个账户
        if str(log.event_id) in ['4648']:
            # 检查是否非工作时间登录
            logTime = datetime.strptime(log.time_generated, "%Y/%m/%d %H:%M:%S")
            if 0 <= logTime.hour < 7:
                for user_hunter in user_hunter_List:
                    if user_hunter.userName == log.accountName:
                        user_hunter.bl1029 = False
            for line in log.message:
                if "Account Whose Credentials Were Used:" in line:
                    flag = 1
                if flag == 1 and "Account Name" in line:
                    targetUser = line.split(":")[1].strip()
                    flag = 0
                if "Network Address" in line or "源网络地址" in line:
                    loginIp = line.split(":")[1].strip()
            if loginIp not in ip_user:
                ip_user[loginIp] = targetUser
            elif ip_user[loginIp] != targetUser:
                for user_hunter in user_hunter_List:
                    if user_hunter.userName == log.accountName:
                        user_hunter.bl1029 = False
        # 检查是否存在Kerberos 服务票据请求失败事件
        if str(log.event_id) in ['4769']:
            # loginTime_k = datetime.strptime(log.time_generated, "%Y/%m/%d %H:%M:%S")
            # if not lastLoginTime_k and lastLoginTime_k - loginTime_k < timedelta(minutes=5):
            #     return False
            # lastLoginTime_k = loginTime_k
            for line in log.message:
                if "Account Name" in line:
                    for user_hunter in user_hunter_List:
                        if user_hunter.userName == log.accountName:
                            user_hunter.bl1029 = False


def bl1030(winrm, nullPasswdAccount, logs, specialAccountList, user_hunter_List, userList):
    try:
        # userList = SelectUserNameList(specialAccountList, winrm)
        code = None
        subCode = None
        # 检查有无空密码用户
        for user in userList:
            result = winrm.execute_powershell(f'net user "{user.name}"')
            if result.get('std_err') not in ['', None]:
                raise RuntimeError(f"select user info error: {result['std_err']}")
            for line in result['std_out'].splitlines():
                if "需要密码" in line:
                    if line.split()[1] == "No":
                        for user_hunter in user_hunter_List:
                            if user_hunter.userName == user.name:
                                user_hunter.bl1030 = False
                if "Password required" in line:
                    if line.split()[1] != "是":
                        for user_hunter in user_hunter_List:
                            if user_hunter.userName == user.name:
                                user_hunter.bl1030 = False
        # 检查是否开启使用空密码的本地账户只允许进行控制台登录
        if not nullPasswdAccount:
            for user_hunter in user_hunter_List:
                user_hunter.bl1030 = False
        # 检查日志有无空密码登录，重置密码操作事件
        count = 0
        user_fail_log = {}
        for log in logs:
            if str(log.event_id) in ['4625']:
                flag = 0
                for line in log.message:
                    if "Status" in line and flag == 0:
                        flag = 1
                        code = line.split(":")[1].strip()
                    if "Status" in line and flag == 1:
                        subCode = line.split(":")[1].strip()
                # 账户名或密码错误
                if code == "0xC0000064" or code == "0xC000006A":
                    if log.accountName not in user_fail_log:
                        user_fail_log[log.accountName] = 1
                    else:
                        user_fail_log[log.accountName] += 1
                        if user_fail_log[log.accountName] > 3:
                            for user_hunter in user_hunter_List:
                                if user_hunter.userName == log.accountName:
                                    user_hunter.bl1030 = False
            if str(log.event_id) in ['4724']:
                for user_hunter in user_hunter_List:
                    if user_hunter.userName == log.accountName:
                        user_hunter.bl1030 = False

    except Exception as ex:
        common.logger.error(f"Error occurred: {repr(ex)}")
        raise ex
    return True


def bl1031(logs, user_hunter_List):
    user_ip = {}
    flag = 0
    for log in logs:
        if str(log.event_id) in ['4624']:
            for line in log.message:
                if "Source Network Address" in line:
                    ip = line.split(":")[1].strip()
                if "New Logon" in line:
                    flag = 1
                if flag == 1 and "Account Name" in line:
                    userName = line.split(":")[1].strip()
                    flag = 0
            if userName not in user_ip:
                user_ip[userName] = ip
            if user_ip[userName] != ip:
                for user_hunter in user_hunter_List:
                    if user_hunter.userName == log.accountName:
                        user_hunter.bl1031 = False
                    if not user_hunter.guestAccount:
                        user_hunter.bl1031 = False


def bl1032(logs, user_hunter_List):
    user_ip = {}
    ip_user = {}
    flag = 0
    for log in logs:
        if str(log.event_id) in ['4624']:
            for line in log.message:
                if "Source Network Address" in line:
                    ip = line.split(":")[1].strip()
                if "New Logon" in line:
                    flag = 1
                if flag == 1 and "Account Name" in line:
                    userName = line.split(":")[1].strip()
                    flag = 0
                if not ipaddress.ip_address(ip).is_private:
                    for user_hunter in user_hunter_List:
                        if user_hunter.userName == log.accountName:
                            user_hunter.bl1032 = False
                if userName not in user_ip:
                    user_ip[userName] = ip
                if user_ip[userName] != ip:
                    for user_hunter in user_hunter_List:
                        if user_hunter.userName == log.accountName:
                            user_hunter.bl1032 = False
                if ip not in ip_user:
                    ip_user[ip] = userName
                elif ip_user[ip] != userName:
                    for user_hunter in user_hunter_List:
                        if user_hunter.userName == log.accountName:
                            user_hunter.bl1032 = False


def bl01ToBl05AndBl013(winrm):
    exportPath = "C:\\secpol_export.inf"
    try:
        # 导出安全配置
        export = winrm.execute_command(f"secedit /export /cfg {exportPath}")
        if export.get('std_err'):
            raise RuntimeError(f"file export error: {export['std_err']}")
    except Exception as ex:
        common.logger.error(f"导出配置文件错误: {repr(ex)}")
        raise ex
    try:
        result = winrm.execute_powershell(f"Get-Content {exportPath}")
        if not result.get('std_out'):
            raise RuntimeError(f"read file error: {result['std_err']}")
    except Exception as ex:
        common.logger.error(f"读取配置文件错误: {repr(ex)}")
        raise ex
    try:
        value = [-1] * 9
        for line in result['std_out'].splitlines():
            if "PasswordComplexity" in line:
                value[0] = True if int(line.split("=")[1].strip()) == 1 else False
            elif "MinimumPasswordLength" in line and "\\" not in line:
                value[1] = True if int(line.split("=")[1].strip()) >= 8 else False
            elif "MinimumPasswordAge" in line:
                value[2] = True if int(line.split("=")[1].strip()) >= 1 else False
            if "PasswordHistorySize" in line:
                value[3] = True if int(line.split("=")[1].strip()) >= 5 else False
            if "LockoutBadCount" in line:
                value[4] = True if int(line.split("=")[1].strip()) <= 5 else False
            if "LockoutDuration" in line:
                value[5] = True if int(line.split("=")[1].strip()) >= 15 else False
            if "AuditAccountLogon" in line:
                value[6] = True if int(line.split("=")[1].strip()) == 3 else False
            if "MaximumPasswordAge" in line and '\\' not in line:
                value[8] = line.split("=")[1].strip()
                value[7] = True if int(line.split("=")[1].strip()) <= 90 else False
        delResult = winrm.execute_command(f"del {exportPath}")
        if delResult.get('std_err'):
            raise RuntimeError(f"del file error: {delResult['std_err']}")
    except Exception as ex:
        common.logger.error(f"Error occurred: {repr(ex)}")
        raise ex

    return value


def bl0006(winrm):
    try:
        result = winrm.execute_powershell("net user guest")
        if not result.get('std_out'):
            raise RuntimeError(f"select Guest Account error: {result['std_err']}")
        if result.get('std_out'):
            for line in result['std_out'].splitlines():
                if "account active" in line.lower() or "账户启用" in line:
                    if "No" in line:
                        return True
                    elif "Yes" in line:
                        return False
    except Exception as ex:
        common.logger.error(f"Error occurred: {repr(ex)}")
        raise ex


def bl0007(winrm):
    try:
        admin = None
        adminGroup = None
        result = winrm.execute_powershell("wmic group where \"SID = 'S-1-5-32-544'\" get Name")
        if not result.get('std_out'):
            raise RuntimeError(f"select administrator error: {result['std_err']} ")
        for line in result['std_out'].splitlines():
            if "Name" not in line and line.strip():
                adminGroup = line.strip()
        result = winrm.execute_powershell(f"wmic useraccount where \"SID like 'S-1-5-21-%-500'\" get Name")
        if not result.get('std_out'):
            raise RuntimeError(f"select administrator error: {result['std_err']} ")
        for line in result['std_out'].splitlines():
            if "Name" not in line and line.strip():
                admin = line.strip()
    except Exception as ex:
        common.logger.error(f"Error occurred: {repr(ex)}")
        raise ex
    if admin != "Administrator" and adminGroup != "Administrators":
        return admin, adminGroup
    return admin, adminGroup


def SelectUserNameList(specialAccountList, winrm):
    flag = 0
    userList = []
    result = winrm.execute_powershell(
        """
        net user | ForEach-Object {
            $users = $_ -split '\\s{2,}'
            $users | ForEach-Object {
                "[" + $_ + "]"
            }
        }
        """
    )
    for line in result['std_out'].splitlines():
        if "-]" in line:
            flag = 1
            continue
        if "The command completed with one or more errors" in line or "The command completed successfully" in line:
            flag = 0
        elif flag == 1:
            if analysis_account_array:
                if line.strip("[]") and line.strip("[]") not in specialAccountList and (line.strip("[]") in analysis_account_array or line.strip("[]").lower() in analysis_account_array):
                    userList.append(line.strip("[]"))
            else:
                #===============自测内容===================
                # if line.strip("[]") and line.strip("[]") not in specialAccountList:
                #     userList.append(line.strip("[]"))
                #=========================================

                #================上线版=====================
                return userList
                #==========================================
    return userList


def bl0008(specialAccountList, winrm):
    try:
        userList = SelectUserNameList(specialAccountList, winrm)
        for user in userList:
            result = winrm.execute_powershell(f'net user "{user}"')
            if not result.get('std_out'):
                raise RuntimeError(f"select {user} logon error: {result['std_err']}")
            for line in result['std_out'].splitlines():
                if "last logon" in line.lower() and "never" in line.lower():
                    return False
                elif "上次登录" in line and "从不" in line:
                    return False
    except Exception as ex:
        common.logger.error(f"Error occurred: {repr(ex)}")
        raise ex
    return True


def selectAuthority(login_user_list, specialAccountList, winrm, hunter, maxPwdAge):
    try:
        userNameList = SelectUserNameList(specialAccountList, winrm)
        userList = []
        user_hunter_List = []
        #记录登录用户
        log_user = []
        #获取当前时间
        now = winrm.execute_powershell(f'Get-Date -Format "yyyy/MM/dd"')
        rightNow = datetime.strptime(now.get('std_out').strip(), "%Y/%m/%d")
        for user in userNameList:
            user_hunter = copy.deepcopy(hunter)
            result = winrm.execute_powershell(f'net user "{user}"')
            if not result.get('std_out'):
                raise RuntimeError(f"select {user} error: {result['std_err']}")
            u = User()
            u.name = user
            user_hunter.userName = user
            if u.name.lower() == "administrator":
                user_hunter.adminAccount = False
            else:
                user_hunter.adminAccount = True
            for line in result['std_out'].splitlines():
                if 'account expires' in line.lower():
                    if 'never' in line.lower():
                        user_hunter.accountExpires = '从不'
                    else:
                        user_hunter.accountExpires = line.split(maxsplit = 2)[2].strip()
                elif '帐户到期' in line:
                    user_hunter.accountExpires = line.split(maxsplit=1)[1].strip()
                if "local group memberships" in line.lower():
                    u.localGroup = " ".join(line.split()[3:])
                if "本地组成员" in line:
                    u.localGroup = " ".join(line.split()[1:])
                if "global group memberships" in line.lower():
                    u.globalGroup = " ".join(line.split()[3:])
                if "全局组成员" in line:
                    u.globalGroup = " ".join(line.split()[1:])
                if "home directory" in line.lower():
                    parts = line.split()
                    if len(parts) > 2:  # 确保至少有3个元素，避免索引越界
                        u.homeDirectory = parts[2]
                    else:
                        u.homeDirectory = None  # 目录为空，防止后续操作报错
                    if u.homeDirectory:  # 进一步确保 homeDirectory 非空
                        authResult = winrm.execute_powershell(f'icacls "{u.homeDirectory}"')
                        if f'{u.homeDirectory}' not in authResult.get('std_out'):
                            u.authority = None
                        else:
                            u.authority = authResult.get('std_out')
                if "主目录" in line.lower():
                    parts = line.split()
                    if len(parts) > 1:  # 确保至少有3个元素，避免索引越界
                        u.homeDirectory = parts[1]
                    else:
                        u.homeDirectory = None  # 目录为空，防止后续操作报错
                    if u.homeDirectory:  # 进一步确保 homeDirectory 非空
                        authResult = winrm.execute_powershell(f'icacls "{u.homeDirectory}"')
                        if f'icacls "{u.homeDirectory}"' not in authResult.get('std_out'):
                            u.authority = None
                        else:
                            u.authority = authResult.get('std_out')
                if "last logon" in line.lower():
                    u.lastLogon = line.split(maxsplit = 2)[2]
                    u.logonTime_detail = line.split(maxsplit = 2)[2].strip()
                    user_hunter.lastLogonTime = u.logonTime_detail
                elif "上次登录" in line.lower():
                    u.lastLogon = line.split(maxsplit=1)[1].strip()
                    u.logonTime_detail = line.split(maxsplit=1)[1].strip()
                if u.lastLogon:
                    if "never" in u.lastLogon.lower() or "从" in u.lastLogon.lower():
                        user_hunter.longUnUsed = False
                    else:
                        user_hunter.longUnUsed = True
                        if u.name not in log_user and u.logonTime_detail and isinstance(u.logonTime_detail, str):
                            original_format = "%Y/%m/%d %H:%M:%S"
                            target_format = "%Y-%m-%d %H:%M:%S"
                            datetime_object = datetime.strptime(u.logonTime_detail, original_format)
                            # 格式化 datetime 对象为目标格式的字符串
                            str_logon_log = f'{u.name},-,{datetime_object.strftime(target_format)}'
                            login_user_list.append(str_logon_log)
                            if user_hunter.log_count <=10:
                                if user_hunter.loginLog == '':
                                    user_hunter.loginLog += str_logon_log
                                else:
                                    user_hunter.loginLog += '\n'+ str_logon_log
                                user_hunter.log_count += 1
                            log_user.append(u.name)
                if "account active" in line.lower() or "账户启用" in line:
                    if "No" in line:
                        u.active = False
                    elif "Yes" in line:
                        u.active = True
                #bl1034 长期未改密(超过90天未改密)
                if "上次设置密码" in line:
                    user_hunter.bl1026_5 = checkPwd(90, line.split()[1], rightNow)
                    user_hunter.lastPwdsetTime = line.split()[1]
                elif "Password last set" in line:
                    user_hunter.bl1026_5 = checkPwd(90, line.split()[3], rightNow)
                    user_hunter.lastPwdsetTime = line.split()[3]
            if not u.homeDirectory:
                user_hunter.bl1027_3 = False
            findCreateTimeScripts =  f'(Get-Item "C:\\Users\\{user_hunter.userName}").CreationTime.ToString("F", [System.Globalization.CultureInfo]::InvariantCulture)'
            createTimeInfo = winrm.execute_powershell(findCreateTimeScripts)
            if createTimeInfo.get('std_out'):
                user_hunter.createTime = createTimeInfo.get('std_out')
            else:
                user_hunter.createTime = '-'
            userList.append(u)
            user_hunter_List.append(user_hunter)
    except Exception as ex:
        common.logger.error(f"Error occurred: {repr(ex)}")
        raise ex
    return userList, user_hunter_List, login_user_list

def checkPwd(maxPwdAge, time, rightNow):
    date_obj = datetime.strptime(time, '%Y/%m/%d')
    if (rightNow - date_obj).days > int(maxPwdAge):
        return False
    else:
        return True


def bl0009(lastUserList, userList):
    return len(lastUserList) == len(userList) and all(
        any(
            user.name == lastUser.name
            and user.authority == lastUser.authority
            and user.localGroup == lastUser.localGroup
            and user.homeDirectory == lastUser.homeDirectory
            and user.globalGroup == lastUser.globalGroup
            for lastUser in lastUserList
        )
        for user in userList
    )


def selectAuthorityChanges(lastUserList, userList, user_hunter_List):
    # 校验用户名是否发生更改
    checked = []
    for user in userList:
        for userLast in lastUserList:
            response = ''
            if user.name == userLast.name:
                # 将对比的两个对象加入已检查列表
                checked.append(user)
                checked.append(userLast)
                # 校验主目录是否发生变更
                if user.homeDirectory != userLast.homeDirectory:
                    if not user.homeDirectory:
                        user.homeDirectory = "空"
                    if not userLast.homeDirectory:
                        userLast.homeDirectory = "空"
                    response += f"用户“{user.name}”主目录由“{userLast.homeDirectory}”变更为“{user.homeDirectory}” "
                # 校验本地组
                if user.localGroup and userLast.localGroup and user.localGroup != userLast.localGroup:
                    removed_groups = [item for item in userLast.localGroup.split() if
                                      item not in user.localGroup.split()]
                    add_Groups = [item for item in user.localGroup.split() if
                                  item not in userLast.localGroup.split()]
                    if removed_groups and removed_groups != ["*None"]:
                        for dif in removed_groups:
                            if dif.strip():
                                response += f"用户“{user.name}”不再属于本地组{dif} "
                    elif removed_groups == ["*None"]:
                        response += f"用户“{user.name}”本地组不再为空 "
                    if add_Groups and removed_groups != ["*None"]:
                        for dif in add_Groups:
                            response += f"用户“{user.name}”被添加进本地组{dif} "
                    elif add_Groups == ["*None"]:
                        response += f"用户“{user.name}”本地组变更为空 "
                # 校验全局组
                if user.globalGroup and userLast.globalGroup and user.globalGroup != userLast.globalGroup:
                    removed_groups = [item for item in userLast.globalGroup.split() if
                                      item not in user.globalGroup.split()]
                    add_Groups = [item for item in user.globalGroup.split() if
                                  item not in userLast.globalGroup.split()]
                    if removed_groups and removed_groups != ["*None"]:
                        for dif in removed_groups:
                            if dif.strip():
                                response += f"用户“{user.name}”不再属于全局组{dif}"
                    elif removed_groups == ["*None"]:
                        response += f"用户“{user.name}”全局组不再为空 "
                    if add_Groups and removed_groups != ["*None"]:
                        for dif in add_Groups:
                            response += f"用户“{user.name}”被添加进全局组{dif} "
                    elif add_Groups == ["*None"]:
                        response += f"用户“{user.name}”全局组变更为空 "
            for user_hunter in user_hunter_List:
                if user_hunter.userName == user.name and response:
                    user_hunter.checkUserAuthority = False
                    user_hunter.authorityChangeDetail = response
    # if [item for item in lastUserList if item not in checked]:
    #     for dif in [item for item in lastUserList if item not in checked]:
    #         response += f"用户“{dif.name}”用户名发生变化或用户被删除 "
    if [item for item in userList if item not in checked]:
        for dif in [item for item in userList if item not in checked]:
            for user_hunter in user_hunter_List:
                if user_hunter.userName == dif.name:
                    user_hunter.checkUserAuthority = False
                    user_hunter.authorityChangeDetail += f"新增用户或有用户名变更为“{dif.name}”"
    return user_hunter_List


def bl0010(winrm):
    try:
        ConsentPromptBehaviorAdmin = -1
        PromptOnSecureDesktop = -1
        uac = -1
        result = winrm.execute_powershell(
            'Get-ItemProperty -Path "HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" -Name ConsentPromptBehaviorAdmin')
        if not result.get('std_out'):
            raise RuntimeError(f"select ConsentPromptBehaviorAdmin error: {result['std_err']}")
        for line in result['std_out'].splitlines():
            if "ConsentPromptBehaviorAdmin" in line:
                ConsentPromptBehaviorAdmin = line.split(":")[1].strip()
        result = winrm.execute_powershell(
            'Get-ItemProperty -Path "HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" -Name PromptOnSecureDesktop')
        if not result.get('std_out'):
            raise RuntimeError(f"select PromptOnSecureDesktop error: {result['std_err']}")
        for line in result['std_out'].splitlines():
            if "PromptOnSecureDesktop" in line:
                PromptOnSecureDesktop = line.split(":")[1].strip()
        # ConsentPromptBehaviorAdmin,PromptOnSecureDesktop不同值对应UAC不同等级
        # 2 ， 1 对应最高等级
        # 5 ， 1 对应默认等级
        # 5 ， 0 对应第二级
        # 0 ， 0 对应关闭UAC
        if ConsentPromptBehaviorAdmin == '2' and PromptOnSecureDesktop == '1':
            uac = 4
        if ConsentPromptBehaviorAdmin == '5' and PromptOnSecureDesktop == '1':
            uac = 3
        if ConsentPromptBehaviorAdmin == '5' and PromptOnSecureDesktop == '0':
            uac = 2
        if ConsentPromptBehaviorAdmin == '0' and PromptOnSecureDesktop == '0':
            uac = 1
        if uac == -1:
            return -1
        elif uac >= 3:
            return True
        else:
            return False
    except Exception as ex:
        common.logger.error(f"Error occurred: {repr(ex)}")
        raise ex


def bl0011(winrm):
    try:
        result = winrm.execute_powershell(
            'Get-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\Terminal Server" -Name fDenyTSConnections')
        if not result.get('std_out'):
            raise RuntimeError(f"select Remote desktop error: {result['std_err']}")
        for line in result['std_out'].splitlines():
            if "fDenyTSConnections" in line:
                if '0' in line:
                    return False
                else:
                    return True
    except Exception as ex:
        common.logger.error(f"Error occurred: {repr(ex)}")
        raise ex
    return -1


def bl0012(winrm):
    try:
        result = winrm.execute_powershell(
            'Get-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp" -Name UserAuthentication')
        if not result.get('std_out'):
            raise RuntimeError(f"select NLA error: {result['std_err']}")
        for line in result['std_out'].splitlines():
            if "UserAuthentication" in line:
                if '1' in line:
                    return True
                else:
                    return False
    except Exception as ex:
        common.logger.error(f"Error occurred: {repr(ex)}")
        raise ex
    return -1


def bl0014(winrm):
    try:
        result = winrm.execute_powershell(
            'Get-ItemProperty -Path "HKLM:\System\CurrentControlSet\Control\Lsa" -Name "RestrictAnonymous"')
        if not result.get('std_out'):
            raise RuntimeError(f"check Is Allow Enumerate Resources error: {result['std_err']}")
        for line in result['std_out'].splitlines():
            if "restrictanonymous" in line:
                if line.split(":")[1].strip() == "1":
                    return True
                else:
                    return False
    except Exception as ex:
        common.logger.error(f"Error occurred: {repr(ex)}")
        raise ex
    return -1


def search_assets_for_accounts(winRM_wrapper, paths, result_queue):
    response = []
    try:
        thread_name = random() * 100
        path_count = 0
        print(str(thread_name) + "线程开始时间" + str(datetime.now()))
        # 测试目录是否存在
        for path in paths:
            if not isinstance(path, str) :
                pass
            check_overtime(result_queue, "内嵌账号子任务搜索中")
            test_dir_command = "Test-Path -Path " + '"' + path + '"'
            exist = winRM_wrapper.execute_powershell(test_dir_command)
            if exist.get('std_out'):
                # 获取当前目录下可能含有内嵌账号的文件名与对应路径
                get_file_name = f'''
                Get-ChildItem -Path "{path}\\*" -Include {embeddedAccountCodeLib}| 
                Select-Object -ExpandProperty FullName
                '''
                try:
                    export = winRM_wrapper.execute_powershell(get_file_name)
                except Exception as ex:
                    winRM_wrapper.connect()
                    export = winRM_wrapper.execute_powershell(get_file_name)
                if export.get('std_out'):
                    file_list = export.get('std_out').splitlines()
                    for line in file_list:
                        if line.strip():
                            actual_path = line.strip()
                            path_count += 1
                            print("工作线程： ["+ str(thread_name)  + "],已查找"+ str(path_count) + "个文件" + actual_path)
                            # 检测所有扫描出来的文件
                            analyze_file_account_command = f'$filePath = "{actual_path}"' + '''
                                # 定义正则表达式模式
                                $patterns = @(
                                    "accessKeyId[:=]\s*([\w-]+)",
                                    "(?i).*corp(Id|Secret)=(\w+)",
                                    "(?i).*qq\.im\.(sdkappid|privateKey|identifier)=(.*)",
                                    "(?i)(?:user(?:name)?\s*[=:])\s*([^\s]+)",
                                    "(?:账户|账户名|用户名|账号|测试账户)\s*[=：:]*\s*([\\w@#!$%^&*-]{3,20})",
                                    "jdbc\.(driver|url|type)\s*=(.*)",
                                    "#jdbc\.(driver|url|type)\s*=(.*)"
                                )
    
                                # 检查文件是否存在
                                if (Test-Path $filePath) {
                                    # 读取文件内容
                                    $content = Get-Content -Path $filePath -Raw
    
                                    # 循环遍历每个正则表达式模式
                                    foreach ($pattern in $patterns) {
                                        # 使用正则表达式匹配文件内容
                                        $matches = [regex]::Matches($content, $pattern)
    
                                        # 输出匹配结果
                                        foreach ($match in $matches) {
                                            Write-Host "$($match.Groups[1].Value)"
                                        }
                                    }
                                } else {
                                    Write-Host "文件不存在：$filePath"
                                }
                                '''
                            result = winRM_wrapper.execute_powershell(analyze_file_account_command)
                            # global file_count
                            # file_count = file_count + 1
                            if result.get('std_out'):
                                analyze_file_passwd_command = f'$filePath = "{actual_path}"' + '''
                                # 定义正则表达式模式
                                $patterns = @(
                                    "accessKeySecret[:=]\s*([\w-]+)",
                                    "(?i)(?:pass(?:word)?\s*[=:])\s*([^\s]+)",
                                    "(?:默认口令|默认密码|口令|密码|测试密码)\s*[=：:]*\s*([\\w@#!$%^&*-]{3,20})"
                                )
    
                                # 检查文件是否存在
                                if (Test-Path $filePath) {
                                    # 读取文件内容
                                    $content = Get-Content -Path $filePath -Raw
    
                                    # 循环遍历每个正则表达式模式
                                    foreach ($pattern in $patterns) {
                                        # 使用正则表达式匹配文件内容
                                        $matches = [regex]::Matches($content, $pattern)
    
                                        # 输出匹配结果
                                        foreach ($match in $matches) {
                                            Write-Host "$($match.Groups[1].Value)"
                                        }
                                    }
                                } else {
                                    Write-Host "文件不存在：$filePath"
                                }
                                '''
                                result_passwd = winRM_wrapper.execute_powershell(analyze_file_passwd_command)
                                if result_passwd.get('std_out') and not actual_path in result_passwd.get('std_out'):
                                    response.append(
                                        f"{actual_path}!#!*{result.get('std_out')}!#!*{result_passwd.get('std_out')}")
        return response
    except Exception as e:
        common.logger.error("内嵌账号搜索异常" + repr(e))
        #程序超时
        if "脚本执行超时" in str(e):
            return response

def search_code(winRM_wrapper, disk):
    directory_path = []
    result_code = []
    try:
        select_code_script = f"""
        Get-ChildItem -Path '{disk}*' -Recurse -Include *.py,*.java,*.c,*.cpp,*.h,*.hpp,*.js,*.ts |
        Select-Object -ExpandProperty DirectoryName |
        Where-Object {{
            $_ -match 'src|service|controller|api|web|core|common|util|model|view|component|test|project'
        }} |
        Sort-Object -Unique
        """.strip()
        try:
            result_code = winRM_wrapper.execute_powershell(select_code_script)
        except Exception as e:
            winRM_wrapper.connect()
        if result_code.get('std_out'):
            for line in result_code.get('std_out').splitlines():
                directory_path.append(line)
    except Exception as e:
        common.logger.error("代码库扫描错误：" + repr(e))
        raise e
    return directory_path

def hunt_window_EnbededAccount(link, result_queue):
    try:
        winRM_wrapper = WinRMWrapper(link.host, link.userName, link.passwd)
        winRM_wrapper.connect()
        result = []
        start = datetime.now()
        directory_path = []
        #读取系统中所有磁盘
        select_disk_script = "Get-PSDrive -PSProvider FileSystem"
        disk_result = winRM_wrapper.execute_powershell(select_disk_script)
        disk_list = []
        if disk_result.get('std_out'):
            for line in disk_result.get('std_out').splitlines():
                if ':\\ ' in line:
                    for part in line.split():
                        if re.search(r'[A-Z]:\\', part):
                            disk_list.append(part)

        futures = []
        result_code = []
        reconnect(winrmList)
        if disk_list:
            with concurrent.futures.ThreadPoolExecutor(max_workers=work_thread_num) as executor:

                for index, disk in enumerate(disk_list):
                    if speed == 1:
                        futures.append(executor.submit(search_code, winrmList[index], disk))
                    else:
                        futures.append(executor.submit(search_code, winrmList[0], disk))

                for future in concurrent.futures.as_completed(futures):
                    try:
                        check_overtime(result_queue,"内嵌账号搜索准备中")
                        # 获取每个线程的返回值
                        result_from_thread = future.result()
                        if result_from_thread:
                            result_code.extend(result_from_thread)
                    except Exception as ex:
                        common.logger.error(f"代码库搜索错误 : {repr(ex)}")
                        raise ex
        if result_code:
            directory_path.extend(result_code)
        print("[thread]代码库搜索完毕,共计路径：" + str(len(directory_path)))
        search_c_path = 'Get-ChildItem -Path "C:\Program Files" -Recurse -Depth 5 | Select-Object -ExpandProperty FullName'
        c_result = winRM_wrapper.execute_powershell(search_c_path)
        if c_result.get('std_out'):
            directory_path.extend(c_result.get('std_out').splitlines())
        directory_path = list(set(directory_path))
        print("[thread]指定搜索路径已添加,共计路径：" + str(len(directory_path)))
        directory_path_list = split_into_n(directory_path, work_thread_num)
        futures = []
        # 重连，保证每个连接对象可用
        reconnect(winrmList)
        with concurrent.futures.ThreadPoolExecutor(max_workers=work_thread_num) as executor:

                for i in range(work_thread_num):
                    if speed == 1:
                        futures.append(executor.submit(search_assets_for_accounts, winrmList[i], directory_path_list[i], result_queue))
                    else:
                        futures.append(executor.submit(search_assets_for_accounts, winrmList[0], directory_path_list[i], result_queue))
                for future in concurrent.futures.as_completed(futures):
                    check_overtime(result_queue, "内嵌账号搜索中")
                    print("[thread]内嵌账号搜索子线程结束"  + str(datetime.now()))
                    # 获取每个线程的返回值
                    result_from_thread = future.result()
                    if result_from_thread:
                        result.extend(result_from_thread)

    except Exception as e:
        common.logger.error(repr(e))
        raise e
    # print(f"扫描内嵌账号总耗时：{(end - start).seconds}seconds, 共扫描{file_count}个文件")
    return result


def do_analysis(data_map, result_queue):
    try:
        special_user_list = []
        login_user_list = []
        # 脚本连接参数
        l = link()
        l.userName = data_map['user']
        l.passwd = data_map['pwd']
        l.host = data_map['location']
        user_data_list = data_map['userDatalist']

        # 格式化内嵌账号代码库搜索类型
        global embeddedAccountCodeLib
        if data_map['embeddedAccountCodeLib']:
            embeddedAccountCodeLib = handle_code_type(data_map['embeddedAccountCodeLib'])

        # 设置脚本执行速度速度(0 单线程， 1 多线程)
        global  speed
        speed = data_map['accountAnalysisRate']

        special_user_data_list = data_map['specialUserList']
        print("特殊账号列表：" + str(special_user_data_list))

        global analysis_account_array
        analysis_account_array = data_map.get('analysisAccountList')
        print("分析账号列表：" + str(analysis_account_array))

        if analysis_account_array is None:
            analysis_account_array = []
        #关闭库日志
        logging.getLogger().setLevel(logging.WARNING)
        if user_data_list == "null":
            user_data_list = None
            l.lastUserList = []
        # 特殊账号
        if special_user_data_list == "null":
            special_user_list = []
        if user_data_list:
            userList_json = list(json.loads(user_data_list))
            for user in userList_json:
                u = User()
                u.name = user['name']
                u.homeDirectory = user['homeDirectory']
                u.localGroup = user['localGroup']
                u.globalGroup = user['globalGroup']
                u.authority = user['authority']
                l.lastUserList.append(u)
        if special_user_data_list:
            for user in special_user_data_list.split(","):
                special_user_list.append(user)
        # 账号安全检查-基线项扫描
        user_hunter_List, userList, login_user_list = safetyInspection(login_user_list, special_user_list, l.lastUserList, l, data_map, result_queue)
        # 内嵌账号开关
        if data_map['embeddedAccountEnable'] == 1:
            #账号安全检查-内嵌账号搜索
            enbededAccount = hunt_window_EnbededAccount(l, result_queue)
            if enbededAccount:
                for ac in enbededAccount:
                    for user in user_hunter_List:
                        if user.userName in ac.split("!#!*")[1]:
                            if user.enbededAccount is None or user.enbededAccount == '':
                                user.enbededAccount = ac.split("!#!*")[0].strip()
                            else:
                                user.enbededAccount = str(user.enbededAccount) + ',' + ac.split("!#!*")[0].strip()
        # 账号安全检查-导出报表
        updateExportData(user_hunter_List, userList, login_user_list)
        # 将用户名转小写，与账号发现统一
        for user in user_hunter_List:
            user.userName = user.userName.lower()
        json_output = json.dumps([user.to_dict() for user in user_hunter_List], indent=4, ensure_ascii=False)
        json_output_userAuth = json.dumps([user.to_dict() for user in userList], indent=4, ensure_ascii=False)
        print(json_output)
        print(json_output_userAuth)
        return user_hunter_List, userList, login_user_list
    except Exception as e:
        common.logger.error("windows脚本执行异常" + repr(e))
        raise e

"""
查询监测进程队列，判断是否超时
"""
def check_overtime(result_queue, err_location=''):
    if not result_queue.empty():
        result = result_queue.get()
        if result:
            result_queue.put(result)
            raise RuntimeError(f"规则执行超时，任务已自动终止，执行时间：{result}，任务状态：{err_location}")


"""
执行命令获取日志（多线程用）
"""
def thread_get_logs(script, win):
    result = win.execute_powershell(script)
    return result.get('std_out')

"""
生成命令list给线程执行
example：[查询上周日志命令，查询上上周日志命令， ... ]
"""
def split_logs_by_time():
    now = datetime.now()
    start_time = now - timedelta(days=30)
    interval_days = (now - start_time).days // work_thread_num
    scripts = []

    for i in range(work_thread_num):
        seg_start = start_time + timedelta(days=i * interval_days)
        seg_end = seg_start + timedelta(days=interval_days)
        if seg_end > now:
            seg_end = now

        ps_cmd = f"""
    Get-WinEvent -FilterHashtable @{{
        LogName='Security';
        Id=@(4723, 4724, 4624);
        StartTime=([datetime]::Parse("{seg_start.strftime('%Y-%m-%dT%H:%M:%S')}"))
        EndTime=([datetime]::Parse("{seg_end.strftime('%Y-%m-%dT%H:%M:%S')}"))
    }} -MaxEvents 10000 |
    Select-Object @{{
        Name='EventID'; Expression={{$_.Id}}
    }},@{{
        Name='TimeGenerated'; Expression={{$_.TimeCreated}}
    }},@{{
        Name='SourceName'; Expression={{$_.ProviderName}}
    }},@{{
        Name='Message'; Expression={{$_.Message}}
    }},@{{
        Name='Keywords'; Expression={{$_.Keywords}}
    }}""".strip()

        scripts.append(ps_cmd)

    return scripts

"""
重新连接每一个连接对象，避免超时自动断开
"""
def reconnect(winrmList):
    for winRM_wrapper in winrmList:
        winRM_wrapper.connect()

"""
为每个线程新建连接对象
"""
def new_connections( link):
    winrmList = []
    for i in range(work_thread_num):
        winRM_wrapper = WinRMWrapper(link.host, link.userName, link.passwd)
        winrmList.append(winRM_wrapper)
    return winrmList

"""
格式化代码库搜索格式
"""
def handle_code_type(embeddedAccountCodeLib):
    try:
        embeddedAccountCodeLib.replace(".", "*.")
        return embeddedAccountCodeLib
    except Exception as e:
        common.logger.error("格式化代码库搜索格式异常" + repr(e))
        raise e

#更新报表导出数据
def updateExportData(user_hunterList, userList, login_user_list):
    for huntUser in user_hunterList:
        for user in userList:
            if huntUser.userName == user.name:
                #更新用户组
                huntUser.ugroup = user.localGroup
                #是否是特权账号
                if huntUser.bl1028_1:
                    huntUser.isPrivilegeExport = '否'
                else:
                    huntUser.isPrivilegeExport = '是'
                #账号状态
                if user.active:
                    huntUser.accountActive = '启用'
                else:
                    huntUser.accountActive = '禁用'
                #账号创建时间
                #createTime
                #账号到期时间
                # huntUser.accountExpires
                #上次登录时间
                if huntUser.lastLogonTime is None:
                    huntUser.lastLoginTime = '从未登录'
                #上次改密时间
                # huntUser.lastPwdsetTime
                #密码策略
                #弱口令策略
                if (not huntUser.minimumPasswordLength or not huntUser.minimumPasswordAge or not huntUser.passwordHistorySize
                        or not huntUser.bl0005_1 or not huntUser.bl0005_2
                        or not huntUser.bl1026_1 or not huntUser.bl1026_2 or not huntUser.bl1026_3 or not huntUser.bl1026_4 or not huntUser.bl1026_5
                ):
                    huntUser.isWeakStrategy = "是"
                    updatePasswordStrategyExport(huntUser)
                else:
                    huntUser.isWeakStrategy = "否"
                # 长期未登录
                if huntUser.bl1027_1 or huntUser.bl1027_4:
                    huntUser.longUnusedExport = '否'
                else:
                    huntUser.longUnusedExport = '是'
                #长期未改密
                if huntUser.bl1026_5:
                    huntUser.longUnchangeExport = '否'
                else:
                    huntUser.longUnchangeExport = '是'
                #非授权登录日志
                #权限
                if huntUser.ugroup != '':
                    huntUser.permission = '当前用户所属组：' + huntUser.ugroup
                else:
                    huntUser.permission = '当前用户不属于任何组'
                continue

#更新密码检测方法
def updatePasswordStrategyExport(huntUser):
    if not huntUser.minimumPasswordLength:
        huntUser.passwordStrategyExport += ''' 检查 本地安全策略 -> 密码策略 -> “最小密码长度”。确保值不小于 14。
        '''
    if not huntUser.minimumPasswordAge:
        huntUser.passwordStrategyExport += ''' 检查 本地安全策略 -> 密码策略 -> “密码最短使用期限”。确保值不低于 1。
        '''
    if not huntUser.passwordHistorySize:
        huntUser.passwordStrategyExport += ''' 检查 本地安全策略 -> 密码策略 -> “强制密码历史记录”。确保值不小于 5。
        '''
    if not huntUser.bl0005_1:
        huntUser.passwordStrategyExport += ''' 检查 本地安全策略 -> 账户锁定策略。“账户锁定阈值” 设置为3-5之间。
        '''
    if not huntUser.bl0005_2:
        huntUser.passwordStrategyExport += '''  检查 本地安全策略 -> 账户锁定策略。“账户锁定时间” 设置不小于15分钟。
        '''
    if not huntUser.bl1026_1:
        huntUser.passwordStrategyExport += '''检查密码复杂性是否启用。
        '''
    if not huntUser.bl1026_2:
        huntUser.passwordStrategyExport += '''检查密码长度是否小于14位。
        '''
    if not huntUser.bl1026_3:
        huntUser.passwordStrategyExport += '''检查最大密码期限是否超过90天。
        '''
    if not huntUser.bl1026_4:
        huntUser.passwordStrategyExport += '''检查最短密码期限是否未设置，允许用户频繁修改密码。
        '''
    if not huntUser.bl1026_5:
        huntUser.passwordStrategyExport += '''检查日志分析近期是否改密
事件日志：事件查看器 -> Windows 日志 -> 安全 -> 事件 ID：
4723：尝试更改账户密码。
4724：尝试重置账户密码。
        '''


data_map = {
    "location": "10.10.10.108",
    "user": "administrator",
    "pwd": "123jkluio!@#",
    "protocol": "http",
    "port": "22",
    "remote": "http://pam-selenium:4444/wd/hub",
    "loginAccount": "",
    "loginAccountPwd": "",
    "database": "",
    "taskId": "132132-DASDAS",
    "discoverEnable": 1,
    "analysisEnable": 1,
    "userDatalist": "",
    "specialUserList": "",
    "accountAnalysisRate": 1,
    "embeddedAccountEnable" : 0,
    "embeddedAccountCodeLib": ".txt,.md,.conf,.json,.cfg,.ini,.properties,.config,.xml,.env,.sql,.yaml,.yml" ,
    "analysisAccountList": []
}

if __name__ == '__main__':
    do_analysis(data_map, Queue())





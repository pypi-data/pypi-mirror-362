import copy
import json
import logging
import math
import os
import queue
import re
import sys
import concurrent.futures
import threading
import time
import traceback
from collections import deque
from datetime import datetime, timezone, timedelta
from multiprocessing import Queue
from random import random

import paramiko
from secmind.rpa_v2 import SSHWrapper
from secmind.rpa_v2 import common
from selenium.webdriver.common import keys


class HuntLinux:
    def __init__(self):
        super().__init__()
        self.bl0027_1 = True
        self.bl0027_2 = True
        self.bl0027_3 = True
        self.bl0027_4 = True
        self.bl0027_5 = True
        self.bl0032 = True
        self.bl0033 = True
        self.bl0034 = True
        self.bl0035 = True
        self.bl0036 = False
        self.bl0036 = False

        self.bl1020_1 = True
        self.bl1020_2 = True
        self.bl1020_3 = True
        self.bl1020_4 = True
        self.bl1020_5 = True
        self.bl1020_6 = True
        self.bl1021_1 = True
        self.bl1021_2 = True
        self.bl1021_3 = True
        self.bl1022_1 = True
        self.bl1022_2 = True
        self.bl1022_3 = True
        self.bl1022_4 = True
        self.bl1023 = True
        self.bl1024 = True
        self.bl1025 = True
        self.bl1033 = False
        self.enbededAccount = ""
        self.authChange = ''
        self.highAuth = True
        self.isPrivilegeExport = ''
        self.logonCount = 0
        #报表导出自定义字段
        self.ugroup = ''
        self.accountActive =''
        self.accountExpires = ''
        self.passwordStrategyExport = ''
        self.lastLoginTime = '-'
        self.createTime = ''
        self.permission = ''
        self.assetVersion = ''
        self.loginLog = ''
    def to_dict(self):
        return {
            "userName": self.userName,
            "bl0028": self.minimumPasswordLength,
            "bl0029": self.minimumPasswordAge,
            "bl0030": self.passwordHistorySize,
            "bl0031": self.lockStrategy,
            "bl0032": self.bl0032,
            "bl0033": self.bl0033,
            "bl0034": self.bl0034,
            "bl0035": self.bl0035,
            "bl0036": self.bl0036,
            "bl0037": self.bl0037,
            "bl0038": self.PasswordAuthentication,
            "bl0039": self.checkIsRecordLoginEvents,
            "bl1023": self.bl1023,
            "bl1024": self.bl1024,
            "bl1025": self.bl1025,
            "bl1033": self.bl1033,
            "enbededAccount": self.enbededAccount,
            "authorityChangeDetail": self.authChange,
            "isHighPermission": self.highAuth,
            #检查子项
            "bl1022_1": self.bl1022_1,
            "bl1022_2": self.bl1022_2,
            "bl1022_3": self.bl1022_3,
            "bl1022_4": self.bl1022_4,

            "bl0027_1": self.bl0027_1,
            "bl0027_2": self.bl0027_2,
            "bl0027_3": self.bl0027_3,
            "bl0027_4": self.bl0027_4,
            "bl0027_5": self.bl0027_5,

            "bl1020_1": self.bl1020_1,
            "bl1020_2": self.bl1020_2,
            "bl1020_3": self.bl1020_3,
            "bl1020_4": self.bl1020_4,
            "bl1020_5": self.bl1020_5,
            "bl1020_6": self.bl1020_6,

            "bl1021_1": self.bl1021_1,
            "bl1021_2": self.bl1021_2,
            "bl1021_3": self.bl1021_3,
            # 报表导出自定义字段
            "ugroup": self.ugroup,
            "isPrivilegeExport": self.isPrivilegeExport,
            "accountActive":self.accountActive,
            "createTime":self.createTime,
            "accountExpires":self.accountExpires,
            "lastLoginTime":self.lastLoginTime,
            "lastPwdsetTime":self.lastPwdsetTime,
            "isWeakStrategy":self.isWeakStrategy,
            "passwordStrategyExport":self.passwordStrategyExport,
            "longUnusedExport":self.longUnusedExport,
            "longUnchangeExport":self.longUnchangeExport,
            "permission":self.permission,
            "assetVersion": self.assetVersion,
            "loginLogExport": self.loginLog,
        }

class User:
    def __init__(self):
        super().__init__()
        self.name = None
        self.UID = None
        self.directory = None
        self.shell = None
        self.GUID = None
        self.directoryAuthority = None
        self.lastLog = None
        self.group = None
        self.active = None
        self.birthday = None

    def to_dict(self):
        return {
            "name": self.name,
            "directory": self.directory,
            "directoryAuthority": self.directoryAuthority,
            "group": self.group,
        }
#  python hunt_linux.py root 123jkluio!@# 10.10.10.58 22 'null' 'null'


def do_analysis(data_map, monitor_queue):
    # 设置连接参数

    user_data_list = data_map['userDatalist']
    special_user_data_list = data_map['specialUserList']

    # 格式化内嵌账号代码库搜索类型
    global embeddedAccountCodeLib
    if data_map['embeddedAccountCodeLib']:
        embeddedAccountCodeLib = handle_code_type(data_map['embeddedAccountCodeLib'])

    # 设置脚本执行速度速度(0 单线程， 1 多线程)
    global speed
    speed = data_map['accountAnalysisRate']
    print(f"当前执行速度{'快' if speed == 1 else '慢'}")

    # 账号分析列表
    global analysis_account_array
    analysis_account_array = data_map.get('analysisAccountList')
    if analysis_account_array is None:
        analysis_account_array = []

    lastUserList = []
    specialList = []
    login_user_list = []
    #关闭库日志
    logging.getLogger().setLevel(logging.WARNING)
    if user_data_list is None:
        user_data_list = []
    #特殊账号
    if special_user_data_list == "null":
        special_user_data_list = []
    if user_data_list and user_data_list.strip():
        userList_json = list(json.loads(user_data_list.strip()))
        for user in userList_json:
            u = User()
            u.name = user['name']
            u.directory = user['directory']
            u.directoryAuthority = user['directoryAuthority']
            u.group = user['group']
            lastUserList.append(u)
    if special_user_data_list:
        for user in special_user_data_list.split(","):
            specialList.append(user)

    """
    user_hunterList 安全检查执行结果
    userList 用户权限（用于对比权限变更）
    login_user_list 登录用户列表（用于未授权登录）
    """
    # 账号安全检查-基线项扫描
    user_hunterList, userList, login_user_list = safetyInspection(login_user_list, specialList, lastUserList, data_map, monitor_queue)

    # 账号安全检查-内嵌账号
    if data_map['embeddedAccountEnable'] == 1:
        result = hunt_linux_EnbededAccount(data_map,user_hunterList, monitor_queue)
        # 内嵌账号判断
        if result:
            for ac in result:
                for user in user_hunterList:
                    if user.userName in ac.split("!#!*")[1]:
                        if not user.enbededAccount or user.enbededAccount == '':
                            user.enbededAccount = user.enbededAccount + ac.split("!#!*")[0]
                        else:
                            user.enbededAccount = user.enbededAccount + ',' + ac.split("!#!*")[0]
    '''
    更新导出数据
    '''
    updateExportData(user_hunterList, userList)
    json_output = json.dumps([user.to_dict() for user in user_hunterList], indent=4, ensure_ascii=False)
    json_output_userAuth = json.dumps([user.to_dict() for user in userList], indent=4, ensure_ascii=False)
    print(json_output)
    print(json_output_userAuth)
    #高权限判断
    for user in user_hunterList:
        if not user.bl0036 or not user.bl1022_1 or not user.bl1022_2 or not user.bl1022_3 or not user.bl1022_4:
            user.highAuth = False
    # 登录用户列表截取100条
    if len(login_user_list) > 100:
        login_user_list = login_user_list[:100]
    return user_hunterList, userList, login_user_list

#更新报表导出数据
def updateExportData(user_hunterList, userList):
    for huntUser in user_hunterList:
        for user in userList:
            if huntUser.userName == user.name:
                #更新用户组
                huntUser.ugroup = ','.join(user.group)
                #是否是特权账号
                if huntUser.bl1022_3:
                    huntUser.isPrivilegeExport = '否'
                else:
                    huntUser.isPrivilegeExport = '是'
                #账号状态
                if user.active:
                    huntUser.accountActive = '启用'
                else:
                    huntUser.accountActive = '禁用'
                #账号创建时间
                if user.birthday:
                    huntUser.createTime = user.birthday
                elif user.birthday == '':
                    huntUser.createTime = '-'
                #账号到期时间
                # huntUser.accountExpires
                #上次登录时间
                if user.lastLog is not None:
                    huntUser.lastLoginTime = user.lastLog.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    huntUser.lastLoginTime = '从未登录'
                #上次改密时间
                # huntUser.lastPwdsetTime
                #密码策略
                #弱口令策略
                if not huntUser.bl0027_1 or not huntUser.bl0027_2 or not huntUser.bl0027_3 or not huntUser.bl0027_4 or not huntUser.bl0027_5 or not huntUser.bl0028 or not huntUser.minimumPasswordAge or not huntUser.passwordHistorySize or not huntUser.lockStrategy or not huntUser.bl1020_1 or not huntUser.bl1020_2 or not huntUser.bl1020_3 or not huntUser.bl1020_4 or not huntUser.bl1020_5 or not huntUser.bl1020_6:
                    huntUser.isWeakStrategy = "是"
                    updatePasswordStrategyExport(huntUser)
                else:
                    huntUser.isWeakStrategy = "否"
                #长期未登录
                if huntUser.bl1021_1 and '从未登录' not in huntUser.lastLoginTime:
                    huntUser.longUnusedExport = '否'
                else:
                    huntUser.longUnusedExport = '是'
                #长期未改密
                if huntUser.bl1033:
                    huntUser.longUnchangeExport = '否'
                else:
                    huntUser.longUnchangeExport = '是'
                #非授权登录日志
                #权限
                huntUser.permission = '当前用户所属组：' + huntUser.ugroup
                if user.directoryAuthority:
                    huntUser.permission += '\n'  '用户主目录权限为：' + user.directoryAuthority
                continue

def updatePasswordStrategyExport(huntUser):
    if not huntUser.bl0027_1:
        huntUser.passwordStrategyExport += '''检查 pam_pwquality 模块配置文件：/etc/security/pwquality.conf，/etc/pam.d/common-password中模块pam_cracklib.so以及pam_pwquality.so。
确认以下参数是否配置（存在默认值，开启模块未设置的情况下取默认值）：
minlen=8：密码最小长度。
'''
    if not huntUser.bl0027_2:
        huntUser.passwordStrategyExport += '''检查 pam_pwquality 模块配置文件：/etc/security/pwquality.conf，/etc/pam.d/common-password中模块pam_cracklib.so以及pam_pwquality.so。
确认以下参数是否配置（存在默认值，开启模块未设置的情况下取默认值）：dcredit=-1：至少包含一个数字
。'''
    if not huntUser.bl0027_3:
        huntUser.passwordStrategyExport += '''检查 pam_pwquality 模块配置文件：/etc/security/pwquality.conf，/etc/pam.d/common-password中模块pam_cracklib.so以及pam_pwquality.so。
确认以下参数是否配置（存在默认值，开启模块未设置的情况下取默认值）：ucredit=-1：至少包含一个大写字母。
'''
    if not huntUser.bl0027_4:
        huntUser.passwordStrategyExport += '''检查 pam_pwquality 模块配置文件：/etc/security/pwquality.conf，/etc/pam.d/common-password中模块pam_cracklib.so以及pam_pwquality.so。
确认以下参数是否配置（存在默认值，开启模块未设置的情况下取默认值）：lcredit=-1：至少包含一个小写字母。
'''
    if not huntUser.bl0027_5:
        huntUser.passwordStrategyExport += '''检查 pam_pwquality 模块配置文件：/etc/security/pwquality.conf，/etc/pam.d/common-password中模块pam_cracklib.so以及pam_pwquality.so。
确认以下参数是否配置（存在默认值，开启模块未设置的情况下取默认值）：ocredit=-1：至少包含一个特殊字符。
'''
    if not huntUser.minimumPasswordLength:
        huntUser.passwordStrategyExport += '''检查/etc/security/pwquality.conf，/etc/pam.d/common-password中模块pam_cracklib.so以及pam_pwquality.so中的minlen参数是否设置为8或更大。
        '''
    if not huntUser.minimumPasswordAge:
        huntUser.passwordStrategyExport += '''检查 /etc/login.defs 文件中的 PASS_MIN_DAYS 参数。
        '''
    if not huntUser.passwordHistorySize:
        huntUser.passwordStrategyExport += '''检查 /etc/security/pwhistory.conf中是否配置了remember
检查/etc/pam.d/system-auth 以及 /etc/pam.d/password-auth，中的模块pam_pwhistory.so配置的remember参数，或/etc/pam.d/common-password里的pam_pwhistory.so模块是否包含remember参数确保值不小于 5并且开启强制避免重复密码。
'''
    if not huntUser.lockStrategy:
        huntUser.passwordStrategyExport += '''centos类内核中检查 /etc/pam.d/system-auth  文件中是否启用并配置了 pam_faillock 模块。
详细参数可以在/etc/pam.d/common-auth内或/etc/security/faillock.conf中设置（若存在该文件）。
Ubuntu类内核中检查/etc/pam.d/common-auth是否对pam_faillock.so进行启用，详细参数可以在/etc/pam.d/common-auth内或/etc/security/faillock.conf中设置(若存在该文件)
检查 /etc/pam.d/sshd中是否对ssh启用faillock模块，并且次数限制是否满足要求
'''
    if not huntUser.bl1020_1:
        huntUser.passwordStrategyExport += '''密码从未更改：lastchg 字段为 0
        。'''
    if not huntUser.bl1020_2:
        huntUser.passwordStrategyExport += '''密码过期未更换：未改密时间超过密码最大使用天数。
        '''
    if not huntUser.bl1020_3:
        huntUser.passwordStrategyExport += '''密码永不过期：expire 字段为空或为 99999。
        '''
    if not huntUser.bl1020_4:
        huntUser.passwordStrategyExport += '''检查/etc/login.defs 如下字段：PASS_MAX_DAYS：密码最大使用天数不超过90天。
        '''
    if not huntUser.bl1020_5:
        huntUser.passwordStrategyExport += '''检查/etc/login.defs 如下字段：PASS_MIN_DAYS：密码最小使用天数不小于1天。
        '''
    if not huntUser.bl1020_6:
        huntUser.passwordStrategyExport += '''检查/etc/login.defs 如下字段：PASS_WARN_AGE：密码过期警告天数不大于15天。
        '''


def safetyInspection(login_user_list, specialAccountList, lastUserList, data_map, monitor_queue):
    global su_flag
    su_flag = False
    try:
        ssh_wrapper, su_flag = ssh_connect(data_map, return_su_flag=True)
        # 设置脚本执行速度
        global work_thread_num
        if speed == 0:
            work_thread_num = int(1)
        else:
            # 查询当前系统核心数，设置工作线程数。
            result, err = ssh_wrapper.execute_command("nproc")
            if result:
                # 向上取整
                work_thread_num = math.ceil(int(result) / 3)
                if work_thread_num > 5:
                    work_thread_num = 5
        # 为线程池创建连接对象
        global ssh_List
        # 为每个线程新建连接对象保证线程安全
        ssh_List = new_connections(data_map)

    except Exception as ex:
        common.logger.error("账号登录失败，请检查账密是否正确或账号是否拥有远程登录权限" + repr(ex))
        raise ex
    try:
        hunter = HuntLinux()
        result_queue = queue.Queue()
        log_thread = threading.Thread(target=bl1021_failLog, args=(ssh_wrapper, result_queue))
        # hunter.failLogList = bl1021_failLog(ssh_wrapper, result_queue)
        log_thread.start()
        #查看资产版本
        hunter.assetVersion = selectVersion(ssh_wrapper)
        # (bl0027)true：符合密码复杂性
        keys = bl0027(ssh_wrapper, hunter)
        # (bl0028)true：密码最小长度位数符合要求
        hunter.minimumPasswordLength = bl0028(ssh_wrapper, keys)
        # (bl0029)true：密码最短使用期限大于1一天
        hunter.minimumPasswordAge = bl0029(ssh_wrapper)
        # (bl0030)True：密码历史记录大于5,若无则默认为0
        hunter.passwordHistorySize = bl0030(ssh_wrapper, keys)
        # 返回锁定阈值与锁定时间
        # retry, locktime = bl0031(ssh_wrapper)
        # （bl0031）true:账户锁定阈值大于5
        hunter.lockStrategy = checkRetry(keys)
        # (bl0038)true:开启远程访问必须使用密钥登录 false：未启用
        hunter.PasswordAuthentication = bl0038(ssh_wrapper)
        # (bl0039)true:启用用户活动日志 false：未启用
        hunter.checkIsRecordLoginEvents = bl0039(ssh_wrapper)
        # 用户信息（过滤掉特殊账号）
        userList, user_hunterList = bl1021_userInfo(login_user_list, specialAccountList, ssh_wrapper, hunter)
        # (bl0032)是否启用guest账户 true:启用 false：未启用
        bl0032(ssh_wrapper, userList, user_hunterList)
        # (bl0033)true:是 false：否 root用户是否为默认名
        bl0033(ssh_wrapper, userList, user_hunterList)
        # true: 无从未登录的用户 false：存在未登录过的用户
        sudo_dict, sudoGroup_dict = bl0035(ssh_wrapper)
        # 返回所有拥有sudo权限的用户与组,组名以%开头
        # 返回拥有sudo权限的组及其组内用户
        if "guest" in sudo_dict or "guest" in sudoGroup_dict:
            for user_hunter in user_hunterList:
                if user_hunter.userName:
                    user_hunter.bl0035 = False
        # (bl0036)true:su里已限制普通用户使用su命令 false：未限制
        bl0036(ssh_wrapper, user_hunterList)
        # (bl0037)true:不允许root用户ssh登录 false：允许
        bl0037(ssh_wrapper, user_hunterList)
        #密码策略详情
        bl1020(ssh_wrapper, user_hunterList)
        #密码最后修改时间检查
        bl1020pro(ssh_wrapper, user_hunterList)
        log_thread.join()
        # 检查是否超时
        check_overtime(monitor_queue, "日志分析")
        print("--------------阻塞线程结束---------------")
        # (bl1021)未使用账户分析
        checkUnUsedAccount(userList, ssh_wrapper, user_hunterList)
        #(bl1022) 高权限配置账户 权限变更
        checkBl1022(userList, ssh_wrapper, lastUserList, user_hunterList)
        #未授权登录日志分析
        unAuthLogon(login_user_list, result_queue, user_hunterList)
        result_loginUserList = []
        login_user_list = deduplicate_keep_order(login_user_list)
        for line in login_user_list:
            #上线需要注释
            if any(keyword in line for keyword in analysis_account_array):
                result_loginUserList.append(line)
        time, err = ssh_wrapper.execute_command(f'LC_TIME=en_US.UTF-8 date "+%Y/%m/%d"')
        if time:
            now = datetime.strptime(time.strip(), "%Y/%m/%d")
        else:
            raise RuntimeError(f"Bl1027 get Date error: {err}")
        #bl1033 长期未改密
        bl1033(ssh_wrapper, user_hunterList, now)
        return user_hunterList, userList, result_loginUserList
    except Exception as ex:
        common.logger.error(repr(ex))
        raise ex
    finally:
        ssh_wrapper.exit()

def selectVersion(ssh_wrapper):
    out, err = ssh_wrapper.execute_command("LC_TIME=en_US.UTF-8 lsb_release -a")
    if out is None or out == '':
        return '资产版本获取失败'
    else:
        for line in out.splitlines():
            if "description" in line.lower():
                return line.split(":")[1]

def monitor_runtime(start_time, q):
    print(f"[监测进程启动] PID: {os.getpid()}")
    while True:
        now = datetime.now()
        elapsed = now - start_time
        print(f"[监测进程] 已运行时间：{elapsed}")

        if elapsed > timedelta(minutes=2 * 60):
            q.put(f"{elapsed}")
            print(f"[监测进程] 检测超时 脚本运行时间:{elapsed}")
        time.sleep(60 * 10)  # 每10分钟检测一次

def bl1033(ssh_wrapper, user_hunterList, now):
    for user_hunter in user_hunterList:
        if user_hunter.userName:
            result, err = ssh_wrapper.execute_command(f"LC_TIME=en_US.UTF-8 chage -l {user_hunter.userName}")
            pwdLastChangeDt = None
            maxDays = None
            if result:
                for line in result.splitlines():
                    if "Last password change" in line or "最近一次密码修改时间" in line:
                        #中英文冒号
                        if ":" in line:
                            pwdLastChange = line.split(":")[1].strip()
                        else:
                            pwdLastChange = line.split("：")[1].strip()
                        try:
                            if 'never' not in pwdLastChange:
                                pwdLastChangeDt = datetime.strptime(pwdLastChange, "%b %d, %Y")
                                user_hunter.lastPwdsetTime = pwdLastChangeDt.strftime("%Y-%m-%d")
                            else:
                                user_hunter.lastPwdsetTime = "从未改密"
                        except Exception as ex:
                            common.logger.error("bl1033获取最后改密事件错误" + repr(ex))
                            raise ex
                    if "Maximum number of days between password change" in line or '两次改变密码之间相距的最大天数' in line:
                        if ":" in line:
                            maxDays = line.split(":")[1].strip()
                        else:
                            maxDays = line.split("：")[1].strip()
                        if maxDays == "从未" or maxDays == "never" or maxDays == '99999':
                            maxDays = 90
                    if pwdLastChangeDt and maxDays:
                        if (now - pwdLastChangeDt).days > int(maxDays):
                            user_hunter.bl1033 = False
                        else:
                            user_hunter.bl1033 = True
                    #账号过期时间
                    if 'Account expires' in line:
                        expires = ''
                        # 中英文冒号
                        if ":" in line and 'never' not in line:
                            expires = line.split(":")[1].strip()
                        elif "：" in line and 'never' not in line:
                            expires = line.split("：")[1].strip()
                        else:
                            user_hunter.accountExpires = '永不过期'
                        try:
                            if 'never' not in expires and expires:
                                user_hunter.accountExpires = datetime.strptime(expires, "%b %d, %Y").strftime("%Y-%m-%d")
                        except Exception as ex:
                            common.logger.error("导出报表中账号过期时间获取错误" + repr(ex))
                            raise ex




def search_assets_for_accounts(ssh_wrapper, paths, monitor_queue):
    response = []
    thread = random() * 100
    count = 0
    for path in paths:
        try:
            # 测试目录是否存在
            test_dir_command = f'test -d {path} && echo "当前目录存在" || echo "当前目录不存在"'
            #ssh超时重连
            try:
                  exist, exist_error = ssh_wrapper.execute_command(test_dir_command)
            except paramiko.SSHException:
                logging.log(logging.WARNING, "ssh连接断开，即将进行重新连接")
                ssh_wrapper.connect()
                exist, exist_error = ssh_wrapper.execute_command(test_dir_command)
            if "当前目录存在" in exist:
                # 检测脚本是否超时
                check_overtime(monitor_queue, "内嵌账号子任务搜索中")
                # 获取当前目录下可能含有内嵌账号的文件名与对应路径
                get_file_name = f'''
               find {path} -maxdepth 1 -type f \( {embeddedAccountCodeLib}\)
                '''
                count += 1
                print("【线程】" + str(thread) + "已扫描" + str(count) + "，正在扫描" + path)
                try:
                    export, error = ssh_wrapper.execute_command(get_file_name)
                except paramiko.SSHException:
                    logging.log(logging.WARNING, "ssh连接断开，即将进行重新连接")
                    ssh_wrapper.connect()
                    export, error = ssh_wrapper.execute_command(get_file_name)
                if export:
                    for actual_path in export.splitlines():
                        # 检测所有扫描出来的文件
                        # print(actual_path)
                        analyze_file_account_command = f'filePath="{actual_path.strip()}"' + '''
                        # 定义正则表达式模式
                        patterns=(
                            "\\baccessKeyId[:=]\s*([\w-]+)"
                            "\\b(?i).*corp(Id|Secret)=(\w+)"
                            "\\b(?i).*qq\.im\.(sdkappid|privateKey|identifier)=(.*)"
                            "\\b(?i)(?:user(?:name)?\s*[=:])\s*([^\s]+)"
                            "\\b(?:账户|账户名|用户名|账号|测试账户)\s*[=：:]*\s*([\\w@#!$%^&*-]{3,20})"
                            "\\bjdbc\.(driver|url|type)\s*=(.*)"
                            "\\b#jdbc\.(driver|url|type)\s*=(.*)"
                        )
        
                        # 检查文件是否存在
                        if [ -f "$filePath" ]; then
                            # 读取文件内容
                            content=$(cat "$filePath")
        
                            # 循环遍历每个正则表达式模式
                            for pattern in "${patterns[@]}"; do
                                # 使用 grep 进行正则匹配
                                # -P 表示 Perl 正则表达式，-o 表示只输出匹配的内容
                                matches=$(echo "$content" | grep -Po "$pattern")
        
                                # 输出匹配结果
                                if [ ! -z "$matches" ]; then
                                    echo "$matches"
                                fi
                            done
                        else
                            echo "文件不存在：$filePath"
                        fi
                        '''
                        try:
                            export, error = ssh_wrapper.execute_command(analyze_file_account_command)
                        except paramiko.SSHException:
                            logging.log(logging.WARNING, "ssh连接断开，即将进行重新连接")
                            ssh_wrapper.connect()
                            export, error = ssh_wrapper.execute_command(analyze_file_account_command)
                        # global file_count
                        # file_count = file_count + 1
                        if export:
                            analyze_file_passwd_command = f'filePath="{actual_path}"' + '''
                            # 定义正则表达式模式
        patterns=(
            "\\baccessKeySecret[:=]\s*([\w-]+)"
            "\\b(?i)(?:pass(?:word)?\s*[=:])\s*([^\s]+)"
            "\\b(?:默认口令|默认密码|口令|密码|测试密码)\s*[=：:]*\s*([\\w@#!$%^&*-]{3,20})"
        )
        
        # 检查文件是否存在
        if [ -f "$filePath" ]; then
            # 读取文件内容
            content=$(cat "$filePath")
        
            # 循环遍历每个正则表达式模式
            for pattern in "${patterns[@]}"; do
                # 使用 grep 进行正则匹配，-P 表示 Perl 正则表达式，-o 表示只输出匹配的内容
                matches=$(echo "$content" | grep -Po "$pattern")
        
                # 输出匹配结果
                if [ ! -z "$matches" ]; then
                    echo "$matches"
                fi
            done
        else
            echo "文件不存在：$filePath"
        fi
                            '''
                            try:
                                export_result, error = ssh_wrapper.execute_command(analyze_file_passwd_command)
                            except paramiko.SSHException:
                                logging.log(logging.WARNING, "ssh连接断开，即将进行重新连接")
                                ssh_wrapper.connect()
                                export_result, error = ssh_wrapper.execute_command(analyze_file_passwd_command)
                            if export_result and not actual_path in export_result:
                                response.append(f"{actual_path}!#!*{export.strip()}!#!*{export_result.strip()}")
        except Exception as e:
            common.logger.error("内嵌账号搜索异常" + repr(e))
            # 程序超时
            if "脚本执行超时" in str(e):
                return response
    return response

def hunt_linux_EnbededAccount(data_map, user_hunterList, monitor_queue):
    ssh_wrapper = ssh_connect(data_map)
    ssh_wrapper.connect()
    result = []
    futures = []
    directory_path = []
    root_file_list = []
    result_code = []
    localPath = []
    # 添加搜索本地文件目录（/etc）
    find_file_path = '''find /etc -maxdepth 5 -type d'''
    find_result_etc, error = ssh_wrapper.execute_command(find_file_path)
    if find_result_etc:
        localPath.extend(find_result_etc.splitlines())
    # 准备搜索代码库
    find_file_path = '''find / -maxdepth 1 -type d'''
    find_result_root, error = ssh_wrapper.execute_command(find_file_path)
    if find_result_root:
        root_file_list = find_result_root.splitlines()
        #删除根目录
        root_file_list = [path for path in root_file_list if path != "/"]
    root_file_list = split_into_n(root_file_list, work_thread_num)
    #用多线程对根目录下每个文件进行代码库扫描
    if root_file_list:
        with concurrent.futures.ThreadPoolExecutor(max_workers=work_thread_num) as executor:
            for index, file in enumerate(root_file_list):
                futures.append(executor.submit(search_code, ssh_List[index], file))
            for future in concurrent.futures.as_completed(futures):
                try:
                    # 获取每个线程的返回值
                    result_from_thread = future.result()
                    if result_from_thread:
                        result_code.extend(result_from_thread)
                except Exception as ex:
                    common.logger.error(f"代码库搜索错误，搜索文件为 :" + str(file) + f" {repr(ex)}")
    if result_code:
        directory_path.extend(result_code)
        print("代码库搜索完成，路径为：" + str(len(directory_path)))
    print("[thread]====代码库搜索完毕")
    #检测脚本是否超时
    check_overtime(monitor_queue, "内嵌账号搜索准备中")
    directory_path.extend(localPath)
    print("添加本地路径完成，路径为：" + str(len(directory_path)))
    # 根据线程数，均匀分割目录
    result_n = split_into_n(directory_path, work_thread_num)
    futures = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=work_thread_num) as executor:
        for i in range(work_thread_num):
            futures.append(executor.submit(search_assets_for_accounts, ssh_List[i], result_n[i], monitor_queue))
        for future in concurrent.futures.as_completed(futures):
            # 获取每个线程的返回值
            result_from_thread = future.result()
            result = result + result_from_thread
    end = datetime.now()
    # print(f"扫描内嵌账号总耗时：{(end - start).seconds}seconds, 共扫描{file_count}个文件")
    return result

def search_code(ssh_wrapper, paths):
    result_all = []
    for path in paths:
        search_script = f'''
            find {path} -type f \( -iname "*.py" -o -iname "*.java" -o -iname "*.c" -o -iname "*.cpp" -o -iname "*.h" -o -iname "*.hpp" -o -iname "*.js" -o -iname "*.ts" -o -iname "*.tsx" -o -iname "*.html" -o -iname "*.css" -o -iname "*.go" -o -iname "*.rb" -o -iname "*.php" -o -iname "*.kt" -o -iname "*.swift" -o -iname "*.rs" -o -iname "*.sh" -o -iname "*.sql" \) | sed 's|/[^/]*$||' | grep -E 'src|service|controller|api|web|core|common|util|model|view|component|test|project' | sort -u
        '''
        result, err = ssh_wrapper.execute_command(search_script)
        if result:
            result_all.extend(result.splitlines())
    return result_all

def bl1020(ssh_wrapper, user_hunterList):
    try:
        output, error = ssh_wrapper.execute_command("cat /etc/login.defs")
        if not error:
            for line in output.splitlines():
                if line.startswith("#"):
                    continue
                if "PASS_MAX_DAYS" in line:
                    if int(line.split()[1]) > 90:
                        for user in user_hunterList:
                            user.bl1020_4 = False
                if "PASS_MIN_DAYS" in line:
                    if int(line.split()[1]) < 1:
                        for user in user_hunterList:
                            user.bl1020_5 = False
                if "PASS_WARN_AGE" in line:
                    if int(line.split()[1]) < 7:
                        for user in user_hunterList:
                            user.bl1020_6 = False

    except Exception as ex:
        common.logger.error(f"Error occurred in bl1020: {repr(ex)}")
        raise ex


def bl1020pro(ssh_wrapper, user_hunterList):
    try:
        epoch = datetime(1970, 1, 1)
        if su_flag:
            ssh_wrapper = ssh_wrapper.execute_command_chain("cat /etc/shadow")
            output = ssh_wrapper.output
            error = ''
        else:
            output, error = ssh_wrapper.execute_command("cat /etc/shadow")
        time, error_Time = ssh_wrapper.execute_command("LC_TIME=en_US.UTF-8 date +'%a %b %d %H:%M:%S %Y' ")
        if not error_Time:
            dt = datetime.strptime(time.strip(), "%a %b %d %H:%M:%S %Y")
        if not error :
            for line in output.splitlines():
                lastSetPwdDate = 0
                expire = 0
                if ":" not in line:
                    continue
                #密码最后更新时间
                user = line.split(":")[0]
                if line.split(":")[2]:
                    lastSetPwdDate = int(line.split(":")[2])
                    now = get_days_since_unix_epoch()
                    if now - lastSetPwdDate > 90:
                        for hunt_user in user_hunterList:
                            if hunt_user.userName == user:
                                hunt_user.bl1020_1 = False
                # 密码从未改密
                else:
                    for hunt_user in user_hunterList:
                        if hunt_user.userName == user:
                            hunt_user.bl1020_1 = False
                #如果密码无过期时间
                if not line.split(":")[4]:
                    for hunt_user in user_hunterList:
                        if hunt_user.userName == user:
                            hunt_user.bl1020_3 = False
                #如果密码过期时间为99999
                if line.split(":")[4]:
                    expire = int(line.split(":")[4])
                    if expire == 99999:
                        for hunt_user in user_hunterList:
                            if hunt_user.userName == user:
                                hunt_user.bl1020_3 = False
                #如果密码长期未改密
                days_since_epoch = int((dt - epoch).days)
                if days_since_epoch > (expire + lastSetPwdDate):
                    for hunt_user in user_hunterList:
                        if hunt_user.userName == user:
                            hunt_user.bl1020_2 = False
    except Exception as ex:
        common.logger.error(f"Error occurred in bl1020pro: {repr(ex)}")
        raise ex

def checkUnUsedAccount(userList, ssh_wrapper, user_hunterList):
    try:
        #找到交互式权限列表
        shells = []
        output, error = ssh_wrapper.execute_command("cat /etc/shells")
        time, error_Time = ssh_wrapper.execute_command("LC_TIME=en_US.UTF-8 date +'%a %b %d %H:%M:%S %z %Y'")
        if not error_Time:
            dt = datetime.strptime(time.strip(), "%a %b %d %H:%M:%S %z %Y")
        if not error:
            for line in output.splitlines():
                if line.startswith("#"):
                    continue
                else:
                    shells.append(line.strip())
        for user in userList:
            #判断有无主目录缺失的用户
            if user.directory is None:
                for user_hunter in user_hunterList:
                    if user_hunter.userName == user:
                        user_hunter.bl1021_3 = False
            # 判断是否非系统用户有交互式权限
            if int(user.UID) < 1000 and user.shell in shells:
                for user_hunter in user_hunterList:
                    if user_hunter.userName == user:
                        user_hunter.bl1021_2 = False
            #判读是否超过90天未登录
            if not user.lastLog or (dt - user.lastLog).days >= 90:
                for user_hunter in user_hunterList:
                    if user_hunter.userName == user.name:
                        user_hunter.bl1021_1 = False
    except Exception as ex:
        common.logger.error(f"Error occurred in checkUnUsedAccount: {repr(ex)}")
        raise ex

    return True


def bl1021_userInfo(login_user_list, specialAccountList, ssh_wrapper, hunter):
    try:
        user_hunterList = []
        checkedUser = []
        output, error = ssh_wrapper.execute_command("cat /etc/passwd")
        userList = []
        script = '''
        LC_TIME=en_US.UTF-8 lastlog | awk '{ 
        if (NF == 8) 
            print $1, $3, $4, $5, $6, $7, $8 
        else if (NF == 9) 
            print $1, $4, $5, $6, $7, $8, $9
        }'
        '''
        if not error:
            for line in output.splitlines():
                user = User()
                user.name = line.split(":")[0]
                #上线需要注释
                if user.name.lower() not in analysis_account_array and user.name not in analysis_account_array:
                    continue
                if user.name.lower() in specialAccountList or user.name in specialAccountList:
                    continue
                user_hunter = copy.deepcopy(hunter)
                user_hunter.userName = user.name
                user.UID = line.split(":")[2]
                user.GUID = line.split(":")[3]
                output, error_dir = ssh_wrapper.execute_command(f'LC_TIME=en_US.UTF-8 groups {user.name}')
                if not error:
                    user.group = output.split(":")[1].split()
                user.directory = line.split(":")[5]
                if user.directory:
                    #查询用户主目录权限
                    output, error_dir = ssh_wrapper.execute_command(f'stat -c "%a" {user.directory}')
                    if not error_dir:
                        user.directoryAuthority = output.strip()
                    #查询该用户主目录创建时间，获取账号创建时间
                    output_birth, error_dir_birth = ssh_wrapper.execute_command(f'LC_TIME=en_US.UTF-8 stat {user.directory}')
                    if not error_dir_birth:
                        for line_b in output_birth.splitlines():
                            if 'Birth' in line_b:
                                user.birthday = line_b.split(":",maxsplit=1)[1].split(".")[0].strip()
                user.shell = line.split(":")[6]
                userList.append(user)
                user_hunterList.append(user_hunter)
        #查询用户最后登录时间信息
        output, error = ssh_wrapper.execute_command(script)
        if not error:
            for line in output.splitlines():
                if line.split()[0] not in checkedUser:
                    checkedUser.append(line.split()[0])
                    login_user_list.append(line.split()[0]+',-,'+datetime.strptime(line.split(maxsplit=1)[1], "%a %b %d %H:%M:%S %z %Y").strftime('%Y-%m-%d %H:%M:%S'))
                for user in userList:
                    if user.name == line.split()[0]:
                        #将最后登录时间转化为datetime对象封装进lastlog属性
                        user.lastLog = datetime.strptime(line.split(maxsplit=1)[1], "%a %b %d %H:%M:%S %z %Y")
        for user in userList:
            if not user.lastLog:
                for user_hunter in user_hunterList:
                    if user.name == user_hunter.userName:
                        user_hunter.bl0034 = False
        #查询账户是否被禁用
        output_passwd, error_passwd = ssh_wrapper.execute_command("cat  /etc/passwd")
        if not error_passwd:
            for line in output_passwd.splitlines():
                for user in userList:
                    if user.name == line.split(":")[0]:
                        if line.split(":")[1] in ["*", "!"]:
                            user.active = False
                        else:
                            user.active = True
        return userList, user_hunterList
    except Exception as ex:
        common.logger.error(f"Error occurred in bl1021_userInfo: {repr(ex)}")
        raise ex


def bl1021_failLog(ssh_wrapper, resultQueue):
    try:
        output, error = ssh_wrapper.execute_command('grep "Failed password" /var/log/auth.log /var/log/secure')
        if output:
            for line in output.splitlines():
                resultQueue.put(line)
        output, error = ssh_wrapper.execute_command('grep "Accepted password" /var/log/auth.log /var/log/secure')
        if output:
            for line in output.splitlines():
                resultQueue.put(line)
        print("-----------------线程执行完毕-------------------")

    except Exception as ex:
        common.logger.error(f"Error occurred in bl1021_failLog: {repr(ex)}")
        raise ex


def checkBl1022(userList, ssh_wrapper, lastUserList, user_hunterList):
    try:
        shells = []
        checkUser = []
        checked = []
        #组名:密码占位符:GID:组内用户列表
        output, error = ssh_wrapper.execute_command('cat /etc/group')
        if not error:
            for line in output.splitlines():
                if line.split(":")[0] == "sudo" or line.split(":")[0] == "wheel":
                    groupUser = line.split(":")[3]
                    if groupUser:
                        for user in groupUser.split(","):
                            if user and user not in checkUser:
                                checkUser.append(user)
        output, error = ssh_wrapper.execute_command("cat /etc/shells")
        if not error:
            for line in output.splitlines():
                if line.startswith("#"):
                    continue
                else:
                    shells.append(line.strip())
        # 校验权限变更
        # 首次检查不进行权限变更校验
        if lastUserList:
            for userNow in userList:
                for userLast in lastUserList:
                    if userNow.name and userLast.name and userNow.name == userLast.name:
                        checked.append(userNow)
                        checked.append(userLast)
                        response = ''
                        # 校验主目录是否发生变更
                        if userNow.directory != userLast.directory:
                            if not userNow.directory:
                                userNow.directory = "空"
                            if not userLast.directory:
                                userLast.directory = "空"
                            response += f"用户“{userNow.name}”主目录由“{userLast.directory}”变更为“{userNow.directory}” "
                        # 校验权限是否发生变更
                        if userNow.directoryAuthority != userLast.directoryAuthority:
                            if not userNow.directoryAuthority:
                                userNow.directoryAuthority = "无权限"
                            if not userLast.directoryAuthority:
                                userLast.directoryAuthority = "无权限"
                            response += f"用户“{userNow.name}”对主目录权限由“{userLast.directoryAuthority}”变更为“{userNow.directoryAuthority}” "
                        # 校验所属组
                        if userNow.group and userLast.group and userNow.group != userLast.group:
                            removed_groups = [item for item in userLast.group if
                                              item not in userNow.group]
                            add_Groups = [item for item in userNow.group if
                                          item not in userLast.group]
                            if removed_groups:
                                for dif in removed_groups:
                                    if dif.strip():
                                        response += f"用户“{userNow.name}”不再属于本地组{dif} "
                            if add_Groups:
                                for dif in add_Groups:
                                    response += f"用户“{userNow.name}”被添加进本地组{dif} "
                        if response:
                            for user_hunter in user_hunterList:
                                if userNow.name == user_hunter.userName:
                                    user_hunter.bl1022_4 = False
                                    user_hunter.authChange = response
                        continue
            if [item for item in userList if item not in checked]:
                for dif in [item for item in userList if item not in checked]:
                    for user_hunter in user_hunterList:
                        if dif.name == user_hunter.userName:
                            user_hunter.bl1022_4 = False
                            user_hunter.authChange += f"新增用户“{dif.name}” "
        for user in userList:
            #主目录为空
            #只有用户自己拥有全部权限,其余情况认为是高权限
            if (user.directoryAuthority is None or user.directoryAuthority == '无权限'
                    or int(user.directoryAuthority) % 10 > 0 or int(user.directoryAuthority)//10 % 10 > 5):
                for user_hunter in user_hunterList:
                    if user.name == user_hunter.userName:
                        user_hunter.bl1022_2 = False
            #系统用户拥有shell权限
            # 明确非交互式 shell 列表
            non_interactive_shells = ["/sbin/nologin", "/bin/false"]
            # 判断逻辑优化
            if int(user.UID) < 1000 and user.shell in shells and user.shell not in non_interactive_shells:
                for user_hunter in user_hunterList:
                    if user.name == user_hunter.userName and user.name not in ['root','sync','shutdown' ,'halt' ]:
                        user_hunter.bl1022_1 = False
            #sudo或者wheel组内成员拥有高权限
            if user.name in checkUser:
                for user_hunter in user_hunterList:
                    if user.name == user_hunter.userName:
                        user_hunter.bl1022_3 = False
            #默认root用户拥有高权限
            if user.UID == "0":
                for user_hunter in user_hunterList:
                    if user.name == user_hunter.userName:
                        user_hunter.bl1022_3 = False
    except Exception as ex:
        common.logger.error(f"Error occurred in bl1022: {repr(ex)}")
        raise ex

def unAuthLogon(login_user_list, q, user_hunterList):
    for line in q.queue:
        ip, account = findIpAndUser(line)
        if account == '':
            continue
        login_user_list.append(account + ',' + ip + ',' +getTime(line).strftime('%Y-%m-%d %H:%M:%S'))
        for user in user_hunterList:
            if user.userName == account:
                if user.logonCount <= 10:
                    if user.loginLog == '':
                        user.loginLog += account + ',' + ip + ',' +getTime(line).strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        user.loginLog += '\n' + account + ',' + ip + ',' +getTime(line).strftime('%Y-%m-%d %H:%M:%S')
                    user.logonCount += 1

def bl1023_Logging(login_user_list, q, user_hunterList):
    try:
        #登录账户名 : 失败次数
        fail_record = {}
        #登录账户名 ： ip
        logIP_record = {}
        #ip登录账户记录
        logUser_record = {}
        queue = deque(maxlen=5)
        if not q.empty():
            for line in q.queue:
                if "Failed password" in line:
                    queue.append(getTime(line))
                    ip, account = findIpAndUser(line)
                    if account == '':
                        continue
                    if account not in login_user_list:
                        login_user_list.append(account)
                    #记录每个ip登录的账户，登录其他账户时认为有风险
                    if ip not in logIP_record:
                        logUser_record[ip] = account
                    elif not logIP_record[ip] == account:
                        for user_hunter in user_hunterList:
                            if user_hunter.userName == account:
                                user_hunter.bl1023 = False
                            if user_hunter.userName == logUser_record[ip]:
                                user_hunter.bl1023 = False
                    # 记录每个账户对应的登录失败次数，过高的认为有安全风险
                    if account in fail_record:
                        fail_record[account] += 1
                        if fail_record[account] >= 5:
                            for user_hunter in user_hunterList:
                                if user_hunter.userName == account:
                                    user_hunter.bl1023 = False
                    else:
                        fail_record[f"{account}"] = 1
                #检查登录成功账户ip是否变化
                elif "Accepted password" in line:
                    queue.append(getTime(line))
                    ip_a, account_a = findIpAndUser(line)
                    # 记录每个ip登录的账户，检测是否存在一个ip登录多个账户
                    if ip_a not in logIP_record:
                        logUser_record[ip_a] = account_a
                    elif not logIP_record[ip_a] == account_a:
                        for user_hunter in user_hunterList:
                            if user_hunter.userName == account_a:
                                user_hunter.bl1023 = False
                    # 记录登录账户的ip，检测ip是否发生变化
                    if account_a not in logIP_record:
                        logIP_record[account_a] = ip_a
                    elif ip_a != logIP_record[account_a]:
                        for user_hunter in user_hunterList:
                            if user_hunter.userName == account_a:
                                user_hunter.bl1023 = False
                # # 创建一个固定长度队列，动态检测五次登录记录时间是否间隔过低
                # if len(queue) == 5 and queue[-1] - queue[0] < timedelta(minutes=5):
                #     return False
    except Exception as ex:
        common.logger.error(f"Error occurred in bl1023_Logging: {repr(ex)}")
        raise ex

def findIpAndUser(line):
    ip = '-'
    account = ''
    if "from" in line:
        ip = line.split("from")[1].split("port")[0].strip()
    if "for" in line:
        account = line.split("for")[1].split("from")[0].strip()
        if 'invalid user' in account:
            account = account.replace('invalid user', '')

    return ip, account.strip()

def getTime(line):
    now = datetime.now()
    if "/var/log/auth.log:" in line:
        line = line.split("/var/log/auth.log:")[1]
    elif "/var/log/secure" in line:
        line = line.split("/var/log/secure:")[1]
    parts = line.split()
    first_three_parts = parts[:3]
    time = ' '.join(first_three_parts)
    dt = datetime.strptime(time, "%b %d %H:%M:%S").replace(year=now.year)
    if dt > now:
        dt = dt.replace(year=now.year - 1)
    return dt



def bl1024(ssh_wrapper, userList, user_hunterList):
    try:
        if su_flag:
            ssh_wrapper = ssh_wrapper.execute_command_chain('''awk -F: '($2 == "") {print $1}' /etc/shadow''')
            output = ssh_wrapper.output
            error = ''
        else:
            output, error = ssh_wrapper.execute_command("cat /etc/shadow")
        output, error = ssh_wrapper.execute_command('''awk -F: '($2 == "") {print $1}' /etc/shadow''')
        if output:
            for line in output.splitlines():
                for user_hunter in user_hunterList:
                    if user_hunter.userName == line.strip():
                        user_hunter.bl1024 = False

    except Exception as ex:
        common.logger.error(f"Error occurred in bl1024: {repr(ex)}")
        raise ex


def bl1025(ssh_wrapper, user_hunterList, q):
    try:
        logIP_record = {}
        for user_hunter in user_hunterList:
            if user_hunter.bl0032 == False:
                user_hunter.bl1025 = False
        if not q.empty():
            #检测账户登录ip是否发生变化
            for line in q.queue:
                if "Accepted password" in line:
                    ip_a, account_a = findIpAndUser(line)
                    if account_a not in logIP_record:
                        logIP_record[account_a] = ip_a
                    elif ip_a != logIP_record[account_a]:
                        for user_hunter in user_hunterList:
                            if user_hunter.userName == account_a:
                                user_hunter.bl1025 = False
    except Exception as ex:
        common.logger.error(f"Error occurred in bl1025_failLog: {repr(ex)}")
        raise ex
    return True


'''
centos 设置密码复杂度 /etc/security/pwquality.conf  /etc/pam.d/system-auth  /etc/pam.d/password-auth
       设置记住密码次数  /etc/pam.d/system-auth /etc/pam.d/system-auth
'''
def bl0027(ssh_wrapper, hunter):
    try:
        #是否启用了相关模块
        failLock_flag = False
        passwd_flag = False
        passwd_remember_flag = False
        #su锁定，ssh锁定只有当两部分都锁定才能通过
        lock_ssh_flag = False
        keys = {
            "minlen": False,
            "dcredit": False,
            "ucredit": False,
            "lcredit": False,
            "ocredit": False,
            "remember": False,
            "retry": False
        }
        #密码复杂度配置文件
        output, error = ssh_wrapper.execute_command("grep -v '^#' /etc/security/pwquality.conf")
        if output:
            for line in output.splitlines():
                if "#" in line:
                    continue
                match = re.search(r'\bminlen\s*=\s*(-?\d+)', line)
                if match:
                    keys["minlen"] = True if int(match.group(1)) >= 8 else False
                match = re.search(r'\bdcredit\s*=\s*(-?\d+)', line)
                if match:
                    keys["dcredit"] = True if int(match.group(1)) <= -1 else False
                match = re.search(r'\bucredit\s*=\s*(-?\d+)', line)
                if match:
                    keys["ucredit"] = True if int(match.group(1)) <= -1 else False
                match = re.search(r'\blcredit\s*=\s*(-?\d+)', line)
                if match:
                    keys["lcredit"] = True if int(match.group(1)) <= -1 else False
                match = re.search(r'\bocredit\s*=\s*(-?\d+)', line)
                if match:
                    keys["ocredit"] = True if int(match.group(1)) <= -1 else False
                    # 为缺失变量赋默认值
        #搜索ubuntu
        keys, failLock_flag, passwd_flag, passwd_remember_flag, lock_su_flag = (
            bl0027_ubuntu(ssh_wrapper, keys, failLock_flag, passwd_flag, passwd_remember_flag))
        #搜索centos
        if not (failLock_flag or lock_su_flag):
            keys, failLock_flag, passwd_flag, passwd_remember_flag, lock_su_flag = (
                bl0027_centos(ssh_wrapper, keys, failLock_flag, passwd_flag, passwd_remember_flag))
        # 查看/etc/security/pwhistory.conf
        # 密码历史记录配置文件
        output, error = ssh_wrapper.execute_command("cat /etc/security/pwhistory.conf")
        if output:
            for line in output.splitlines():
                if "#" in line:
                    continue
                # 记住重复密码次数
                match = re.search(r'\bremember\s*=\s*(-?\d+)', line)
                if match:
                    keys["remember"] = True if int(match.group(1)) >= 5 else False
        # 密码失败锁定配置文件
        # 查看/etc/security/faillock.conf
        output, error = ssh_wrapper.execute_command("cat /etc/security/faillock.conf")
        if failLock_flag:
            if output:
                for line in output.splitlines():
                    if "#" in line:
                        continue
                    # 锁定密码次数
                    # conf中参数生效必须在common-auth中被引用
                    if "deny" in line and "even_deny_root" not in line:
                        match = re.search(r'\bdeny\s*=\s*(-?\d+)', line)
                        if match:
                            lock_su_flag = True if 0 <= int(match.group(1)) < 5 else False
        #未在pam模块中设置强制密码历史记录
        if not passwd_remember_flag and keys["remember"]:
            keys["remember"] = False
        # 验证ssh是否限制登录失败次数
        keys["retry"] = check_lock_ssh(ssh_wrapper, lock_su_flag)
        if not keys["minlen"]:
            hunter.bl0027_1 = False
        if not keys["dcredit"]:
            hunter.bl0027_2 = False
        if not keys["ucredit"]:
            hunter.bl0027_3 = False
        if not keys["lcredit"]:
            hunter.bl0027_4 = False
        if not keys["ocredit"]:
            hunter.bl0027_5 = False

        return keys
    except Exception as ex:
        common.logger.error(f"Error occurred in bl0027: {repr(ex)}")
        raise ex


def bl0027_centos(ssh_wrapper, keys, failLock_flag, passwd_flag, passwd_remember_flag):
    #system-auth中设置的记住密码历史是否满足
    rem_sys_auth_flag = False
    #passwd-auth中设置的记住密码历史是否满足
    rem_pwd_auth_flag = False
    #system-auth中设置的参数是否符合要求，符合则已对su命令进行锁定，只有对su与ssh均锁定才算成功
    lock_su_flag = False
    # 二者均满足才能判定为True
    #必须设置preauth与authfail,authsucc且都满足要求账号锁定策略才算成功
    lock_pre = False
    lock_fail = False
    lock_authsucc = False
    output, error = ssh_wrapper.execute_command("cat /etc/pam.d/system-auth")
    if output:
        for line in output.splitlines():
            if "#" in line:
                continue
            #记住重复密码次数
            #pam_unix.so针对centos7及以前版本，pam_pwhistory.so对应之后版本
            if "pam_pwhistory.so" in line and "use_authtok" in line and "enforce_for_root" in line:
                passwd_remember_flag = True
                match = re.search(r'\bremember\s*=\s*(-?\d+)', line)
                if match:
                    rem_sys_auth_flag = True if int(match.group(1)) >= 5 else False
            #账户锁定次数
            if "pam_faillock.so" in line:
                match = re.search(r'\bdeny\s*=\s*(-?\d+)', line)
                if "preauth" in line:
                    lock_pre = True
                    if match and 0 <= int(match.group(1)) < 5:
                        lock_su_flag = True
                    else:
                        lock_su_flag = False
                elif "authfail" in line and lock_pre:
                    lock_fail = True
                    if match and 0 <= int(match.group(1)) < 5:
                        lock_su_flag = True
                    else:
                        lock_su_flag = False
                elif "authsucc" in line and lock_fail:
                    lock_authsucc = True
            if "pam_pwquality.so" in line:
                passwd_flag = True
        #必须都设置且参数满足要求才符合
        if lock_pre and lock_fail and lock_authsucc:
            #faillock模块启用正确表示
            failLock_flag = True
        else:
            lock_su_flag = False
    #查看password-auth
    output, error = ssh_wrapper.execute_command("cat /etc/pam.d/password-auth")
    if output:
        for line in output.splitlines():
            if "#" in line:
                continue
            #记住重复密码次数
            if "pam_pwhistory.so" in line and "use_authtok" in line and "enforce_for_root" in line:
                passwd_remember_flag = True
                match = re.search(r'\bremember\s*=\s*(-?\d+)', line)
                if match:
                    rem_pwd_auth_flag = True if int(match.group(1)) >= 5 else False
            #账户锁定次数
            # if "pam_faillock.so" in line:
            #     failLock_pwd_flag = True
            #     match = re.search(r'\bdeny\s*=\s*(-?\d+)', line)
            #     if match and 0 <= int(match.group(1)) <= 2:
            #         lock_pwd_flag = True
            if "pam_pwquality.so" in line:
                passwd_flag = True
    if rem_pwd_auth_flag and rem_sys_auth_flag:
        keys["remember"] = True
    else:
        keys["remember"] = False
    return keys, failLock_flag, passwd_flag, passwd_remember_flag, lock_su_flag

#验证ssh是否限制登录失败次数
def check_lock_ssh(ssh_wrapper, lock_su_flag):
    #验证顺序是否正确
    pre_flag = False
    mid_flag = False
    end_flag = False
    if not lock_su_flag:
        return False
    else:
        output, error = ssh_wrapper.execute_command("cat /etc/pam.d/sshd")
        if output:
            for line in output.splitlines():
                if line.startswith("#"):
                    continue
                if "pam_faillock.so" in line and "preauth" in line and "auth" in line:
                    match = re.search(r'\bdeny\s*=\s*(-?\d+)', line)
                    if not (match and 0 <= int(match.group(1)) < 5):
                        return False
                    else:
                        pre_flag = True
                        continue
                if "pam_faillock.so" in line and pre_flag and "auth" in line:
                    match = re.search(r'\bdeny\s*=\s*(-?\d+)', line)
                    if not (match and 0 <= int(match.group(1)) < 5):
                        return False
                    else:
                        mid_flag = True
                        continue
                if "pam_faillock.so" in line and mid_flag and "account" in line:
                    end_flag = True
            return end_flag


def bl0027_ubuntu(ssh_wrapper, keys, failLock_flag, passwd_flag, passwd_remember_flag):
    # system-auth中设置的参数是否符合要求，符合则已对su命令进行锁定，只有对su与ssh均锁定才算成功
    lock_su_flag = False
    # 二者均满足才能判定为True
    # 必须设置preauth与authfail,authsucc且都满足要求账号锁定策略才算成功
    lock_pre = False
    lock_fail = False
    lock_authsucc = False
    output, error = ssh_wrapper.execute_command("cat /etc/pam.d/common-password")
    if output:
        for line in output.splitlines():
            if "pam_cracklib.so" in line or "pam_pwquality.so" in line:
                for part in line.split():
                    if "minlen" in part:
                        keys["minlen"] = True if int(part.split("=")[1].strip()) >= 8 else False
                    if "dcredit" in part:
                        keys["dcredit"] = True if int(part.split("=")[1].strip()) <= -1 else False
                    if "ucredit" in part:
                        keys["ucredit"] = True if int(part.split("=")[1].strip()) <= -1 else False
                    if "lcredit" in part:
                        keys["lcredit"] = True if int(part.split("=")[1].strip()) <= -1 else False
                    if "ocredit" in part:
                        keys["ocredit"] = True if int(part.split("=")[1].strip()) <= -1 else False
            if "remember" in line and "use_authtok" in line and "enforce_for_root" in line and "pam_pwhistory.so" in line:
                passwd_remember_flag = True
                match = re.search(r'\bremember\s*=\s*(-?\d+)', line)
                if match:
                    keys["remember"] = True if int(match.group(1)) >= 5 else False
            elif "use_authtok" in line and "enforce_for_root" in line:
                passwd_remember_flag = True
            if "pam_pwquality.so" in line:
                passwd_flag = True
    output, error = ssh_wrapper.execute_command("cat /etc/pam.d/common-auth")
    if output:
        #验证设置顺序正确
        flag_pre = False
        flag_result = False
        for line in output.splitlines():
            if "#" in line:
                continue
            #确保common-auth内设置顺序正确
            if "preauth" in line:
                flag_pre = True
            if "pam_unix.so" in line and flag_pre:
                flag_result = True
            if "pam_faillock" in line:
                match = re.search(r'\bdeny\s*=\s*(-?\d+)', line)
                if "preauth" in line:
                    lock_pre = True
                    if match and 0 <= int(match.group(1)) < 5:
                        lock_su_flag = True
                    else:
                        lock_su_flag = False
                elif "authfail" in line and lock_pre:
                    lock_fail = True
                    if match and 0 <= int(match.group(1)) < 5:
                        lock_su_flag = True
                    else:
                        lock_su_flag = False
                elif "authsucc" in line and lock_fail:
                    lock_authsucc = True
        #必须都设置且参数满足要求才符合
        if lock_pre and lock_fail and lock_authsucc:
            #faillock模块启用正确表示
            failLock_flag = True
        else:
            lock_su_flag = False
    return keys, failLock_flag, passwd_flag, passwd_remember_flag, lock_su_flag


def bl0028(ssh_wrapper, keys):
    try:
        if keys["minlen"]:
            return True
        else:
            return False
    except Exception as ex:
        common.logger.error(f"Error occurred in bl0028: {repr(ex)}")
        raise ex



def bl0029(ssh_wrapper):
    try:
        output, error = ssh_wrapper.execute_command("cat  /etc/login.defs")
        if error.strip():
            raise RuntimeError(f"read file error: {error}")
        for line in output.splitlines():
            if "#" in line:
                continue
            else:
                if "PASS_MIN_DAYS" in line:
                    if int(line.split()[1].strip()) >= 1:
                        return True
                    else:
                        return False
        raise RuntimeError(f"not find PASS_MIN_DAYS")
    except Exception as ex:
        common.logger.error(f"Error occurred in bl0029: {repr(ex)}")
        raise ex


def bl0030(ssh_wrapper, keys):
    try:
        if keys["remember"]:
            return True
        else:
            return False
    except Exception as ex:
        common.logger.error(f"Error occurred in bl0030: {repr(ex)}")
        raise ex


def checkRetry(keys):
    if keys["retry"]:
        return True
    else:
        return False

def bl0032(ssh_wrapper, userList ,user_hunterList):
    for user in userList:
        if user.name.lower() == "guest" and user.active:
            for hunter in user_hunterList:
                hunter.bl0032 = False


def bl0033(ssh_wrapper, userList, user_hunterList):
    for user in userList:
        if user.name.lower() == "root":
            for hunter in user_hunterList:
                if hunter.userName.lower() == user.name:
                    hunter.bl0033 = False



def bl0034(userList):
    try:
        for user in userList:
            if user.lastLog is None:
                return False
        return True
    except Exception as ex:
        common.logger.error(f"Error occurred in bl0034: {repr(ex)}")
        raise ex


def bl0035(ssh_wrapper):
    try:
        users = []
        groups = []
        sudo_dict = {}
        sudoGroup_dict = []
        output, error = ssh_wrapper.execute_command(r"grep -E '^%sudo|ALL=' /etc/sudoers /etc/sudoers.d/*")
        for line in output.splitlines():
            if line.split(":", maxsplit=1)[1].split(maxsplit=1)[0] in "#":
                continue
            name = line.split(":", maxsplit=1)[1].split(maxsplit=1)[0]
            auth = line.split(":", maxsplit=1)[1].split(maxsplit=1)[1]
            sudo_dict[name] = auth
            if name.startswith("%"):
                groups.append(name[1:])
            else:
                users.append(name)
        for group in groups:
            output, error = ssh_wrapper.execute_command(f"grep '^{group}:' /etc/group")
            if error.strip() not in [""]:
                raise RuntimeError(f"search group error: {error}")
            if output.strip() not in [""] and group == output.split(":", maxsplit=1)[0]:
                sudoGroup_dict.append(output.strip().split(":", 3)[3].split(","))

        return sudo_dict, sudoGroup_dict
    except Exception as ex:
        common.logger.error(f"Error occurred in bl0035: {repr(ex)}")
        raise ex


def bl0036(ssh_wrapper, user_hunterList):
    try:
        output, error = ssh_wrapper.execute_command("cat /etc/pam.d/su")
        if error.strip():
            raise RuntimeError(f"read file error: {error}")
        for line in output.splitlines():
            if not line.startswith("#") and all(keyword in line for keyword in ["auth", "pam_wheel.so", "required"]):
                for user_hunter in user_hunterList:
                    user_hunter.bl0036 = True
    except Exception as ex:
        common.logger.error(f"Error occurred in bl0036: {repr(ex)}")
        raise ex


def bl0037(ssh_wrapper, user_hunterList):
    try:
        if su_flag:
            ssh_wrapper = ssh_wrapper.execute_command_chain("cat /etc/ssh/sshd_config")
            output = ssh_wrapper.output
            error = ''
        else:
            output, error = ssh_wrapper.execute_command("cat /etc/ssh/sshd_config")
        if error.strip():
            raise RuntimeError(f"read file error: {error}")
        for line in output.splitlines():
            if "PermitRootLogin" in line:
                if not line.startswith("#") and line.split()[1] == "yes":
                    for user_hunter in user_hunterList:
                        user_hunter.bl0037 = True
                else:
                    for user_hunter in user_hunterList:
                        user_hunter.bl0037 = False
    except Exception as ex:
        common.logger.error(f"Error occurred in bl0037: {repr(ex)}")
        raise ex


def bl0038(ssh_wrapper):
    try:
        if su_flag:
            ssh_wrapper = ssh_wrapper.execute_command_chain("cat /etc/ssh/sshd_config")
            output = ssh_wrapper.output
            error = ''
        else:
            output, error = ssh_wrapper.execute_command("cat /etc/ssh/sshd_config")
        if error.strip():
            raise RuntimeError(f"read /etc/ssh/sshd_config error: {error}")
        for line in output.splitlines():
            if "PasswordAuthentication" in line:
                if not line.startswith("#") and line.split()[1] == "yes":
                    return True
                else:
                    return False
    except Exception as ex:
        common.logger.error(f"Error occurred in bl0038: {repr(ex)}")
        raise ex


def bl0039(ssh_wrapper):
    try:
        output, error = ssh_wrapper.execute_command("sudo auditctl -l")
        if error.strip():
            return False
        for line in output.splitlines():
            if "-w /etc/passwd -p wa -k passwd_changes" in line:
                return True
            else:
                return False
    except Exception as ex:
        common.logger.error(f"Error occurred in bl0039: {repr(ex)}")
        raise ex

"""
list去重（保留原顺序）
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
查询监测进程队列，判断是否超时
"""
def check_overtime(result_queue, err_location=''):
    if not result_queue.empty():
        result = result_queue.get()
        if result:
            result_queue.put(result)
            raise RuntimeError(f"规则执行超时，任务已自动终止，执行时间：{result}，任务状态：{err_location}")



"""
重新连接每一个连接对象，避免超时自动断开
"""
def reconnect(shhList):
    for ssh_wrapper in shhList:
        ssh_wrapper.connect()

"""
为每个线程新建连接对象
"""
def new_connections(data_map):
    connection_List = []
    for i in range(work_thread_num):
        ssh_wrapper = ssh_connect(data_map)
        connection_List.append(ssh_wrapper)
    return connection_List

"""
格式化代码库搜索格式
"""
def handle_code_type(embeddedAccountCodeLib):
    try:
        """
        .txt,.md,.conf,.json,.cfg,.ini,.properties,.config,.xml,.env,.sql,.yaml,.yml  ————turn to————>
        -iname "*.txt" -o -iname "*.md" -o -iname "*.conf" -o -iname "*.json" -o -iname "*.cfg" -o -iname "*.ini" -o -iname "*.properties" -o -iname "*.config" -o -iname "*.xml" -o -iname "*.env" -o -iname "*.sql" -o -iname "*.yaml" -o -iname "*.yml" 
        """
        result = ''
        for index, suffix in enumerate(embeddedAccountCodeLib.split(",")):
            suffix = suffix.strip()
            if suffix.startswith("."):
                suffix = suffix[1:]
            if suffix:
                if index == len(embeddedAccountCodeLib.split(",")) - 1:
                    whole_file_name = f'-iname "{suffix}" '
                else:
                    whole_file_name = f'-iname "{suffix}" -o '
                result += whole_file_name
        return result
    except Exception as e:
        common.logger.error("格式化代码库搜索格式异常" + repr(e))
        raise e


def split_into_n(arr, n):
    """
    将数组分为n份
    """
    length = len(arr)
    k, r = divmod(length, n)
    result = []
    start = 0
    for i in range(n):
        end = start + k + (1 if i < r else 0)
        result.append(arr[start:end])
        start = end
    return result


def ssh_connect(data_map, return_su_flag=False):
    """
    ssh连接
        su_flag:是否通过切换账号实现登录特权账号（true：是， false：不是）
        -return_su_flag=False（默认-不返回su_flag）
    """
    if data_map['loginAccount'] and data_map['loginAccountPwd']:
        ssh_wrapper = SSHWrapper(data_map['location'], data_map['loginAccount'], data_map['loginAccountPwd'],
                                 data_map['port'])
        ssh_wrapper.connect()
        # 开启链路
        ssh_wrapper.start_chain(2)
        ssh_wrapper.execute_command_chain('su - ' + data_map['user'])
        ssh_wrapper.execute_command_chain(data_map['pwd'])
        su_flag = True
    else:
        ssh_wrapper = SSHWrapper(data_map['location'], data_map['user'], data_map['pwd'], data_map['port'])
        ssh_wrapper.connect()
        su_flag = False
    # 根据是否传入 return_su_flag 返回不同的值
    if not return_su_flag:
        return ssh_wrapper
    else:
        return ssh_wrapper, su_flag

def get_days_since_unix_epoch():
    """
     获取当前系统的 Unix 纪元时间
    """
    now = datetime.now(timezone.utc)
    epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
    days = (now - epoch).days
    return int(days)

data_map = {
    "location": "10.10.10.58",
    "user": "root",
    "pwd": "123jkluio!@#",
    "protocol": "SSH",
    "port": "22",
    "remote": "http://pam-selenium:4444/wd/hub",
    "loginAccount": "",
    "loginAccountPwd": "",
    "database": "",
    "taskId": "132132-DASDAS",
    "discoverEnable": 1,
    "analysisEnable": 1,
    "specialUserList": "",
    "analysisAccountList": [],
    "accountAnalysisRate": 1,
    "embeddedAccountEnable": 0,
    "embeddedAccountCodeLib": ".txt,.md,.conf,.json,.cfg,.ini,.properties,.config,.xml,.env,.sql,.yaml,.yml",
    "userDatalist":'''
    '''
}
if __name__ == '__main__':
    do_analysis(data_map, Queue())

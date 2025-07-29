import copy
import json
import logging
from datetime import timedelta, datetime, timezone
from venv import logger

import pytz
from ldap3 import Server, Connection, ALL, NTLM, SIMPLE
import concurrent.futures
from secmind.rpa_v2 import common

search_filter_users = '(&(|(objectClass=user)(objectClass=person))(!(objectClass=computer)))'
search_filter_trust = '(objectClass=trustedDomain)'
search_filter_domain = '(objectClass=domainDNS)'
search_attributes_trust = ['*']
search_attributes_domain = ['pwdProperties', 'minPwdLength', 'minPwdAge', 'pwdHistoryLength', 'lockoutDuration',
                            'lockOutObservationWindow', 'lockoutThreshold', 'pwdProperties', 'whenChanged', 'maxPwdAge',
                            ]

search_attributes_users = ['sAMAccountName', 'lastLogonTimestamp', 'badPwdCount', 'pwdLastSet', 'memberOf',
                           'distinguishedName', 'userAccountControl', 'badPasswordTime', 'scriptPath',
                           'msDS-FailedInteractiveLogonCount', 'lastLogon', 'adminCount', 'description',
                           'msDS-AllowedToDelegateTo', 'logonHours', 'userWorkStations', 'lockoutTime',
                           'description', 'ntSecurityDescriptor', 'whenCreated']
search_filter_structure = '(objectClass=organizationalUnit)'
search_attributes_structure = ['ou', 'description', 'distinguishedName']
search_filter_NotOU = '(&(|(objectClass=user)(objectClass=person))(!(|(objectClass=organizationalUnit)(objectClass=computer))))'
def do_analysis(data_map, monitor_queue):
    try:
        server_address = data_map['location'] # 域控制器地址
        global wholeUserName
        wholeUserName = data_map['user']  # AD 用户名（格式：域\用户名）
        password = data_map['pwd'] # AD 用户密码
        global analysis_account_array
        analysis_account_array = data_map.get('analysisAccountList')
        if analysis_account_array is None:
            analysis_account_array = []
        # 登录用户名
        global loginUser
        # 认证方式
        global logon_authority
        # 解析域名
        if '\\' in wholeUserName:
            # NetBIOS 域名 + 用户名格式
            domin = wholeUserName.split('\\')[0]
            loginUser = wholeUserName.split('\\')[1]
            search_base_domain = domain_to_search_base(domin)
            logon_authority = 'NTLM'
        elif "@" in wholeUserName:
            # User Principal Name（UPN）格式
            domin = wholeUserName.split('@')[1]
            loginUser = wholeUserName.split('@')[0]
            search_base_domain = domain_to_search_base(domin)
            logon_authority = 'SIMPLE'
        elif "CN" in wholeUserName and "DC" in wholeUserName:
            search_base_domain = extract_dc_from_dn(wholeUserName)
            logon_authority = 'SIMPLE'
        else:
            raise Exception("账号格式错误")
        special_user_data_list = data_map['specialUserList']
        specialList = []
        #关闭库日志
        logging.getLogger().setLevel(logging.WARNING)
        # 特殊账号
        if special_user_data_list == "null":
            special_user_data_list = []
        if special_user_data_list:
            for user_sp in special_user_data_list.split(","):
                specialList.append(user_sp)
        try:
            server = Server(server_address, get_info=ALL)
            if logon_authority == 'NTLM':
                conn = Connection(server, user=wholeUserName, password=password, authentication=NTLM, auto_bind=True)
            else:
                conn = Connection(server, user=wholeUserName, password=password, authentication=SIMPLE, auto_bind=True)
            conn.unbind()
        except Exception as ex:
            common.logger.error(f"登录失败请检查账号密码是否正确: {repr(ex)}")
            raise ex
        return safetyInspection(server, wholeUserName, password, server_address, search_base_domain, specialList )
    except Exception as ex:
        common.logger.error(f"安全检查脚本执行发生错误{repr(ex)}")
        raise ex
#安全检查


class HuntWindowAD:
    def __init__(self):
        super().__init__()
        #全局参数
        self.maxPwdAge = False
        self.defaultAccount = True
        self.bl0015 = False
        self.bl0016 = False
        self.bl0017 = False
        self.bl0018 = False
        self.bl0035 = True
        self.LockoutDuration = False
        self.LockoutThreshold = False
        self.LockoutObservationWindow = False
        #用户单项检查检测
        self.bl0021 = True
        self.bl0022 = True
        self.bl0024 = True
        self.bl0025 = True
        self.bl0026 = True
        self.passwdOverDue = True
        self.cardFlag = True
        self.userWorkStations = True
        self.tryLog = True
        self.notLogged = True
        self.scriptPath = True
        #检查子项
        self.bl0019_1 = False
        self.bl0019_2 = False
        self.bl0019_3 = False
        self.bl0020_1 = True
        self.bl0020_2 = True
        self.bl1001_1 = True
        self.bl1001_2 = True
        self.bl1001_4 = True
        self.bl1001_5 = True
        self.bl1002_1 = True
        self.bl1002_2 = True
        self.bl1002_3 = True
        self.bl1002_4 = True
        self.bl1002_5 = True
        #聚合逻辑判断
        self.bl1003 = True
        self.bl1004 = True
        self.bl1006 = True
        self.bl1007 = True
        self.bl1009 = True
        self.bl1010 = True
        self.bl1011 = True
        self.bl1012 = True
        self.bl1013 = True
        self.bl1014 = True
        self.bl1015 = True
        self.bl1016 = True
        self.user = []
        self.lastLogonTimestamp = None
        self.lastLogonTime = None

        self.logonCount =0
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
        """ 将对象转换为字典 """
        return {
            "userName": self.userName,
            "bl0015": self.bl0015,
            "bl0016": self.bl0016,
            "bl0017": self.bl0017,
            "bl0018": self.bl0018,
            "bl0021": self.bl0021,
            "bl0022": self.bl0022,
            "bl0024": self.bl0024,
            "bl0025": self.bl0025,
            "bl0026": self.bl0026,
            "bl0035": self.bl0035,

            "bl1003": self.bl1003,
            "bl1004": self.bl1004,
            "bl1006": self.bl1006,
            "bl1007": self.bl1007,
            "bl1009": self.bl1009,
            "bl1010": self.bl1010,
            "bl1011": self.bl1011,
            "bl1012": self.bl1012,
            "bl1013": self.bl1013,
            "bl1014": self.bl1014,
            "bl1015": self.bl1015,
            "bl1016": self.bl1016,
            "bl1019": self.bl1019,
            "isHighPermission": self.highAuth,

            #检查子项
            "bl0019_1": self.bl0019_1,
            "bl0019_2": self.bl0019_2,
            "bl0019_3": self.bl0019_3,
            "bl0020_1": self.bl0020_1,
            "bl0020_2": self.bl0020_2,
            "bl1001_1": self.bl1001_1,
            "bl1001_2": self.bl1001_2,
            "bl1001_4": self.bl1001_4,
            "bl1001_5": self.bl1001_5,
            "bl1002_1": self.bl1002_1,
            "bl1002_2": self.bl1002_2,
            "bl1002_3": self.bl1002_3,
            "bl1002_4": self.bl1002_4,
            "bl1002_5": self.bl1002_5,
            #删除1008

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
            "loginLogExport": self.loginLog,
        }
class User:
    def __init__(self):
        super().__init__()
        self.tempFlag = False
        self.accountDisable = False
        self.allowLogonTime = None
        self.lastLogonTime = None


#检查域全局参数设置
def domain_parameter_inspection(conn, hunt):
    print("[INFO] 查询成功，结果如下：")
    # bl0015 -- bl0019 默认为false，检测到符合要求的设置之后设置为true
    for entry in conn.entries:
        # bl0015
        if 'pwdProperties' in entry:
            pwdComplex = entry['pwdProperties'].value
            if int(pwdComplex) & 0x1:
                hunt.bl0015 = True
        # bl0016
        if 'minPwdLength' in entry:
            if int(entry['minPwdLength'].value) < 8:
                hunt.bl0016 = False
        if 'minPwdAge' in entry:
            one_day = timedelta(days=1)
            if not entry['minPwdAge'].value >= one_day:
                hunt.bl0017 = False
        if 'maxPwdAge' in entry and entry['maxPwdAge'].value:
            ninety_day = timedelta(days=90)
            hunt.maxPwdAgeSize = entry['maxPwdAge'].value
            if entry['maxPwdAge'].value >= ninety_day:
                hunt.maxPwdAge = False
        if 'pwdHistoryLength' in entry:
            if int(entry['pwdHistoryLength'].value) >= 5:
                hunt.bl0018 = True
        if 'lockoutDuration' in entry:
            min15 = timedelta(minutes=15)
            if entry['lockoutDuration'].value >= min15 and int(entry['lockoutThreshold'].value) > 0:
                hunt.bl0019_2 = True
            else:
                hunt.bl0019_2 = False
        if 'lockoutThreshold' in entry:
            if int(entry['lockoutThreshold'].value) >= 5:
                hunt.bl0019_1 = True
            else:
                hunt.bl0019_1 = False
        if 'lockOutObservationWindow' in entry:
            min15 = timedelta(minutes=15)
            # 锁定窗口时间未定义时，时间为1560秒
            if entry['lockOutObservationWindow'].value >= min15 and int(entry['lockoutThreshold'].value) > 0:
                hunt.bl0019_3 = True
            else:
                hunt.bl0019_3 = False

    return hunt

#用户数据分析
def user_parameter_inspection(entries, hunt, user_count, special_account, hunterUserList):
    if hunt.maxPwdAgeSize:
        maxPwdAge = hunt.maxPwdAgeSize
    else:
        maxPwdAge = None
    # 获取当前的utf时间
    now = datetime.now()
    now_utc = now.replace(tzinfo=pytz.UTC)
    epoch_start = datetime(1601, 1, 1, tzinfo=pytz.utc)
    epoch_start_notZinfo = datetime(1601, 1, 1)
    time_difference = now_utc - epoch_start
    for entry in entries:
        if not entry['sAMAccountName'].value:
            continue
        user = User()
        user_count = user_count + 1
        #扫描忽略特殊账号
        if entry['sAMAccountName'].value is None or entry['sAMAccountName'].value in special_account:
            continue
        #==========上线取消注释=========
        if not analysis_account_array or (entry['sAMAccountName'].value not in analysis_account_array and
                                          entry['sAMAccountName'].value.lower() not in analysis_account_array):
            # print(f"跳过用户{entry['sAMAccountName'].value}")
            continue
        # user.memberOf = []
        user_hunter = copy.deepcopy(hunt)
        user_hunter.userName = entry['sAMAccountName'].value.lower()
        if entry['sAMAccountName'].value == 'administrator':
            user_hunter.bl0022 = False
        #0021:guest 默认为false
        if 'guest' in str(entry['distinguishedName'].value):
            if not int(entry['userAccountControl'].value) & 0x02:
                user_hunter.bl0021 = False
        #报表导出，账号创建时间
        if 'whenCreated' in entry and entry['whenCreated'].value:
            if isinstance(entry['whenCreated'].value, datetime):
                user_hunter.createTime = entry['whenCreated'].value.strftime("%Y-%m-%d %H:%M:%S")
        #长时间未登录
        try:
            if 'lastLogonTimestamp' in entry and entry['lastLogonTimestamp'].value:
                ninety_days = timedelta(days=90)
                if isinstance(entry['lastLogonTimestamp'].value, datetime):
                    if (now_utc - entry['lastLogonTimestamp'].value) >= ninety_days or not entry['lastLogonTimestamp'].value:
                        user_hunter.bl0026 = False
                        user_hunter.lastLogonTimestamp = entry['lastLogonTimestamp'].value
                #ad域获取到的是FILETIME时间，从1601年1月1日开始的100纳秒间隔数
                #首先通过int(entry['lastLogonTimestamp'].value)/ 10**7 - 11644473600，转化为unix时间，UNIX时间戳是从1970年开始的
                elif isinstance(entry['lastLogonTimestamp'].value, str):
                    filetime_raw = entry['lastLogonTimestamp'].value
                    if filetime_raw:
                        try:
                            filetime_int = int(filetime_raw)
                            unix_time = filetime_int / 10 ** 7 - 11644473600  # FILETIME -> UNIX 时间戳
                            if (time_difference.seconds - unix_time) >= ninety_days.seconds:
                                user_hunter.bl0026 = False
                            user_hunter.lastLogonTimestamp = datetime.utcfromtimestamp(unix_time).replace(
                                tzinfo=timezone.utc)
                        except Exception:
                            user_hunter.lastLogonTimestamp = None

            #从未登录
            elif'lastLogonTimestamp' in entry and not entry['lastLogonTimestamp'].value:
                user_hunter.bl0026 = False
                user_hunter.lastLogonTimestamp = None
        except Exception as ex:
            common.logger.error(f"长时间未登录数据处理异常: {repr(ex)}")
            raise ex
        if 'lastLogon' in entry:
            #从未登录
            utc = pytz.UTC
            tenYearAgo = datetime(2015, 4, 1, 12, 0, 0, tzinfo=utc)
            if  entry['lastLogon'].value:
                if isinstance(entry['lastLogon'].value, str):
                    seconds_since_1601 = int(entry['lastLogon'].value) / 10_000_000
                    last_logon_datetime = epoch_start + timedelta(seconds=seconds_since_1601)
                    if last_logon_datetime < tenYearAgo:
                        user_hunter.notLogged = False
                        user_hunter.lastLogonTime = last_logon_datetime
                        if 'badPasswordTime' in entry and entry['badPasswordTime'].value:
                            if entry['badPasswordTime'].value > last_logon_datetime:
                                user_hunter.tryLog = False
                elif isinstance(entry['lastLogon'].value, datetime) and entry['lastLogon'].value < tenYearAgo:
                    user_hunter.notLogged = False
                    user_hunter.lastLogonTime = entry['lastLogon'].value
                    if 'badPasswordTime' in entry and entry['badPasswordTime'].value:
                        if entry['badPasswordTime'].value > entry['lastLogon'].value:
                            user_hunter.tryLog = False


        if 'userAccountControl' in entry and  entry['userAccountControl'].value:
            #不使用智能卡登录
            if user_hunter.cardFlag and not int(entry['userAccountControl'].value) & 0x40000:
                user_hunter.cardFlag = False

            if not int(entry['userAccountControl'].value) & 0x01:
                user_hunter.scriptFlag = False

            #普通账户
            if int(entry['userAccountControl'].value) & 0x100:
                user.normalUser = True
            else:
                user.normalUser = False

            if int(entry['userAccountControl'].value) & 0x2:
                #true 已禁用账户
                user.accountDisable = True
                user_hunter.accountDisable = True
            else:
                user.accountDisable = False
                user_hunter.accountDisable = False

            # 用户不需要密码
            if int(entry['userAccountControl'].value) & 0x20:
                user_hunter.bl0035 = False
            else:
                user_hunter.bl0035 = True

        if 'badPwdCount' in entry and entry['badPwdCount'].value is not None and int(entry['badPwdCount'].value) >= 5:
            user_hunter.bl0020_1 = False
        if 'lockoutTime' in entry and entry['lockoutTime'].value is not None and entry['lockoutTime'].value:
            if (now_utc - entry['lockoutTime'].value).days <= 30:
                # 频繁账户锁定检查
                user_hunter.bl0020_2 = False
        try:
            if 'pwdLastSet' in entry and entry['pwdLastSet'].value and user_hunter.bl0025:
                if isinstance(entry['pwdLastSet'].value, datetime):
                    if (now_utc - entry['pwdLastSet'].value).days > 90:
                        user_hunter.bl0025 = False
                        user_hunter.passwdOverDue = False
                    user_hunter.lastPwdsetTime = entry['pwdLastSet'].value.strftime("%Y-%m-%d %H:%M:%S")
                    if maxPwdAge:
                        user_hunter.accountExpires = (entry['pwdLastSet'].value + maxPwdAge).strftime("%Y-%m-%d %H:%M:%S")
                elif isinstance(entry['pwdLastSet'].value, str):
                    # print("类型为字符" + str(entry['pwdLastSet'].value))
                    if (int(entry['pwdLastSet'].value) - time_difference.days) >= 90:
                        user_hunter.bl0025 = False
                        user_hunter.passwdOverDue = False
                    # 将 FILETIME 值转换为秒
                    seconds_since_1601 = int(entry['pwdLastSet'].value / 10_000_000)
                    # 计算对应的 datetime 对象
                    user_hunter.accountExpires = (epoch_start_notZinfo + timedelta(seconds=seconds_since_1601) + maxPwdAge).strftime("%Y-%m-%d %H:%M:%S")
                    user_hunter.lastPwdsetTime = (epoch_start_notZinfo + timedelta(seconds=seconds_since_1601)).strftime("%Y-%m-%d %H:%M:%S")


        except Exception as ex:
            common.logger.error(f"处理datetime异常: {repr(ex)}")
            raise ex
        # 仅有一个分组时返回字符串，如果对其使用for遍历会出错分情况讨论
        if 'memberOf' in entry and user_hunter.bl0024 :
            if isinstance(entry['memberOf'].value, list):
                for group in entry['memberOf'].value:
                    if 'Remote Desktop Users' in group:
                        user_hunter.bl0024 = False
                    if 'Domain Admins' in group:
                        user_hunter.bl1013 = False
                    if user_hunter.ugroup == '':
                        user_hunter.ugroup += str(group)
                    else:
                        user_hunter.ugroup += ';' + str(group)
            else:
                if entry['memberOf'].value and 'Remote Desktop Users' in entry['memberOf'].value:
                    user_hunter.bl0024 = False
                if entry['memberOf'].value and 'Domain Admins' in entry['memberOf'].value:
                    user_hunter.bl1013 = False
                if entry['memberOf'].value and user_hunter.ugroup == '':
                    user_hunter.ugroup += str(entry['memberOf'].value)
                elif entry['memberOf'].value:
                    user_hunter.ugroup += ';' + str(entry['memberOf'].value)
        if 'scriptPath' in entry and entry['scriptPath'].value:
            user_hunter.scriptPath = False
        if 'description' in entry and entry['description'].value:
            if any(key in entry['description'].value for key in ["test", "temp"]):
                user.tempFlag = True
        if 'msDS-AllowedToDelegateTo' in entry:
            user.AllowedToDelegateTo = entry['msDS-AllowedToDelegateTo']
        if 'logonHours' in entry and entry['logonHours'].value:
            user.allowLogonTime = entry['logonHours'].value
        if 'userWorkStations' in entry:
            if not entry['userWorkStations'].value:
                user_hunter.userWorkStations = False

        # 总体聚合逻辑判断
        user_hunter = judgment(user_hunter, user)
        hunterUserList.append(user_hunter)
    return hunterUserList, user_count

def judgment(hunt, user):

    # 暴力破解密码风险
    if not (hunt.bl0020_1):
        hunt.bl1001_1 = False
    if not (hunt.bl0020_2):
        hunt.bl1001_2 = False
    if not (hunt.tryLog):
        hunt.bl1001_4 = False
    if not (hunt.notLogged):
        hunt.bl1001_5 = False

    # 密码违反策略检查 bl0025（密码过期，空密码） bl0015 （开启密码复杂性） bl0016（最短密码长度） bl0017（密码最短使用期限） bl0018（密码历史记录）
    if not (hunt.bl0025):
        hunt.bl1002_1 = False
    if not (hunt.bl0015):
        hunt.bl1002_2 = False
    if not (hunt.bl0016):
        hunt.bl1002_4 = False
    if not (hunt.bl0017):
        hunt.bl1002_3 = False
    if not (hunt.bl0018):
        hunt.bl1002_5 = False

    # 密码锁定频率检查 bl0020(近期锁定) _1 _2 bl0019_1  _2 _3（锁定参数设置）
    # if not (hunt.bl0020 and hunt.bl0019):
    #     hunt.bl1003 = False

    # 账户长期未使用 bl0026（长期未使用）
    if not hunt.bl0026:
        hunt.bl1004 = False

    # 默认账户风险 bl0021(guest) bl0022(administrator)
    if not (hunt.bl0021 and hunt.bl0022):
        hunt.bl1006 = False

    # 异常权限配置 bl0024(用户有远程登录权限)
    if not hunt.bl0024:
        hunt.bl1007 = False

    # 弱密码 bl0025（密码过期，空密码） bl0015 （开启密码复杂性） bl0016（最短密码长度） bl0017（密码最短使用期限） bl0018（密码历史记录）
    if not (hunt.bl0025 and hunt.bl0015 and hunt.bl0016 and hunt.bl0017 and hunt.bl0018):
        hunt.bl1008 = False

    # 临时账户风险 tempFlag(默认不是临时账户) accountDisable（默认未禁用）
    if hunt.bl1009 and user.tempFlag and not user.accountDisable:
        hunt.bl1009 = False


    # 未启用或未登录账户 bl0026（长期未使用）
    if not hunt.bl0026:
        hunt.bl1011 = False

    #自动化账户风险 scriptPath(true 默认/无数据， false存在路径)
    if not hunt.scriptPath :
        hunt.bl1012 = False

    #密码过期 passwdOverDue:密码过期 默认false
    if not hunt.passwdOverDue:
        hunt.bl1014 = False

    #登录时间检查 allowLogonTime:允许登录时间二进制表示 lastLogonTime上次登录时间默认为none
    if user.allowLogonTime and user.lastLogonTime:

        # 计算 lastLogonTime 是星期几（0=周一, ..., 6=周日）
        weekday = (hunt.lastLogonTime.weekday() + 1) % 7  # AD 的 week 以周日（0）开始
        hour = hunt.lastLogonTime.hour  # 获取小时数

        # 计算 bit 偏移量
        bit_index = (weekday * 24) + hour  # 计算该时间点在 168 位中的位置

        # 计算所在字节和字节内的 bit 位置
        byte_index = bit_index // 8
        bit_position = 7 - (bit_index % 8)  # bit 在字节内的位置（高位在前）

        # 读取该 bit 是否为 1
        if hunt.bl1015 and not (hunt.allowLogonTime[byte_index] & (1 << bit_position)):
            hunt.bl1015 = False

    #非交互式登录账户
    if not (hunt.cardFlag and hunt.userWorkStations):
        hunt.bl1016 = False
    return hunt

#获取cookie
def get_cookie(conn):
    if 'controls' in conn.result and conn.result['controls']:
        controls = conn.result['controls']
        for key, controls_value in controls.items():
            if 'value' in controls_value and controls_value.get('value').get('cookie'):
                return controls_value.get('value').get('cookie')

#合并判断

#数据合并
def dataMerge(result_hunt, thread_hunt):
    for attr, value in result_hunt.__dict__.items():
        if value and "bl" in attr:
            for attr_thread, value_thread in thread_hunt.__dict__.items():
                if attr == attr_thread and not value_thread:
                    result_hunt.__dict__[attr_thread] = attr_thread
    return result_hunt


#分页查询目标位置
def paginatedQueries(target_search_base, local_conn, hunt, special_account):
    hunterUserList = []
    try:

        user_count = 0
        page_size = 20  # 每页数量
        cookie = None
        #将搜索域设置为用户部门
        # target_search_base = 'OU=' + target_search_base + ',' + search_base_domain
        #首次查询
        local_conn.search(
            search_base=target_search_base,
            search_filter=search_filter_users,
            search_scope='LEVEL',
            attributes=search_attributes_users,
            paged_size=page_size,
            paged_cookie=cookie
        )
        # 通过分页查询的cookie判断当前查询的位置，cookie为None时查询完毕
        cookie = get_cookie(local_conn)
        #针对当前页的数据进行检查
        if local_conn.entries:
            hunterUserList, user_count = user_parameter_inspection(local_conn.entries, hunt, user_count, special_account, hunterUserList)
        while cookie:
            local_conn.search(
                search_base=target_search_base,
                search_filter=search_filter_users,
                search_scope='LEVEL',
                attributes=search_attributes_users,
                paged_size=page_size,
                paged_cookie=cookie
            )
            hunterUserList, user_count = user_parameter_inspection(local_conn.entries, hunt, user_count, special_account, hunterUserList)
            cookie = get_cookie(local_conn)

    except Exception as ex:
        common.logger.error(f"分页查询异常: {repr(ex)}")
        raise ex
    finally:
        #释放连接对象
        local_conn.unbind()
    return hunterUserList


#更新报表导出数据
def updateExportData(user_hunterList):
    for huntUser in user_hunterList:
        #更新用户组
        # huntUser.ugroup
        #是否是特权账号
        if huntUser.bl1013:
            huntUser.isPrivilegeExport = '否'
        else:
            huntUser.isPrivilegeExport = '是'
        #账号状态
        if huntUser.accountDisable:
            huntUser.accountActive = '禁用'
        else:
            huntUser.accountActive = '启用'
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
        if (not huntUser.bl0015 or not huntUser.bl0016 or not huntUser.bl0017 or not huntUser.bl0018
                or not huntUser.bl0019_1 or not huntUser.bl0019_2 or not huntUser.bl0019_3
                or not huntUser.bl0020_1 or not huntUser.bl0020_2
                or not huntUser.bl1001_1 or not huntUser.bl1001_2 or not huntUser.bl1001_4 or not huntUser.bl1001_5
                or not huntUser.bl1002_1 or not huntUser.bl1002_2 or not huntUser.bl1002_3 or not huntUser.bl1002_4 or not huntUser.bl1002_5
        ):
            huntUser.isWeakStrategy = "是"
            updatePasswordStrategyExport(huntUser)
        else:
            huntUser.isWeakStrategy = "否"
        # 长期未登录
        if huntUser.bl1011:
            huntUser.longUnusedExport = '否'
        else:
            huntUser.longUnusedExport = '是'
        #长期未改密
        if huntUser.bl1014:
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
    if not huntUser.bl0015:
        huntUser.passwordStrategyExport += '''检查字段 pwdProperties密码复杂性是否开启。
        '''
    if not huntUser.bl0016:
        huntUser.passwordStrategyExport += '''检查字段minPwdLength的值是否小于12。
        '''
    if not huntUser.bl0017:
        huntUser.passwordStrategyExport += '''查询字段 minPwdAge，确保值为 1 或更高。
        '''
    if not huntUser.bl0018:
        huntUser.passwordStrategyExport += '''查询字段pwdHistoryLength，确保值不小于10。
        '''
    if not huntUser.bl0019_1:
        huntUser.passwordStrategyExport += '''确保以下值：lockoutThreshold=5。
        '''
    if not huntUser.bl0019_2:
        huntUser.passwordStrategyExport += '''确保以下值：lockoutDuration=15。
        '''
    if not huntUser.bl0019_3:
        huntUser.passwordStrategyExport += '''确保以下值：lockoutObservationWindow=15
        '''
    if not huntUser.bl0020_1:
        huntUser.passwordStrategyExport += '''查询所有用户：badPwdCount字段：错误密码次数过多（大于等于5次）
        '''
    if not huntUser.bl0020_2:
        huntUser.passwordStrategyExport += '''查询所有用户：lockoutTime字段：检查近期（30天内）是否被锁定过。
        '''
    if not huntUser.bl1001_1:
        huntUser.passwordStrategyExport += ''' 连续多次尝试登录失败：通过 badPwdCount 字段检测尝试失败次数。连续失败规则：badPwdCount >= 阈值 (如5次)。
        '''
    if not huntUser.bl1001_2:
        huntUser.passwordStrategyExport += ''' 账户锁定记录：通过 lockoutTime 字段检测近期是否被锁定。频繁锁定规则：检测近期(30天内)是否被锁定。
        '''
    if not huntUser.bl1001_4:
        huntUser.passwordStrategyExport += ''' 检查是否未登录期间发生错误密码登录事件
        '''
    if not huntUser.bl1001_5:
        huntUser.passwordStrategyExport += ''' 检测是否有未登录用户
        '''
    if not huntUser.bl1002_1:
        huntUser.passwordStrategyExport += ''' 如果密码未更改时间过长，空密码或密码已过期但仍可使用，则标记为不安全。
        '''
    if not huntUser.bl1002_2:
        huntUser.passwordStrategyExport += ''' 是否开启了“密码必须符合复杂性要求”
        '''
    if not huntUser.bl1002_3:
        huntUser.passwordStrategyExport += ''' 密码使用期限是否满足要求 
        '''
    if not huntUser.bl1002_4:
        huntUser.passwordStrategyExport += ''' 密码最短密码长度是否满足要求 
        '''
    if not huntUser.bl1002_5:
        huntUser.passwordStrategyExport += ''' 密码历史记录是否满足要求，查询字段pwdHistoryLength，确保值不小于10。
        '''


#程序执行入口
def safetyInspection(server, username, password, server_address, search_base_domain, special_account):
    try:
        #count = 0
        hunterUserList = []
        hunt = HuntWindowAD()
        #start = datetime.now()
        if logon_authority == 'NTLM':
            conn = Connection(server, user=wholeUserName, password=password, authentication=NTLM, auto_bind=True)
        else:
            conn = Connection(server, user=wholeUserName, password=password, authentication=SIMPLE, auto_bind=True)
        # 开始查询目标域全局参数
        try:
            conn.search(
                search_base=search_base_domain,
                search_filter=search_filter_domain,
                search_scope='SUBTREE',
                attributes=search_attributes_domain,
            )
        except Exception as e:
            # 域不存在,可能是域名不完整
            if "com" not in search_base_domain or "COM" not in search_base_domain:
                search_base_domain = search_base_domain + ',DC=com'
            conn.search(
                search_base=search_base_domain,
                search_filter=search_filter_domain,
                search_scope='SUBTREE',
                attributes=search_attributes_domain,
            )
        if conn.entries:
            # 检查域中的全局参数
            hunt = domain_parameter_inspection(conn, hunt)
        # 信任关系滥用检查
        conn.search(
            search_base=search_base_domain,
            search_filter=search_filter_trust,
            search_scope='SUBTREE',
            attributes=search_attributes_trust,
        )
        if conn.entries:
            for entry in conn.entries:
                if entry["trustDirection"].value > 0:
                    hunt.bl1019 = False
                if entry["trustType"].value:
                    hunt.bl1019 = False
        else:
            hunt.bl1019 = True
        #检查扫描域的目录结构
        conn.search(
            search_base=search_base_domain,
            search_filter=search_filter_structure,
            search_scope='SUBTREE',
            attributes=search_attributes_structure
        )


        if conn.entries:
            hunterUserList = []
            user_count = 0
            year_2015 = datetime(2015, 1, 1).replace(tzinfo=timezone.utc)
            categories = []
            categories = conn.entries
            notOuUsers = []
            #检查非ou内的用户
            conn.search(
                search_base=search_base_domain,
                search_filter=search_filter_NotOU,
                search_scope='SUBTREE',
                attributes=search_attributes_users
            )
            for entry in conn.entries:
                if "OU" not in entry.distinguishedName.value:
                    notOuUsers.append(entry)
            hunterUserList, user_count = user_parameter_inspection(notOuUsers, hunt, user_count, special_account, hunterUserList)
            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                futures = []
                login_user_list = []
                for entry in categories:
                    if entry is None or 'distinguishedName' not in entry:
                        logger.warning(f"无效的 entry: {entry}")
                        continue
                    #为每个线程新建一个连接对象保证线程安全
                    if logon_authority == 'NTLM':
                        conn_thread = Connection(server, user=wholeUserName, password=password, authentication=NTLM,
                                          auto_bind=True)
                    else:
                        conn_thread = Connection(server, user=wholeUserName, password=password, authentication=SIMPLE,
                                          auto_bind=True)
                    hunt_thread = copy.deepcopy(hunt)
                    futures.append(executor.submit(paginatedQueries, entry['distinguishedName'].value, conn_thread, hunt_thread, special_account))
                for future in concurrent.futures.as_completed(futures):
                    if future.result():
                        hunter_users = future.result()
                        hunterUserList += hunter_users
                        for user in hunterUserList:
                            if user.lastLogonTimestamp and user.lastLogonTimestamp > year_2015 and user.userName:
                                login_user_list.append(f"{user.userName},-,{user.lastLogonTimestamp.strftime('%Y-%m-%d %H:%M:%S')}")
                                if user.logonCount <=10:
                                    if user.loginLog == '':
                                        user.loginLog += f"{user.userName},-,{user.lastLogonTimestamp.strftime('%Y-%m-%d %H:%M:%S')}"
                                    else:
                                        user.loginLog += '\n' + f"{user.userName},-,{user.lastLogonTimestamp.strftime('%Y-%m-%d %H:%M:%S')}"
                                    user.logonCount += 1
                            if user.lastLogonTime and isinstance(user.lastLogonTime, datetime) and user.lastLogonTime > year_2015:
                                login_user_list.append(f"{user.userName},-,{user.lastLogonTime.strftime('%Y-%m-%d %H:%M:%S')}")
                                if user.logonCount <=10:
                                    if user.loginLog == '':
                                        user.loginLog += f"{user.userName},-,{user.lastLogonTimestamp.strftime('%Y-%m-%d %H:%M:%S')}"
                                    else:
                                        user.loginLog += '\n' + f"{user.userName},-,{user.lastLogonTimestamp.strftime('%Y-%m-%d %H:%M:%S')}"
                                    user.logonCount += 1
        #对登录用户进行去重
        login_user_list = list(set(login_user_list))
        #end = datetime.now()
        for user in hunterUserList:
            if user.bl1013 and user.bl1007 and user.bl1012:
                user.highAuth = True
            else:
                user.highAuth = False
        updateExportData(hunterUserList)
        json_output = json.dumps([user.to_dict() for user in hunterUserList], indent=4, ensure_ascii=True)
        print(json_output)
        #空数组保持导出格式一致
        authority = []
        if len(login_user_list) > 100:
            login_user_list = login_user_list[:100]
        return hunterUserList, authority, login_user_list
        # 处理结果
        # print(f"扫描windowAD域总耗时：{(end - start).seconds}seconds, 共扫描{len(hunterUserList)}个用户")

    # 释放连接对象
        conn.unbind()
    except Exception as e:
        logger.exception(f"线程执行异常：{e}")
        raise e


def domain_to_search_base(domain_name: str) -> str:
    """
    将完整域名转化为 LDAP 搜索的 base DN 格式
    例如 "xx.zxc.xx.com" -> "DC=xx,DC=zxc,DC=xx,DC=com"

    :param domain_name: 域名字符串，如 "xx.zxc.xx.com"
    :return: LDAP base DN 字符串
    """
    # example.com ————> DC=example,DC=com
    if "." in domain_name:
        parts = domain_name.split('.')
        dc_parts = [f"DC={part}" for part in parts if part]  # 过滤空字符串
        search_base = ','.join(dc_parts)
        return search_base
    # 仅有一项
    if "." not in domain_name and "," not in domain_name:
        return f"DC={domain_name}"
    else:
        return domain_name

def extract_dc_from_dn(dn: str, target_keys=('CN', 'OU', 'DC')) -> str:
    """
    提取 DN 中指定字段（默认提取 CN、OU、DC），并额外返回 base_dn
    base_dn 是所有 DC= 部分拼接后的字符串，作为 LDAP
    """
    dn_parts = {}
    dc_parts = []  # 用于拼接 base_dn

    for part in dn.split(','):
        if '=' in part:
            key, value = part.strip().split('=', 1)
            key_upper = key.upper()
            if key_upper in target_keys:
                if key_upper == 'DC':
                    dc_parts.append(f"{key}={value}")
                if key_upper in dn_parts:
                    if isinstance(dn_parts[key_upper], list):
                        dn_parts[key_upper].append(value)
                    else:
                        dn_parts[key_upper] = [dn_parts[key_upper], value]
                else:
                    dn_parts[key_upper] = value

    # 拼接 base_dn
    dn_parts['base_dn'] = ','.join(dc_parts)
    return dn_parts['base_dn']

# "user": "zxc.COM\Administrator",
data_map = {
    "location": "10.10.10.118",
    "user": "zxc.com\\Administrator",
    "pwd": "123jkluio!@#",
    "protocol": "rdp",
    "port": "3389",
    "remote": "http://pam-selenium:4444/wd/hub",
    "taskId": "68119762857aba000b161317-681197d0857aba000b161448",
    "weakPasswordEnable": 1,
    "discoverEnable": 1,
    "analysisEnable": 1,
    "specialUserList": "",
    "analysisAccountList": [
        "user3520",
        "user3460",
        "wandou\\Administrator",
        "lwb",
        "user3500"
    ],
    "crackUserDatalist": [

    ]
}
if __name__ == '__main__':
    do_analysis(data_map)


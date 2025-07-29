import concurrent
import logging
import os
import random
import subprocess
import time
from asyncio import futures

from datetime import datetime, timedelta
from multiprocessing import Process, Queue
from pathlib import Path
from threading import Thread

import dmPython
import psycopg2
import pymssql
from secmind.rpa_v2 import common, WinRMWrapper, SSHWrapper
import paramiko
import pymysql
from ldap3 import Server, Connection, ALL, NTLM
import cx_Oracle

john_path = '/root/john-1.9.0-Jumbo-1/run/john'
codebook_path = '/root/service/codebook/'

def do_task(data_map):

    userNameList = data_map['user']
    dataBaseList = data_map['database']
    job_id = data_map['password']
    protocol = data_map['protocol']
    #关闭库日志
    logging.getLogger().setLevel(logging.WARNING)
    logging.getLogger("dmPython").disabled = True
    logging.getLogger("psycopg2").disabled = True
    logging.getLogger("pymssql").disabled = True
    logging.getLogger("secmind.rpa_v2").disabled = True
    logging.getLogger("pymysql").disabled = True
    logging.getLogger("cx_Oracle").disabled = True
    result = []
    try:
        # 判断是否用自定义密码本
        wordlist = f'{codebook_path}codebook.txt'
        if os.path.exists(f'{codebook_path}{job_id}.txt'):
            print(f"本地存在密码本，路径为：{codebook_path}{job_id}.txt")
            wordlist = f'{codebook_path}{job_id}.txt'
        else:
            if codebook(job_id):
                wordlist = f'{codebook_path}{job_id}.txt'
    except Exception as e:
        logging.error(e)
    dir_path = f'{codebook_path}{job_id}.txt'
    with open(dir_path, 'r', encoding='utf-8') as file:
        passWordList = file.read()
    start = datetime.now()
    result_queue = Queue()
    #设置为守护进程，主线程终止监测进程立刻终止避免资源浪费
    t = Thread(target=monitor_runtime, args=(start, result_queue), daemon=True)
    # 工作线程数
    work_thread_num = 3
    t.start()
    if protocol == 'oracle':
        detect_oracle(userNameList, passWordList, data_map, result, dataBaseList, result_queue, work_thread_num)
    elif protocol == 'mysql' or protocol == 'db_kundb':
        detect_mysql(userNameList, passWordList, data_map, result, result_queue, work_thread_num)
    elif protocol == 'dameng':
        detect_dameng(userNameList, passWordList, data_map, result, result_queue, work_thread_num)
    elif protocol == 'sqlserver':
        detect_sqlserver(userNameList, passWordList, data_map, result, dataBaseList, result_queue, work_thread_num)
    elif protocol == 'postgresql' or protocol == 'kingbase8':
        detect_postgre(userNameList, passWordList, data_map, result, dataBaseList, result_queue, work_thread_num)
    elif protocol == 'rdp':
        detect_windows(userNameList, passWordList, data_map, result, result_queue, work_thread_num)
    elif protocol == 'ssh':
        detect_linux(userNameList, passWordList, data_map, result, result_queue, work_thread_num)
    # end = datetime.now()
    # total_seconds = (end - start).total_seconds()
    # print(f"总耗时：{total_seconds} 秒")
    return str(result)

def codebook(id):
    import requests
    print("请求密码本")
    response = requests.post(f'http://xpam-runner-core:33100/account/device/codebook?jobId={id}')

    # 检查请求是否成功
    if response.status_code == 200:
        print("请求成功")
        if response.text:
            # 打开本地文件进行写入
            with open(f'{codebook_path}{id}.txt', 'w') as f:
                f.write(response.text)
            return True
    else:
        common.logger.error('请求失败，状态码：', response.status_code)
    return False

def monitor_runtime(start_time, q):
    print(f"[监测进程启动] PID: {os.getpid()}")
    while True:
        now = datetime.now()
        elapsed = now - start_time
        print(f"[监测进程] 已运行时间：{elapsed}")

        if elapsed > timedelta(minutes=60*2):
            q.put(f"{elapsed}")
            print(f"[监测进程] 检测超时，脚本运行时间：{elapsed}")
        time.sleep(60 * 10)  # 每10分钟检测一次

def detect_mysql(userNameList, passWordList, data_map, result, result_queue, work_thread_num, account_discover_map=None):
    checked = []
    common.logger.info("=====userNameList类型：" + str(type(userNameList)))
    if isinstance(userNameList, str):
        if not isinstance(userNameList, list):
            userNameList = userNameList.splitlines()
    common.logger.info("=====passWordList类型：" + str(type(passWordList)))
    if isinstance(passWordList, str):
        if not isinstance(passWordList, list):
            passWordList = passWordList.splitlines()
    common.logger.info("=====处理后userNameList类型：" + str(type(userNameList)))
    common.logger.info("=====处理后passWordList类型：" + str(type(passWordList)))
    # 多线程进行爆破
    futures = []
    userNameList = split_into_n(userNameList, work_thread_num)
    with concurrent.futures.ThreadPoolExecutor(max_workers=work_thread_num) as executor:
        for index, file in enumerate(userNameList):
            if account_discover_map is None:
                futures.append(executor.submit(mysql_detail, userNameList[index], passWordList, data_map, result_queue))
            else:
                futures.append(executor.submit(mysql_detail, userNameList[index], passWordList, data_map, result_queue, account_discover_map))
        for future in concurrent.futures.as_completed(futures):
            # 获取每个线程的返回值
            result_from_thread = future.result()
            if result_from_thread:
                result.extend(result_from_thread)

def mysql_detail(userNameList, passWordList, data_map, result_queue, account_discover_map=None):
    checked = []
    result = []
    for username in userNameList:
        checked.append(username)
        print(f"===资产探测中====当前用户：{username}, 进度：{(len(checked) / len(userNameList)) * 100:.2f}%")
        for password in passWordList:
            if not result_queue.empty():
                result = result_queue.get()
                if result:
                    raise RuntimeError(f"脚本执行超时，任务已自动终止，执行时间：{result}，当前状态：扫描未纳管账号中")
            try:
                connect = pymysql.connect(
                    host=data_map['location'],
                    user=username,
                    password=password)
                cursor = connect.cursor()
                info = 'ip:' + data_map['location'] + ' username:' + username + ' password:' + password
                result.append(info)
            except Exception as ex:
                pass
        # 更新账号状态为已检测
        if account_discover_map is not None:
            account_info = account_discover_map.get(username)
            if account_info is None:
                continue
            account_info["timedOutMessage"] = "success"
    return result

def detect_dameng(userNameList, passWordList, data_map, result, result_queue, work_thread_num, account_discover_map=None):
    common.logger.info("=====userNameList类型：" + str(type(userNameList)))
    if isinstance(userNameList, str):
        if not isinstance(userNameList, list):
            userNameList = userNameList.splitlines()
    common.logger.info("=====passWordList类型：" + str(type(passWordList)))
    if isinstance(passWordList, str):
        if not isinstance(passWordList, list):
            passWordList = passWordList.splitlines()
    common.logger.info("=====处理后userNameList类型：" + str(type(userNameList)))
    common.logger.info("=====处理后passWordList类型：" + str(type(passWordList)))
    # 多线程进行爆破
    futures = []
    userNameList = split_into_n(userNameList, work_thread_num)
    with concurrent.futures.ThreadPoolExecutor(max_workers=work_thread_num) as executor:
        for index, file in enumerate(userNameList):
            if account_discover_map is None:
                futures.append(executor.submit(dameng_detail, userNameList[index], passWordList, data_map, result_queue))
            else:
                futures.append(
                    executor.submit(dameng_detail, userNameList[index], passWordList, data_map, result_queue, account_discover_map))

        for future in concurrent.futures.as_completed(futures):
            # 获取每个线程的返回值
            result_from_thread = future.result()
            if result_from_thread:
                result.extend(result_from_thread)

def dameng_detail(userNameList, passWordList, data_map, result_queue, account_discover_map=None):
    checked = []
    result = []
    for username in userNameList:
        checked.append(username)
        print(
            f"===资产探测中====当前用户：{username}, 进度：{(len(checked) / len(userNameList)) * 100:.2f}%")
        for password in passWordList:
            if not result_queue.empty():
                result = result_queue.get()
                if result:
                    raise RuntimeError(f"脚本执行超时，任务已自动终止，执行时间：{result}，当前状态：扫描未纳管账号中")
            try:
                connect = dmPython.connect(
                    server=data_map['location'],
                    port=int(data_map['port']),
                    user=username,
                    password=password)
                cursor = connect.cursor()
                info = 'ip:' + data_map['location'] + ' username:' + username + ' password:' + password
                result.append(info)
            except Exception as ex:
                pass
        # 更新账号状态为已检测
        if account_discover_map is not None:
            account_info = account_discover_map.get(username)
            if account_info is None:
                continue
            account_info["timedOutMessage"] = "success"
    return result

def detect_oracle(userNameList, passWordList, data_map, result, dataBaseList, result_queue, work_thread_num, account_discover_map=None):
    common.logger.info("=====userNameList类型：" + str(type(userNameList)))
    if isinstance(userNameList, str):
        if not isinstance(userNameList, list):
            userNameList = userNameList.splitlines()
    common.logger.info("=====passWordList类型：" + str(type(passWordList)))
    if isinstance(passWordList, str):
        if not isinstance(passWordList, list):
            passWordList = passWordList.splitlines()
    common.logger.info("=====处理后userNameList类型：" + str(type(userNameList)))
    common.logger.info("=====处理后passWordList类型：" + str(type(passWordList)))
    if dataBaseList is None or dataBaseList == '' or len(dataBaseList) == 0:
        if 'database' in data_map and data_map['database'] != '':
            dataBaseList = data_map['database']
        else:
            dataBaseList = getDb()
    if isinstance(dataBaseList, str):
        dataBaseList = dataBaseList.splitlines()

    # 多线程进行爆破
    futures = []
    userNameList = split_into_n(userNameList, work_thread_num)
    with concurrent.futures.ThreadPoolExecutor(max_workers=work_thread_num) as executor:
        for index, file in enumerate(userNameList):
            if account_discover_map is None:
                futures.append(executor.submit(oracle_detail, userNameList[index], passWordList, data_map, result_queue, dataBaseList))
            else:
                futures.append(executor.submit(oracle_detail, userNameList[index], passWordList, data_map, result_queue,
                                               dataBaseList, account_discover_map))
        for future in concurrent.futures.as_completed(futures):
            # 获取每个线程的返回值
            result_from_thread = future.result()
            if result_from_thread:
                result.extend(result_from_thread)

def oracle_detail(userNameList, passWordList, data_map, result_queue, dataBaseList, account_discover_map=None):
    lock_flag = False
    t = random.randint(1, 100)
    checked = []
    result = []
    for username in userNameList:
        checked.append(username)
        print(f"==={t}资产探测中====当前用户：{username}, 进度：{(len(checked) / len(userNameList)) * 100:.2f}%")
        for password in passWordList:
            print(
                f"==={t}资产探测中====当前用户：{username}, 密码：{password},时间：{datetime.now()}")
            if not result_queue.empty():
                result = result_queue.get()
                if result:
                    raise RuntimeError(f"脚本执行超时，任务已自动终止，执行时间：{result}，当前状态：扫描未纳管账号中")
            for database in dataBaseList:
                try:
                    print(
                        f"==={t}开始碰撞====当前用户：{username}, 密码：{password},时间：{datetime.now()}")
                    url = "{0}/{1}@{2}:{3}/{4}".format(username, password, data_map['location'], data_map['port'],
                                                       database)
                    connect = cx_Oracle.connect(url)
                    cursor = connect.cursor()
                    info = 'ip:' + data_map[
                        'location'] + ' username:' + username + ' password:' + password + ' database:' + database
                    result.append(info)
                except Exception as ex:
                    print(
                        f"==={t}碰撞失败====当前用户：{username}, 密码：{password},时间：{datetime.now()}")
                    print( ex)
                    # time.sleep(0.5)
                    if ex.args[0].code == 28000:
                        print("当前账户被锁定")
                        lock_flag = True
                        # break;
                    pass
            if lock_flag:
                break
        # 更新账号状态为已检测
        if account_discover_map is not None:
            account_info = account_discover_map.get(username)
            if account_info is None:
                continue
            account_info["timedOutMessage"] = "success"
        if lock_flag:
            lock_flag = False
            continue
    return result

def detect_sqlserver(userNameList, passWordList, data_map, result, dataBaseList, result_queue, work_thread_num, account_discover_map=None):
    common.logger.info("=====userNameList类型：" + str(type(userNameList)))
    if isinstance(userNameList, str):
        if not isinstance(userNameList, list):
            userNameList = userNameList.splitlines()
    common.logger.info("=====passWordList类型：" + str(type(passWordList)))
    if isinstance(passWordList, str):
        if not isinstance(passWordList, list):
            passWordList = passWordList.splitlines()
    common.logger.info("=====处理后userNameList类型：" + str(type(userNameList)))
    common.logger.info("=====处理后passWordList类型：" + str(type(passWordList)))
    if dataBaseList is None or dataBaseList == '' or len(dataBaseList) == 0:
        if 'database' in data_map and data_map['database'] != '':
            dataBaseList = data_map['database']
        else:
            dataBaseList = getDb()
    if isinstance(dataBaseList, str):
        dataBaseList = dataBaseList.splitlines()
    # 多线程进行爆破
    futures = []
    userNameList = split_into_n(userNameList, work_thread_num)
    with concurrent.futures.ThreadPoolExecutor(max_workers=work_thread_num) as executor:
        for index, file in enumerate(userNameList):
            if account_discover_map is None:
                futures.append(executor.submit(sqlserver_detail, userNameList[index], passWordList, data_map, result_queue,
                                           dataBaseList))
            else:
                futures.append(
                    executor.submit(sqlserver_detail, userNameList[index], passWordList, data_map, result_queue,
                                    dataBaseList, account_discover_map))
        for future in concurrent.futures.as_completed(futures):
            # 获取每个线程的返回值
            result_from_thread = future.result()
            if result_from_thread:
                result.extend(result_from_thread)

def sqlserver_detail(userNameList, passWordList, data_map, result_queue, dataBaseList, account_discover_map=None):
    result = []
    checked = []
    for username in userNameList:
        checked.append(username)
        print(
            f"===资产探测中====当前用户：{username}, 进度：{(len(checked) / len(userNameList)) * 100:.2f}%")
        for password in passWordList:
            if not result_queue.empty():
                result = result_queue.get()
                if result:
                    raise RuntimeError(f"脚本执行超时，任务已自动终止，执行时间：{result}，当前状态：扫描未纳管账号中")
            for database in dataBaseList:
                try:
                    connect = pymssql.connect(
                        host=data_map['location'],
                        port=data_map['port'],
                        database=database,
                        user=username,
                        password=password)
                    cursor = connect.cursor()
                    info = 'ip:' + data_map[
                        'location'] + ' username:' + username + ' password:' + password + ' database:' + database
                    result.append(info)
                except Exception as ex:
                    pass
        # 更新账号状态为已检测
        if account_discover_map is not None:
            account_info = account_discover_map.get(username)
            if account_info is None:
                continue
            account_info["timedOutMessage"] = "success"
    return result

def detect_postgre(userNameList, passWordList, data_map, result, dataBaseList, result_queue, work_thread_num, account_discover_map=None):
    common.logger.info("=====userNameList类型：" + str(type(userNameList)))
    if isinstance(userNameList, str):
        if not isinstance(userNameList, list):
            userNameList = userNameList.splitlines()
    common.logger.info("=====passWordList类型：" + str(type(passWordList)))
    if isinstance(passWordList, str):
        if not isinstance(passWordList, list):
            passWordList = passWordList.splitlines()
    common.logger.info("=====处理后userNameList类型：" + str(type(userNameList)))
    common.logger.info("=====处理后passWordList类型：" + str(type(passWordList)))
    if dataBaseList is None or dataBaseList == '' or len(dataBaseList) == 0:
        if 'database' in data_map and data_map['database'] != '':
            dataBaseList = data_map['database']
        else:
            dataBaseList = getDb()
    if isinstance(dataBaseList, str):
        dataBaseList = dataBaseList.splitlines()

    # 多线程进行爆破
    futures = []
    userNameList = split_into_n(userNameList, work_thread_num)
    with concurrent.futures.ThreadPoolExecutor(max_workers=work_thread_num) as executor:
        for index, file in enumerate(userNameList):
            if account_discover_map is None:
                futures.append(executor.submit(postgres_detail, userNameList[index], passWordList, data_map, result_queue,
                                           dataBaseList))
            else:
                futures.append(
                    executor.submit(postgres_detail, userNameList[index], passWordList, data_map, result_queue,
                                    dataBaseList, account_discover_map))
        for future in concurrent.futures.as_completed(futures):
            # 获取每个线程的返回值
            result_from_thread = future.result()
            if result_from_thread:
                result.extend(result_from_thread)

def postgres_detail(userNameList, passWordList, data_map, result_queue, dataBaseList, account_discover_map=None):
    checked = []
    result = []
    for username in userNameList:
        checked.append(username)
        print(
            f"===资产探测中====当前用户：{username}, 进度：{(len(checked) / len(userNameList)) * 100:.2f}%")
        for password in passWordList:
            if not result_queue.empty():
                result = result_queue.get()
                if result:
                    raise RuntimeError(f"脚本执行超时，任务已自动终止，执行时间：{result}，当前状态：扫描未纳管账号中")
            for database in dataBaseList:
                try:
                    conn_params = {
                        "dbname": database,
                        "user": username,
                        "password": password,
                        "host": data_map['location'],
                        "port": data_map['port']
                    }
                    connect = psycopg2.connect(**conn_params)
                    cursor = connect.cursor()
                    info = 'ip:' + data_map[
                        'location'] + ' username:' + username + ' password:' + password + ' database:' + database
                    result.append(info)
                except Exception as ex:
                    pass
        # 更新账号状态为已检测
        if account_discover_map is not None:
            account_info = account_discover_map.get(username)
            if account_info is None:
                continue
            account_info["timedOutMessage"] = "success"
    return result

def detect_windows(userNameList, passWordList, data_map, result, result_queue, work_thread_num, account_discover_map=None):
    common.logger.info("=====userNameList类型：" + str(type(userNameList)))
    if isinstance(userNameList, str):
        if not isinstance(userNameList, list):
            userNameList = userNameList.splitlines()
    common.logger.info("=====passWordList类型：" + str(type(passWordList)))
    if isinstance(passWordList, str):
        if not isinstance(passWordList, list):
            passWordList = passWordList.splitlines()
    common.logger.info("=====处理后userNameList类型：" + str(type(userNameList)))
    common.logger.info("=====处理后passWordList类型：" + str(type(passWordList)))

    # 多线程进行爆破
    futures = []
    userNameList = split_into_n(userNameList, work_thread_num)
    with concurrent.futures.ThreadPoolExecutor(max_workers=work_thread_num) as executor:
        for index, file in enumerate(userNameList):
            if account_discover_map is None:
                futures.append(
                    executor.submit(windows_detail, userNameList[index], passWordList, data_map, result_queue))
            else:
                futures.append(
                    executor.submit(windows_detail, userNameList[index], passWordList, data_map, result_queue, account_discover_map ))
        for future in concurrent.futures.as_completed(futures):
            # 获取每个线程的返回值
            result_from_thread = future.result()
            if result_from_thread:
                result.extend(result_from_thread)

def windows_detail(userNameList, passWordList, data_map, result_queue, account_discover_map=None):
    checked = []
    result = []
    for username in userNameList:
        checked.append(username)
        print(f"===资产探测中====当前用户：{username}, 进度：{(len(checked) / len(userNameList)) * 100:.2f}%")
        for password in passWordList:
            if not result_queue.empty():
                result = result_queue.get()
                if result:
                    raise RuntimeError(f"脚本执行超时，任务已自动终止，执行时间：{result}，当前状态：扫描未纳管账号中")
            try:
                winrm_wrapper = WinRMWrapper(host=data_map['location'], username=username, password=password)
                winrm_wrapper.connect()
                info = 'ip:' + data_map[
                    'location'] + ' username:' + username + ' password:' + password + ' database:'
                result.append(info)
            except Exception as ex:
                pass
        # 更新账号状态为已检测
        if account_discover_map is not None:
            account_info = account_discover_map.get(username)
            if account_info is None:
                continue
            account_info["timedOutMessage"] = "success"
    return result

def detect_windowsAD(userNameList, passWordList, data_map, result, result_queue, domain, work_thread_num, account_discover_map=None):
    common.logger.info("=====userNameList类型：" + str(type(userNameList)))
    if isinstance(userNameList, str):
        if not isinstance(userNameList, list):
            userNameList = userNameList.splitlines()
    common.logger.info("=====passWordList类型：" + str(type(passWordList)))
    if isinstance(passWordList, str):
        if not isinstance(passWordList, list):
            passWordList = passWordList.splitlines()
    common.logger.info("=====处理后userNameList类型：" + str(type(userNameList)))
    common.logger.info("=====处理后passWordList类型：" + str(type(passWordList)))

    # 多线程进行爆破
    futures = []
    userNameList = split_into_n(userNameList, work_thread_num)
    with concurrent.futures.ThreadPoolExecutor(max_workers=work_thread_num) as executor:
        for index, file in enumerate(userNameList):
            if account_discover_map is None:
                futures.append(executor.submit(windowsAD_detail, userNameList[index], passWordList, data_map, result_queue, domain))
            else:
                futures.append(
                    executor.submit(windowsAD_detail, userNameList[index], passWordList, data_map, result_queue,
                                    domain,account_discover_map))
        for future in concurrent.futures.as_completed(futures):
            # 获取每个线程的返回值
            result_from_thread = future.result()
            if result_from_thread:
                result.extend(result_from_thread)

def windowsAD_detail(userNameList, passWordList, data_map, result_queue, domain, account_discover_map=None):
    result = []
    checked = []
    for username in userNameList:
        if "\\" not in username:
            username = domain + "\\" + username
        checked.append(username)
        print(
            f"===资产探测中====当前用户：{username}, 进度：{(len(checked) / len(userNameList)) * 100:.2f}%")
        for password in passWordList:
            if not result_queue.empty():
                result = result_queue.get()
                if result:
                    raise RuntimeError(f"脚本执行超时，任务已自动终止，执行时间：{result}，当前状态：扫描未纳管账号中")
            try:
                server = Server(data_map['location'], get_info=ALL)
                conn = Connection(server, user=username, password=password, authentication=NTLM, auto_bind=True)
                conn.unbind()
                info = 'ip:' + data_map[
                    'location'] + ' username:' + username + ' password:' + password + ' database:'
                if conn.extend.standard.who_am_i() is None:
                    raise Exception("登录失败：请检查账号或密码是否正确。当前连接被识别为匿名绑定，未使用有效身份认证")
                result.append(info)
            except Exception as ex:
                pass
        # 更新账号状态为已检测
        if account_discover_map is not None:
            account_info = account_discover_map.get(username)
            if account_info is None:
                continue
            account_info["timedOutMessage"] = "success"
    return result

def detect_linux(userNameList, passWordList, data_map, result, result_queue, work_thread_num, account_discover_map=None):
    checked = []
    common.logger.info("=====userNameList类型：" + str(type(userNameList)))
    if isinstance(userNameList, str):
        if not isinstance(userNameList, list):
            userNameList = userNameList.splitlines()
    common.logger.info("=====passWordList类型：" + str(type(passWordList)))
    if isinstance(passWordList, str):
        if not isinstance(passWordList, list):
            passWordList = passWordList.splitlines()
    common.logger.info("=====处理后userNameList类型：" + str(type(userNameList)))
    common.logger.info("=====处理后passWordList类型：" + str(type(passWordList)))
    # 多线程进行爆破
    futures = []
    userNameList = split_into_n(userNameList, work_thread_num)
    with concurrent.futures.ThreadPoolExecutor(max_workers=work_thread_num) as executor:
        for index, file in enumerate(userNameList):
            if account_discover_map is None:
                futures.append(
                    executor.submit(linux_detail, userNameList[index], passWordList, data_map, result_queue))
            else:
                futures.append(
                    executor.submit(linux_detail, userNameList[index], passWordList, data_map, result_queue, account_discover_map))
        for future in concurrent.futures.as_completed(futures):
            # 获取每个线程的返回值
            result_from_thread = future.result()
            if result_from_thread:
                result.extend(result_from_thread)

def linux_detail(userNameList, passWordList, data_map, result_queue, account_discover_map=None):
    checked = []
    result = []
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for username in userNameList:
        checked.append(username)
        print(f"===资产探测中====当前用户：{username}, 进度：{(len(checked) / len(userNameList)) * 100:.2f}%")
        for password in passWordList:
            if not result_queue.empty():
                result = result_queue.get()
                if result:
                    raise RuntimeError(f"脚本执行超时，任务已自动终止，执行时间：{result}，当前状态：扫描未纳管账号中")
            print(
                f"===资产探测中,开始连接====当前用户：{username}, 密码：{password},时间：{datetime.now()}")

            try:
                client.connect(
                    hostname=data_map['location'],
                    port=data_map['port'],
                    username=username,
                    password=password,
                    timeout=10,
                    banner_timeout=15,
                    allow_agent=False,
                    look_for_keys=False
                )
                print(
                    f"===资产探测中,连接结束了哦====当前用户：{username}, 密码：{password},时间：{datetime.now()}")
                info = 'ip:' + data_map['location'] + ' username:' + username + ' password:' + password
                result.append(info)
            except paramiko.AuthenticationException:
                print(
                    f"===资产探测中,认证失败====当前用户：{username}, 密码：{password},时间：{datetime.now()}")
                pass
            except paramiko.SSHException as e:
                print(f"SSH连接过于频繁：{e}")
                pass
            except Exception as ex:
                pass
            finally:
                client.close()
        # 更新账号状态为已检测
        if account_discover_map is not None:
            account_info = account_discover_map.get(username)
            if account_info is None:
                continue
            account_info["timedOutMessage"] = "success"
    return result

def getDb():
    dir_path = f'/root/xpam-ruleworker/scripts/push/database.txt'
    if os.path.exists(dir_path):
        with open(dir_path, 'r', encoding='utf-8') as file:
            dbList = file.read()
    else:
        dbList = '''Public
orcl
master
'''
    return dbList.splitlines()

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

if __name__ == '__main__':
    common.go(do_task)
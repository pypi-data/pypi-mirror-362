# !/usr/bin/python
# -*- coding:utf-8 -*-
# Author: Pete Yan <pete.yan@aliyun.com>
# Date  : 2021/9/8
# eg: -r 2 -u admin -p En&4sODTkuCh -t local -n Fn&4sODTkuCh -l https://47.101.139.48/
import getopt
import signal
import sys
import time
import traceback

from secmind.rpa import DesiredCapabilities
from secmind.rpa import Options
from secmind.rpa import webdriver


class PamConnector:
    def __init__(self, args):
        self.args = args
        self.run_fn = None
        self.user = None
        self.pwd = None
        self.type = None
        self.new_pwd = None
        self.location = None
        self.driver = None

    def verify_login(self):
        try:
            self.driver.get(self.location)
            self.driver.find_element_by_id("username").send_keys(self.user)
            time.sleep(1)
            self.driver.find_element_by_id("password").send_keys(self.pwd)
            time.sleep(1)
            self.driver.find_element_by_id("loginbtn").click()
            time.sleep(1)
            self.driver.switch_to.frame("topframe")
            result = self.driver.find_element_by_id("loginuser").is_enabled()
            if result:
                print("result=" + "true")
            else:
                print("result=" + "false")
        except Exception:
            print(traceback.print_exc())
            print("result=" + "false")
        finally:
            if self.driver is not None:
                self.driver.quit()

    def verify_modify_pwd(self):
        try:
            self.driver.get(self.location)
            self.driver.find_element_by_id("username").send_keys(self.user)
            time.sleep(1)
            self.driver.find_element_by_id("password").send_keys(self.pwd)
            time.sleep(1)
            self.driver.find_element_by_id("loginbtn").click()
            time.sleep(1)
            self.driver.switch_to.frame("topframe")
            if self.driver.find_element_by_id("loginuser").is_enabled():
                self.driver.switch_to.parent_frame()
                self.driver.switch_to.frame('menu')
                self.driver.find_element_by_xpath("//span[contains(.,'系统维护')]").click()
                time.sleep(2)
                self.driver.find_element_by_xpath("//span[contains(.,'密码修改')]").click()
                self.driver.switch_to.parent_frame()
                self.driver.switch_to.frame('content')
                time.sleep(1)
                cur_pwd = self.driver.find_element_by_name('curpwd')
                cur_pwd.clear()
                cur_pwd.send_keys(self.pwd)
                time.sleep(1)
                new_pwd1 = self.driver.find_element_by_name('newpwd1')
                new_pwd1.clear()
                new_pwd1.send_keys(self.new_pwd)
                time.sleep(1)
                new_pwd2 = self.driver.find_element_by_name('newpwd2')
                new_pwd2.clear()
                new_pwd2.send_keys(self.new_pwd)
                self.driver.find_element_by_xpath("//input[@value='提交修改']").click()
                self.driver.switch_to.alert.accept()
                print("result=" + "true")
            else:
                print("result=" + "false")
        except Exception:
            print(traceback.print_exc())
            print("result=" + "false")
        finally:
            if self.driver is not None:
                self.driver.quit()

    def get_driver(self):
        if self.type == 'local':
            options = Options()
            options.add_argument('--allow-running-insecure-content')
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--no-sandbox')
            self.driver = webdriver.Chrome('./chromedriver', options=options)
        elif self.type == 'remote':
            options = Options()
            options.add_argument('--allow-running-insecure-content')
            options.add_argument('--ignore-certificate-errors')
            # driver = webdriver.Chrome(options=options)
            driver = webdriver.Remote(command_executor='http://81.68.68.227:4444/wd/hub',
                                      desired_capabilities=DesiredCapabilities.CHROME, options=options)
            driver.maximize_window()
            self.driver = driver

    def action(self):
        if len(self.args) > 0:
            try:
                argv = self.args[1:]
                opts, args = getopt.getopt(argv, "r:u:p:t:n:l:")
                for opt, arg in opts:
                    if opt in ['-r']:
                        self.run_fn = arg
                    elif opt in ['-u']:
                        self.user = arg
                    elif opt in ['-p']:
                        self.pwd = arg
                    elif opt in ['-t']:
                        self.type = arg
                    elif opt in ['-n']:
                        self.new_pwd = arg
                    elif opt in ['-l']:
                        self.location = arg

                if self.run_fn == '1':
                    self.get_driver()
                    self.verify_login()
                elif self.run_fn == '2':
                    self.get_driver()
                    self.verify_modify_pwd()
            except Exception as e:
                print(traceback.print_exc())


def main():
    if len(sys.argv) < 2:
        print('Abort: Please input command arguments!')
        exit(0)
    connector = PamConnector(sys.argv)
    connector.action()


def quit_main(signum, frame):
    print('Quit successful by user action.')
    sys.exit()


if __name__ == '__main__':
    print('-= WELCOME TO SECMIND-PAM =-')
    try:
        signal.signal(signal.SIGINT, quit_main)
        signal.signal(signal.SIGTSTP, quit_main)
        signal.signal(signal.SIGTERM, quit_main)
        main()
    except Exception:
        print(traceback.print_exc())

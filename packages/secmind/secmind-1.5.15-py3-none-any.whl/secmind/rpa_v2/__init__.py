import ddddocr
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from secmind.rpa_v2.entity.task_execution_result import TaskExecutionResult
from secmind.rpa_v2.samba.samba_wrapper import SambaWrapper
from secmind.rpa_v2.selenium.selenium_general_verify import GeneralVerify
from secmind.rpa_v2.selenium.selenium_wrapper import SeleniumWrapper
from secmind.rpa_v2.ssh.ssh_wrapper import SSHWrapper
from secmind.rpa_v2.telnet.telnet_wrapper import TelnetWrapper
from secmind.rpa_v2.utils import captcha
from secmind.rpa_v2.utils import common
from secmind.rpa_v2.utils.log import LogWrapper
from secmind.rpa_v2.winrm.winrm_wrapper import WinRMWrapper

webdriver = webdriver
DesiredCapabilities = DesiredCapabilities
Options = Options
By = By

WebElement = WebElement
EC = EC
WebDriverWait = WebDriverWait
Keys = Keys

GeneralVerify = GeneralVerify
DoTaskResult = TaskExecutionResult
SeleniumWrapper = SeleniumWrapper
LogWrapper = LogWrapper
wandouocr = ddddocr
captcha = captcha
SSHWrapper = SSHWrapper
TelnetWrapper = TelnetWrapper
WinRMWrapper = WinRMWrapper

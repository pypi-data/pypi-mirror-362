import datetime
import os
import time
from typing import List

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from secmind.rpa_v2.utils import captcha
from secmind.rpa_v2.utils.common import custom_exception_handler_class
from selenium.webdriver.common.action_chains import ActionChains
# 如需自定义异常提示语，只需要在调用方法参数中添加error_message="xxxxxxx"即可
@custom_exception_handler_class
class SeleniumWrapper:
    SCREENSHOT_DIR = "screenshot"
    PAGE_SOURCE_DIR = "page-source"
    SCREENSHOT_SUFFIX = ".png"
    PAGE_SOURCE_SUFFIX = ".html"

    def __init__(self, extra_options: List[str] = None, options_level: int = 0, init_driver: bool = True):
        self.__driver = None
        self.__extra_options = extra_options
        if init_driver:
            self.__init_driver(options_level)

    def __init_driver(self, options_level):
        mode = os.getenv('SELENIUM-MODE')
        path = os.getenv('SELENIUM-PATH')
        url = os.getenv('SELENIUM-URL')
        if mode is None:
            raise ValueError("环境变量中未读取到selenium到运行模式，请在环境变量中设置selenium-mode=local或remote.")
        if mode == 'local' and path is None:
            raise ValueError("环境变量中未读取到selenium路径，请在环境变量中设置selenium-path=/xx/xx.")
        if mode == 'remote' and url is None:
            raise ValueError(
                "环境变量中未读取到selenium url，请在环境变量中设置selenium-url=http://xx.xx.xx.xx:xxx/wd/hub")

        options = Options()
        options.add_argument('--allow-running-insecure-content')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--no-sandbox')
        if options_level > 0:
            options.add_argument("--disable-extensions")
            options.add_argument("--dns-prefetch-disable")
        if options_level > 1:
            prefs = {"profile.managed_default_content_settings.images": 2}
            options.add_experimental_option("prefs", prefs)
        if self.__extra_options is not None:
            for extra_option in self.__extra_options:
                options.add_argument(extra_option)

        if mode == 'local':
            self.__driver = webdriver.Chrome(path, options=options)
        elif mode == 'remote':
            options.add_argument('--headless')
            self.__driver = webdriver.Remote(command_executor=url,
                                             desired_capabilities=DesiredCapabilities.CHROME, options=options)
        self.__driver.maximize_window()

    # 获取Driver，仅当使用封装类之外的方法时调用
    def get_driver(self):
        return self.__driver

    def set_driver(self, driver):
        self.__driver = driver

    # 打开网址
    def open_url(self, url):
        self.__driver.get(url)

    # 获取工作目录
    def get_work_dir(self):
        workdir = os.getenv('SELENIUM-WORKDIR')
        if workdir is None:
            raise ValueError("环境变量中未读取到selenium工作路径，请在环境变量中设置selenium-workdir=/xx/xx.")
        return workdir

    def __mk_workdir(self, name):
        workdir = self.get_work_dir()
        now = datetime.datetime.now()
        parent_dir = os.path.join(workdir, name, now.strftime('%Y-%m-%d'))
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)
        return parent_dir, now

    # 截图
    def screenshot(self, name):
        parent_dir, now = self.__mk_workdir(SeleniumWrapper.SCREENSHOT_DIR)
        path = os.path.join(parent_dir, now.strftime("%H-%M-%S-%f-") + name + SeleniumWrapper.SCREENSHOT_SUFFIX)
        self.__driver.save_screenshot(path)
        return path

    # 保存网页
    def dump_page_source(self, name):
        parent_dir, now = self.__mk_workdir(SeleniumWrapper.PAGE_SOURCE_DIR)
        path = os.path.join(parent_dir, now.strftime("%H-%M-%S-%f-") + name + SeleniumWrapper.PAGE_SOURCE_SUFFIX)
        page_source = self.__driver.page_source
        with open(path, 'w', encoding='utf-8') as file:
            file.write(page_source)
        return path

    # 退出
    def exit(self):
        self.__driver.quit()

    # 识别验证码
    def recognize_captcha(self, locator, online_recognize: bool = True, wait_captcha_load_time: int = 5):
        self.wait_for_seconds(wait_captcha_load_time)
        captcha_image = self.find_element(locator).screenshot_as_base64
        if online_recognize:
            recognize_code = captcha.recognize_captcha_online(captcha_image)
        else:
            recognize_code = captcha.recognize_captcha_offline(captcha_image)
        return recognize_code

    def find_element(self, locator, timeout=5):
        dom: WebElement = WebDriverWait(self.__driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
        return dom

    def find_elements(self, locator, timeout=5):
        dom: List[WebElement] = WebDriverWait(self.__driver, timeout).until(
            EC.presence_of_all_elements_located(locator)
        )
        return dom

    def click(self, locator):
        element = self.find_element(locator)
        element.click()

    def enter_text(self, locator, text):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def get_element_text(self, locator):
        element = self.find_element(locator)
        return element.text

    def switch_to_frame(self, locator):
        frame = self.find_element(locator)
        self.__driver.switch_to.frame(frame)

    def switch_to_default_content(self):
        self.__driver.switch_to.default_content()

    def get_title(self):
        return self.__driver.title

    def get_current_url(self):
        return self.__driver.current_url

    def execute_script(self, script, *args):
        return self.__driver.execute_script(script, *args)

    def get_all_cookies(self):
        return self.__driver.get_cookies()

    def add_cookie(self, cookie_dict):
        self.__driver.add_cookie(cookie_dict)

    def delete_all_cookies(self):
        self.__driver.delete_all_cookies()

    def press_key(self, locator, key):
        element = self.find_element(locator)
        element.send_keys(getattr(Keys, key))

    def get_element_attribute(self, locator, attribute):
        element = self.find_element(locator)
        if element:
            return element.get_attribute(attribute)
        return None

    def is_element_enabled(self, locator):
        element = self.find_element(locator)
        return element.is_enabled()

    def is_element_displayed(self, locator):
        element = self.find_element(locator)
        return element.is_displayed()

    def wait_for_seconds(self, seconds):
        time.sleep(seconds)
    def mouse_hover(self, locator):
        actions = ActionChains(self.__driver)
        actions.move_to_element(self.find_element(locator)).perform()
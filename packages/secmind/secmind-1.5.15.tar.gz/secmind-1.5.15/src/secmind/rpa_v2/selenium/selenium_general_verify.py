import traceback
from typing import Optional

from secmind.rpa_v2.entity.task_execution_result import TaskExecutionResult
from secmind.rpa_v2.selenium.selenium_wrapper import SeleniumWrapper
from secmind.rpa_v2.utils.common import custom_exception_handler_class
from secmind.rpa_v2.utils.log import LogWrapper


class InnerElementInfo:
    def __init__(self, element, value=None):
        self.element = element
        self.value = value


@custom_exception_handler_class
class GeneralVerify:
    def __init__(self):
        self.wait_captcha_load_time = None
        self.online_recognize = True
        self.confirm_element_info: Optional[InnerElementInfo] = None
        self.submit_button_element_info: Optional[InnerElementInfo] = None
        self.captcha_input_element_info: Optional[InnerElementInfo] = None
        self.captcha_image_element_info: Optional[InnerElementInfo] = None
        self.password_element_info: Optional[InnerElementInfo] = None
        self.login_element_info: Optional[InnerElementInfo] = None
        self.url = None
        self.selenium_wrapper = SeleniumWrapper()
        self.logger = LogWrapper().get_logger()

    # 设置加载的网址
    def load_url(self, url):
        self.url = url
        return self

    # 设置登录框和值
    def set_login_name(self, locator, value):
        self.login_element_info = InnerElementInfo(locator, value)
        return self

    # 设置密码框和值
    def set_password(self, locator, value):
        self.password_element_info = InnerElementInfo(locator, value)
        return self

    # 设置验证码图像位置
    def set_captcha_img(self, locator, online_recognize: bool = True, wait_captcha_load_time: int = 5):
        self.captcha_image_element_info = InnerElementInfo(locator)
        self.online_recognize = online_recognize
        self.wait_captcha_load_time = wait_captcha_load_time
        return self

    # 设置验证码框
    def set_captcha_input(self, locator):
        self.captcha_input_element_info = InnerElementInfo(locator)
        return self

    # 设置提交按钮
    def set_submit_button(self, locator):
        self.submit_button_element_info = InnerElementInfo(locator)
        return self

    # 设置确认元素和值（值可选）
    def set_confirm_element(self, locator, value=None):
        self.confirm_element_info = InnerElementInfo(locator, value)
        return self

    # 获取返回结果
    def get_login_result(self):
        task_execution_result = TaskExecutionResult()
        try:
            self.selenium_wrapper.get_driver().get(self.url)
            self.selenium_wrapper.find_element(self.login_element_info.element).send_keys(self.login_element_info.value)
            self.selenium_wrapper.find_element(self.password_element_info.element).send_keys(
                self.password_element_info.value)

            if self.captcha_image_element_info is not None:
                captcha_input = self.selenium_wrapper.find_element(self.captcha_input_element_info.element)

                recognize_code = self.selenium_wrapper.recognize_captcha(self.captcha_image_element_info.element,
                                                                         self.online_recognize,
                                                                         self.wait_captcha_load_time)
                captcha_input.send_keys(recognize_code)

            submit_button = self.selenium_wrapper.find_element(self.submit_button_element_info.element)
            submit_button.click()

            confirm_element = self.selenium_wrapper.find_element(self.confirm_element_info.element)
            if self.confirm_element_info.value is None:
                task_execution_result.data = True
            else:
                task_execution_result.data = self.confirm_element_info.value in confirm_element.text
            self.selenium_wrapper.screenshot(self.login_element_info.value)
            task_execution_result.success = True
        except Exception as e:
            self.logger.error(e)
            task_execution_result.stack = traceback.format_exc()
            task_execution_result.msg = repr(e)
        finally:
            self.selenium_wrapper.exit()
            task_execution_result.log = self.logger.get_log_text_with_close()

        return task_execution_result

from secmind.rpa_v2 import By
from secmind.rpa_v2 import SeleniumWrapper
from secmind.rpa_v2 import common


def do_task(data_map):
    selenium_wrapper = SeleniumWrapper()
    try:
        selenium_wrapper.open_url(data_map['location'])

        selenium_wrapper.enter_text((By.XPATH, "//input[@placeholder='账号']"), data_map['user'])

        selenium_wrapper.enter_text((By.XPATH, "//input[@placeholder='密码']"), data_map['pwd'])

        captcha_code = selenium_wrapper.recognize_captcha(
            (By.CSS_SELECTOR, ".el-input-group__append > .cursor-pointer"),
            False)

        selenium_wrapper.enter_text((By.XPATH, "//input[@placeholder='验证码']"), captcha_code)

        selenium_wrapper.click((By.CSS_SELECTOR, ".el-form-item__content > .el-button"))

        selenium_wrapper.find_element((By.XPATH, "//span[@title='打开系统配置']"))

        selenium_wrapper.screenshot(data_map['user'])
        selenium_wrapper.exit()
        return True
    except Exception as ex:
        common.logger.error(repr(ex))
        raise ex
    finally:
        selenium_wrapper.exit()


common.go(do_task)

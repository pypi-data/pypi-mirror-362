from secmind.rpa_v2 import By
from secmind.rpa_v2 import GeneralVerify
from secmind.rpa_v2.utils import common


def do_task(data_map):
    general_verify = GeneralVerify()
    general_verify.load_url(data_map['location']) \
        .set_login_name((By.XPATH, "//input[@placeholder='账号']"), data_map['user']) \
        .set_password((By.XPATH, "//input[@placeholder='密码']"), data_map['pwd']) \
        .set_captcha_img((By.CSS_SELECTOR, ".el-input-group__append > .cursor-pointer"), False) \
        .set_captcha_input((By.XPATH, "//input[@placeholder='验证码']")) \
        .set_submit_button((By.CSS_SELECTOR, ".el-form-item__content > .el-button")) \
        .set_confirm_element((By.XPATH, "//span[@title='打开系统配置']"))

    return general_verify.get_login_result()


common.go(do_task)

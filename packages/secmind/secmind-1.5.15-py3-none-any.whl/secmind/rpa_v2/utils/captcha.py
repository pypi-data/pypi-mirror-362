import hashlib
import json

import ddddocr
import requests

ocr = ddddocr.DdddOcr(beta=True, show_ad=False)


def recognize_captcha_online(base64img):
    img_text = ''
    status = requests.get(url='https://pam-openapi.secmind.cn/api/net/status')
    if json.loads(status.text).get('success'):
        sign_plain = "WwanDdou" + "" + base64img + "" + "vgdffs"
        hl = hashlib.md5()
        hl.update(sign_plain.encode(encoding='utf-8'))
        sign_cipher = hl.hexdigest()
        params = {
            'sign': sign_cipher,
            'typeId': '',
            'image': base64img,
            'assetType': ''
        }
        resp = requests.post(json=params, url='https://pam-openapi.secmind.cn/api/captcha/identity')
        resp_data = json.loads(resp.text)
        if resp_data.get('success') is True:
            img_text = resp_data.get('code')
    else:
        img_text = ""
    return img_text


def recognize_captcha_offline(base64img):
    ocr.set_ranges(6)
    res = ocr.classification(base64img, probability=True)
    s = ""
    for i in res['probability']:
        s += res['charsets'][i.index(max(i))]
    return s

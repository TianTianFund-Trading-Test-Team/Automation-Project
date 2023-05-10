import time
from urllib.parse import urljoin

import execjs
import requests
from _pytest import unittest

from conftest import read_yaml3, write_yaml3, read_yaml1, read_yaml4, read_yaml2

DES_js = '''
const CryptoJS = require('crypto-js');
function decryptSecretStr(message, key) {
    iv = 'V8?eA%0.'   
    useKey = CryptoJS.enc.Utf8.parse(key)    
    decryptStr = CryptoJS.DES.decrypt(message, useKey,{
        iv: CryptoJS.enc.Utf8.parse(iv),
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7,
    });
    return decryptStr.toString(CryptoJS.enc.Utf8);
 }
'''
RSA_js = '''
const jsdom = require("jsdom");
const {JSDOM} = jsdom;
const dom = new JSDOM(`<!DOCTYPE html><p>Hello world</p>`);
window = dom.window;
document = window.document;
XMLHttpRequest = window.XMLHttpRequest;
const JSEncrypt = require('jsencrypt');
function rsaEncrypt(password, publickey) {
    encrypt = new JSEncrypt();
    defaultKey = 'MIGdMA0GCSqGSIb3DQEBAQUAA4GLADCBhwKBgQCLP6ZcIprFKWIxjTxcSr+EMbN259A7C3EpUS1plUB8Tp6rvflI5CBrgRFkFQ1HWPpPlpaXbBL1NRsK0JhRuU3RMGnjW6ZOUKsgLwbQa95TialXDHwP3/fCrkJWD6jU4IRpOUy9UbENmYwBfIWt9rVBTN4+X75K/nOUWp8Jd03s7wIBAw==';
    encrypt.setPublicKey(publickey || defaultKey);
    result = encrypt.encrypt(decodeURIComponent(password));
    return result || '';
}
'''


# 获取6位密码完整流程
class get_L2Password():
    # 前端请求GetLatestRsaPubKey（获取加密后的rsa公钥）

    def user_Register_Secu(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/Register/Secu")
        datas = {
            "UserId": read_yaml2()["CustomerNo"],
            "ClientPub": "YTXbqLrTsblP9yfphkKZ*fYQmzcez%Ga",  # 随机生成32位 （这里为了方便固定）

            "PhoneType": "IPhone",
            "ServerVersion": "6.5.8",
            "CToken": read_yaml2()["CToken"],
            "UToken": read_yaml2()["UToken"],
            "MobileKey": "01F12605-0E93-4BCB-AD67-D46C1DDA604B"
        }
        res = requests.request(method='post', url=url, params=datas)
        key = res.json()["Data"]["SecuPub"]
        write_yaml3({"key": key})

    # DES 解密  获得公钥PubKey
    def DES_decrypto(self):
        ctx = execjs.compile(DES_js, cwd=r"E:/Python/pythonProject/node_modules")  # JS库绝对路径

        key = "YTXbqLrTsblP9yfphkKZ*fYQmzcez%Ga"  # 32位随机
        message = read_yaml3()["key"]  # 请求Secu返回的加密公钥

        # 使用execjs执行DES解密函数
        decrypted = ctx.call("decryptSecretStr", message, key)  # str
        Decrypted = eval(decrypted)
        write_yaml3({"PubKey": Decrypted.get('PubKey')})  # 解密后的公钥明文

    # RSA 加密  得到L2Password
    def rsa_encrypto(self):
        ctx = execjs.compile(RSA_js, cwd=r"E:/Python/pythonProject/node_modules")
        str_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))  # 真实时间
        content = "123321" + "|" + str_time  # 交易密码默认123321
        # 使用execjs执行RSA加密
        password = ctx.call('rsaEncrypt', content, read_yaml3()["PubKey"])
        write_yaml3({"L2Password": password})

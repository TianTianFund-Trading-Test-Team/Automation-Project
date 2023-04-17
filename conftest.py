from urllib.parse import urljoin

import pytest
import requests
import json
import yaml
import jsonpath as jsonpath


# 读取test_configuration 配置表（账号密码）
def read_yaml1():
    with open("test_configuration.yaml", encoding="utf-8") as f:
        value = yaml.load(f, Loader=yaml.FullLoader)
        return value


# 读取test_params(CUToken,BankCardNo,BankAccountNo,SubAccountNo)
def read_yaml2():
    with open("test_params.yaml", encoding="utf-8") as f:
        value = yaml.load(f, Loader=yaml.FullLoader)
        return value


# 读取test_params2(存放临时参数，traceID，单号等等）
def read_yaml3():
    with open("test_params2.yaml", encoding="utf-8") as f:
        value = yaml.load(f, Loader=yaml.FullLoader)
        return value


# 读取test_input(输入参数）
def read_yaml4():
    with open("test_input.yaml", encoding="utf-8") as f:
        value = yaml.load(f, Loader=yaml.FullLoader)
        return value


# 写入test_params
def write_yaml2(data):
    with open("test_params.yaml", encoding="utf-8", mode="a") as f:
        value = yaml.dump(data, stream=f, allow_unicode=True)


# 写入test_params2
def write_yaml3(data):
    with open("test_params2.yaml", encoding="utf-8", mode="a") as f:
        value = yaml.dump(data, stream=f, allow_unicode=True)


# 清空test_params（每次自动化只清理一次）
@pytest.fixture(scope="session", autouse=True)
def clear_yaml2():
    with open("test_params.yaml", mode='w', encoding='utf-8') as f:
        f.truncate()


# 清空test_params2
def clear_yaml3():
    with open("test_params2.yaml", mode='w', encoding='utf-8') as f:
        f.truncate()


# 在所有接口请求之前执行获取cToken(非校验用CToken）
@pytest.fixture(scope="session", autouse=True)
def get_cToken():
    url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/home/GetCToken")
    datas = {
        "DeviceName": "iPhone",
        "DeviceType": "iPhone14,3",
        "DeviceOS": "iOS 16.1",
        "ServerVersion": "6.5.8",
        "MobileKey": "01F12605-0E93-4BCB-AD67-D46C1DDA604B"
    }
    res = requests.request(method='post', url=url, params=datas)
    cToken = res.json()["Data"]
    write_yaml2({"cToken": cToken})


# 获取CustomerNo，CToken,UToken
@pytest.fixture(scope="session", autouse=True)
def get_z_CUToken():
    url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/Account/LoginForMobileReturnContextId")
    datas = {
        "Account": read_yaml1()[read_yaml4()["Acc"]],
        "Password": read_yaml1()[read_yaml4()["Pas"]],
        "CertificateType": "0",
        "Client": "AppCockClock",
        "UseSlide": "false",
        "VerifyCode": "null",
        "RealClientIp": "null",
        "VerifyCodeType": "null",
        "DeviceName": "iPhone",
        "DeviceType": "IOS16.1",
        "DeviceOS": "iOS 16.1",
        "ServerVersion": "6.5.8",
        "CToken": read_yaml2()["cToken"],
        "MobileKey": "01F12605-0E93-4BCB-AD67-D46C1DDA604B"
    }
    res = requests.request(method='post', url=url, params=datas)
    CToken = res.json()["Data"]["CToken"]
    UToken = res.json()["Data"]["UToken"]
    CustomerNo = res.json()["Data"]["CustomerNo"]
    write_yaml2({"CToken": CToken})
    write_yaml2({"UToken": UToken})
    write_yaml2({"CustomerNo": CustomerNo})


# 获取第一张银行卡号 BankCardNo, BankAccountNo
@pytest.fixture(scope="session", autouse=True)
def get_z_z_BankCardNo():
    url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/Business/hqb/banks")
    datas = {
        "UserId": read_yaml2()["CustomerNo"],
        "PhoneType": "IPhone",
        "ServerVersion": "6.5.8",
        "CToken": read_yaml2()["CToken"],
        "MobileKey": "01F12605-0E93-4BCB-AD67-D46C1DDA604B",
        "UToken": read_yaml2()["UToken"]
    }
    res = requests.request(method='post', url=url, params=datas)
    BankCardNo = res.json()["Data"]["CashBagBankCardList"][0]["BankCardNo"]
    BankAccountNo = res.json()["Data"]["CashBagBankCardList"][0]["AccountNo"]
    write_yaml2({"BankCardNo": BankCardNo})
    write_yaml2({"BankAccountNo": BankAccountNo})


# 获取 SubAccountNo
@pytest.fixture(scope="session", autouse=True)
def get_z_SubAccountNo():
    url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubA/SubAAssetMult")
    datas = {
        "UserId": read_yaml2()["CustomerNo"],
        "PageType": "null",
        "PhoneType": "IPhone",
        "ServerVersion": "6.5.8",
        "CToken": read_yaml2()["CToken"],
        "MobileKey": "01F12605-0E93-4BCB-AD67-D46C1DDA604B",
        "UToken": read_yaml2()["UToken"]
    }
    res = requests.request(method='post', url=url, params=datas)
    SubAccountNo = res.json()["Data"]["ListGroup"][0]["SubAccountNo"]
    write_yaml2({"SubAccountNo": SubAccountNo})

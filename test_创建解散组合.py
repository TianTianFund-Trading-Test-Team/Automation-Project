import os
import time
from urllib.parse import urljoin

import pytest
import requests
import allure

from conftest import read_yaml2, write_yaml2, write_yaml3, read_yaml3, clear_yaml3, read_yaml1, read_yaml4


@allure.feature('创建解散组合')
class Test_Create_and_Disband_SubAccount():
    @allure.story('验证名称是否正常 /user/suba/VerifyName')
    # 验证名称
    def test_User_suba_VerifyName(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/user/suba/VerifyName")
        datas = {
            "Name": read_yaml4()["Name"],

            "PhoneType": "IPhone",
            "ServerVersion": "6.5.8",
            "CToken": read_yaml2()["CToken"],
            "UToken": read_yaml2()["UToken"],
            "MobileKey": "01F12605-0E93-4BCB-AD67-D46C1DDA604B"
        }
        res = requests.request(method='post', url=url, params=datas)
        IsValid = res.json()["Data"]["IsValid"]
        ErrorMessage = res.json()["Data"]["ErrorMessage"]
        with allure.step('接口是否正常调通'):
            if res.status_code == 200:
                assert True
            else:
                assert False, '接口状态码非200'
        with allure.step('名称是否正常'):
            if IsValid == True:
                assert True, '名称正常'
            else:
                assert False, ErrorMessage

    @allure.story('验证名称是否正常 旧版 /User/SubAccount/VerifySubAccountName')
    # 验证组合名称 旧版
    def test_User_SubAccount_VerifySubAccountName(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubAccount/VerifySubAccountName")
        datas = {
            "SubAccountName": read_yaml4()["Name"],

            "PhoneType": "IPhone",
            "ServerVersion": "6.5.8",
            "CToken": read_yaml2()["CToken"],
            "UToken": read_yaml2()["UToken"],
            "MobileKey": "01F12605-0E93-4BCB-AD67-D46C1DDA604B"
        }
        res = requests.request(method='post', url=url, params=datas)
        IsValid = res.json()["Data"]["IsValid"]
        ErrorMessage = res.json()["Data"]["ErrorMessage"]
        with allure.step('接口是否正常调通'):
            if res.status_code == 200:
                assert True
            else:
                assert False, '接口状态码非200'
        with allure.step('名称是否正常'):
            if IsValid == True:
                assert True, '名称正常'
            else:
                assert False, ErrorMessage

    @allure.story('选择投资风格 /User/SubAccount/SubAccountPropertyStyle')
    # 选择投资风格
    def test_User_SubAccount_SubAccountPropertyStyle(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubAccount/SubAccountPropertyStyle")
        datas = {

            "PhoneType": "IPhone",
            "ServerVersion": "6.5.8",
            "CToken": read_yaml2()["CToken"],
            "UToken": read_yaml2()["UToken"],
            "MobileKey": "01F12605-0E93-4BCB-AD67-D46C1DDA604B"
        }
        res = requests.request(method='post', url=url, params=datas)
        with allure.step('接口是否正常调通'):
            if res.status_code == 200:
                assert True
            else:
                assert False, '接口状态码非200'

    @allure.story('创建组合 /User/SubA/CreateSubA')
    # 创建组合
    def test_User_SubA_CreateSubA(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubA/CreateSubA")
        datas = {
            "UserId": read_yaml2()["CustomerNo"],
            "CustomizeProperty": '',
            "Property": "P1",  # 上个接口参数 组合标签
            "Style": "S2",  # 上个接口参数 组合类型
            "Name": read_yaml4()["Name"],

            "PhoneType": "IPhone",
            "ServerVersion": "6.5.8",
            "CToken": read_yaml2()["CToken"],
            "UToken": read_yaml2()["UToken"],
            "MobileKey": "01F12605-0E93-4BCB-AD67-D46C1DDA604B"
        }
        res = requests.request(method='post', url=url, params=datas)
        ErrorCode = res.json()["ErrorCode"]
        ErrorMessage = res.json()["ErrorMessage"]
        with allure.step('接口是否正常调通'):
            if res.status_code == 200:
                assert True
            else:
                assert False, '接口状态码非200'
        with allure.step('组合是否创建成功'):
            if ErrorCode == 0:
                assert True, '创建组合成功'
                subAccountNo = res.json()["Data"]["SubAccountNo"]
                clear_yaml3()
                write_yaml3({"subAccountNo": subAccountNo})
            else:
                assert False, ErrorMessage
                clear_yaml3()

    @allure.story('解散组合 /User/SubA/DisbandSubA')
    # 解散组合
    def test_User_SubA_DisbandSubA(self):
        if read_yaml3() is None:
            pytest.skip(), '创建组合失败，无法解散组合'
        else:
            url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubA/DisbandSubA")
            datas = {
                "UserId": read_yaml2()["CustomerNo"],
                "SubAccountNo": read_yaml3()["subAccountNo"],
                "Password": read_yaml1()[read_yaml4()["Pas"]],

                "PhoneType": "IPhone",
                "ServerVersion": "6.5.8",
                "CToken": read_yaml2()["CToken"],
                "UToken": read_yaml2()["UToken"],
                "MobileKey": "01F12605-0E93-4BCB-AD67-D46C1DDA604B"
            }
            res = requests.request(method='post', url=url, params=datas)
            ErrorCode = res.json()["ErrorCode"]
            ErrorMessage = res.json()["ErrorMessage"]
            with allure.step('接口是否正常调通'):
                if res.status_code == 200:
                    assert True
                else:
                    assert False, '接口状态码非200'
            with allure.step('组合是否解散成功'):
                if ErrorCode == 0:
                    assert True, '解散组合成功'
                    clear_yaml3()
                else:
                    assert False, ErrorMessage




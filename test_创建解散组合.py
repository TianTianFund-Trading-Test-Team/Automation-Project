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
        with allure.step('接口是否正常调通'):
            if res.status_code == 200:
                assert True
                with allure.step('接口是否返回正常'):
                    ErrorCode = res.json()["ErrorCode"]
                    ErrorMessage = res.json()["ErrorMessage"]
                    if ErrorCode == 0:
                        assert True
                        IsValid = res.json()["Data"]["IsValid"]
                        ErrorMessage = res.json()["Data"]["ErrorMessage"]
                        with allure.step('名称是否正常'):
                            if IsValid == True:
                                assert True, '名称正常'
                            else:
                                assert False, ErrorMessage
                    else:
                        clear_yaml3()
                        assert False, ErrorMessage
            else:
                assert False, '接口状态码非200'

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
        with allure.step('接口是否正常调通'):
            if res.status_code == 200:
                assert True
                with allure.step('接口是否返回正常'):
                    ErrorCode = res.json()["ErrorCode"]
                    ErrorMessage = res.json()["ErrorMessage"]
                    if ErrorCode == 0:
                        assert True
                        with allure.step('名称是否正常'):
                            IsValid = res.json()["Data"]["IsValid"]
                            ErrorMessage1 = res.json()["Data"]["ErrorMessage"]
                            if IsValid == True:
                                assert True, '名称正常'
                            else:
                                assert False, ErrorMessage1
                    else:
                        clear_yaml3()
                        assert False, ErrorMessage

            else:
                assert False, '接口状态码非200'

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
                with allure.step('接口是否返回正常'):
                    ErrorCode = res.json()["ErrorCode"]
                    ErrorMessage = res.json()["ErrorMessage"]
                    if ErrorCode == 0:
                        assert True
                    else:
                        clear_yaml3()
                        assert False, ErrorMessage
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
        with allure.step('接口是否正常调通'):
            if res.status_code == 200:
                assert True
                with allure.step('组合是否创建成功'):
                    ErrorCode = res.json()["ErrorCode"]
                    ErrorMessage = res.json()["ErrorMessage"]
                    if ErrorCode == 0:
                        assert True, '创建组合成功'
                        subAccountNo = res.json()["Data"]["SubAccountNo"]
                        clear_yaml3()
                        write_yaml3({"subAccountNo": subAccountNo})
                    else:
                        clear_yaml3()
                        assert False, ErrorMessage
            else:
                assert False, '接口状态码非200'

    @allure.story('修改组合名称 /User/SubA/UpdateSubANP')
    # 修改组合名称
    def test_User_SubA_UpdateSubANP(self):
        if read_yaml3() is None:
            pytest.skip(), '创建组合失败，无法修改组合信息'
        else:
            url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubA/UpdateSubANP")
            datas = {
                "UserId": read_yaml2()["CustomerNo"],
                "SubAccountNo": read_yaml3()["subAccountNo"],
                "ShutDownSubAccount": "false",
                "UpdateName": "Name",
                "UpdateValue": read_yaml4()["Name_EX"],
                "PrivacyMode": "",

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
                    ErrorCode = res.json()["ErrorCode"]
                    ErrorMessage = res.json()["ErrorMessage"]
                    with allure.step('修改组合名称是否成功'):
                        if ErrorCode == 0:
                            assert True, '修改组合名称成功'
                        else:
                            assert False, ErrorMessage
                else:
                    assert False, '接口状态码非200'

    @allure.story('修改组合个性标签 /User/SubA/UpdateSubANP')
    # 修改组合个性标签
    def test_User_SubA_UpdateSubANP2(self):
        if read_yaml3() is None:
            pytest.skip(), '创建组合失败，无法修改组合信息'
        else:
            url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubA/UpdateSubANP")
            datas = {
                "UserId": read_yaml2()["CustomerNo"],
                "SubAccountNo": read_yaml3()["subAccountNo"],
                "ShutDownSubAccount": "false",
                "UpdateName": "Property",
                "UpdateValue": read_yaml4()["Property"],
                "PrivacyMode": "",

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
                    ErrorCode = res.json()["ErrorCode"]
                    ErrorMessage = res.json()["ErrorMessage"]
                    with allure.step('修改组合标签是否成功'):
                        if ErrorCode == 0:
                            assert True, '修改组合标签成功'
                        else:
                            assert False, ErrorMessage
                else:
                    assert False, '接口状态码非200'

    @allure.story('修改组合风格 /User/SubA/UpdateSubANP')
    # 修改组合风格
    def test_User_SubA_UpdateSubANP3(self):
        if read_yaml3() is None:
            pytest.skip(), '创建组合失败，无法修改组合信息'
        else:
            url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubA/UpdateSubANP")
            datas = {
                "UserId": read_yaml2()["CustomerNo"],
                "SubAccountNo": read_yaml3()["subAccountNo"],
                "ShutDownSubAccount": "false",
                "UpdateName": "Style",
                "UpdateValue": read_yaml4()["Style"],
                "PrivacyMode": "",

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
                    ErrorCode = res.json()["ErrorCode"]
                    ErrorMessage = res.json()["ErrorMessage"]
                    with allure.step('修改组合风格是否成功'):
                        if ErrorCode == 0:
                            assert True, '修改组合风格成功'
                        else:
                            assert False, ErrorMessage
                else:
                    assert False, '接口状态码非200'

    @allure.story('修改组合投资理念 /User/SubA/UpdateSubANP')
    # 修改组合投资理念
    def test_User_SubA_UpdateSubANP4(self):
        if read_yaml3() is None:
            pytest.skip(), '创建组合失败，无法修改组合信息'
        else:
            url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubA/UpdateSubANP")
            datas = {
                "UserId": read_yaml2()["CustomerNo"],
                "SubAccountNo": read_yaml3()["subAccountNo"],
                "ShutDownSubAccount": "false",
                "UpdateName": "Idea",
                "UpdateValue": read_yaml4()["Idea"],
                "PrivacyMode": "",

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
                    ErrorCode = res.json()["ErrorCode"]
                    ErrorMessage = res.json()["ErrorMessage"]
                    with allure.step('修改组合投资理念是否成功'):
                        if ErrorCode == 0:
                            assert True, '修改组合投资理念成功'
                        else:
                            assert False, ErrorMessage
                else:
                    assert False, '接口状态码非200'

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
            with allure.step('接口是否正常调通'):
                if res.status_code == 200:
                    assert True
                    ErrorCode = res.json()["ErrorCode"]
                    ErrorMessage = res.json()["ErrorMessage"]
                    with allure.step('组合是否解散成功'):
                        if ErrorCode == 0:
                            assert True, '解散组合成功'
                            clear_yaml3()
                        else:
                            assert False, ErrorMessage
                else:
                    assert False, '接口状态码非200'

    @allure.story('创建第二个组合 /User/SubA/CreateSubA')
    # 创建第二个组合
    def test_User_SubA_CreateSubA2(self):
        time.sleep(3)  # 中台会提示请勿重复提交。
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
        with allure.step('接口是否正常调通'):
            if res.status_code == 200:
                assert True
                with allure.step('组合是否创建成功'):
                    ErrorCode = res.json()["ErrorCode"]
                    ErrorMessage = res.json()["ErrorMessage"]
                    if ErrorCode == 0:
                        assert True, '创建组合成功'
                        subAccountNo = res.json()["Data"]["SubAccountNo"]
                        clear_yaml3()
                        write_yaml3({"subAccountNo": subAccountNo})
                    else:
                        clear_yaml3()
                        assert False, ErrorMessage
            else:
                assert False, '接口状态码非200'

    @allure.story('解散组合 /User/SubA/DisbandSubANP')
    # 解散组合
    def test_User_SubA_DisbandSubANP(self):
        if read_yaml3() is None:
            pytest.skip(), '创建组合失败，无法解散组合'
        else:
            url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubA/DisbandSubANP")
            datas = {
                "UserId": read_yaml2()["CustomerNo"],
                "SubAccountNo": read_yaml3()["subAccountNo"],

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
                    ErrorCode = res.json()["ErrorCode"]
                    ErrorMessage = res.json()["ErrorMessage"]
                    with allure.step('组合是否解散成功'):
                        if ErrorCode == 0:
                            assert True, '解散组合成功'
                            clear_yaml3()
                        else:
                            assert False, ErrorMessage
                else:
                    assert False, '接口状态码非200'

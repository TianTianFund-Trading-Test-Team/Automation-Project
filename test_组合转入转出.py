import os
import time
from urllib.parse import urljoin

import pytest
import requests
import allure

from conftest import read_yaml2, write_yaml2, write_yaml3, read_yaml3, clear_yaml3, read_yaml1, read_yaml4


@allure.feature('组合转入转出 ')
class Test_TransferShare_Sub():
    @allure.story('组合转入基金列表 /User/SubA/SubASummary')
    # 组合转入基金列表
    def test_User_SubA_SubASummary(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubA/SubASummary")
        datas = {
            "UserId": read_yaml2()["CustomerNo"],
            "SubType": "-1",

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
                ShareId = res.json()["Data"]["SubAccounts"][0]["Details"][0]["ShareId"]
                clear_yaml3()
                write_yaml3({"ShareId": ShareId})
            else:
                assert False, '接口状态码非200'

    @allure.story('组合转入基金列表 /User/SubA/SubATransferShare')
    # 组合转入基金列表
    def test_User_SubA_SubATransferShare(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubA/SubATransferShare")
        datas = {
            "PassWord": read_yaml1()[read_yaml4()["Pas"]],
            "UserId": read_yaml2()["CustomerNo"],
            "Shares": read_yaml3()["ShareId"],
            "Vols": read_yaml4()["Vols"],
            "SubAccountNo": read_yaml2()["SubAccountNo"],

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
                with allure.step('组合转入转出是否成功'):
                    if ErrorCode == 0:
                        assert True, '申请受理成功'
                    else:
                        assert False, ErrorMessage
            else:
                assert False, '接口状态码非200'

    @allure.story('组合转入基金列表 /User/SubA/SubASummary')
    # 组合转入基金列表
    def test_User_SubA_SubASummary2(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubA/SubASummary")
        datas = {
            "UserId": read_yaml2()["CustomerNo"],
            "SubType": "-1",

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
                ShareId = res.json()["Data"]["SubAccounts"][0]["Details"][0]["ShareId"]
                clear_yaml3()
                write_yaml3({"ShareId": ShareId})
            else:
                assert False, '接口状态码非200'

    @allure.story('组合转入基金列表 /User/SubA/SubATransferShareNP')
    # 组合转入基金列表
    def test_User_SubA_SubATransferShareNP(self):
        time.sleep(2)
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubA/SubATransferShareNP")
        datas = {
            "UserId": read_yaml2()["CustomerNo"],
            "Shares": read_yaml3()["ShareId"],
            "Vols": read_yaml4()["Vols"],
            "SubAccountNo": read_yaml2()["SubAccountNo"],

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
                with allure.step('组合转入转出是否成功'):
                    if ErrorCode == 0:
                        assert True, '申请受理成功'
                    else:
                        assert False, ErrorMessage
            else:
                assert False, '接口状态码非200'


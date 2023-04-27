import json
import os
import time
from urllib.parse import urljoin

import pytest
import requests
import allure

from conftest import read_yaml2, write_yaml2, write_yaml3, read_yaml3, clear_yaml3, read_yaml1, read_yaml4, write_yaml5, \
    read_yaml5, clear_yaml5


@allure.feature('组合卖出 660以下输入密码')
class Test_redeem_Sub():
    @allure.story('获取组合内份额 /User/SubA/SubARatioRedeemOverviewV2')
    # 获取组合内份额
    def test_User_SubA_SubARatioRedeemOverviewV2(self):
        clear_yaml3()
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubA/SubARatioRedeemOverviewV2")
        datas = {
            "UserId": read_yaml2()["CustomerNo"],
            "SubAccountNo": read_yaml2()["SubAccountNo"],
            "Type": "",

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

    @allure.story('等比例卖出组合回银行卡 /User/SubA/SubARatioRedeemCards')
    # 等比例卖出组合
    def test_User_SubA_SubARatioRedeemCards(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubA/SubARatioRedeemCards")
        datas = {
            "Password": read_yaml1()[read_yaml4()["Pas"]],
            "UserId": read_yaml2()["CustomerNo"],
            "SubAccountNo": read_yaml2()["SubAccountNo"],
            "Type": 1,  # 回银行卡 1   回活期宝 2
            "ObjectFundCode": read_yaml4()["FundCode_HQB_ZHM"],  # 活期宝基金代码,不传回银行卡
            "Percent": read_yaml4()["Percent"],
            "IsCustomizeRatio": 0,
            "FundAppsJson": "",

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
                with allure.step('组合卖出是否正常'):
                    if ErrorCode == 0:
                        assert True
                        write_yaml3({"Result": True})
                    else:
                        clear_yaml3()
                        assert False, ErrorMessage
            else:
                assert False, '接口状态码非200'

    @allure.story('组合卖出在途可撤单列表 /api/mobile/Query/GetQueryInfosQuickUse')
    # 交易查询 组合卖出在途可撤单列表
    def test_api_mobile_Query_GetQueryInfosQuickUse(self):
        if read_yaml3() is None:
            pytest.skip(), "组合卖出未成功"
        else:
            time.sleep(2)  # 撤单后接着查询，中间有延迟
            url = "https://tquerycoreapi8.1234567.com.cn/api/mobile/Query/GetQueryInfosQuickUse"
            datas = {
                "utoken": read_yaml2()["UToken"],
                "uid": read_yaml2()["CustomerNo"],
                "mobileKey": "01F12605-0E93-4BCB-AD67-D46C1DDA604B",
                "customerNo": read_yaml2()["CustomerNo"],
                "deviceid": "01F12605-0E93-4BCB-AD67-D46C1DDA604B",
                "ctoken": read_yaml2()["CToken"],
                "serverversion": "6.5.8",
                "rtype": "app",
                "data": "{{\"PageIndex\": 1, \"PageSize\": 20, \"FundCode\": \"\", \"DateType\": \"3\", \"BusType\":\"22\",\"Statu\":\"7\", \"Account\": \"\", \"SubAccountNo\": \"\", \"CustomerNo\": \"{}\" }}".format(
                    read_yaml2()["CustomerNo"])
            }
            res = requests.request(method='post', url=url, json=datas)
            print(res.json())
            with allure.step('接口是否正常调通'):
                if res.status_code == 200:
                    assert True
                    ErrorCode = res.json()["ErrorCode"]
                    ErrorMessage = res.json()["ErrorMessage"]
                    with allure.step('组合卖出是否正常'):
                        if ErrorCode is None:
                            assert True
                            Count = res.json()["TotalCount"] - 1
                            if Count >= 0:
                                BusinSerialNo = res.json()["responseObjects"][Count]["ID"]
                                BusinessType = res.json()["responseObjects"][Count]["BusinessCode"]
                                clear_yaml3()
                                write_yaml3({"BusinSerialNo": BusinSerialNo})
                                write_yaml3({"BusinessType": BusinessType})
                            else:
                                clear_yaml3()

                        else:
                            clear_yaml3()
                            assert False, ErrorMessage
                else:
                    assert False, "接口状态非200"

    @allure.story('组合卖撤单 /Trade/FundTrade/RevokeOrder')
    # 组合卖撤单
    def test_Trade_FundTrade_RevokeOrder(self):
        if read_yaml3() is None:
            pytest.skip(), '组合卖未成功或已撤单'
        else:
            time.sleep(2)  # 单号落库时间慢，设个延迟防止报错
            url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/Trade/FundTrade/RevokeOrder")
            datas = {
                "Password": read_yaml1()[read_yaml4()["Pas"]],
                "UserId": read_yaml2()["CustomerNo"],
                "BusinId": read_yaml3()["BusinSerialNo"],
                "BusinType": read_yaml3()["BusinessType"],
                "IsRevokedToCashBag": "false",
                "DisplayBusinType": read_yaml3()["BusinessType"],

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
                    with allure.step('组合卖撤单是否成功'):
                        if ErrorCode == 0:
                            assert True, '撤单受理成功'
                        else:
                            assert False, ErrorMessage
                else:
                    assert False, '接口状态码非200'
            self.test_api_mobile_Query_GetQueryInfosQuickUse()
            self.test_Trade_FundTrade_RevokeOrder()


@allure.feature('组合卖出回活期宝 660以下免密')
class Test_redeem_Sub_NP():
    @allure.story('获取组合内份额 /User/SubA/SubARatioRedeemOverviewV2')
    # 获取组合内份额
    def test_User_SubA_SubARatioRedeemOverviewV2(self):
        clear_yaml3()
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubA/SubARatioRedeemOverviewV2")
        datas = {
            "UserId": read_yaml2()["CustomerNo"],
            "SubAccountNo": read_yaml2()["SubAccountNo"],
            "Type": "",

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

    @allure.story('等比例卖出组合回活期宝 免密 /User/SubA/SubARatioRedeemCardsNP')
    # 等比例卖出组合
    def test_User_SubA_SubARatioRedeemCardsNP(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubA/SubARatioRedeemCardsNP")
        datas = {

            "UserId": read_yaml2()["CustomerNo"],
            "SubAccountNo": read_yaml2()["SubAccountNo"],
            "Type": 2,  # 回银行卡 1   回活期宝 2
            "ObjectFundCode": "004545",  # 活期宝基金代码,不传回银行卡
            "Percent": read_yaml4()["Percent"],
            "IsCustomizeRatio": 0,
            "FundAppsJson": "",

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
                with allure.step('组合卖出是否正常'):
                    if ErrorCode == 0:
                        assert True
                        write_yaml3({"Result": True})
                    else:
                        clear_yaml3()
                        assert False, ErrorMessage
            else:
                assert False, '接口状态码非200'

    @allure.story('组合卖出在途可撤单列表 /api/mobile/Query/GetQueryInfosQuickUse')
    # 交易查询 组合卖出在途可撤单列表
    def test_api_mobile_Query_GetQueryInfosQuickUse(self):
        if read_yaml3() is None:
            pytest.skip(), "组合卖出未成功"
        else:
            time.sleep(2)  # 撤单后接着查询，中间有延迟
            url = urljoin(read_yaml1()[read_yaml4()["Env_Tquery"]], "/api/mobile/Query/GetQueryInfosQuickUse")
            datas = {
                "utoken": read_yaml2()["UToken"],
                "uid": read_yaml2()["CustomerNo"],
                "mobileKey": "01F12605-0E93-4BCB-AD67-D46C1DDA604B",
                "customerNo": read_yaml2()["CustomerNo"],
                "deviceid": "01F12605-0E93-4BCB-AD67-D46C1DDA604B",
                "ctoken": read_yaml2()["CToken"],
                "serverversion": "6.5.8",
                "rtype": "app",
                "data": "{{\"PageIndex\": 1, \"PageSize\": 20, \"FundCode\": \"\", \"DateType\": \"3\", \"BusType\":\"22\",\"Statu\":\"7\", \"Account\": \"\", \"SubAccountNo\": \"\", \"CustomerNo\": \"{}\" }}".format(
                    read_yaml2()["CustomerNo"])
            }
            res = requests.request(method='post', url=url, json=datas)
            print(res.json())
            with allure.step('接口是否正常调通'):
                if res.status_code == 200:
                    assert True
                    ErrorCode = res.json()["ErrorCode"]
                    ErrorMessage = res.json()["ErrorMessage"]
                    with allure.step('组合卖出是否正常'):
                        if ErrorCode is None:
                            assert True
                            Count = res.json()["TotalCount"] - 1
                            if Count >= 0:
                                BusinSerialNo = res.json()["responseObjects"][Count]["ID"]
                                BusinessType = res.json()["responseObjects"][Count]["BusinessCode"]
                                clear_yaml3()
                                write_yaml3({"BusinSerialNo": BusinSerialNo})
                                write_yaml3({"BusinessType": BusinessType})
                            else:
                                clear_yaml3()

                        else:
                            clear_yaml3()
                            assert False, ErrorMessage
                else:
                    assert False, "接口状态非200"

    @allure.story('组合卖撤单 免密 /Trade/FundTrade/RevokeOrderNP')
    # 组合卖撤单
    def test_Trade_FundTrade_RevokeOrderNP(self):
        if read_yaml3() is None:
            pytest.skip(), '组合卖未成功或已撤单'
        else:
            time.sleep(2)  # 单号落库时间慢，设个延迟防止报错
            url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/Trade/FundTrade/RevokeOrderNP")
            datas = {
                "UserId": read_yaml2()["CustomerNo"],
                "BusinId": read_yaml3()["BusinSerialNo"],
                "BusinType": read_yaml3()["BusinessType"],
                "IsRevokedToCashBag": "false",
                "DisplayBusinType": read_yaml3()["BusinessType"],

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
                    with allure.step('组合卖撤单是否成功'):
                        if ErrorCode == 0:
                            assert True, '撤单受理成功'
                        else:
                            assert False, ErrorMessage
                else:
                    assert False, '接口状态码非200'
            self.test_api_mobile_Query_GetQueryInfosQuickUse()
            self.test_Trade_FundTrade_RevokeOrderNP()

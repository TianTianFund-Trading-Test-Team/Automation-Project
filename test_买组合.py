import os
import time
from urllib.parse import urljoin

import pytest
import requests
import allure

from conftest import read_yaml2, write_yaml2, write_yaml3, read_yaml3, clear_yaml3, read_yaml1, read_yaml4


@allure.feature('买组合 660以下输入密码')
class Test_buy_Sub():
    @allure.story('交易留痕 /Business/home/NoticeStayTrace')
    # 交易留痕
    def test_Business_home_NoticeStayTrace(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/Business/home/NoticeStayTrace")
        datas = {
            "UserId": read_yaml2()["CustomerNo"],
            "FundCode": "null",
            "CToken": read_yaml2()["CToken"],
            "UToken": read_yaml2()["UToken"]
        }
        res = requests.request(method='post', url=url, params=datas)
        with allure.step('接口是否正常调通'):
            if res.status_code == 200:
                assert True
                TraceID = res.json()["Data"]["TraceID"]
                write_yaml3({"TraceID": TraceID})
            else:
                assert False, '接口状态码非200'

    @allure.story('买组合 /User/SubA/CommitOrderCus')
    # 买组合 660以下输密码
    def test_User_SubA_CommitOrderCus(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubA/CommitOrderCus")
        datas = {
            "Password": read_yaml1()[read_yaml4()["Pas"]],
            "TradeType": read_yaml4()["TradeType_Sub"],
            "UserId": read_yaml2()["CustomerNo"],
            "BankAccountNo": read_yaml2()["BankAccountNo"],
            "CouponsType": "",
            "CouponsId": "",
            "FundCode": "",
            "TotalAmounts": read_yaml4()["Amount"],
            "FundAppsJson": "",
            "TraceID": read_yaml3()["TraceID"],
            "RecommanderNo": "",
            "SubAccountNo": "",
            "FollowingSubAccountNo": read_yaml2()["SubAccountNo"],
            "IsRemittance": "false",
            "IsPayPlus": "false",
            "RatioRefundType": "",
            "TradeFlow": "default",
            "InstalledApp": "false",
            "AppScheme": "",

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
                with allure.step('买组合请求成功'):
                    if ErrorCode == 0:
                        assert True, '买组合请求成功'
                        ContextId = res.json()["Data"]["ContextId"]
                        AppSheetSerialNo = res.json()["Data"]["AppSheetSerialNo"]
                        BusinType = res.json()["Data"]["BusinType"]
                        clear_yaml3()
                        write_yaml3({"ContextId": ContextId})
                        write_yaml3({"AppSheetSerialNo": AppSheetSerialNo})
                        write_yaml3({"BusinType": BusinType})
                    else:
                        assert False, ErrorMessage
            else:
                assert False, '接口状态码非200'

    @allure.story('买组合结果页 /User/SubA/CompleteOrderCus')
    def test_User_SubA_CompleteOrderCus(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubA/CompleteOrderCus")
        datas = {
            "UserId": read_yaml2()["CustomerNo"],
            "ContextId": read_yaml3()["ContextId"],
            "VerifyCode": "",
            "BankAppPayResult": "",
            "BankCallBackContextId": "",
            "TradeFlow": "",
            "CancelPay": "false",

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
                ErrorMessage1 = res.json()["ErrorMessage"]
                with allure.step('买组合受理结果是否正常展示'):
                    if ErrorCode == 0:
                        assert True
                        PayError = res.json()["Data"]["PayError"]
                        ErrorMessage = res.json()["Data"]["ListTips"][0]["ThirdTitle"]
                        with allure.step('买组合受理结果是否成功'):
                            if PayError == '':
                                assert True, '买组合成功'
                                write_yaml3({"Succeed": True})
                            else:
                                write_yaml3({"Succeed": False})
                                assert False, ErrorMessage
                    else:
                        assert False, ErrorMessage1
            else:
                assert False, '接口状态码非200'

    @allure.story('买组合撤单 /Trade/FundTrade/RevokeOrder')
    # 买组合撤单
    def test_Trade_FundTrade_RevokeOrder(self):
        if read_yaml3()["Succeed"] == False:
            pytest.skip(), '买基金失败无法撤单'
        else:
            time.sleep(2)  # 单号落库时间慢，设个延迟防止报错
            url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/Trade/FundTrade/RevokeOrder")
            datas = {
                "Password": read_yaml1()[read_yaml4()["Pas"]],
                "UserId": read_yaml2()["CustomerNo"],
                "BusinId": read_yaml3()["AppSheetSerialNo"],
                "BusinType": read_yaml3()["BusinType"],
                "IsRevokedToCashBag": "false",
                "DisplayBusinType": read_yaml3()["BusinType"],

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
                    with allure.step('买基金到组合撤单是否成功'):
                        if ErrorCode == 0:
                            assert True, '撤单受理成功'
                        else:
                            assert False, ErrorMessage
                else:
                    assert False, '接口状态码非200'


@allure.feature('买组合 660以下免密')
class Test_buy_Sub_NP():
    @allure.story('交易留痕 /Business/home/NoticeStayTrace')
    # 交易留痕
    def test_Business_home_NoticeStayTrace(self):
        clear_yaml3()
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/Business/home/NoticeStayTrace")
        datas = {
            "UserId": read_yaml2()["CustomerNo"],
            "FundCode": "null",
            "CToken": read_yaml2()["CToken"],
            "UToken": read_yaml2()["UToken"]
        }
        res = requests.request(method='post', url=url, params=datas)
        with allure.step('接口是否正常调通'):
            if res.status_code == 200:
                assert True
                TraceID = res.json()["Data"]["TraceID"]
                write_yaml3({"TraceID": TraceID})
            else:
                assert False, '接口状态码非200'

    @allure.story('买组合 /User/SubA/CommitOrderCusNP')
    # 买组合 660以下免密
    def test_User_SubA_CommitOrderCusNP(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubA/CommitOrderCusNP")
        datas = {
            "TradeType": read_yaml4()["TradeType_Sub"],
            "UserId": read_yaml2()["CustomerNo"],
            "BankAccountNo": read_yaml2()["BankAccountNo"],
            "CouponsType": "",
            "CouponsId": "",
            "FundCode": "",
            "TotalAmounts": read_yaml4()["Amount"],
            "FundAppsJson": "",
            "TraceID": read_yaml3()["TraceID"],
            "RecommanderNo": "",
            "SubAccountNo": "",
            "FollowingSubAccountNo": read_yaml2()["SubAccountNo"],
            "IsRemittance": "false",
            "IsPayPlus": "false",
            "RatioRefundType": "",
            "TradeFlow": "default",
            "InstalledApp": "false",
            "AppScheme": "",

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
                with allure.step('买组合请求成功'):
                    if ErrorCode == 0:
                        assert True, '买组合请求成功'
                        ContextId = res.json()["Data"]["ContextId"]
                        AppSheetSerialNo = res.json()["Data"]["AppSheetSerialNo"]
                        BusinType = res.json()["Data"]["BusinType"]
                        clear_yaml3()
                        write_yaml3({"ContextId": ContextId})
                        write_yaml3({"AppSheetSerialNo": AppSheetSerialNo})
                        write_yaml3({"BusinType": BusinType})
                    else:
                        assert False, ErrorMessage
            else:
                assert False, '接口状态码非200'

    @allure.story('买组合结果页 /User/SubA/CompleteOrderCus')
    def test_User_SubA_CompleteOrderCus(self):
        time.sleep(5)
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubA/CompleteOrderCus")
        datas = {
            "UserId": read_yaml2()["CustomerNo"],
            "ContextId": read_yaml3()["ContextId"],
            "VerifyCode": "",
            "BankAppPayResult": "",
            "BankCallBackContextId": "",
            "TradeFlow": "",
            "CancelPay": "false",

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
                ErrorMessage1 = res.json()["ErrorMessage"]
                with allure.step('买组合受理结果是否正常展示'):
                    if ErrorCode == 0:
                        assert True
                        PayError = res.json()["Data"]["PayError"]
                        ErrorMessage = res.json()["Data"]["ListTips"][0]["ThirdTitle"]
                        with allure.step('买组合受理结果是否成功'):
                            if PayError == '':
                                assert True, '买组合成功'
                                write_yaml3({"Succeed": True})
                            else:
                                write_yaml3({"Succeed": False})
                                assert False, ErrorMessage
                    else:
                        assert False, ErrorMessage1
            else:
                assert False, '接口状态码非200'

    @allure.story('买组合撤单 免密 /Trade/FundTrade/RevokeOrderNP')
    # 买组合撤单 免密
    def test_Trade_FundTrade_RevokeOrderNP(self):
        if read_yaml3()["Succeed"] == False:
            pytest.skip(), '买基金失败无法撤单'
        else:
            time.sleep(2)  # 单号落库时间慢，设个延迟防止报错
            url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/Trade/FundTrade/RevokeOrderNP")
            datas = {
                "Password": read_yaml1()[read_yaml4()["Pas"]],
                "UserId": read_yaml2()["CustomerNo"],
                "BusinId": read_yaml3()["AppSheetSerialNo"],
                "BusinType": read_yaml3()["BusinType"],
                "IsRevokedToCashBag": "false",
                "DisplayBusinType": read_yaml3()["BusinType"],

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
                    with allure.step('买基金到组合撤单是否成功'):
                        if ErrorCode == 0:
                            assert True, '撤单受理成功'
                        else:
                            assert False, ErrorMessage
                else:
                    assert False, '接口状态码非200'

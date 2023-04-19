import os
import time
from urllib.parse import urljoin

import pytest
import requests
import allure

from conftest import read_yaml2, write_yaml2, write_yaml3, read_yaml3, clear_yaml3, read_yaml1, read_yaml4


@allure.feature('买基金到组合 660以下输入密码')
class Test_buy_fund_to_Sub():
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
        TraceID = res.json()["Data"]["TraceID"]
        write_yaml3({"TraceID": TraceID})

    @allure.story('买基金到组合 /Trade/FundTrade/CommitOrder')
    # 买基金到组合 660以下输密码
    def test_Trade_FundTrade_CommitOrder(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/Trade/FundTrade/CommitOrder")
        datas = {
            "Password": read_yaml1()[read_yaml4()["Pas"]],
            "TradeType": read_yaml4()["TradeType"],
            "UserId": read_yaml2()["CustomerNo"],
            "BankAccountNo": read_yaml2()["BankAccountNo"],
            "CouponsType": "",
            "CouponsId": "",
            "FundCode": "000001",
            "TotalAmounts": 10.00,
            "FundAppsJson": read_yaml4()["FundAppsJson"],
            "TraceID": read_yaml3()["TraceID"],
            "RecommanderNo": "",
            "SubAccountNo": read_yaml2()["SubAccountNo"],
            "FollowingSubAccountNo": "",
            "IsRemittance": "false",
            "IsPayPlus": "false",
            "RatioRefundType": "",
            "InstalledApp": "false",

            "PhoneType": "IPhone",
            "ServerVersion": "6.5.8",
            "CToken": read_yaml2()["CToken"],
            "UToken": read_yaml2()["UToken"],
            "MobileKey": "01F12605-0E93-4BCB-AD67-D46C1DDA604B"
        }
        res = requests.request(method='post', url=url, params=datas)
        ErrorCode = res.json()["ErrorCode"]
        AppSerialNo = res.json()["Data"]["AppSerialNo"]
        BusinType = res.json()["Data"]["BusinType"]

        clear_yaml3()
        write_yaml3({"AppSerialNo": AppSerialNo})
        write_yaml3({"BusinType": BusinType})
        with allure.step('接口是否正常调通'):
            if res.status_code == 200:
                assert True
            else:
                assert False, '接口状态码非200'
        with allure.step('买基金到组合请求成功'):
            if ErrorCode == 0:
                assert True
            else:
                assert False, '登录状态已过期，请重新登录'
        time.sleep(5)

    @allure.story('买基金到组合结果页 /Trade/FundTrade/OrderResult')
    def test_Trade_FundTrade_OrderResult(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/Trade/FundTrade/OrderResult")
        datas = {
            "AppSerialNo": read_yaml3()["AppSerialNo"],
            "ParentAppSerialNo": '',
            "BusinType": read_yaml3()["BusinType"],
            "Mode": '',
            "TradeModeType": '',
            "UserId": read_yaml2()["CustomerNo"],

            "PhoneType": "IPhone",
            "ServerVersion": "6.5.8",
            "CToken": read_yaml2()["CToken"],
            "UToken": read_yaml2()["UToken"],
            "MobileKey": "01F12605-0E93-4BCB-AD67-D46C1DDA604B"
        }
        res = requests.request(method='post', url=url, params=datas)
        ErrorCode = res.json()["ErrorCode"]
        PayError = res.json()["Data"]["PayError"]
        ErrorMessage = res.json()["Data"]["ListTips"][0]["ThirdTitle"]
        """
        write_yaml3({"PayError": PayError})
        """
        with allure.step('接口是否正常调通'):
            if res.status_code == 200:
                assert True
            else:
                assert False, '接口状态码非200'
        with allure.step('买基金到组合受理结果是否正常展示'):
            if ErrorCode == 0:
                assert True
            else:
                assert False, '登录状态已过期，请重新登录'
        with allure.step('买基金到组合受理结果是否成功'):
            if PayError == '':
                assert True, '买基金到组合成功'
            else:
                assert False, ErrorMessage


@allure.feature('买基金到组合 660以下免密')
class Test_buy_fund_to_Sub_NP():
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
        TraceID = res.json()["Data"]["TraceID"]
        write_yaml3({"TraceID": TraceID})

    @allure.story('买基金到组合免密 /Trade/FundTrade/CommitOrderNP')
    # 买基金到组合 660以下免密
    def test_Trade_FundTrade_CommitOrder(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/Trade/FundTrade/CommitOrderNP")
        datas = {
            "TradeType": read_yaml4()["TradeType"],
            "UserId": read_yaml2()["CustomerNo"],
            "BankAccountNo": read_yaml2()["BankAccountNo"],
            "CouponsType": "",
            "CouponsId": "",
            "FundCode": "000001",
            "TotalAmounts": 10.00,
            "FundAppsJson": read_yaml4()["FundAppsJson"],
            "TraceID": read_yaml3()["TraceID"],
            "RecommanderNo": "",
            "SubAccountNo": read_yaml2()["SubAccountNo"],
            "FollowingSubAccountNo": "",
            "IsRemittance": "false",
            "IsPayPlus": "false",
            "RatioRefundType": "",
            "InstalledApp": "false",

            "PhoneType": "IPhone",
            "ServerVersion": "6.5.8",
            "CToken": read_yaml2()["CToken"],
            "UToken": read_yaml2()["UToken"],
            "MobileKey": "01F12605-0E93-4BCB-AD67-D46C1DDA604B"
        }
        res = requests.request(method='post', url=url, params=datas)
        ErrorCode = res.json()["ErrorCode"]
        AppSerialNo = res.json()["Data"]["AppSerialNo"]
        BusinType = res.json()["Data"]["BusinType"]

        clear_yaml3()
        write_yaml3({"AppSerialNo": AppSerialNo})
        write_yaml3({"BusinType": BusinType})
        with allure.step('接口是否正常调通'):
            if res.status_code == 200:
                assert True
            else:
                assert False, '接口状态码非200'
        with allure.step('买基金到组合请求成功'):
            if ErrorCode == 0:
                assert True
            else:
                assert False, '登录状态已过期，请重新登录'
        time.sleep(5)

    @allure.story('买基金到组合结果页 /Trade/FundTrade/OrderResult')
    def test_Trade_FundTrade_OrderResult(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/Trade/FundTrade/OrderResult")
        datas = {
            "AppSerialNo": read_yaml3()["AppSerialNo"],
            "ParentAppSerialNo": '',
            "BusinType": read_yaml3()["BusinType"],
            "Mode": '',
            "TradeModeType": '',
            "UserId": read_yaml2()["CustomerNo"],

            "PhoneType": "IPhone",
            "ServerVersion": "6.5.8",
            "CToken": read_yaml2()["CToken"],
            "UToken": read_yaml2()["UToken"],
            "MobileKey": "01F12605-0E93-4BCB-AD67-D46C1DDA604B"
        }
        res = requests.request(method='post', url=url, params=datas)
        ErrorCode = res.json()["ErrorCode"]
        PayError = res.json()["Data"]["PayError"]
        ErrorMessage = res.json()["Data"]["ListTips"][0]["ThirdTitle"]
        """
        write_yaml3({"PayError": PayError})
        """
        with allure.step('接口是否正常调通'):
            if res.status_code == 200:
                assert True
            else:
                assert False, '接口状态码非200'
        with allure.step('买基金到组合受理结果是否正常展示'):
            if ErrorCode == 0:
                assert True
            else:
                assert False, '登录状态已过期，请重新登录'
        with allure.step('买基金到组合受理结果是否成功'):
            if PayError == '':
                assert True, '买基金到组合成功'
            else:
                assert False, ErrorMessage


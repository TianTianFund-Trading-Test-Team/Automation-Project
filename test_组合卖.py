import os
import time
from urllib.parse import urljoin

import pytest
import requests
import allure

from conftest import read_yaml2, write_yaml2, write_yaml3, read_yaml3, clear_yaml3, read_yaml1, read_yaml4


@allure.feature('组合卖出 660以下输入密码')
class Test_redeem_Sub():
    @allure.story('获取组合内份额 /User/SubA/SubARatioRedeemOverviewV2')
    # 获取组合内份额
    def test_User_SubA_SubARatioRedeemOverviewV2(self):
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

    @allure.story('等比例卖出组合 /User/SubA/SubARatioRedeemCards')
    # 等比例卖出组合
    def test_User_SubA_SubARatioRedeemCards(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubA/SubARatioRedeemCards")
        datas = {
            "Password": read_yaml1()[read_yaml4()["Pas"]],
            "UserId": read_yaml2()["CustomerNo"],
            "SubAccountNo": read_yaml2()["SubAccountNo"],
            "Type": read_yaml4()["Type"],  # 回银行卡 1   回活期宝 2
            "ObjectFundCode": read_yaml1()["FundCode_HQB_ZHM"],  # 活期宝基金代码,不传回银行卡
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
            else:
                assert False, '接口状态码非200'
        ErrorCode = res.json()["ErrorCode"]
        ErrorMessage = res.json()["Data"]["ListTips"][0]["ThirdTitle"]
        with allure.step('组合卖出是否正常'):
            if ErrorCode == 0:
                assert True
            else:
                assert False, ErrorMessage

    @allure.story('等比例卖出组合 免密 /User/SubA/SubARatioRedeemCardsNP')
    # 等比例卖出组合 免密
    def test_User_SubA_SubARatioRedeemCardsNP(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubA/SubARatioRedeemCardsNP")
        datas = {
            "UserId": read_yaml2()["CustomerNo"],
            "SubAccountNo": read_yaml2()["SubAccountNo"],
            "Type": read_yaml4()["Type"],  # 回银行卡 1   回活期宝 2
            "ObjectFundCode": read_yaml1()["FundCode_HQB_ZHM"],  # 活期宝基金代码，不传回银行卡
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
            else:
                assert False, '接口状态码非200'
        ErrorCode = res.json()["ErrorCode"]
        ErrorMessage = res.json()["Data"]["ListTips"][0]["ThirdTitle"]
        with allure.step('组合卖出是否正常'):
            if ErrorCode == 0:
                assert True
            else:
                assert False, ErrorMessage

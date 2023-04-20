import os
import time
from urllib.parse import urljoin

import pytest
import requests
import allure

from conftest import read_yaml2, write_yaml2, write_yaml3, read_yaml3, clear_yaml3, read_yaml1, read_yaml4


@allure.feature('组合内基金普通卖出 24')
class Test_redeem_Fund_Sub():
    @allure.story('子账户持仓 /User/Asset/GetFundAssetListOfSubV2')
    # 获取子账户持仓 混合型
    def test_User_Asset_GetFundAssetListOfSubV2(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/Asset/GetFundAssetListOfSubV2")
        datas = {
            "UserId": read_yaml2()["CustomerNo"],
            "SubAccountNo": read_yaml2()["SubAccountNo"],
            "UnifiedType": "HH",  # 筛选类型： HH 混合； ZS 指数； GP 股票； ZQ 债券； QD QD基金； HB 货币基金
            "BankCardNo": "",

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
        FundCode = res.json()["Data"]["AssetDetails"][0]["FundCode"]
        clear_yaml3()
        write_yaml3({"FundCode": FundCode})

    @allure.story('持仓详情（组合） /User/home/GetShareDetail')
    # 获取特定基金的组合份额
    def test_User_home_GetShareDetail(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/home/GetShareDetail")
        datas = {
            "UserId": read_yaml2()["CustomerNo"],
            "SubAccountNo": read_yaml2()["SubAccountNo"],
            "FundCode": read_yaml3()["FundCode"],
            "IsBaseAsset": "false",
            "TransactionAccountId": "",
            "NeedReturnZeroVolItems": "false",

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
        ShareId = res.json()["Data"]["Shares"][0]["ShareId"]
        AvailableShare = res.json()["Data"]["Shares"][0]["AvailableShare"]
        write_yaml3({"ShareId": ShareId})
        write_yaml3({"AvailableShare": AvailableShare})

    @allure.story('卖组合单基金 /Business/hqb/MakeRedemption')
    # 卖组合单基金
    def test_Business_hqb_MakeRedemption(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/Business/hqb/MakeRedemption")
        datas = {
            "Password": read_yaml1()[read_yaml4()["Pas"]],
            "CustomerNo": "",
            "UserId": read_yaml2()["CustomerNo"],
            "PayType": read_yaml4()["PayType"],
            "Vol": read_yaml4()["Vol"],
            "ShareID": read_yaml3()["ShareId"],
            "RedemptionFlag": "1",
            "RechargeCashBagFundCode": read_yaml4()["FundCode_HQB"],  # 活期宝基金
            "IsQuickToCashBag": "false",
            "FldParam": "",
            "SubAccountNo": read_yaml2()["SubAccountNo"],

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
        with allure.step('卖单只组合基金回活期宝是否成功'):
            if ErrorCode == 0:
                assert True, '申请赎回成功'
            else:
                assert False, ErrorMessage

    @allure.story('卖组合单基金 免密 /Business/hqb/MakeRedemptionNP')
    # 卖组合单基金 免密
    def test_Business_hqb_MakeRedemptionNP(self):
        time.sleep(3)
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/Business/hqb/MakeRedemptionNP")
        datas = {
            "CustomerNo": "",
            "UserId": read_yaml2()["CustomerNo"],
            "PayType": read_yaml4()["PayType"],
            "Vol": read_yaml4()["Vol"],
            "ShareID": read_yaml3()["ShareId"],
            "RedemptionFlag": "1",
            "RechargeCashBagFundCode": read_yaml4()["FundCode_HQB"],
            "IsQuickToCashBag": "false",
            "FldParam": "",
            "SubAccountNo": read_yaml2()["SubAccountNo"],

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
        with allure.step('卖组合内单基金是否成功'):
            if ErrorCode == 0:
                assert True, '申请赎回成功'
            else:
                assert False, ErrorMessage


@allure.feature('组合内基金卖出极速回活期宝 815 ')
class Test_redeem_Fund_Sub():
    @allure.story('子账户持仓 /User/Asset/GetFundAssetListOfSubV2')
    # 获取子账户持仓 混合型
    def test_User_Asset_GetFundAssetListOfSubV2(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/Asset/GetFundAssetListOfSubV2")
        datas = {
            "UserId": read_yaml2()["CustomerNo"],
            "SubAccountNo": read_yaml2()["SubAccountNo"],
            "UnifiedType": "HH",  # 筛选类型： HH 混合； ZS 指数； GP 股票； ZQ 债券； QD QD基金； HB 货币基金
            "BankCardNo": "",

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
        FundCode = res.json()["Data"]["AssetDetails"][0]["FundCode"]
        clear_yaml3()
        write_yaml3({"FundCode": FundCode})

    @allure.story('持仓详情（组合） /User/home/GetShareDetail')
    # 获取特定基金的组合份额
    def test_User_home_GetShareDetail(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/home/GetShareDetail")
        datas = {
            "UserId": read_yaml2()["CustomerNo"],
            "SubAccountNo": read_yaml2()["SubAccountNo"],
            "FundCode": read_yaml3()["FundCode"],
            "IsBaseAsset": "false",
            "TransactionAccountId": "",
            "NeedReturnZeroVolItems": "false",

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
        ShareId = res.json()["Data"]["Shares"][0]["ShareId"]
        AvailableShare = res.json()["Data"]["Shares"][0]["AvailableShare"]
        write_yaml3({"ShareId": ShareId})
        write_yaml3({"AvailableShare": AvailableShare})

    @allure.story('卖组合单基金极速回活期宝 /Business/Home/SFTransfer')
    # 卖组合单基金极速回活期宝
    def test_Business_Home_SFTransfer(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/Business/Home/SFTransfer")
        datas = {
            "Pwd": read_yaml1()[read_yaml4()["Pas"]],
            "UserId": read_yaml2()["CustomerNo"],
            "ShareID": read_yaml3()["ShareId"],
            "FldParam": "",

            "FundIn": "015419",  # 活期宝基金
            "SubAccountNoIn": "",
            "FundCode": "015419",  # 活期宝基金
            "FundOut": read_yaml3()["FundCode"],
            "FundAmount": read_yaml4()["FundAmount"],
            "LargeRedemptionFlag": "1",
            "TraceID": "",
            "IsAllTransfer": "false",

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
        with allure.step('卖单只组合基金回活期宝是否成功'):
            if ErrorCode == 0:
                assert True, '申请赎回成功'
            else:
                assert False, ErrorMessage

    @allure.story('卖组合单基金极速回活期宝 免密 /Business/Home/SFTransferNP')
    # 卖组合单基金极速回活期宝 免密
    def test_Business_Home_SFTransferNP(self):
        time.sleep(2)
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/Business/Home/SFTransferNP")
        datas = {
            "UserId": read_yaml2()["CustomerNo"],
            "ShareID": read_yaml3()["ShareId"],
            "FldParam": "",

            "FundIn": "015419",  # 活期宝基金
            "SubAccountNoIn": "",
            "FundCode": "015419",  # 活期宝基金
            "FundOut": read_yaml3()["FundCode"],
            "FundAmount": read_yaml4()["FundAmount"],
            "LargeRedemptionFlag": "1",
            "TraceID": "",
            "IsAllTransfer": "false",

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
        with allure.step('卖单只组合基金回活期宝是否成功'):
            if ErrorCode == 0:
                assert True, '申请赎回成功'
            else:
                assert False, ErrorMessage

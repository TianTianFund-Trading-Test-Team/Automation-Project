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
                FundCode = res.json()["Data"]["AssetDetails"][0]["FundCode"]
                clear_yaml3()
                write_yaml3({"FundCode": FundCode})
            else:
                assert False, '接口状态码非200'

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
                with allure.step('选择大于10份额的ID'):  # 因为多卡才做的逻辑。这个接口没有排序也没有字段返回份额数量
                    for i in range(5):
                        try:
                            if res.json()["Data"]["Shares"][i - 1]["AvailableShare"] > 10:
                                assert True
                                AvailableShare = res.json()["Data"]["Shares"][i - 1]["AvailableShare"]
                                ShareId = res.json()["Data"]["Shares"][i - 1]["ShareId"]
                                write_yaml3({"ShareId": ShareId})
                                write_yaml3({"AvailableShare": AvailableShare})
                                break
                        except IndexError:
                            pass
            else:
                assert False, '接口状态码非200'

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
        with allure.step('接口是否正常调通'):
            if res.status_code == 200:
                assert True
                ErrorCode = res.json()["ErrorCode"]
                ErrorMessage = res.json()["ErrorMessage"]
                with allure.step('卖单只组合基金回活期宝是否成功'):
                    if ErrorCode == 0:
                        assert True, '申请赎回成功'
                        BusinSerialNo = res.json()["Data"]["JumpParams"]["BusinSerialNo"]
                        BusinessType = res.json()["Data"]["JumpParams"]["BusinessType"]
                        clear_yaml3()
                        write_yaml3({"BusinSerialNo": BusinSerialNo})
                        write_yaml3({"BusinessType": BusinessType})
                        write_yaml3({"Succeed": True})
                    else:
                        write_yaml3({"Succeed": False})
                        assert False, ErrorMessage
            else:
                assert False, '接口状态码非200'

    @allure.story('买组合撤单 免密 /Trade/FundTrade/RevokeOrder')
    # 买组合撤单 免密
    def test_Trade_FundTrade_RevokeOrder(self):
        if read_yaml3()["Succeed"] == False:
            pytest.skip(), '买基金失败无法撤单'
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
                    with allure.step('24 撤单是否成功'):
                        if ErrorCode == 0:
                            assert True, '撤单受理成功'
                        else:
                            assert False, ErrorMessage
                else:
                    assert False, '接口状态码非200'


@allure.feature('组合内基金普通卖出 免密 24')
class Test_redeem_Fund_Sub_NP():
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
                FundCode = res.json()["Data"]["AssetDetails"][0]["FundCode"]
                clear_yaml3()
                write_yaml3({"FundCode": FundCode})
            else:
                assert False, '接口状态码非200'

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
                with allure.step('选择大于10份额的ID'):  # 因为多卡才做的逻辑。这个接口没有排序也没有字段返回份额数量
                    for i in range(5):
                        try:
                            if res.json()["Data"]["Shares"][i - 1]["AvailableShare"] > 10:
                                assert True
                                AvailableShare = res.json()["Data"]["Shares"][i - 1]["AvailableShare"]
                                ShareId = res.json()["Data"]["Shares"][i - 1]["ShareId"]
                                write_yaml3({"ShareId": ShareId})
                                write_yaml3({"AvailableShare": AvailableShare})
                                break
                        except IndexError:
                            pass
            else:
                assert False, '接口状态码非200'

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
        with allure.step('接口是否正常调通'):
            if res.status_code == 200:
                assert True
                ErrorCode = res.json()["ErrorCode"]
                ErrorMessage = res.json()["ErrorMessage"]
                with allure.step('卖组合内单基金是否成功'):
                    if ErrorCode == 0:
                        BusinSerialNo = res.json()["Data"]["JumpParams"]["BusinSerialNo"]
                        BusinessType = res.json()["Data"]["JumpParams"]["BusinessType"]
                        clear_yaml3()
                        write_yaml3({"BusinSerialNo": BusinSerialNo})
                        write_yaml3({"BusinessType": BusinessType})
                        write_yaml3({"Succeed": True})
                    else:
                        write_yaml3({"Succeed": False})
                        assert False, ErrorMessage
            else:
                assert False, '接口状态码非200'

    @allure.story('组合内基金卖出撤单 免密 /Trade/FundTrade/RevokeOrderNP')
    # 买组合撤单 免密
    def test_Trade_FundTrade_RevokeOrderNP(self):
        if read_yaml3()["Succeed"] == False:
            pytest.skip(), '买基金失败无法撤单'
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
                    with allure.step('24 撤单是否成功'):
                        if ErrorCode == 0:
                            assert True, '撤单受理成功'
                        else:
                            assert False, ErrorMessage
                else:
                    assert False, '接口状态码非200'


@allure.feature('组合内基金卖出极速回活期宝 815 ')
class Test_Quick_redeem_Fund_Sub():
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
                FundCode = res.json()["Data"]["AssetDetails"][0]["FundCode"]  # 写死的取第一个
                clear_yaml3()
                write_yaml3({"FundCode": FundCode})
            else:
                assert False, '接口状态码非200'

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
                with allure.step('选择大于10份额的ID'):  # 因为多卡才做的逻辑。这个接口没有排序也没有字段返回份额数量
                    for i in range(5):
                        try:
                            if res.json()["Data"]["Shares"][i - 1]["AvailableShare"] > 10:
                                assert True
                                AvailableShare = res.json()["Data"]["Shares"][i - 1]["AvailableShare"]
                                ShareId = res.json()["Data"]["Shares"][i - 1]["ShareId"]
                                write_yaml3({"ShareId": ShareId})
                                write_yaml3({"AvailableShare": AvailableShare})
                                break
                        except IndexError:
                            pass
            else:
                assert False, '接口状态码非200'

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
        with allure.step('接口是否正常调通'):
            if res.status_code == 200:
                assert True
                ErrorCode = res.json()["ErrorCode"]
                ErrorMessage = res.json()["ErrorMessage"]
                with allure.step('卖单只组合基金回活期宝是否成功'):
                    if ErrorCode == 0:
                        assert True, '申请赎回成功'
                        clear_yaml3()
                        BusinSerialNo = res.json()["Data"]["JumpParams"]["BusinSerialNo"]
                        BusinessType = res.json()["Data"]["JumpParams"]["BusinessType"]
                        write_yaml3({"BusinSerialNo": BusinSerialNo})
                        write_yaml3({"BusinessType": BusinessType})
                    else:
                        assert False, ErrorMessage
            else:
                assert False, '接口状态码非200'

    @allure.story('815撤单 /Trade/FundTrade/RevokeOrder')
    # 815撤单
    def test_Trade_FundTrade_RevokeOrder(self):
        if read_yaml3() is None:
            pytest.skip(), '没有HH基金份额或者份额不足无法发起超级转换'
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
                    with allure.step('超级转换撤单是否成功'):
                        if ErrorCode == 0:
                            assert True, '撤单受理成功'
                        else:
                            assert False, ErrorMessage
                else:
                    assert False, '接口状态码非200'


@allure.feature('组合内基金卖出极速回活期宝 免密 815 ')
class Test_Quick_redeem_Fund_Sub_NP():
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
                FundCode = res.json()["Data"]["AssetDetails"][0]["FundCode"]  # 写死的取第一个
                clear_yaml3()
                write_yaml3({"FundCode": FundCode})
            else:
                assert False, '接口状态码非200'

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
                with allure.step('选择大于10份额的ID'):  # 因为多卡才做的逻辑。这个接口没有排序也没有字段返回份额数量
                    for i in range(5):
                        try:
                            if res.json()["Data"]["Shares"][i - 1]["AvailableShare"] > 10:
                                assert True
                                AvailableShare = res.json()["Data"]["Shares"][i - 1]["AvailableShare"]
                                ShareId = res.json()["Data"]["Shares"][i - 1]["ShareId"]
                                write_yaml3({"ShareId": ShareId})
                                write_yaml3({"AvailableShare": AvailableShare})
                                break
                        except IndexError:
                            pass
            else:
                assert False, '接口状态码非200'

    @allure.story('卖组合单基金极速回活期宝 免密 /Business/Home/SFTransferNP')
    # 卖组合单基金极速回活期宝 免密
    def test_Business_Home_SFTransferNP(self):
        time.sleep(4)
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
        with allure.step('接口是否正常调通'):
            if res.status_code == 200:
                assert True
                ErrorCode = res.json()["ErrorCode"]
                ErrorMessage = res.json()["ErrorMessage"]
                with allure.step('卖单只组合基金回活期宝是否成功'):
                    if ErrorCode == 0:
                        assert True, '申请赎回成功'
                        clear_yaml3()
                        BusinSerialNo = res.json()["Data"]["JumpParams"]["BusinSerialNo"]
                        BusinessType = res.json()["Data"]["JumpParams"]["BusinessType"]
                        write_yaml3({"BusinSerialNo": BusinSerialNo})
                        write_yaml3({"BusinessType": BusinessType})
                    else:
                        assert False, ErrorMessage
            else:
                assert False, '接口状态码非200'

    @allure.story('815撤单 免密 /Trade/FundTrade/RevokeOrderNP')
    # 815撤单 免密
    def test_Trade_FundTrade_RevokeOrderNP(self):
        if read_yaml3() is None:
            pytest.skip(), '没有HH基金份额或者份额不足无法发起超级转换'
        else:
            time.sleep(2)  # 单号落库时间慢，设个延迟防止报错
            url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/Trade/FundTrade/RevokeOrderNP")
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
                    with allure.step('超级转换撤单是否成功'):
                        if ErrorCode == 0:
                            assert True, '撤单受理成功'
                        else:
                            assert False, ErrorMessage
                else:
                    assert False, '接口状态码非200'

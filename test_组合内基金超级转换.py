import os
import time
from urllib.parse import urljoin

import pytest
import requests
import allure

from conftest import read_yaml2, write_yaml2, write_yaml3, read_yaml3, clear_yaml3, read_yaml1, read_yaml4, read_yaml5, \
    write_yaml5, clear_yaml5

# 全局变量
g_key = 0


def modify_g_key():
    global g_key
    if g_key < read_yaml5()["Count"] - 1:
        g_key = g_key + 1
    else:
        assert False, '组合内基金均不支持超级转换'


@allure.feature('组合内基金超级转换 815')
class Test_CJZH_Sub():
    @allure.story('持仓详情 003333 /User/home/GetShareDetail')
    # 获取003333起购金额
    def test_User_home_GetShareDetail_003333(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/home/GetShareDetail")
        datas = {
            "UserId": read_yaml2()["CustomerNo"],
            "SubAccountNo": "",
            "FundCode": "003333",
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
                clear_yaml5()
                MinSg = res.json()["Data"]["MinSg"]
                write_yaml5({"MinSg": MinSg})  # 拿003333最小申购金额
            else:
                assert False, '接口状态码非200'

    @allure.story('子账户持仓 /User/Asset/GetFundAssetListOfSubV2')
    # 获取子账户持仓 HH型
    def test_User_Asset_GetFundAssetListOfSubV2(self):
        clear_yaml3()
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
                Res = res.json()["Data"]["AssetDetails"]
                with allure.step('组合里是否有HH基金'):
                    if Res == []:
                        clear_yaml3()
                        assert False, '组合内没有HH基金'
                    else:
                        assert True
                        Count = res.json()["Data"]["AssetCounts"]["HH"]
                        FundCode = res.json()["Data"]["AssetDetails"][g_key]["FundCode"]
                        clear_yaml3()
                        write_yaml3({"FundCode": FundCode})
                        write_yaml5({"Count": Count})
                        write_yaml2({"g_key": g_key})
            else:
                assert False, '接口状态码非200'

    @allure.story('持仓详情（组合） /User/home/GetShareDetail')
    # 获取特定基金的组合份额
    def test_User_home_GetShareDetail(self):
        if read_yaml3() is None:
            pytest.skip(), '没有HH基金份额无法发起超级转换'
        else:
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
                    Enable815 = res.json()["Data"]["Enable815"]
                    if Enable815 == True:
                        FundNav = res.json()["Data"]["FundNav"]
                        for i in range(5):  # 因为多卡才做的逻辑。这个接口没有排序也没有字段返回份额数量
                            try:
                                if res.json()["Data"]["Shares"][i - 1]["AvailableShare"] > (
                                        read_yaml5()["MinSg"] / FundNav) / 0.9:
                                    BankCardNo = res.json()["Data"]["Shares"][i - 1]["BankCardNo"]
                                    BankAccountNo = res.json()["Data"]["Shares"][i - 1]["BankAccountNo"]
                                    ShareId = res.json()["Data"]["Shares"][i - 1]["ShareId"]
                                    write_yaml3({"BankCardNo": BankCardNo})
                                    write_yaml3({"BankAccountNo": BankAccountNo})
                                    write_yaml3({"ShareId": ShareId})
                                break
                            except IndexError:
                                clear_yaml3()
                                pass
                        try:
                            if read_yaml3() == {'FundCode': read_yaml3()["FundCode"]}:
                                clear_yaml3()
                                '该基金没有份额可以做超级转换'
                        except TypeError:
                            clear_yaml3()
                            pass
                    else:
                        clear_yaml3()
                        '该基金不支持股基转换'
                else:
                    assert False, '接口状态码非200'

    @allure.story('转换详情（组合） /Trade/FundTrade/TransferOverview')
    # 获取转换的最小转出
    def test_Trade_FundTrade_TransferOverview(self):
        if read_yaml3() is None:
            modify_g_key()
            self.test_User_home_GetShareDetail_003333()
            self.test_User_Asset_GetFundAssetListOfSubV2()
            self.test_User_home_GetShareDetail()
            self.test_Trade_FundTrade_TransferOverview()
        else:
            url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/Trade/FundTrade/TransferOverview")
            datas = {
                "UserId": read_yaml2()["CustomerNo"],
                "FundCodeOut": read_yaml3()["FundCode"],
                "FundCodeIn": "003333",
                "TransferType": '',
                "BankCardNo": read_yaml3()["BankCardNo"],
                "BankAccountNo": read_yaml3()["BankAccountNo"],

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
                    FundNav = res.json()["Data"]["TranOutFund"]["FundNav"]
                    MinRedeem = res.json()["Data"]["TranOutFund"]["MinRedeem"]
                    MinHoldShares = res.json()["Data"]["TranOutFund"]["MinHoldShares"]
                    AvailableVol = res.json()["Data"]["TranOutFund"]["RedeemShareAndRateList"][0]["AvailableVol"]
                    FundAmount_CJZH = round((read_yaml5()["MinSg"] / FundNav) / 0.9, 2)+0.01  # 中台进位问题
                    if MinRedeem < FundAmount_CJZH:
                        if AvailableVol - FundAmount_CJZH > MinHoldShares:
                            write_yaml3({"FundAmount_CJZH": FundAmount_CJZH})
                        else:
                            write_yaml3({"FundAmount_CJZH": AvailableVol})
                    else:
                        if AvailableVol - MinRedeem > MinHoldShares:
                            write_yaml3({"FundAmount_CJZH": MinRedeem})
                        else:
                            write_yaml3({"FundAmount_CJZH": AvailableVol})
                else:
                    assert False, '接口状态码非200'

    @allure.story('交易留痕 /Business/home/NoticeStayTrace')
    # 交易留痕
    def test_Business_home_NoticeStayTrace(self):
        if read_yaml3() is None:
            pytest.skip(), '没有HH基金份额或者份额不足无法发起超级转换'
        else:
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

    @allure.story('组合内基金超级转换 /Business/Home/SFTransfer')
    # 组合内基金超级转换
    def test_Business_Home_SFTransfer(self):
        if read_yaml3() is None:
            pytest.skip(), '没有HH基金份额或者份额不足无法发起超级转换'
        else:
            url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/Business/Home/SFTransfer")
            datas = {
                "Pwd": read_yaml1()[read_yaml4()["Pas"]],
                "UserId": read_yaml2()["CustomerNo"],
                "ShareID": read_yaml3()["ShareId"],
                "FldParam": "",

                "FundIn": "003333",  # 非活期宝基金，高端理财等无法买入到组合的基金
                "SubAccountNoIn": read_yaml2()["SubAccountNo"],
                "FundCode": "003333",  # 非活期宝基金，高端理财等无法买入到组合的基金
                "FundOut": read_yaml3()["FundCode"],
                "FundAmount": read_yaml3()["FundAmount_CJZH"],
                "LargeRedemptionFlag": "1",
                "IsAllTransfer": "false",
                "TraceID": read_yaml3()["TraceID"],

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
                    with allure.step('组合内基金转换是否成功'):
                        if ErrorCode == 0:
                            assert True, '申请受理成功'
                            clear_yaml3()
                            BusinSerialNo = res.json()["Data"]["JumpParams"]["BusinSerialNo"]
                            BusinessType = res.json()["Data"]["JumpParams"]["BusinessType"]
                            write_yaml3({"BusinSerialNo": BusinSerialNo})
                            write_yaml3({"BusinessType": BusinessType})
                        else:
                            clear_yaml3()
                            assert False, ErrorMessage
                else:
                    assert False, '接口状态码非200'

    @allure.story('815撤单 /Trade/FundTrade/RevokeOrder')
    # 815撤单
    def test_Trade_FundTrade_RevokeOrder(self):
        if read_yaml3() is None:
            pytest.skip(), '由于没有HH基金份额，份额不足，资金池超限等原因无法发起超级转换'
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


@allure.feature('组合内基金超级转换 815 免密')
class Test_CJZH_Sub_NP():

    @allure.story('持仓详情 003333 /User/home/GetShareDetail')
    # 获取003333起购金额
    def test_User_home_GetShareDetail_003333(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/home/GetShareDetail")
        datas = {
            "UserId": read_yaml2()["CustomerNo"],
            "SubAccountNo": "",
            "FundCode": "003333",
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
                clear_yaml5()
                MinSg = res.json()["Data"]["MinSg"]
                write_yaml5({"MinSg": MinSg})  # 拿003333最小申购金额
            else:
                assert False, '接口状态码非200'

    @allure.story('子账户持仓 /User/Asset/GetFundAssetListOfSubV2')
    # 获取子账户持仓 HH型
    def test_User_Asset_GetFundAssetListOfSubV2(self):
        clear_yaml3()
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
                Res = res.json()["Data"]["AssetDetails"]
                with allure.step('组合里是否有HH基金'):
                    if Res == []:
                        clear_yaml3()
                        assert False, '组合内没有HH基金'
                    else:
                        assert True
                        Count = res.json()["Data"]["AssetCounts"]["HH"]
                        FundCode = res.json()["Data"]["AssetDetails"][g_key]["FundCode"]
                        clear_yaml3()
                        write_yaml3({"FundCode": FundCode})
                        write_yaml5({"Count": Count})
                        write_yaml2({"g_key": g_key})
            else:
                assert False, '接口状态码非200'

    @allure.story('持仓详情（组合） /User/home/GetShareDetail')
    # 获取特定基金的组合份额
    def test_User_home_GetShareDetail(self):
        if read_yaml3() is None:
            pytest.skip(), '没有HH基金份额无法发起超级转换'
        else:
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
                    Enable815 = res.json()["Data"]["Enable815"]
                    if Enable815 == True:
                        FundNav = res.json()["Data"]["FundNav"]
                        for i in range(5):  # 因为多卡才做的逻辑。这个接口没有排序也没有字段返回份额数量
                            try:
                                if res.json()["Data"]["Shares"][i - 1]["AvailableShare"] > (
                                        read_yaml5()["MinSg"] / FundNav) / 0.9:
                                    BankCardNo = res.json()["Data"]["Shares"][i - 1]["BankCardNo"]
                                    BankAccountNo = res.json()["Data"]["Shares"][i - 1]["BankAccountNo"]
                                    ShareId = res.json()["Data"]["Shares"][i - 1]["ShareId"]
                                    write_yaml3({"BankCardNo": BankCardNo})
                                    write_yaml3({"BankAccountNo": BankAccountNo})
                                    write_yaml3({"ShareId": ShareId})
                                break
                            except IndexError:
                                clear_yaml3()
                                pass
                        try:
                            if read_yaml3() == {'FundCode': read_yaml3()["FundCode"]}:
                                clear_yaml3()
                                '该基金没有份额可以做超级转换'
                        except TypeError:
                            clear_yaml3()
                            pass
                    else:
                        clear_yaml3()
                        '该基金不支持股基转换'
                else:
                    assert False, '接口状态码非200'

    @allure.story('转换详情（组合） /Trade/FundTrade/TransferOverview')
    # 获取转换的最小转出
    def test_Trade_FundTrade_TransferOverview(self):
        if read_yaml3() is None:
            modify_g_key()
            self.test_User_home_GetShareDetail_003333()
            self.test_User_Asset_GetFundAssetListOfSubV2()
            self.test_User_home_GetShareDetail()
            self.test_Trade_FundTrade_TransferOverview()
        else:
            url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/Trade/FundTrade/TransferOverview")
            datas = {
                "UserId": read_yaml2()["CustomerNo"],
                "FundCodeOut": read_yaml3()["FundCode"],
                "FundCodeIn": "003333",
                "TransferType": '',
                "BankCardNo": read_yaml3()["BankCardNo"],
                "BankAccountNo": read_yaml3()["BankAccountNo"],

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
                    FundNav = res.json()["Data"]["TranOutFund"]["FundNav"]
                    MinRedeem = res.json()["Data"]["TranOutFund"]["MinRedeem"]
                    MinHoldShares = res.json()["Data"]["TranOutFund"]["MinHoldShares"]
                    AvailableVol = res.json()["Data"]["TranOutFund"]["RedeemShareAndRateList"][0]["AvailableVol"]
                    FundAmount_CJZH = round((read_yaml5()["MinSg"] / FundNav) / 0.9, 2)+0.01
                    if MinRedeem < FundAmount_CJZH:
                        if AvailableVol - FundAmount_CJZH > MinHoldShares:
                            write_yaml3({"FundAmount_CJZH": FundAmount_CJZH})
                        else:
                            write_yaml3({"FundAmount_CJZH": AvailableVol})
                    else:
                        if AvailableVol - MinRedeem > MinHoldShares:
                            write_yaml3({"FundAmount_CJZH": MinRedeem})
                        else:
                            write_yaml3({"FundAmount_CJZH": AvailableVol})
                else:
                    assert False, '接口状态码非200'

    @allure.story('交易留痕 /Business/home/NoticeStayTrace')
    # 交易留痕
    def test_Business_home_NoticeStayTrace(self):
        if read_yaml3() is None:
            pytest.skip(), '没有HH基金份额或者份额不足无法发起超级转换'
        else:
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

    @allure.story('组合内基金超级转换 免密 /Business/Home/SFTransferNP')
    # 组合内基金超级转换 免密
    def test_Business_Home_SFTransferNP(self):
        if read_yaml3() is None:
            pytest.skip(), '没有HH基金份额或者份额不足无法发起超级转换'
        else:
            time.sleep(3)
            url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/Business/Home/SFTransferNP")
            datas = {
                "UserId": read_yaml2()["CustomerNo"],
                "ShareID": read_yaml3()["ShareId"],
                "FldParam": "",

                "FundIn": "003333",  # 非活期宝基金，高端理财等无法买入到组合的基金
                "SubAccountNoIn": read_yaml2()["SubAccountNo"],
                "FundCode": "003333",  # 非活期宝基金，高端理财等无法买入到组合的基金
                "FundOut": read_yaml3()["FundCode"],
                "FundAmount": read_yaml3()["FundAmount_CJZH"],
                "LargeRedemptionFlag": "1",
                "TraceID": read_yaml3()["TraceID"],

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
                    with allure.step('组合内基金转换是否成功'):
                        if ErrorCode == 0:
                            assert True, '申请受理成功'
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
            pytest.skip(), '由于没有HH基金份额，份额不足，资金池超限等原因无法发起超级转换'
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
                    with allure.step('超级转换撤单是否成功'):
                        if ErrorCode == 0:
                            assert True, '撤单受理成功'
                        else:
                            assert False, ErrorMessage
                else:
                    assert False, '接口状态码非200'

import os
import time
from urllib.parse import urljoin

import pytest
import requests
import allure

from conftest import read_yaml2, write_yaml2, write_yaml3, read_yaml3, clear_yaml3, read_yaml1, read_yaml4


@allure.feature('组合内基金超级转换 815')
class Test_CJZH_Sub():
    @allure.story('子账户持仓 /User/Asset/GetFundAssetListOfSubV2')
    # 获取子账户持仓 QD型
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
        Res = res.json()["Data"]["AssetDetails"]
        with allure.step('组合里是否有HH基金'):
            if Res == []:
                clear_yaml3()
                assert False, '组合内没有HH基金'
            else:
                assert True
                AssetValue = res.json()["Data"]["AssetDetails"][0]["AssetValue"]
                with allure.step('HH基金是否有足够份额'):
                    if AssetValue > '15':
                        assert True
                        FundCode = res.json()["Data"]["AssetDetails"][0]["FundCode"]
                        clear_yaml3()
                        write_yaml3({"FundCode": FundCode})
                    else:
                        clear_yaml3()
                        assert False, '份额不足无法发起'

    @allure.story('持仓详情（组合） /User/home/GetShareDetail')
    # 获取特定基金的组合份额
    def test_User_home_GetShareDetail(self):
        if read_yaml3() is None:
            pytest.skip(), '没有HH基金份额或者份额不足无法发起超级转换'
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
                else:
                    assert False, '接口状态码非200'
            for i in range(3):
                if res.json()["Data"]["Shares"][i - 1]["AvailableShare"] > 14:
                    AvailableShare = res.json()["Data"]["Shares"][i - 1]["AvailableShare"]
                    ShareId = res.json()["Data"]["Shares"][i - 1]["ShareId"]
                    write_yaml3({"ShareId": ShareId})
                    write_yaml3({"AvailableShare": AvailableShare})
                    break

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
            TraceID = res.json()["Data"]["TraceID"]
            write_yaml3({"TraceID": TraceID})

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

                "FundIn": "000001",  # 非活期宝基金，高端理财等无法买入到组合的基金
                "SubAccountNoIn": read_yaml2()["SubAccountNo"],
                "FundCode": "000001",  # 非活期宝基金，高端理财等无法买入到组合的基金
                "FundOut": read_yaml3()["FundCode"],
                "FundAmount": read_yaml4()["FundAmount_CJZH"],
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
            ErrorCode = res.json()["ErrorCode"]
            ErrorMessage = res.json()["ErrorMessage"]
            with allure.step('接口是否正常调通'):
                if res.status_code == 200:
                    assert True
                else:
                    assert False, '接口状态码非200'
            with allure.step('组合内基金转换是否成功'):
                if ErrorCode == 0:
                    assert True, '申请受理成功'
                else:
                    assert False, ErrorMessage

    @allure.story('交易留痕2 890免密 /Business/home/NoticeStayTrace')
    # 交易留痕2
    def test_Business_home_NoticeStayTrace2(self):
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
            TraceID2 = res.json()["Data"]["TraceID"]
            write_yaml3({"TraceID2": TraceID2})

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

                "FundIn": "000001",  # 非活期宝基金，高端理财等无法买入到组合的基金
                "SubAccountNoIn": read_yaml2()["SubAccountNo"],
                "FundCode": "000001",  # 非活期宝基金，高端理财等无法买入到组合的基金
                "FundOut": read_yaml3()["FundCode"],
                "FundAmount": read_yaml4()["FundAmount_CJZH"],
                "LargeRedemptionFlag": "1",
                "TraceID": read_yaml3()["TraceID2"],  # 890放一个类，TraceID会有两个

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
            with allure.step('组合内基金转换是否成功'):
                if ErrorCode == 0:
                    assert True, '申请受理成功'
                else:
                    assert False, ErrorMessage

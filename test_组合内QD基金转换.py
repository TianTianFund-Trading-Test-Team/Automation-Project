import os
import time
from urllib.parse import urljoin

import pytest
import requests
import allure

from conftest import read_yaml2, write_yaml2, write_yaml3, read_yaml3, clear_yaml3, read_yaml1, read_yaml4


@allure.feature('组合内QD基金普通卖出 890')
class Test_redeem_QDFund_Sub():
    @allure.story('子账户持仓 /User/Asset/GetFundAssetListOfSubV2')
    # 获取子账户持仓 QD型
    def test_User_Asset_GetFundAssetListOfSubV2(self):
        clear_yaml3()
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/Asset/GetFundAssetListOfSubV2")
        datas = {
            "UserId": read_yaml2()["CustomerNo"],
            "SubAccountNo": read_yaml2()["SubAccountNo"],
            "UnifiedType": "QD",  # 筛选类型： HH 混合； ZS 指数； GP 股票； ZQ 债券； QD QD基金； HB 货币基金
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
        with allure.step('组合里是否有QD基金'):
            if Res == []:
                clear_yaml3()
                assert False, '组合内没有QD基金'
            else:
                assert True
                AssetValue = res.json()["Data"]["AssetDetails"][0]["AssetValue"]
                with allure.step('QD基金是否有足够份额'):
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
            pytest.skip(), '没有QD基金份额或者份额不足无法发起890'
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
            with allure.step('是否存在份额可以QD转换'):  # 因为多卡才做的逻辑。这个接口没有排序也没有字段返回份额数量
                for i in range(5):
                    try:
                        if res.json()["Data"]["Shares"][i - 1]["AvailableShare"] > 14:
                            AvailableShare = res.json()["Data"]["Shares"][i - 1]["AvailableShare"]
                            ShareId = res.json()["Data"]["Shares"][i - 1]["ShareId"]
                            write_yaml3({"ShareId": ShareId})
                            write_yaml3({"AvailableShare": AvailableShare})
                            break
                    except IndexError:
                        pass

                if read_yaml3() == {'FundCode': read_yaml3()["FundCode"]}:
                    clear_yaml3()
                    assert False, '没有足够的QD基金份额做890'

    @allure.story('交易留痕 /Business/home/NoticeStayTrace')
    # 交易留痕
    def test_Business_home_NoticeStayTrace(self):
        if read_yaml3() is None:
            pytest.skip(), '没有QD基金份额或者份额不足无法发起890'
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

    @allure.story('组合内QD基金转换 /Business/Home/SFT1Transfer')
    # 组合内QD基金转换
    def test_Business_Home_SFT1Transfer(self):
        if read_yaml3() is None:
            pytest.skip(), '没有QD基金份额或者份额不足无法发起890'
        else:
            url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/Business/Home/SFT1Transfer")
            datas = {
                "Pwd": read_yaml1()[read_yaml4()["Pas"]],
                "UserId": read_yaml2()["CustomerNo"],
                "ShareID": read_yaml3()["ShareId"],
                "FldParam": "",

                "FundIn": "000001",  # 非活期宝基金，高端理财等无法买入到组合的基金
                "SubAccountNoIn": "",
                "FundCode": "000001",  # 非活期宝基金，高端理财等无法买入到组合的基金
                "FundOut": read_yaml3()["FundCode"],
                "FundAmount": read_yaml4()["FundAmount_CJZH"],
                "LargeRedemptionFlag": "1",
                "TraceID": read_yaml3()["TraceID"],
                "FromSubAccountNo": read_yaml2()["SubAccountNo"],
                "ToSubAccountNo": read_yaml2()["SubAccountNo"],

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
            with allure.step('组合内QD基金转换是否成功'):
                if ErrorCode == 0:
                    assert True, '申请受理成功'
                else:
                    assert False, ErrorMessage

    @allure.story('交易留痕2 890免密 /Business/home/NoticeStayTrace')
    # 交易留痕2
    def test_Business_home_NoticeStayTrace2(self):
        if read_yaml3() is None:
            pytest.skip(), '没有QD基金份额或者份额不足无法发起890'
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

    @allure.story('组合内QD基金转换 免密 /Business/Home/SFT1TransferNP')
    # 组合内QD基金转换 免密
    def test_Business_Home_SFT1TransferNP(self):
        if read_yaml3() is None:
            pytest.skip(), '没有QD基金份额或者份额不足无法发起890'
        else:
            time.sleep(3)
            url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/Business/Home/SFT1TransferNP")
            datas = {
                "UserId": read_yaml2()["CustomerNo"],
                "ShareID": read_yaml3()["ShareId"],
                "FldParam": "",

                "FundIn": "000001",  # 非活期宝基金，高端理财等无法买入到组合的基金
                "SubAccountNoIn": "",
                "FundCode": "000001",  # 非活期宝基金，高端理财等无法买入到组合的基金
                "FundOut": read_yaml3()["FundCode"],
                "FundAmount": read_yaml4()["FundAmount_CJZH"],
                "LargeRedemptionFlag": "1",
                "TraceID": read_yaml3()["TraceID2"],  # 890放一个类，TraceID会有两个
                "FromSubAccountNo": read_yaml2()["SubAccountNo"],
                "ToSubAccountNo": read_yaml2()["SubAccountNo"],

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
            with allure.step('组合内QD基金转换是否成功'):
                if ErrorCode == 0:
                    assert True, '申请受理成功'
                else:
                    assert False, ErrorMessage

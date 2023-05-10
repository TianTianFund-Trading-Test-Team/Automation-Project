
from urllib.parse import urljoin
import requests
import allure

from conftest import read_yaml2, write_yaml2, write_yaml3, read_yaml3, clear_yaml3, read_yaml1, read_yaml4


@allure.feature('买基金到组合 汇款支付 660以下')
class Test_UnifiedBuy_fund_to_Sub():
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

    @allure.story('买基金到组合 汇款支付 /Business/Home/UnifiedBuyFund')
    # 买基金到组合 660以下免密
    def test_Business_Home_UnifiedBuyFund(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/Business/Home/UnifiedBuyFund")
        datas = {
            "Password": read_yaml1()[read_yaml4()["Pas"]],
            "IsPayPlus": "0",
            "CouponsType": "",
            "CouponsId": "",
            "CustomerNo": read_yaml2()["CustomerNo"],
            "UserId": read_yaml2()["CustomerNo"],
            "BankAccountNo": read_yaml2()["BankAccountNo"],
            "FundCode": "000001",
            "Amount": 1000.00,
            "AmountList": "",
            "ChargeType": "",
            "PayWay": "bank",
            "TraceID": read_yaml3()["TraceID"],
            "RecommanderNo": "",
            "SubAccountNo": read_yaml2()["SubAccountNo"],
            "FollowingSubAccountNo": "",
            "IsSubAPlanB": "false",
            "Remittance": "true",
            "FldParam": "",
            "RatioRefundType": "",

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
                with allure.step('买基金到组合汇款支付请求成功'):
                    if ErrorCode == 0:
                        assert True
                    else:
                        clear_yaml3()
                        assert False, ErrorMessage
            else:
                assert False, '接口状态码非200'

@allure.feature('买基金到组合 汇款支付 660以下 免密')
class Test_UnifiedBuy_fund_to_Sub():
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

    @allure.story('买基金到组合 汇款支付 免密 /Business/Home/UnifiedBuyFundNP')
    # 买基金到组合 660以下免密
    def test_Business_Home_UnifiedBuyFundNP(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/Business/Home/UnifiedBuyFundNP")
        datas = {
            "IsPayPlus": "0",
            "CouponsType": "",
            "CouponsId": "",
            "CustomerNo": read_yaml2()["CustomerNo"],
            "UserId": read_yaml2()["CustomerNo"],
            "BankAccountNo": read_yaml2()["BankAccountNo"],
            "FundCode": "000001",
            "Amount": 1000.00,
            "AmountList": "",
            "ChargeType": "",
            "PayWay": "bank",
            "TraceID": read_yaml3()["TraceID"],
            "RecommanderNo": "",
            "SubAccountNo": read_yaml2()["SubAccountNo"],
            "FollowingSubAccountNo": "",
            "IsSubAPlanB": "false",
            "Remittance": "true",
            "FldParam": "",
            "RatioRefundType": "",

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
                with allure.step('买基金到组合汇款支付请求成功'):
                    if ErrorCode == 0:
                        assert True
                    else:
                        clear_yaml3()
                        assert False, ErrorMessage
            else:
                assert False, '接口状态码非200'

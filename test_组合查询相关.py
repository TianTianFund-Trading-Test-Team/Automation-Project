import os
import time
from urllib.parse import urljoin

import pytest
import requests
import allure

from conftest import read_yaml2, write_yaml2, write_yaml3, read_yaml3, clear_yaml3, read_yaml1, read_yaml4


@allure.feature('组合详情')
class Test_SubAccount_details():
    @allure.story('组合详情页V2 /User/SubA/SubAGradingIndexDetailV2')
    # 组合详情页V2（最新版）
    def test_User_SubA_SubAGradingIndexDetailV2(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubA/SubAGradingIndexDetailV2")
        datas = {
            "UserId": read_yaml2()["CustomerNo"],
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
            else:
                assert False, '接口状态码非200'

    @allure.story('组合详情页 旧版调用 /User/SubA/SubAGradingIndexDetail')
    # 组合详情页（旧版）
    def test_User_SubA_SubAGradingIndexDetail(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubA/SubAGradingIndexDetail")
        datas = {
            "UserId": read_yaml2()["CustomerNo"],
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
            else:
                assert False, '接口状态码非200'

    @allure.story('组合详情页 旧版调用 /User/SubAccount/GetSubAccountGradingIndex')
    # 组合详情页（最旧版）
    def test_User_SubAccount_GetSubAccountGradingIndex(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubAccount/GetSubAccountGradingIndex")
        datas = {
            "UserId": "",
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
            else:
                assert False, '接口状态码非200'


@allure.feature('组合日收益')
class Test_SubAccount_DailyProfit():
    @allure.story('组合日收益  /User/SubA/SubADailyProfit')
    # 组合日收益
    def test_User_SubA_SubADailyProfit(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubA/SubADailyProfit")
        datas = {
            "UserId": read_yaml2()["CustomerNo"],
            "SubAccountNo": read_yaml2()["SubAccountNo"],
            "PageNum": 1,
            "PageCount": 30,

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

    @allure.story('组合日收益 旧版  /User/SubAccount/GetDailyProfit')
    # 组合日收益 旧版
    def test_User_SubAccount_GetDailyProfit(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubAccount/GetDailyProfit")
        datas = {
            "UserId": read_yaml2()["CustomerNo"],
            "SubAccountNo": read_yaml2()["SubAccountNo"],
            "PageNum": 1,
            "PageCount": 30,

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


@allure.feature('组合月度相关接口')
class Test_SubAccount_MonthlyProfit():
    @allure.story('组合月收益 /User/SubA/SubAMonthlyProfit')
    # 组合月收益
    def test_User_SubA_SubAMonthlyProfit(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubA/SubAMonthlyProfit")
        datas = {
            "UserId": read_yaml2()["CustomerNo"],
            "SubAccountNo": read_yaml2()["SubAccountNo"],
            "StartTime": "2021-10-15",
            "EndTime": "2023-03-15",

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

    @allure.story('组合月度分析 /User/SubA/SubAMonthlyAnalysis')
    # 组合月度分析
    def test_User_SubA_SubAMonthlyAnalysis(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubA/SubAMonthlyAnalysis")
        datas = {
            "UserId": read_yaml2()["CustomerNo"],
            "SubAccountNo": read_yaml2()["SubAccountNo"],
            "StartTime": "2021-10-15",
            "EndTime": "2023-03-15",

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

    @allure.story('组合自然月度收益 /User/SubA/SubNaturalMonthProfit')
    # 组合自然月度收益
    def test_User_SubA_SubNaturalMonthProfit(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubA/SubNaturalMonthProfit")
        datas = {
            "UserId": read_yaml2()["CustomerNo"],
            "SubAccountNo": read_yaml2()["SubAccountNo"],
            "ProfitYear": "2023",
            "ProfitMonth": "2023-03",

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

    @allure.story('组合月度收益 旧版 /User/SubAccount/GetMonthlyAnalysis')
    # 组合月度收益 旧版
    def test_User_SubAccount_GetMonthlyAnalysis(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubAccount/GetMonthlyAnalysis")
        datas = {
            "UserId": read_yaml2()["CustomerNo"],
            "SubAccountNo": read_yaml2()["SubAccountNo"],
            "StartTime": "2021-08-15",
            "EndTime": "2023-03-15",

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


@allure.feature('组合评分和基本信息')
class Test_SubAccount_SubAScoreInfo():
    @allure.story('组合评分和基本信息 /User/SubA/SubAScoreInfo')
    # 组合区间指标
    def test_User_SubA_SubAScoreInfo(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubA/SubAScoreInfo")
        datas = {
            "UserId": read_yaml2()["CustomerNo"],
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
            else:
                assert False, '接口状态码非200'

    @allure.story('组合评分和基本信息 旧版 /User/SubAccount/GetSubAccountScoreInfo')
    # 组合区间指标 旧版
    def test_User_SubAccount_GetSubAccountScoreInfo(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubAccount/GetSubAccountScoreInfo")
        datas = {
            "UserId": read_yaml2()["CustomerNo"],
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
            else:
                assert False, '接口状态码非200'

    @allure.story('获取区间收益 旧版 /User/SubAccount/GetIntervalProfit')
    # 组合区间指标 旧版
    def test_User_SubAccount_GetIntervalProfit(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubAccount/GetIntervalProfit")
        datas = {
            "UserId": read_yaml2()["CustomerNo"],
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
            else:
                assert False, '接口状态码非200'


@allure.feature('组合持仓占比')
class Test_SubAccount_SubAScoreInfo():
    @allure.story('组合持仓占比 /User/SubA/SubAPositionV2')
    # 组合持仓占比
    def test_User_SubA_SubAPositionV2(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubA/SubAPositionV2")
        datas = {
            "UserId": read_yaml2()["CustomerNo"],
            "SubAccountNo": read_yaml2()["SubAccountNo"],
            "SearchDate": "2023-03-15",

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

    @allure.story('组合持仓占比 旧版 /User/SubA/SubAPosition')
    # 组合持仓占比 旧版
    def test_User_SubA_SubAPosition(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubA/SubAPosition")
        datas = {
            "UserId": read_yaml2()["CustomerNo"],
            "SubAccountNo": read_yaml2()["SubAccountNo"],
            "SearchDate": "2023-03-15",
            "ProportionType": 0,

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

    @allure.story('组合持仓占比 最旧版 /User/SubAccount/GetPositioningData')
    # 组合持仓占比 最旧版
    def test_User_SubAccount_GetPositioningData(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubAccount/GetPositioningData")
        datas = {
            "UserId": read_yaml2()["CustomerNo"],
            "SubAccountNo": read_yaml2()["SubAccountNo"],
            "SearchDate": "2023-03-15",
            "ProportionType": 0,

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


@allure.feature('组合估值')
class Test_SubAccount_SubAValuationProfit():
    @allure.story('组合估值 /User/SubA/SubAValuationProfit')
    # 组合估值
    def test_User_SubA_SubAValuationProfit(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubA/SubAValuationProfit")
        datas = {
            "UserId": read_yaml2()["CustomerNo"],
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
            else:
                assert False, '接口状态码非200'

    @allure.story('组合估值 旧版 /User/SubAccount/GetValuationIntervalProfit')
    # 组合估值
    def test_User_SubAccount_GetValuationIntervalProfit(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubAccount/GetValuationIntervalProfit")
        datas = {
            "UserId": read_yaml2()["CustomerNo"],
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
            else:
                assert False, '接口状态码非200'


@allure.feature('其余组合相关接口')
class Test_SubAccount_SubAValuationProfit():
    @allure.story('组合历史净值 /User/SubA/SubAProfit')
    # 组合估值
    def test_User_SubA_SubAProfit(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubA/SubAProfit")
        datas = {
            "UserId": read_yaml2()["CustomerNo"],
            "SubAccountNo": read_yaml2()["SubAccountNo"],
            "IntervalType": 9,  # 0 累计收益； 1 单位净值
            "DataType": 1,

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

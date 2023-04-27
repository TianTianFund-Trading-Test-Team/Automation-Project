import os
import time
from urllib.parse import urljoin

import pytest
import requests
import allure

from conftest import read_yaml2, write_yaml2, write_yaml3, read_yaml3, clear_yaml3, read_yaml1, read_yaml4


@allure.feature('组合转入转出 ')
class Test_TransferShare_Sub():
    @allure.story('组合转入基金列表 /User/SubA/SubASummary')
    # 组合转入基金列表
    def test_User_SubA_SubASummary(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubA/SubASummary")
        datas = {
            "UserId": read_yaml2()["CustomerNo"],
            "SubType": "-1",

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
                with allure.step('接口是否返回正常'):
                    ErrorCode = res.json()["ErrorCode"]
                    ErrorMessage = res.json()["ErrorMessage"]
                    if ErrorCode == 0:
                        assert True
                        ShareId = res.json()["Data"]["SubAccounts"][0]["Details"][0]["ShareId"]
                        clear_yaml3()
                        write_yaml3({"ShareId": ShareId})
                    else:
                        clear_yaml3()
                        assert False, ErrorMessage
            else:
                assert False, '接口状态码非200'

    @allure.story('组合转入基金列表 /User/SubA/SubATransferShare')
    # 组合转入基金列表
    def test_User_SubA_SubATransferShare(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubA/SubATransferShare")
        datas = {
            "PassWord": read_yaml1()[read_yaml4()["Pas"]],
            "UserId": read_yaml2()["CustomerNo"],
            "Shares": read_yaml3()["ShareId"],
            "Vols": read_yaml4()["Vols"],
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
                with allure.step('组合转入转出是否成功'):
                    if ErrorCode == 0:
                        assert True, '申请受理成功'
                    else:
                        assert False, ErrorMessage
            else:
                assert False, '接口状态码非200'

    @allure.story('组合853在途列表 /api/mobile/Query/GetOnWayQueryInfosQuickUse')
    # 交易查询 组合卖出在途可撤单列表
    def test_api_mobile_Query_GetOnWayQueryInfosQuickUse(self):
        if read_yaml3() is None:
            pytest.skip(), "组合转入转出未成功"
        else:
            time.sleep(2)  # 撤单后接着查询，中间有延迟
            url = urljoin(read_yaml1()[read_yaml4()["Env_Tquery"]], "/api/mobile/Query/GetOnWayQueryInfosQuickUse")
            datas = {
                "utoken": read_yaml2()["UToken"],
                "uid": read_yaml2()["CustomerNo"],
                "mobileKey": "01F12605-0E93-4BCB-AD67-D46C1DDA604B",
                "customerNo": read_yaml2()["CustomerNo"],
                "deviceid": "01F12605-0E93-4BCB-AD67-D46C1DDA604B",
                "ctoken": read_yaml2()["CToken"],
                "serverversion": "6.5.8",
                "rtype": "app",
                "data": "{{\"PageIndex\": 1, \"PageSize\": 20, \"FundCode\": \"\", \"DateType\": \"1\", "
                        "\"BusType\":\"0\",\"Statu\":\"1\",  \"SubAccountNo\": \"{}\", \"CustomerNo\": \"{}\" "
                        "}}".format(
                    read_yaml2()["SubAccountNo"], read_yaml2()["CustomerNo"])
            }
            res = requests.request(method='post', url=url, json=datas)
            print(res.json())
            with allure.step('接口是否正常调通'):
                if res.status_code == 200:
                    assert True
                    ErrorCode = res.json()["ErrorCode"]
                    ErrorMessage = res.json()["ErrorMessage"]
                    with allure.step('交易查询是否正常'):
                        if ErrorCode is None:
                            assert True

                            BusinSerialNo = res.json()["responseObjects"][0]["OnWayLst"][0]["ID"]
                            BusinessType = res.json()["responseObjects"][0]["OnWayLst"][0]["BusinessCode"]
                            clear_yaml3()
                            write_yaml3({"BusinSerialNo": BusinSerialNo})
                            write_yaml3({"BusinessType": BusinessType})
                        else:
                            clear_yaml3()
                            assert False, ErrorMessage
                else:
                    assert False, "接口状态非200"

    @allure.story('组合转入撤单 /Trade/FundTrade/RevokeOrder')
    # 组合转入撤单
    def test_Trade_FundTrade_RevokeOrder(self):
        if read_yaml3() is None:
            pytest.skip(), '组合转入未成功'
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
                    with allure.step('组合转入撤单是否成功'):
                        if ErrorCode == 0:
                            assert True, '撤单受理成功'
                        else:
                            assert False, ErrorMessage
                else:
                    assert False, '接口状态码非200'


@allure.feature('组合转入转出 免密 ')
class Test_TransferShare_Sub_NP():
    @allure.story('组合转入基金列表 /User/SubA/SubASummary')
    # 组合转入基金列表
    def test_User_SubA_SubASummary(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubA/SubASummary")
        datas = {
            "UserId": read_yaml2()["CustomerNo"],
            "SubType": "-1",

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
                with allure.step('接口是否返回正常'):
                    ErrorCode = res.json()["ErrorCode"]
                    ErrorMessage = res.json()["ErrorMessage"]
                    if ErrorCode == 0:
                        assert True
                        ShareId = res.json()["Data"]["SubAccounts"][0]["Details"][0]["ShareId"]
                        clear_yaml3()
                        write_yaml3({"ShareId": ShareId})
                    else:
                        clear_yaml3()
                        assert False, ErrorMessage
            else:
                assert False, '接口状态码非200'

    @allure.story('组合转入 免密 /User/SubA/SubATransferShareNP')
    # 组合转入
    def test_User_SubA_SubATransferShareNP(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubA/SubATransferShareNP")
        datas = {
            "PassWord": read_yaml1()[read_yaml4()["Pas"]],
            "UserId": read_yaml2()["CustomerNo"],
            "Shares": read_yaml3()["ShareId"],
            "Vols": read_yaml4()["Vols"],
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
                with allure.step('组合转入转出是否成功'):
                    if ErrorCode == 0:
                        assert True, '申请受理成功'
                    else:
                        assert False, ErrorMessage
            else:
                assert False, '接口状态码非200'

    @allure.story('组合853在途列表 /api/mobile/Query/GetOnWayQueryInfosQuickUse')
    # 交易查询 组合卖出在途可撤单列表
    def test_api_mobile_Query_GetOnWayQueryInfosQuickUse(self):
        if read_yaml3() is None:
            pytest.skip(), "组合转入转出未成功"
        else:
            time.sleep(2)  # 撤单后接着查询，中间有延迟
            url = urljoin(read_yaml1()[read_yaml4()["Env_Tquery"]], "/api/mobile/Query/GetOnWayQueryInfosQuickUse")
            datas = {
                "utoken": read_yaml2()["UToken"],
                "uid": read_yaml2()["CustomerNo"],
                "mobileKey": "01F12605-0E93-4BCB-AD67-D46C1DDA604B",
                "customerNo": read_yaml2()["CustomerNo"],
                "deviceid": "01F12605-0E93-4BCB-AD67-D46C1DDA604B",
                "ctoken": read_yaml2()["CToken"],
                "serverversion": "6.5.8",
                "rtype": "app",
                "data": "{{\"PageIndex\": 1, \"PageSize\": 20, \"FundCode\": \"\", \"DateType\": \"1\", "
                        "\"BusType\":\"0\",\"Statu\":\"1\",  \"SubAccountNo\": \"{}\", \"CustomerNo\": \"{}\" "
                        "}}".format(
                    read_yaml2()["SubAccountNo"], read_yaml2()["CustomerNo"])
            }
            res = requests.request(method='post', url=url, json=datas)
            print(res.json())
            with allure.step('接口是否正常调通'):
                if res.status_code == 200:
                    assert True
                    ErrorCode = res.json()["ErrorCode"]
                    ErrorMessage = res.json()["ErrorMessage"]
                    with allure.step('交易查询是否正常'):
                        if ErrorCode is None:
                            assert True

                            BusinSerialNo = res.json()["responseObjects"][0]["OnWayLst"][0]["ID"]
                            BusinessType = res.json()["responseObjects"][0]["OnWayLst"][0]["BusinessCode"]
                            clear_yaml3()
                            write_yaml3({"BusinSerialNo": BusinSerialNo})
                            write_yaml3({"BusinessType": BusinessType})
                        else:
                            clear_yaml3()
                            assert False, ErrorMessage
                else:
                    assert False, "接口状态非200"

    @allure.story('组合转入撤单 免密 /Trade/FundTrade/RevokeOrderNP')
    # 组合转入撤单
    def test_Trade_FundTrade_RevokeOrderNP(self):
        if read_yaml3() is None:
            pytest.skip(), '组合转入未成功'
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
                    with allure.step('组合转入撤单是否成功'):
                        if ErrorCode == 0:
                            assert True, '撤单受理成功'
                        else:
                            assert False, ErrorMessage
                else:
                    assert False, '接口状态码非200'

import time
from urllib.parse import urljoin

import pytest
import requests
import allure

from conftest import read_yaml2, write_yaml2, write_yaml3, read_yaml3, clear_yaml3, read_yaml1, read_yaml4, read_yaml5, \
    clear_yaml5, write_yaml5
from get_num6pwd import get_L2Password

# 全局变量
g_key = 0
a_key = 0
b_key = 0
c_key = 0


# 遍历QD基金 890 使用
def modify_g_key():
    global g_key
    try:
        if g_key < read_yaml5()["Count"] - 1:
            g_key = g_key + 1
        else:
            assert False, '组合内基金均不支持QD基金转换'
    except KeyError:
        assert False, '组合内没有QD基金'


# 遍历混合基金 24 使用
def modify_a_key():
    global a_key
    if a_key < read_yaml5()["Count"] - 1:
        a_key = a_key + 1
    else:
        assert False, '组合内基金都不满足卖出条件'


# 遍历混合基金 815 使用
def modify_b_key():
    global b_key
    try:
        if b_key < read_yaml5()["Count"] - 1:
            b_key = b_key + 1
        else:
            assert False, '组合内基金均不支持超级转换'
    except KeyError:
        assert False, '组合内没有HH基金'


# 遍历混合基金 36 使用
def modify_c_key():
    global c_key
    try:
        if c_key < read_yaml5()["Count"] - 1:
            c_key = c_key + 1
        else:
            clear_yaml3()
            assert False, '组合内基金均不支持基金转换'
    except KeyError:
        clear_yaml3()
        assert False, '组合内没有HH基金'


@allure.feature('活期宝买基金到组合 6位密码')
class Test_buy_fund_to_Sub_L2():
    @allure.story('交易留痕 /Business/home/NoticeStayTrace')
    # 交易留痕
    def test_Business_home_NoticeStayTrace(self):
        clear_yaml3()
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

    @allure.story('活期宝买基金到组合 6位密码 /Trade/FundTrade/CommitOrderL2')
    def test_Trade_FundTrade_CommitOrderL2(self):
        get_L2Password.user_Register_Secu(self)
        get_L2Password.DES_decrypto(self)
        get_L2Password.rsa_encrypto(self)
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/Trade/FundTrade/CommitOrderL2")
        datas = {
            "L2Password": read_yaml3()["L2Password"],
            "SecuId": "feefd4d8095a4dc3b31863dfb71dde3f",  # 固定的
            "EncryptStr": "",
            "TradeType": "AsyJCJY022",  # 活期宝
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
        with allure.step('接口是否正常调通'):
            if res.status_code == 200:
                assert True
                ErrorCode = res.json()["ErrorCode"]
                ErrorMessage = res.json()["ErrorMessage"]
                with allure.step('买基金到组合请求成功'):
                    if ErrorCode == 0:
                        assert True
                        AppSerialNo = res.json()["Data"]["AppSerialNo"]
                        BusinType = res.json()["Data"]["BusinType"]
                        clear_yaml3()
                        write_yaml3({"AppSerialNo": AppSerialNo})
                        write_yaml3({"BusinType": BusinType})
                    else:
                        assert False, ErrorMessage
            else:
                assert False, '接口状态码非200'

    @allure.story('买基金到组合结果页 /Trade/FundTrade/OrderResult')
    def test_Trade_FundTrade_OrderResult(self):
        if read_yaml3() is None:
            pytest.skip(), '交易密码错误'
        else:
            time.sleep(5)
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
            with allure.step('接口是否正常调通'):
                if res.status_code == 200:
                    assert True
                    ErrorCode = res.json()["ErrorCode"]
                    ErrorMessage1 = res.json()["ErrorMessage"]
                    with allure.step('买基金到组合受理结果是否正常展示'):
                        if ErrorCode == 0:
                            assert True
                            PayError = res.json()["Data"]["PayError"]
                            ErrorMessage = res.json()["Data"]["ListTips"][0]["ThirdTitle"]
                            with allure.step('买基金到组合受理结果是否成功'):
                                if PayError == '':
                                    assert True, '买基金到组合成功'
                                    write_yaml3({"Succeed": True})
                                else:
                                    write_yaml3({"Succeed": False})
                                    assert False, ErrorMessage
                        else:
                            assert False, ErrorMessage1
                else:
                    assert False, '接口状态码非200'

    @allure.story('买基金到组合撤单 /Trade/FundTrade/RevokeOrder')
    # 买基金到组合撤单
    def test_Trade_FundTrade_RevokeOrder(self):
        if read_yaml3()["Succeed"] == False or read_yaml3() is None:
            pytest.skip(), '买基金失败无法撤单或者交易密码错误'
        else:
            time.sleep(2)  # 单号落库时间慢，设个延迟防止报错
            url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/Trade/FundTrade/RevokeOrder")
            datas = {
                "Password": read_yaml1()[read_yaml4()["Pas"]],
                "UserId": read_yaml2()["CustomerNo"],
                "BusinId": read_yaml3()["AppSerialNo"],
                "BusinType": read_yaml3()["BusinType"],
                "IsRevokedToCashBag": "false",
                "DisplayBusinType": read_yaml3()["BusinType"],

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
                    with allure.step('买基金到组合撤单是否成功'):
                        if ErrorCode == 0:
                            assert True, '撤单受理成功'
                        else:
                            assert False, ErrorMessage
                else:
                    assert False, '接口状态码非200'


@allure.feature('活期宝买组合 6位密码')
class Test_buy_Sub_L2():
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

    @allure.story('买组合 /User/SubA/CommitOrderCusL2')
    # 买组合 660以下输密码
    def test_User_SubA_CommitOrderCusL2(self):
        get_L2Password.user_Register_Secu(self)
        get_L2Password.DES_decrypto(self)
        get_L2Password.rsa_encrypto(self)
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubA/CommitOrderCusL2")
        datas = {
            "L2Password": read_yaml3()["L2Password"],
            "SecuId": "feefd4d8095a4dc3b31863dfb71dde3f",  # 固定的
            "EncryptStr": "",
            "TradeType": "HQBX022-ZH",
            "UserId": read_yaml2()["CustomerNo"],
            "BankAccountNo": read_yaml2()["BankAccountNo"],
            "CouponsType": "",
            "CouponsId": "",
            "FundCode": "",
            "TotalAmounts": read_yaml4()["Amount"],
            "FundAppsJson": "",
            "TraceID": read_yaml3()["TraceID"],
            "RecommanderNo": "",
            "SubAccountNo": "",
            "FollowingSubAccountNo": read_yaml2()["SubAccountNo"],
            "IsRemittance": "false",
            "IsPayPlus": "false",
            "RatioRefundType": "",
            "TradeFlow": "default",
            "InstalledApp": "false",
            "AppScheme": "",

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
                with allure.step('买组合请求成功'):
                    if ErrorCode == 0:
                        assert True, '买组合请求成功'
                        ContextId = res.json()["Data"]["ContextId"]
                        AppSheetSerialNo = res.json()["Data"]["AppSheetSerialNo"]
                        BusinType = res.json()["Data"]["BusinType"]
                        clear_yaml3()
                        write_yaml3({"ContextId": ContextId})
                        write_yaml3({"AppSheetSerialNo": AppSheetSerialNo})
                        write_yaml3({"BusinType": BusinType})
                    else:
                        assert False, ErrorMessage
            else:
                assert False, '接口状态码非200'

    @allure.story('买组合结果页 /User/SubA/CompleteOrderCus')
    def test_User_SubA_CompleteOrderCus(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubA/CompleteOrderCus")
        datas = {
            "UserId": read_yaml2()["CustomerNo"],
            "ContextId": read_yaml3()["ContextId"],
            "VerifyCode": "",
            "BankAppPayResult": "",
            "BankCallBackContextId": "",
            "TradeFlow": "",
            "CancelPay": "false",

            "PhoneType": "IPhone",
            "ServerVersion": "6.5.8",
            "CToken": read_yaml2()["CToken"],
            "UToken": read_yaml2()["UToken"],
            "MobileKey": "01F12605-0E93-4BCB-AD67-D46C1DDA604B"
        }

        res = requests.request(method='post', url=url, params=datas)
        time.sleep(3)  # 交易结果有延迟
        with allure.step('接口是否正常调通'):
            if res.status_code == 200:
                assert True
                ErrorCode = res.json()["ErrorCode"]
                ErrorMessage1 = res.json()["ErrorMessage"]
                with allure.step('买组合受理结果是否正常展示'):
                    if ErrorCode == 0:
                        assert True
                        PayError = res.json()["Data"]["PayError"]
                        ErrorMessage = res.json()["Data"]["ListTips"][0]["ThirdTitle"]
                        with allure.step('买组合受理结果是否成功'):
                            if PayError == '':
                                assert True, '买组合成功'
                                write_yaml3({"Succeed": True})
                            else:
                                write_yaml3({"Succeed": False})
                                assert False, ErrorMessage
                    else:
                        assert False, ErrorMessage1
            else:
                assert False, '接口状态码非200'

    @allure.story('买组合撤单 /Trade/FundTrade/RevokeOrder')
    # 买组合撤单
    def test_Trade_FundTrade_RevokeOrder(self):
        if read_yaml3()["Succeed"] == False:
            pytest.skip(), '买组合失败无法撤单'
        else:
            time.sleep(2)  # 单号落库时间慢，设个延迟防止报错
            url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/Trade/FundTrade/RevokeOrder")
            datas = {
                "Password": read_yaml1()[read_yaml4()["Pas"]],
                "UserId": read_yaml2()["CustomerNo"],
                "BusinId": read_yaml3()["AppSheetSerialNo"],
                "BusinType": read_yaml3()["BusinType"],
                "IsRevokedToCashBag": "false",
                "DisplayBusinType": 8191,

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
                    with allure.step('买组合撤单是否成功'):
                        if ErrorCode == 0:
                            assert True, '撤单受理成功'
                        else:
                            assert False, ErrorMessage
                else:
                    assert False, '接口状态码非200'


@allure.feature('创建解散组合 6位密码')
class Test_Create_and_Disband_SubAccount_L2():
    @allure.story('验证名称是否正常 /user/suba/VerifyName')
    # 验证名称
    def test_User_suba_VerifyName(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/user/suba/VerifyName")
        datas = {
            "Name": read_yaml4()["Name"],

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
                        IsValid = res.json()["Data"]["IsValid"]
                        ErrorMessage = res.json()["Data"]["ErrorMessage"]
                        with allure.step('名称是否正常'):
                            if IsValid == True:
                                assert True, '名称正常'
                            else:
                                assert False, ErrorMessage
                    else:
                        clear_yaml3()
                        assert False, ErrorMessage
            else:
                assert False, '接口状态码非200'

    @allure.story('验证名称是否正常 旧版 /User/SubAccount/VerifySubAccountName')
    # 验证组合名称 旧版
    def test_User_SubAccount_VerifySubAccountName(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubAccount/VerifySubAccountName")
        datas = {
            "SubAccountName": read_yaml4()["Name"],

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
                        with allure.step('名称是否正常'):
                            IsValid = res.json()["Data"]["IsValid"]
                            ErrorMessage1 = res.json()["Data"]["ErrorMessage"]
                            if IsValid == True:
                                assert True, '名称正常'
                            else:
                                assert False, ErrorMessage1
                    else:
                        clear_yaml3()
                        assert False, ErrorMessage

            else:
                assert False, '接口状态码非200'

    @allure.story('选择投资风格 /User/SubAccount/SubAccountPropertyStyle')
    # 选择投资风格
    def test_User_SubAccount_SubAccountPropertyStyle(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubAccount/SubAccountPropertyStyle")
        datas = {

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
                    else:
                        clear_yaml3()
                        assert False, ErrorMessage
            else:
                assert False, '接口状态码非200'

    @allure.story('创建组合 /User/SubA/CreateSubA')
    # 创建组合
    def test_User_SubA_CreateSubA(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubA/CreateSubA")
        datas = {
            "UserId": read_yaml2()["CustomerNo"],
            "CustomizeProperty": '',
            "Property": "P1",  # 上个接口参数 组合标签
            "Style": "S2",  # 上个接口参数 组合类型
            "Name": read_yaml4()["Name"],

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
                with allure.step('组合是否创建成功'):
                    ErrorCode = res.json()["ErrorCode"]
                    ErrorMessage = res.json()["ErrorMessage"]
                    if ErrorCode == 0:
                        assert True, '创建组合成功'
                        subAccountNo = res.json()["Data"]["SubAccountNo"]
                        clear_yaml3()
                        write_yaml3({"subAccountNo": subAccountNo})
                    else:
                        clear_yaml3()
                        assert False, ErrorMessage
            else:
                assert False, '接口状态码非200'

    @allure.story('修改组合名称 /User/SubA/UpdateSubANP')
    # 修改组合名称
    def test_User_SubA_UpdateSubANP(self):
        if read_yaml3() is None:
            pytest.skip(), '创建组合失败，无法修改组合信息'
        else:
            url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubA/UpdateSubANP")
            datas = {
                "UserId": read_yaml2()["CustomerNo"],
                "SubAccountNo": read_yaml3()["subAccountNo"],
                "ShutDownSubAccount": "false",
                "UpdateName": "Name",
                "UpdateValue": read_yaml4()["Name_EX"],
                "PrivacyMode": "",

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
                    with allure.step('修改组合名称是否成功'):
                        if ErrorCode == 0:
                            assert True, '修改组合名称成功'
                        else:
                            assert False, ErrorMessage
                else:
                    assert False, '接口状态码非200'

    @allure.story('修改组合个性标签 /User/SubA/UpdateSubANP')
    # 修改组合个性标签
    def test_User_SubA_UpdateSubANP2(self):
        if read_yaml3() is None:
            pytest.skip(), '创建组合失败，无法修改组合信息'
        else:
            url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubA/UpdateSubANP")
            datas = {
                "UserId": read_yaml2()["CustomerNo"],
                "SubAccountNo": read_yaml3()["subAccountNo"],
                "ShutDownSubAccount": "false",
                "UpdateName": "Property",
                "UpdateValue": read_yaml4()["Property"],
                "PrivacyMode": "",

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
                    with allure.step('修改组合标签是否成功'):
                        if ErrorCode == 0:
                            assert True, '修改组合标签成功'
                        else:
                            assert False, ErrorMessage
                else:
                    assert False, '接口状态码非200'

    @allure.story('修改组合风格 /User/SubA/UpdateSubANP')
    # 修改组合风格
    def test_User_SubA_UpdateSubANP3(self):
        if read_yaml3() is None:
            pytest.skip(), '创建组合失败，无法修改组合信息'
        else:
            url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubA/UpdateSubANP")
            datas = {
                "UserId": read_yaml2()["CustomerNo"],
                "SubAccountNo": read_yaml3()["subAccountNo"],
                "ShutDownSubAccount": "false",
                "UpdateName": "Style",
                "UpdateValue": read_yaml4()["Style"],
                "PrivacyMode": "",

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
                    with allure.step('修改组合风格是否成功'):
                        if ErrorCode == 0:
                            assert True, '修改组合风格成功'
                        else:
                            assert False, ErrorMessage
                else:
                    assert False, '接口状态码非200'

    @allure.story('修改组合投资理念 /User/SubA/UpdateSubANP')
    # 修改组合投资理念
    def test_User_SubA_UpdateSubANP4(self):
        if read_yaml3() is None:
            pytest.skip(), '创建组合失败，无法修改组合信息'
        else:
            url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubA/UpdateSubANP")
            datas = {
                "UserId": read_yaml2()["CustomerNo"],
                "SubAccountNo": read_yaml3()["subAccountNo"],
                "ShutDownSubAccount": "false",
                "UpdateName": "Idea",
                "UpdateValue": read_yaml4()["Idea"],
                "PrivacyMode": "",

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
                    with allure.step('修改组合投资理念是否成功'):
                        if ErrorCode == 0:
                            assert True, '修改组合投资理念成功'
                        else:
                            assert False, ErrorMessage
                else:
                    assert False, '接口状态码非200'

    @allure.story('解散组合 6位密码 /User/SubA/DisbandSubAL2')
    # 解散组合
    def test_User_SubA_DisbandSubAL2(self):
        if read_yaml3() is None:
            pytest.skip(), '创建组合失败，无法解散组合'
        else:
            get_L2Password.user_Register_Secu(self)
            get_L2Password.DES_decrypto(self)
            get_L2Password.rsa_encrypto(self)
            url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubA/DisbandSubAL2")
            datas = {
                "UserId": read_yaml2()["CustomerNo"],
                "SubAccountNo": read_yaml3()["subAccountNo"],
                "L2Password": read_yaml3()["L2Password"],
                "SecuId": "feefd4d8095a4dc3b31863dfb71dde3f",  # 固定的
                "EncryptStr": "",

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
                    with allure.step('组合是否解散成功'):
                        if ErrorCode == 0:
                            assert True, '解散组合成功'
                            clear_yaml3()
                        else:
                            assert False, ErrorMessage
                else:
                    assert False, '接口状态码非200'


@allure.feature('组合内QD基金 890  6位密码')
class Test_redeem_QDFund_Sub_L2():
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
                with allure.step('接口返回是否正常'):
                    ErrorCode = res.json()["ErrorCode"]
                    ErrorMessage = res.json()["ErrorMessage"]
                    with allure.step('组合内基金转换是否成功'):
                        if ErrorCode == 0:
                            assert True
                            clear_yaml5()
                            MinSg = res.json()["Data"]["MinSg"]
                            write_yaml5({"MinSg": MinSg})  # 拿003333最小申购金额
                        else:
                            clear_yaml3()
                            assert False, ErrorMessage
            else:
                assert False, '接口状态码非200'

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
                with allure.step('接口返回是否正常'):
                    ErrorCode = res.json()["ErrorCode"]
                    ErrorMessage = res.json()["ErrorMessage"]
                    with allure.step('组合内基金转换是否成功'):
                        if ErrorCode == 0:
                            assert True
                            Res = res.json()["Data"]["AssetDetails"]
                            with allure.step('组合里是否有QD基金'):
                                if Res == []:
                                    clear_yaml3()
                                    assert False, '组合内没有QD基金'
                                else:
                                    assert True
                                    Count = res.json()["Data"]["AssetCounts"]["QD"]
                                    FundCode = res.json()["Data"]["AssetDetails"][g_key]["FundCode"]
                                    clear_yaml3()
                                    write_yaml3({"FundCode": FundCode})
                                    write_yaml5({"Count": Count})
                        else:
                            clear_yaml3()
                            assert False, ErrorMessage
            else:
                assert False, '接口状态码非200'

    @allure.story('持仓详情 /User/home/GetShareDetail')
    # 获取特定基金的所有份额
    def test_User_home_GetShareDetail_all(self):
        if read_yaml3() is None:
            pytest.skip(), '没有HH基金份额无法发起超级转换'
        else:
            url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/home/GetShareDetail")
            datas = {
                "UserId": read_yaml2()["CustomerNo"],
                "SubAccountNo": "",
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
                    with allure.step('接口返回是否正常'):
                        ErrorCode = res.json()["ErrorCode"]
                        ErrorMessage = res.json()["ErrorMessage"]
                        with allure.step('组合内基金转换是否成功'):
                            if ErrorCode == 0:
                                assert True
                                AvailableShare_all = res.json()["Data"]["AvailableShare"]
                                write_yaml3({"AvailableShare_all": AvailableShare_all})
                            else:
                                assert False, ErrorMessage
                else:
                    clear_yaml3()
                    assert False, '接口状态码非200'

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
                    with allure.step('接口返回是否正常'):
                        ErrorCode = res.json()["ErrorCode"]
                        ErrorMessage = res.json()["ErrorMessage"]
                        with allure.step('组合内基金转换是否成功'):
                            if ErrorCode == 0:
                                assert True
                                Enable890 = res.json()["Data"]["Enable890"]
                                if Enable890 == True:
                                    FundNav = res.json()["Data"]["FundNav"]
                                    MinSh = res.json()["Data"]["MinSh"]
                                    for i in range(5):  # 因为多卡才做的逻辑。这个接口没有排序也没有字段返回份额数量
                                        try:
                                            if res.json()["Data"]["Shares"][i - 1]["AvailableShare"] > (
                                                    read_yaml5()["MinSg"] / FundNav) / 0.9 and \
                                                    res.json()["Data"]["Shares"][i - 1]["AvailableShare"] >= MinSh:
                                                BankCardNo = res.json()["Data"]["Shares"][i - 1]["BankCardNo"]
                                                BankAccountNo = res.json()["Data"]["Shares"][i - 1]["BankAccountNo"]
                                                ShareId = res.json()["Data"]["Shares"][i - 1]["ShareId"]
                                                AvailableShare = res.json()["Data"]["Shares"][i - 1]["AvailableShare"]
                                                write_yaml3({"BankCardNo": BankCardNo})
                                                write_yaml3({"BankAccountNo": BankAccountNo})
                                                write_yaml3({"ShareId": ShareId})
                                                write_yaml3({"AvailableShare": AvailableShare})
                                                break
                                        except IndexError:
                                            clear_yaml3()
                                            pass
                                    try:
                                        if read_yaml3() == {'FundCode': read_yaml3()["FundCode"]}:
                                            clear_yaml3()
                                            '该基金没有份额可以做QD转换'
                                    except TypeError:
                                        clear_yaml3()
                                        pass
                                else:
                                    clear_yaml3()
                                    '该基金不支持QD转换'
                            else:
                                clear_yaml3()
                                assert False, ErrorMessage
                else:
                    assert False, '接口状态码非200'

    @allure.story('转换详情（组合） /Trade/FundTrade/TransferOverview')
    # 获取转换的最小转出
    def test_Trade_FundTrade_TransferOverview(self):
        if read_yaml3() is None:
            modify_g_key()
            self.test_User_home_GetShareDetail_003333()
            self.test_User_Asset_GetFundAssetListOfSubV2()
            self.test_User_home_GetShareDetail_all()
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
                    with allure.step('接口返回是否正常'):
                        ErrorCode = res.json()["ErrorCode"]
                        ErrorMessage = res.json()["ErrorMessage"]
                        with allure.step('组合内基金转换是否成功'):
                            if ErrorCode == 0:
                                assert True
                                FundNav = res.json()["Data"]["TranOutFund"]["FundNav"]
                                MinRedeem = res.json()["Data"]["TranOutFund"]["MinRedeem"]
                                MinHoldShares = res.json()["Data"]["TranOutFund"]["MinHoldShares"]
                                AvailableVol = read_yaml3()["AvailableShare_all"]
                                FundAmount_CJZH = round((read_yaml5()["MinSg"] / FundNav) / 0.9, 2) + 0.01
                                if MinRedeem < FundAmount_CJZH:
                                    if AvailableVol - FundAmount_CJZH > MinHoldShares:
                                        write_yaml3({"FundAmount_CJZH": FundAmount_CJZH})
                                    else:
                                        clear_yaml3(), '当前基金多卡持有，当前卡全部赎回时，剩余份额不满足最小保留，请先进行份额合并。'
                                else:
                                    if AvailableVol - MinRedeem > MinHoldShares:
                                        write_yaml3({"FundAmount_CJZH": MinRedeem})
                                    else:
                                        clear_yaml3(), '当前基金多卡持有，当前卡全部赎回时，剩余份额不满足最小保留，请先进行份额合并。'
                            else:
                                assert False, ErrorMessage
                else:
                    assert False, '接口状态码非200'

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
            with allure.step('接口是否正常调通'):
                if res.status_code == 200:
                    assert True
                    with allure.step('接口返回是否正常'):
                        ErrorCode = res.json()["ErrorCode"]
                        ErrorMessage = res.json()["ErrorMessage"]
                        with allure.step('组合内基金转换是否成功'):
                            if ErrorCode == 0:
                                assert True
                                TraceID = res.json()["Data"]["TraceID"]
                                write_yaml3({"TraceID": TraceID})
                            else:
                                assert False, ErrorMessage
                else:
                    assert False, '接口状态码非200'

    @allure.story('组合内QD基金转换 /Trade/FundTrade/SFT1TransferL2')
    # 组合内QD基金转换
    def test_Trade_FundTrade_SFT1TransferL2(self):
        if read_yaml3() is None:
            pytest.skip(), '没有QD基金份额或者份额不足无法发起890'
        else:
            get_L2Password.user_Register_Secu(self)
            get_L2Password.DES_decrypto(self)
            get_L2Password.rsa_encrypto(self)
            url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/Trade/FundTrade/SFT1TransferL2")
            datas = {
                "L2Password": read_yaml3()["L2Password"],
                "SecuId": "feefd4d8095a4dc3b31863dfb71dde3f",  # 固定的
                "EncryptStr": "",
                "UserId": read_yaml2()["CustomerNo"],
                "ShareID": read_yaml3()["ShareId"],
                "FldParam": "",

                "FundIn": "003333",  # 非活期宝基金，高端理财等无法买入到组合的基金
                "SubAccountNoIn": "",
                "FundCode": "003333",  # 非活期宝基金，高端理财等无法买入到组合的基金
                "FundOut": read_yaml3()["FundCode"],
                "FundAmount": read_yaml3()["FundAmount_CJZH"],
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
            with allure.step('接口是否正常调通'):
                if res.status_code == 200:
                    assert True
                    ErrorCode = res.json()["ErrorCode"]
                    ErrorMessage = res.json()["ErrorMessage"]
                    with allure.step('组合内QD基金转换是否成功'):
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

    @allure.story('890撤单 /Trade/FundTrade/RevokeOrder')
    # 890撤单
    def test_Trade_FundTrade_RevokeOrder(self):
        if read_yaml3() is None:
            pytest.skip(), '没有QD基金份额或者份额不足无法发起超级转换'
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
                    with allure.step('QD基金撤单是否成功'):
                        if ErrorCode == 0:
                            assert True, '撤单受理成功'
                        else:
                            assert False, ErrorMessage
                else:
                    assert False, '接口状态码非200'


@allure.feature('组合内基金普通卖出回活期宝 24 6位密码')
class Test_redeem_Fund_Sub_L2():
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
                with allure.step('接口是否返回正常'):
                    ErrorCode = res.json()["ErrorCode"]
                    ErrorMessage = res.json()["ErrorMessage"]
                    if ErrorCode == 0:
                        assert True
                        clear_yaml3()
                        clear_yaml5()
                        FundCode = res.json()["Data"]["AssetDetails"][a_key]["FundCode"]
                        Count = res.json()["Data"]["AssetCounts"]["HH"]
                        write_yaml5({"Count": Count})
                        write_yaml3({"FundCode": FundCode})
                    else:
                        clear_yaml3()
                        assert False, ErrorMessage
            else:
                assert False, '接口状态码非200'

    @allure.story('持仓详情 所有 /User/home/GetShareDetail')
    # 获取特定基金的所有份额
    def test_User_home_GetShareDetail_ALL(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/home/GetShareDetail")
        datas = {
            "UserId": read_yaml2()["CustomerNo"],
            "SubAccountNo": "",
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
                with allure.step('接口是否返回正常'):
                    ErrorCode = res.json()["ErrorCode"]
                    ErrorMessage = res.json()["ErrorMessage"]
                    if ErrorCode == 0:
                        assert True
                        AvailableShare_all = res.json()["Data"]["AvailableShare"]
                        write_yaml3({"AvailableShare_all": AvailableShare_all})
                    else:
                        clear_yaml3()
                        assert False, ErrorMessage
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
                with allure.step('接口是否返回正常'):
                    ErrorCode = res.json()["ErrorCode"]
                    ErrorMessage = res.json()["ErrorMessage"]
                    if ErrorCode == 0:
                        assert True
                        with allure.step('选择大于最小赎回的份额的ID'):  # 因为多卡才做的逻辑。这个接口没有排序也没有字段返回份额数量
                            for i in range(5):
                                try:
                                    if res.json()["Data"]["Shares"][i - 1]["AvailableShare"] > res.json()["Data"][
                                        "MinSh"]:
                                        assert True
                                        MinSh = res.json()["Data"]["MinSh"]
                                        MinHold = res.json()["Data"]["MinHold"]
                                        EnableSh = res.json()["Data"]["EnableSh"]
                                        if EnableSh == True:
                                            if read_yaml3()["AvailableShare_all"] - MinSh - 0.01 > MinHold:
                                                AvailableShare = res.json()["Data"]["Shares"][i - 1]["AvailableShare"]
                                                ShareId = res.json()["Data"]["Shares"][i - 1]["ShareId"]
                                                Vol = res.json()["Data"]["MinSh"] + 0.01  # 。。有基金最小赎回是0的
                                                write_yaml3({"ShareId": ShareId})
                                                write_yaml3({"AvailableShare": AvailableShare})
                                                write_yaml3({"Vol": Vol})
                                                break
                                            else:
                                                clear_yaml3()
                                                assert False, '赎回后小于最低保留'
                                        else:
                                            clear_yaml3()
                                            assert False, '该基金暂停赎回'
                                    else:
                                        clear_yaml3()
                                        assert False, '没有大于最小赎回的单卡可用份额'
                                except IndexError:
                                    clear_yaml3()
                                    pass
                    else:
                        clear_yaml3()
                        assert False, ErrorMessage

            else:
                assert False, '接口状态码非200'

    @allure.story('卖组合单基金回活期宝 /Business/hqb/MakeRedemptionL2')
    # 卖组合单基金
    def test_Business_hqb_MakeRedemptionL2(self):
        if read_yaml3() is None:
            modify_a_key()
            self.test_User_Asset_GetFundAssetListOfSubV2()
            self.test_User_home_GetShareDetail_ALL()
            self.test_User_home_GetShareDetail()
            self.test_Business_hqb_MakeRedemption()
        else:
            get_L2Password.user_Register_Secu(self)
            get_L2Password.DES_decrypto(self)
            get_L2Password.rsa_encrypto(self)
            url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/Business/hqb/MakeRedemptionL2")
            datas = {
                "L2Password": read_yaml3()["L2Password"],
                "SecuId": "feefd4d8095a4dc3b31863dfb71dde3f",  # 固定的
                "EncryptStr": "",
                "CustomerNo": "",
                "UserId": read_yaml2()["CustomerNo"],
                "PayType": "cash",
                "Vol": read_yaml3()["Vol"],
                "ShareID": read_yaml3()["ShareId"],
                "RedemptionFlag": "1",
                "RechargeCashBagFundCode": "004545",  # 活期宝基金
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

    @allure.story('组合内基金卖出撤单 免密 /Trade/FundTrade/RevokeOrder')
    # 组合内基金卖出撤单 免密
    def test_Trade_FundTrade_RevokeOrder(self):
        if read_yaml3() is None or read_yaml3()["Succeed"] == False:
            pytest.skip(), '买基金失败无法撤单'
        else:
            time.sleep(4)  # 单号落库时间慢，设个延迟防止报错
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


@allure.feature('组合内基金卖出极速回活期宝 815 6位密码')
class Test_Quick_redeem_Fund_Sub_L2():
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
                with allure.step('接口是否返回正常'):
                    ErrorCode = res.json()["ErrorCode"]
                    ErrorMessage = res.json()["ErrorMessage"]
                    if ErrorCode == 0:
                        assert True
                        clear_yaml3()
                        clear_yaml5()
                        FundCode = res.json()["Data"]["AssetDetails"][a_key]["FundCode"]
                        Count = res.json()["Data"]["AssetCounts"]["HH"]
                        write_yaml5({"Count": Count})
                        write_yaml3({"FundCode": FundCode})
                    else:
                        clear_yaml3()
                        assert False, ErrorMessage
            else:
                assert False, '接口状态码非200'

    @allure.story('持仓详情 所有 /User/home/GetShareDetail')
    # 获取特定基金的所有份额
    def test_User_home_GetShareDetail_ALL(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/home/GetShareDetail")
        datas = {
            "UserId": read_yaml2()["CustomerNo"],
            "SubAccountNo": "",
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
                with allure.step('接口是否返回正常'):
                    ErrorCode = res.json()["ErrorCode"]
                    ErrorMessage = res.json()["ErrorMessage"]
                    if ErrorCode == 0:
                        assert True
                        AvailableShare_all = res.json()["Data"]["AvailableShare"]
                        write_yaml3({"AvailableShare_all": AvailableShare_all})
                    else:
                        clear_yaml3()
                        assert False, ErrorMessage
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
                with allure.step('接口是否返回正常'):
                    ErrorCode = res.json()["ErrorCode"]
                    ErrorMessage = res.json()["ErrorMessage"]
                    if ErrorCode == 0:
                        assert True
                        with allure.step('选择大于最小赎回的份额的ID'):  # 因为多卡才做的逻辑。这个接口没有排序也没有字段返回份额数量
                            for i in range(5):
                                try:
                                    if res.json()["Data"]["Shares"][i - 1]["AvailableShare"] > res.json()["Data"][
                                        "MinSh"]:
                                        assert True
                                        MinSh = res.json()["Data"]["MinSh"]
                                        MinHold = res.json()["Data"]["MinHold"]
                                        Enable815 = res.json()["Data"]["Enable815"]
                                        EnableSh = res.json()["Data"]["EnableSh"]
                                        if EnableSh == True:
                                            if Enable815 == True:
                                                if read_yaml3()["AvailableShare_all"] - MinSh - 0.01 > MinHold:
                                                    AvailableShare = res.json()["Data"]["Shares"][i - 1][
                                                        "AvailableShare"]
                                                    ShareId = res.json()["Data"]["Shares"][i - 1]["ShareId"]
                                                    Vol = res.json()["Data"]["MinSh"] + 0.01  # 。。有基金最小赎回是0的
                                                    write_yaml3({"ShareId": ShareId})
                                                    write_yaml3({"AvailableShare": AvailableShare})
                                                    write_yaml3({"Vol": Vol})
                                                    break
                                                else:
                                                    clear_yaml3()
                                                    assert False, '赎回后小于最低保留'
                                            else:
                                                clear_yaml3()
                                                assert False, '该基金不支持815'
                                        else:
                                            assert False, '该基金暂停赎回'
                                    else:
                                        clear_yaml3()
                                        assert False, '没有大于最小赎回的单卡可用份额'
                                except IndexError:
                                    clear_yaml3()
                                    pass
                    else:
                        clear_yaml3()
                        assert False, ErrorMessage
            else:
                assert False, '接口状态码非200'

    @allure.story('卖组合单基金极速回活期宝 /Trade/FundTrade/SFTransferL2')
    # 卖组合单基金极速回活期宝
    def test_Trade_FundTrade_SFTransferL2(self):
        if read_yaml3() is None:
            modify_a_key()
            self.test_User_Asset_GetFundAssetListOfSubV2()
            self.test_User_home_GetShareDetail_ALL()
            self.test_User_home_GetShareDetail()
            self.test_Business_Home_SFTransfer()
        else:
            get_L2Password.user_Register_Secu(self)
            get_L2Password.DES_decrypto(self)
            get_L2Password.rsa_encrypto(self)
            url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/Trade/FundTrade/SFTransferL2")
            datas = {
                "L2Password": read_yaml3()["L2Password"],
                "SecuId": "feefd4d8095a4dc3b31863dfb71dde3f",  # 固定的
                "EncryptStr": "",
                "UserId": read_yaml2()["CustomerNo"],
                "ShareID": read_yaml3()["ShareId"],
                "FldParam": "",

                "FundIn": "015419",  # 活期宝基金
                "SubAccountNoIn": "",
                "FundCode": "015419",  # 活期宝基金
                "FundOut": read_yaml3()["FundCode"],
                "FundAmount": read_yaml3()["Vol"],
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
            time.sleep(4)  # 单号落库时间慢，设个延迟防止报错
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


@allure.feature('组合内基金超级转换 815 6位密码')
class Test_CJZH_Sub_L2():
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
                with allure.step('接口是否返回正常'):
                    ErrorCode = res.json()["ErrorCode"]
                    ErrorMessage = res.json()["ErrorMessage"]
                    if ErrorCode == 0:
                        assert True
                        clear_yaml5()
                        MinSg = res.json()["Data"]["MinSg"]
                        write_yaml5({"MinSg": MinSg})  # 拿003333最小申购金额
                    else:
                        clear_yaml3()
                        assert False, ErrorMessage
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
                with allure.step('接口是否返回正常'):
                    ErrorCode = res.json()["ErrorCode"]
                    ErrorMessage = res.json()["ErrorMessage"]
                    if ErrorCode == 0:
                        assert True
                        Res = res.json()["Data"]["AssetDetails"]
                        with allure.step('组合里是否有HH基金'):
                            if Res == []:
                                clear_yaml3()
                                assert False, '组合内没有HH基金'
                            else:
                                assert True
                                Count = res.json()["Data"]["AssetCounts"]["HH"]
                                FundCode = res.json()["Data"]["AssetDetails"][b_key]["FundCode"]
                                clear_yaml3()
                                write_yaml3({"FundCode": FundCode})
                                write_yaml5({"Count": Count})
                    else:
                        clear_yaml3()
                        assert False, ErrorMessage
            else:
                assert False, '接口状态码非200'

    @allure.story('持仓详情 /User/home/GetShareDetail')
    # 获取特定基金的所有份额
    def test_User_home_GetShareDetail_all(self):
        if read_yaml3() is None:
            pytest.skip(), '没有HH基金份额无法发起超级转换'
        else:
            url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/home/GetShareDetail")
            datas = {
                "UserId": read_yaml2()["CustomerNo"],
                "SubAccountNo": "",
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
            time.sleep(1)  # 公测13分区请求返回有点慢，加的逻辑
            res = requests.request(method='post', url=url, params=datas)
            with allure.step('接口是否正常调通'):
                if res.status_code == 200:
                    assert True
                    with allure.step('接口是否返回正常'):
                        ErrorCode = res.json()["ErrorCode"]
                        ErrorMessage = res.json()["ErrorMessage"]
                        if ErrorCode == 0:
                            assert True
                            AvailableShare_all = res.json()["Data"]["AvailableShare"]
                            write_yaml3({"AvailableShare_all": AvailableShare_all})
                        else:
                            clear_yaml3()
                            assert False, ErrorMessage
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
                    with allure.step('接口是否返回正常'):
                        ErrorCode = res.json()["ErrorCode"]
                        ErrorMessage = res.json()["ErrorMessage"]
                        if ErrorCode == 0:
                            assert True
                            Enable815 = res.json()["Data"]["Enable815"]
                            if Enable815 == True:
                                FundNav = res.json()["Data"]["FundNav"]
                                MinSh = res.json()["Data"]["MinSh"]
                                for i in range(5):  # 因为多卡才做的逻辑。这个接口没有排序也没有字段返回份额数量
                                    try:
                                        if res.json()["Data"]["Shares"][i - 1]["AvailableShare"] > (
                                                read_yaml5()["MinSg"] / FundNav) / 0.9 and \
                                                res.json()["Data"]["Shares"][i - 1][
                                                    "AvailableShare"] >= MinSh:
                                            BankCardNo = res.json()["Data"]["Shares"][i - 1]["BankCardNo"]
                                            BankAccountNo = res.json()["Data"]["Shares"][i - 1]["BankAccountNo"]
                                            ShareId = res.json()["Data"]["Shares"][i - 1]["ShareId"]
                                            AvailableShare = res.json()["Data"]["Shares"][i - 1]["AvailableShare"]
                                            write_yaml3({"BankCardNo": BankCardNo})
                                            write_yaml3({"BankAccountNo": BankAccountNo})
                                            write_yaml3({"ShareId": ShareId})
                                            write_yaml3({"AvailableShare": AvailableShare})
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
                            clear_yaml3()
                            assert False, ErrorMessage
                else:
                    assert False, '接口状态码非200'

    @allure.story('转换详情（组合） /Trade/FundTrade/TransferOverview')
    # 获取转换的最小转出
    def test_Trade_FundTrade_TransferOverview(self):
        if read_yaml3() is None:
            modify_b_key()
            self.test_User_home_GetShareDetail_003333()
            self.test_User_Asset_GetFundAssetListOfSubV2()
            self.test_User_home_GetShareDetail_all()
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
                    with allure.step('接口是否返回正常'):
                        ErrorCode = res.json()["ErrorCode"]
                        ErrorMessage = res.json()["ErrorMessage"]
                        if ErrorCode == 0:
                            assert True
                            FundNav = res.json()["Data"]["TranOutFund"]["FundNav"]
                            MinRedeem = res.json()["Data"]["TranOutFund"]["MinRedeem"]
                            MinHoldShares = res.json()["Data"]["TranOutFund"]["MinHoldShares"]
                            AvailableVol = read_yaml3()["AvailableShare_all"]
                            FundAmount_CJZH = round((read_yaml5()["MinSg"] / FundNav) / 0.9, 2) + 0.01
                            if MinRedeem < FundAmount_CJZH:
                                if AvailableVol - FundAmount_CJZH > MinHoldShares:
                                    write_yaml3({"FundAmount_CJZH": FundAmount_CJZH})
                                else:
                                    clear_yaml3(), '当前基金多卡持有，当前卡全部赎回时，剩余份额不满足最小保留，请先进行份额合并。'
                            else:
                                if AvailableVol - MinRedeem > MinHoldShares:
                                    write_yaml3({"FundAmount_CJZH": MinRedeem})
                                else:
                                    clear_yaml3(), '当前基金多卡持有，当前卡全部赎回时，剩余份额不满足最小保留，请先进行份额合并。'
                        else:
                            clear_yaml3()
                            assert False, ErrorMessage
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
                    with allure.step('接口是否返回正常'):
                        ErrorCode = res.json()["ErrorCode"]
                        ErrorMessage = res.json()["ErrorMessage"]
                        if ErrorCode == 0:
                            assert True
                            TraceID = res.json()["Data"]["TraceID"]
                            write_yaml3({"TraceID": TraceID})
                        else:
                            clear_yaml3()
                            assert False, ErrorMessage
                else:
                    assert False, '接口状态码非200'

    @allure.story('组合内基金超级转换 /Trade/FundTrade/SFTransferL2')
    # 组合内基金超级转换
    def test_Trade_FundTrade_SFTransferL2(self):
        if read_yaml3() is None:
            pytest.skip(), '没有HH基金份额或者份额不足无法发起超级转换'
        else:
            get_L2Password.user_Register_Secu(self)
            get_L2Password.DES_decrypto(self)
            get_L2Password.rsa_encrypto(self)
            url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/Trade/FundTrade/SFTransferL2")
            datas = {
                "L2Password": read_yaml3()["L2Password"],
                "SecuId": "feefd4d8095a4dc3b31863dfb71dde3f",  # 固定的
                "EncryptStr": "",
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


@allure.feature('组合内基金基金转换 36 6位密码')
class Test_JJZH_Sub_L2():
    @allure.story('子账户持仓 /User/Asset/GetFundAssetListOfSubV2')
    # 获取子账户持仓 HH型
    def test_User_Asset_GetFundAssetListOfSubV2(self):
        clear_yaml3()
        clear_yaml5()
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
                with allure.step('接口是否返回正常'):
                    ErrorCode = res.json()["ErrorCode"]
                    ErrorMessage = res.json()["ErrorMessage"]
                    if ErrorCode == 0:
                        assert True
                        Res = res.json()["Data"]["AssetDetails"]
                        with allure.step('组合里是否有HH基金'):
                            if Res == []:
                                clear_yaml3()
                                assert False, '组合内没有HH基金'
                            else:
                                assert True
                                Count = res.json()["Data"]["AssetCounts"]["HH"]
                                FundCode = res.json()["Data"]["AssetDetails"][c_key]["FundCode"]
                                clear_yaml3()
                                write_yaml3({"FundCode": FundCode})
                                write_yaml5({"Count": Count})
                    else:
                        clear_yaml3()
                        assert False, ErrorMessage
            else:
                assert False, '接口状态码非200'

    @allure.story('基金转换列表 /Business/home/GetTransIntoFundList')
    # 获取基金转换列表
    def test_Business_home_GetTransIntoFundList(self):
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/Business/home/GetTransIntoFundList")
        datas = {
            "FundCode": read_yaml3()["FundCode"],

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
                        try:
                            FundCode1 = res.json()["Data"]["AvailableFundList"][0]["TransIntoFunds"][0]
                            write_yaml3({"FundCode1": FundCode1})
                        except IndexError:
                            pass
                            '该基金不能基金转换'
                    else:
                        clear_yaml3()
                        assert False, ErrorMessage
            else:
                assert False, '接口状态码非200'

    @allure.story('持仓详情 基金转换转入基金 /User/home/GetShareDetail')
    # 获取转入基金信息
    def test_User_home_GetShareDetail_JJZH(self):
        if read_yaml3() == {'FundCode': read_yaml3()["FundCode"]}:
            modify_g_key()
            self.test_User_Asset_GetFundAssetListOfSubV2()
            self.test_Business_home_GetTransIntoFundList()
            self.test_User_home_GetShareDetail_JJZH()
        else:
            url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/home/GetShareDetail")
            datas = {
                "UserId": read_yaml2()["CustomerNo"],
                "SubAccountNo": "",
                "FundCode": read_yaml3()["FundCode1"],
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
                    with allure.step('接口是否返回正常'):
                        ErrorCode = res.json()["ErrorCode"]
                        ErrorMessage = res.json()["ErrorMessage"]
                        if ErrorCode == 0:
                            assert True
                            MinSg = res.json()["Data"]["MinSg"]
                            write_yaml5({"MinSg": MinSg})
                        else:
                            clear_yaml3()
                            assert False, ErrorMessage
                else:
                    assert False, '接口状态码非200'

    @allure.story('持仓详情 /User/home/GetShareDetail')
    # 获取特定基金的所有份额
    def test_User_home_GetShareDetail_all(self):
        if read_yaml3() is None:
            pytest.skip(), '没有HH基金份额无法发起超级转换'
        else:
            url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/home/GetShareDetail")
            datas = {
                "UserId": read_yaml2()["CustomerNo"],
                "SubAccountNo": "",
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
            time.sleep(1)  # 公测13分区请求返回有点慢，加的逻辑
            res = requests.request(method='post', url=url, params=datas)
            with allure.step('接口是否正常调通'):
                if res.status_code == 200:
                    assert True
                    with allure.step('接口是否返回正常'):
                        ErrorCode = res.json()["ErrorCode"]
                        ErrorMessage = res.json()["ErrorMessage"]
                        if ErrorCode == 0:
                            assert True
                            AvailableShare_all = res.json()["Data"]["AvailableShare"]
                            write_yaml3({"AvailableShare_all": AvailableShare_all})
                        else:
                            clear_yaml3()
                            assert False, ErrorMessage
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
                    with allure.step('接口是否返回正常'):
                        ErrorCode = res.json()["ErrorCode"]
                        ErrorMessage = res.json()["ErrorMessage"]
                        if ErrorCode == 0:
                            assert True
                            Enable36 = res.json()["Data"]["Enable36"]
                            if Enable36 == True:
                                FundNav = res.json()["Data"]["FundNav"]
                                MinSh = res.json()["Data"]["MinSh"]
                                for i in range(5):  # 因为多卡才做的逻辑。这个接口没有排序也没有字段返回份额数量
                                    try:
                                        if res.json()["Data"]["Shares"][i - 1]["AvailableShare"] > (
                                                read_yaml5()["MinSg"] / FundNav) / 0.9 and \
                                                res.json()["Data"]["Shares"][i - 1][
                                                    "AvailableShare"] >= MinSh:
                                            BankCardNo = res.json()["Data"]["Shares"][i - 1]["BankCardNo"]
                                            BankAccountNo = res.json()["Data"]["Shares"][i - 1]["BankAccountNo"]
                                            ShareId = res.json()["Data"]["Shares"][i - 1]["ShareId"]
                                            AvailableShare = res.json()["Data"]["Shares"][i - 1]["AvailableShare"]
                                            write_yaml3({"BankCardNo": BankCardNo})
                                            write_yaml3({"BankAccountNo": BankAccountNo})
                                            write_yaml3({"ShareId": ShareId})
                                            write_yaml3({"AvailableShare": AvailableShare})
                                            break
                                    except IndexError:
                                        clear_yaml3()
                                        pass
                                try:
                                    if read_yaml3() == {'FundCode': read_yaml3()["FundCode"]}:
                                        clear_yaml3()
                                        '该基金没有份额可以做基金转换'
                                except TypeError:
                                    clear_yaml3()
                                    pass
                            else:
                                clear_yaml3()
                                '该基金不支持基金转换'
                        else:
                            clear_yaml3()
                            assert False, ErrorMessage
                else:
                    assert False, '接口状态码非200'

    @allure.story('转换详情（组合） /Trade/FundTrade/TransferOverview')
    # 获取转换的最小转出
    def test_Trade_FundTrade_TransferOverview(self):
        if read_yaml3() is None:
            modify_c_key()
            self.test_User_Asset_GetFundAssetListOfSubV2()
            self.test_Business_home_GetTransIntoFundList()
            self.test_User_home_GetShareDetail_JJZH()
            self.test_User_home_GetShareDetail_all()
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
                    with allure.step('接口是否返回正常'):
                        ErrorCode = res.json()["ErrorCode"]
                        ErrorMessage = res.json()["ErrorMessage"]
                        if ErrorCode == 0:
                            assert True
                            FundNav = res.json()["Data"]["TranOutFund"]["FundNav"]
                            MinRedeem36 = res.json()["Data"]["TranOutFund"]["MinRedeem36"]
                            MinHoldShares = res.json()["Data"]["TranOutFund"]["MinHoldShares"]
                            AvailableVol = read_yaml3()["AvailableShare_all"]
                            FundAmount_CJZH = round((read_yaml5()["MinSg"] / FundNav) / 0.9, 2) + 0.01
                            if MinRedeem36 < FundAmount_CJZH:
                                if AvailableVol - FundAmount_CJZH > MinHoldShares:
                                    write_yaml3({"FundAmount_CJZH": FundAmount_CJZH})
                                else:
                                    clear_yaml3(), '当前基金多卡持有，当前卡全部赎回时，剩余份额不满足最小保留，请先进行份额合并。'
                                    modify_g_key()
                                    self.test_User_Asset_GetFundAssetListOfSubV2()
                                    self.test_Business_home_GetTransIntoFundList()
                                    self.test_User_home_GetShareDetail_JJZH()
                                    self.test_User_home_GetShareDetail_all()
                                    self.test_User_home_GetShareDetail()
                                    self.test_Trade_FundTrade_TransferOverview()
                            else:
                                if AvailableVol - MinRedeem36 > MinHoldShares:
                                    write_yaml3({"FundAmount_CJZH": MinRedeem36})
                                else:
                                    clear_yaml3(), '当前基金多卡持有，当前卡全部赎回时，剩余份额不满足最小保留，请先进行份额合并。'
                                    modify_g_key()
                                    self.test_User_Asset_GetFundAssetListOfSubV2()
                                    self.test_Business_home_GetTransIntoFundList()
                                    self.test_User_home_GetShareDetail_JJZH()
                                    self.test_User_home_GetShareDetail_all()
                                    self.test_User_home_GetShareDetail()
                                    self.test_Trade_FundTrade_TransferOverview()
                        else:
                            clear_yaml3()
                            assert False, ErrorMessage
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
                    with allure.step('接口是否返回正常'):
                        ErrorCode = res.json()["ErrorCode"]
                        ErrorMessage = res.json()["ErrorMessage"]
                        if ErrorCode == 0:
                            assert True
                            TraceID = res.json()["Data"]["TraceID"]
                            write_yaml3({"TraceID": TraceID})
                        else:
                            clear_yaml3()
                            assert False, ErrorMessage
                else:
                    assert False, '接口状态码非200'

    @allure.story('组合内基金超级转换 /Trade/FundTrade/FTransferL2')
    # 组合内基金超级转换
    def test_Trade_FundTrade_FTransferL2(self):
        if read_yaml3() is None:
            pytest.skip(), '没有HH基金份额或者份额不足无法发起超级转换'
        else:
            get_L2Password.user_Register_Secu(self)
            get_L2Password.DES_decrypto(self)
            get_L2Password.rsa_encrypto(self)
            url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/Trade/FundTrade/FTransferL2")
            datas = {
                "L2Password": read_yaml3()["L2Password"],
                "SecuId": "feefd4d8095a4dc3b31863dfb71dde3f",  # 固定的
                "EncryptStr": "",
                "UserId": read_yaml2()["CustomerNo"],
                "ShareID": read_yaml3()["ShareId"],
                "FldParam": "",
                "Uid": "",
                "FundOut": read_yaml3()["FundCode"],
                "FundIn": read_yaml3()["FundCode1"],
                "ShareId": read_yaml3()["ShareId"],
                "FundAmount": read_yaml3()["FundAmount_CJZH"],
                "LargeRedemptionFlag": "1",
                "TraceID": read_yaml3()["TraceID"],
                "TraceTime": "",
                "FundRisk": "",
                "CustomerRisk": "",
                "FundCode": read_yaml3()["FundCode1"],

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


@allure.feature('组合卖出 6位密码 ')
class Test_redeem_Sub_L2():
    @allure.story('获取组合内份额 /User/SubA/SubARatioRedeemOverviewV2')
    # 获取组合内份额
    def test_User_SubA_SubARatioRedeemOverviewV2(self):
        clear_yaml3()
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

    @allure.story('等比例卖出组合回银行卡 /User/SubA/SubARatioRedeemCardsL2')
    # 等比例卖出组合
    def test_User_SubA_SubARatioRedeemCardsL2(self):
        get_L2Password.user_Register_Secu(self)
        get_L2Password.DES_decrypto(self)
        get_L2Password.rsa_encrypto(self)
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/User/SubA/SubARatioRedeemCardsL2")
        datas = {
            "L2Password": read_yaml3()["L2Password"],
            "SecuId": "feefd4d8095a4dc3b31863dfb71dde3f",  # 固定的
            "EncryptStr": "",
            "UserId": read_yaml2()["CustomerNo"],
            "SubAccountNo": read_yaml2()["SubAccountNo"],
            "Type": 1,  # 回银行卡 1   回活期宝 2
            "ObjectFundCode": read_yaml4()["FundCode_HQB_ZHM"],  # 活期宝基金代码,不传回银行卡
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
                ErrorCode = res.json()["ErrorCode"]
                ErrorMessage = res.json()["ErrorMessage"]
                with allure.step('组合卖出是否正常'):
                    if ErrorCode == 0:
                        assert True
                        write_yaml3({"Result": True})
                    else:
                        clear_yaml3()
                        assert False, ErrorMessage
            else:
                assert False, '接口状态码非200'

    @allure.story('组合卖出在途可撤单列表 /api/mobile/Query/GetQueryInfosQuickUse')
    # 交易查询 组合卖出在途可撤单列表
    def test_api_mobile_Query_GetQueryInfosQuickUse(self):
        if read_yaml3() is None:
            pytest.skip(), "组合卖出未成功"
        else:
            time.sleep(2)  # 撤单后接着查询，中间有延迟
            url = "https://tquerycoreapi8.1234567.com.cn/api/mobile/Query/GetQueryInfosQuickUse"
            datas = {
                "utoken": read_yaml2()["UToken"],
                "uid": read_yaml2()["CustomerNo"],
                "mobileKey": "01F12605-0E93-4BCB-AD67-D46C1DDA604B",
                "customerNo": read_yaml2()["CustomerNo"],
                "deviceid": "01F12605-0E93-4BCB-AD67-D46C1DDA604B",
                "ctoken": read_yaml2()["CToken"],
                "serverversion": "6.5.8",
                "rtype": "app",
                "data": "{{\"PageIndex\": 1, \"PageSize\": 20, \"FundCode\": \"\", \"DateType\": \"3\", \"BusType\":\"22\",\"Statu\":\"7\", \"Account\": \"\", \"SubAccountNo\": \"\", \"CustomerNo\": \"{}\" }}".format(
                    read_yaml2()["CustomerNo"])
            }
            res = requests.request(method='post', url=url, json=datas)
            print(res.json())
            with allure.step('接口是否正常调通'):
                if res.status_code == 200:
                    assert True
                    ErrorCode = res.json()["ErrorCode"]
                    ErrorMessage = res.json()["ErrorMessage"]
                    with allure.step('组合卖出是否正常'):
                        if ErrorCode is None:
                            assert True
                            Count = res.json()["TotalCount"] - 1
                            if Count >= 0:
                                BusinSerialNo = res.json()["responseObjects"][Count]["ID"]
                                BusinessType = res.json()["responseObjects"][Count]["BusinessCode"]
                                clear_yaml3()
                                write_yaml3({"BusinSerialNo": BusinSerialNo})
                                write_yaml3({"BusinessType": BusinessType})
                            else:
                                clear_yaml3()

                        else:
                            clear_yaml3()
                            assert False, ErrorMessage
                else:
                    assert False, "接口状态非200"

    @allure.story('组合卖撤单 /Trade/FundTrade/RevokeOrder')
    # 组合卖撤单
    def test_Trade_FundTrade_RevokeOrder(self):
        if read_yaml3() is None:
            pytest.skip(), '组合卖未成功或已撤单'
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
                    with allure.step('组合卖撤单是否成功'):
                        if ErrorCode == 0:
                            assert True, '撤单受理成功'
                        else:
                            assert False, ErrorMessage
                else:
                    assert False, '接口状态码非200'
            self.test_api_mobile_Query_GetQueryInfosQuickUse()
            self.test_Trade_FundTrade_RevokeOrder()


@allure.feature('买基金到组合 汇款支付 6位密码')
class Test_UnifiedBuy_fund_to_Sub_L2():
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

    @allure.story('买基金到组合 汇款支付 6位密码 /Business/Home/UnifiedBuyFundL2')
    # 买基金到组合 660以下免密
    def test_Business_Home_UnifiedBuyFundNP(self):
        get_L2Password.user_Register_Secu(self)
        get_L2Password.DES_decrypto(self)
        get_L2Password.rsa_encrypto(self)
        url = urljoin(read_yaml1()[read_yaml4()["Env"]], "/Business/Home/UnifiedBuyFundL2")
        datas = {
            "L2Password": read_yaml3()["L2Password"],
            "SecuId": "feefd4d8095a4dc3b31863dfb71dde3f",  # 固定的
            "EncryptStr": "",
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

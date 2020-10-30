#!/usr/bin/python
# -*- coding:utf-8 -*-
import base64
import pytest
import requests
from suds.client import Client
from requests_ntlm import HttpNtlmAuth
from src import ApiSetup
from src.dms.base import WebServiceHandler, DMSBase


@pytest.mark.skip("同步好使，测测异步")
def test_InvokeWebservice_via_request():
    url = "http://62.234.26.35:7047/DynamicsNAV/WS/K302%20Zhuhai%20JJ/Codeunit/DMSWebAPI"
    username = "NAVWebUser"
    password = "Hytc_1qaz@WSX"

    headers = {
        "Content-Type": "text/xml",
        "SOAPAction": "HandleCVInfoWithEntryNo"
    }
    # postcontent='<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><HandleFAWithEntryNo xmlns="urn:microsoft-dynamics-schemas/codeunit/DMSWebAPI"><entryNo>6516</entryNo><_CalledBy>0</_CalledBy></HandleFAWithEntryNo></soap:Body></soap:Envelope>'
    postcontent='<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><HandleCVInfoWithEntryNo xmlns="urn:microsoft-dynamics-schemas/codeunit/DMSWebAPI"><entryNo>6541</entryNo><_CalledBy>0</_CalledBy></HandleCVInfoWithEntryNo></soap:Body></soap:Envelope>'
    req = requests.post(url, headers=headers, auth=HttpNtlmAuth(username, password), data=postcontent.encode('utf-8'))
    print(req, req.text)


@pytest.mark.skip("不测suds了")
def test_sudspy3_via_qq():
    url = 'http://www.webxml.com.cn/webservices/qqOnlineWebService.asmx?wsdl'
    client = Client(url)
    print(client)
    result = client.service.qqCheckOnline("49273395")

    print("QQ在线结果为：" + result)


def test_ws_via_request(init_app):
    username = "NAVWebUser"
    password = "Hytc_1qaz@WSX"
    soap_action = "urn:microsoft-dynamics-schemas/codeunit/DMSWebAPI:HandleOtherWithEntryNo"
    api_setup = ApiSetup(Company_Code="test", API_Code="testws", Data_Format=2, CallBack_Address="http://62.234.26.35:7047/DynamicsNAV/WS/%s/Codeunit/DMSWebAPI")
    wsh = WebServiceHandler(api_setup, soap_username=username, soap_password=password)
    ws_url = wsh.soapAddress("K302%20Zhuhai%20JJ")
    ws_env = WebServiceHandler.soapEnvelope(method_name="HandleOtherWithEntryNo", entry_no=6594)
    # result = wsh.call_web_service(ws_url, ws_env, direction=DMSBase.DIRECT_NAV, soap_action="urn:microsoft-dynamics-schemas/codeunit/DMSWebAPI:HandleCVInfoWithEntryNo", need_async=True)
    result = wsh.invoke_async(ws_url, soap_action, data=ws_env)
    print(result, result.status_code)
    assert result is not None

#!/usr/bin/python
# -*- coding:utf-8 -*-
import base64
import pytest
import requests
from suds.client import Client
from suds.transport.https import WindowsHttpAuthenticated, HttpAuthenticated
from requests_ntlm import HttpNtlmAuth

# @pytest.mark.skip("试试别的方法")
def test_ws_custvend_via_suds():
    url = "http://62.234.26.35:7047/DynamicsNAV/WS/K302%20Zhuhai%20JJ/Codeunit/DMSWebAPI"
    username = '.\\NAVWebUser'
    password = "Hytc_1qaz@WSX"

    ntlm = WindowsHttpAuthenticated(username=username, password=password)
    client = Client(url, transport=ntlm)
    # t = HttpAuthenticated(username=username, password=password)
    # client = Client(url, transport=t)

    # str1 = '%s:%s' % (username, password)
    # be = base64.encodestring(str1.encode(encoding="utf-8"))
    # print(type(be))
    # base64string = be.replace(b'\n', b'')
    # authenticationHeader = {
    #     "SOAPAction": "HandleCVInfoWithEntryNo",
    #     "Authorization": "Basic %s" % base64string
    # }
    # client = Client(url, headers=authenticationHeader)

    print(client)
    res = client.service.HandleCVInfoWithEntryNo(6515, 0)
    print(res)


@pytest.mark.skip("request貌似无法调用")
def test_InvokeWebservice_via_request():
    url = "http://62.234.26.35:7047/DynamicsNAV/WS/K302%20Zhuhai%20JJ/Codeunit/DMSWebAPI"
    username = "NAVWebUser"
    password = "Hytc_1qaz@WSX"

    postcontent='<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><HandleFAWithEntryNo xmlns="urn:microsoft-dynamics-schemas/codeunit/DMSWebAPI"><entryNo>6516</entryNo><_CalledBy>0</_CalledBy></HandleCVInfoWithEntryNo></soap:Body></soap:Envelope>'
    req = requests.post(url, auth=HttpNtlmAuth(username, password), data=postcontent.encode('utf-8'), headers={'Content-Type': 'text/xml'})
    print(req, req.text)


def test_sudspy3_via_qq():
    url = 'http://www.webxml.com.cn/webservices/qqOnlineWebService.asmx?wsdl'
    client = Client(url)
    print(client)
    result = client.service.qqCheckOnline("49273395")

    print("QQ在线结果为：" + result)


def test_ws_via_spnego():
    import spnego
    url = "http://62.234.26.35:7047/DynamicsNAV/WS/K302%20Zhuhai%20JJ/Codeunit/DMSWebAPI?wsdl"
    username = '.\\NAVWebUser'
    password = "Hytc_1qaz@WSX"
    client = spnego.client(username, password, protocol='ntlm')
    negotiate = client.step()

    challenge = exchange_data(negotiate)
    authenticate = client.step(challenge)
    exchange_data(authenticate)

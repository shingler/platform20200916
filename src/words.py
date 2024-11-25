#!/usr/bin/python
# -*- coding:utf-8 -*-
# 提示话术定义


# 提醒邮件话术模板
class Notice:
    # 提醒邮件标题模板
    title = 'DMS Interface Error (Company Code: {0}, Data Type: {1} )'
    # 提醒邮件内容模板
    # 0=data_type; 1=company_code; 2=api_code; 3=error_message; 4=url
    content = '''<html>
<head>
<meta http-equiv=Content-Type content="text/html; charset=UTF-8">
</head>
<body>
<div class=WordSection1>
<p class=MsoNormal>Dear User,</p>
<p class=MsoNormal>There are some errors occurred during system import DMS <span style="color: rgb(255, 0, 0);"><strong>{0}</strong></span> Interface Data, the first error message like below:</span></p>
<p class=MsoNormal>Company Code: {1}, <br/>API Code: {2}, <br/>Error Message:{3}</span></p>
<p class=MsoNormal>Please check error log in NAV interface platform (URL:<a href="{4}" target="_self">{4}</a>).</p>
<p class=MsoNormal>If you have any questions, please contact NAV support team with Email:<a href="mailto:phnav.support@hytci.com" target="_self">phnav.support@hytci.com</a>!</p>
<p class=MsoNormal>Navision system</p>
</div>
</body>
</html>'''


# 数据导入错误消息模板
class DataImport:
    _some_field_is_empty = "{0} can not be null!"
    _file_repeat = "XML file:{0} is already existing in system, can not import again! "
    _file_not_exist = "There is no XML file:{0}!"
    _file_too_big = "The XML file size {0}M is beyond system allowed size {1}M, please check XML file!"
    _load_timeout = "Timeout for reading file:{0}"
    _content_is_too_big = "The length of content (field:{0} \"{3}\" ) exceeds the max length {1} in file: {2}"
    _node_not_exists = "Node:{0} is missing!"
    _json_http_error = "Task<{0}, {1}> dms request http error, status_code={2}"
    _json_is_empty = "Task<{0}, {1}> JSON API return nothing"
    _json_request_error = "Task<{0}, {1}> JSON API request failed. reason is: {2}"
    _param_out_setup_error = "Task<{0}, {1}> api out param setup error, parent node {2} is missing!"

    @classmethod
    def field_is_empty(cls, field):
        return cls._some_field_is_empty.format(field)

    @classmethod
    def file_is_repeat(cls, file_path):
        return cls._file_repeat.format(file_path)

    @classmethod
    def file_not_exist(cls, file_path):
        return cls._file_not_exist.format(file_path)

    @classmethod
    def file_too_big(cls, expect, actual):
        return cls._file_too_big.format(actual, expect)

    @classmethod
    def load_timeout(cls, file_path):
        return cls._load_timeout.format(file_path)

    @classmethod
    # @param str path 文件路径
    # @param dict cnt 内容超长的具体信息，{key=节点名, expect=预期长度, content=内容}
    def content_is_too_big(cls, path, cnt):
        return cls._content_is_too_big.format(cnt["key"], cnt["expect"], path, cnt["content"])

    @classmethod
    def node_not_exists(cls, nodes):
        message = cls._node_not_exists.format(','.join(nodes))
        return message

    @classmethod
    def json_is_empty(cls, company_code, api_code):
        return cls._json_is_empty.format(company_code, api_code)

    @classmethod
    def json_request_fail(cls, company_code, api_code, reason):
        return cls._json_request_error.format(company_code, api_code, reason)

    @classmethod
    def param_out_setup_error(cls, company_code, api_code, p_name):
        return cls._param_out_setup_error.format(company_code, api_code, p_name)

    @classmethod
    def json_http_error(cls, company_code, api_code, http_code):
        return cls._json_http_error.format(company_code, api_code, http_code)


# 程序运行时报错消息模板
class RunResult:
    _sucess = "Task<{0}, {1}> Operation successful, Entry No:{2}"
    _fail = "Task<{0}, {1}> failed, reason is {2}"
    _retry = "According to system setting, the task<{0}, {1}> will be tried again"
    _send_notify = "According to system setting, the task<{0}, {1}> will send notification email"
    _task_start = "Task<{0}, {1}> is running"
    _task_not_reach_time = "The Time for Task<{0}, {1}> is not arrived"

    @classmethod
    def success(cls, company_code, api_code, entry_no):
        return cls._sucess.format(company_code, api_code, entry_no)

    @classmethod
    def fail(cls, company_code, api_code, reason):
        return cls._fail.format(company_code, api_code, reason)

    @classmethod
    def retry(cls, company_code, api_code):
        return cls._retry.format(company_code, api_code)

    @classmethod
    def send_notify(cls, company_code, api_code):
        return cls._send_notify.format(company_code, api_code)

    @classmethod
    def task_start(cls, company_code, api_code):
        return cls._task_start.format(company_code, api_code)

    @classmethod
    def task_not_reach_time(cls, company_code, api_code):
        return cls._task_not_reach_time.format(company_code, api_code)


# API错误提示模板
class WebApi:
    _field_empty = "{0} can not be empty!"
    _invalid_value = "the field {0} has an invalid value: {1}"
    _api_type_not_support = "the {0} is not supported"
    _other_error = "there's something wrong, please contact us."
    _method_error = "Request method is incorrect, please retry with POST"
    _company_not_found = "The company code \"{0}\" is not found"
    _api_not_found = "The company code \"{0}\" with api code \"{1}\" is not found"

    @classmethod
    def filed_empty(cls, field):
        return cls._field_empty.format(field)

    @classmethod
    def invalid_value(cls, key, value):
        return cls._invalid_value.format(key, value)

    @classmethod
    def api_type_not_support(cls, api_name):
        return cls._api_type_not_support.format(api_name)

    @classmethod
    def internal_error(cls):
        return cls._other_error

    @classmethod
    def method_error(cls):
        return cls._method_error

    @classmethod
    def company_not_found(cls, company_code):
        return cls._company_not_found.format(company_code)

    @classmethod
    def api_not_found(cls, company_code, api_code):
        return cls._api_not_found.format(company_code, api_code)

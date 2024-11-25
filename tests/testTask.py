# 任务运行的测试用例
import gevent.monkey
gevent.monkey.patch_all()
import random
import pytest

from bin import cust_vend, fa, invoice, other
from src import UserList
from src.dms.notification import Notification
from src.dms.task import Task
from src.error import DataLoadError, DataLoadTimeOutError, DataImportRepeatError
from src.models import nav
from src.models.dms import NotificationUser, Company
from src.models.log import NotificationLog


runner = None
current_task = None
load_error = None
global_vars = {
    "retry": False, "notify": False, "entry_no": 0
}


# 从数据库随机读取一个任务
def test_1_load_task(init_app):
    task_list = Task.load_tasks()
    one_task = random.choice(task_list)
    # one_task = task_list[0]
    assert one_task.Company_Code != ""
    assert one_task.API_Code != ""
    assert type(one_task.Fail_Handle) == int
    print(one_task)
    globals()["current_task"] = Task(one_task)


# 让这个任务执行失败（根据失败处理，进行重试测试）
# @pytest.mark.skip("测试成功时忽略")
def test_2_run_task(init_app):
    one_task = globals()["current_task"]
    company_code = one_task.Company_Code
    api_code = one_task.API_Code
    entry_no = 0
    runner = None

    try:
        if one_task.API_Code.startswith("CustVendInfo"):
            runner = cust_vend
        elif one_task.API_Code.startswith("FA"):
            runner = fa
        elif one_task.API_Code.startswith("Invoice"):
            runner = invoice
        elif one_task.API_Code.startswith("Other"):
            runner = other

        globals()["runner"] = runner
        entry_no = runner.main(company_code=company_code, api_code=api_code)
        assert entry_no != 0
        print("读取成功，Entry_No=%d" % entry_no)
        global_vars["entry_no"] = entry_no
        # 更新成功执行时间
        one_task.update_execute_time()

    except Exception as ex:
        print(ex)
        # 失败处理，主要读取task里的Fail_Handle字段
        if one_task.api_task_setup.Fail_Handle == 1:
            print("Fail Handle设置为1，不继续执行")
        elif one_task.api_task_setup.Fail_Handle == 4:
            print("Fail Handle设置为4，将发送提醒但不继续执行")
            globals()["load_error"] = ex
            global_vars["notify"] = True
        else:
            print("Fail Handle设置不为1，将重试")
            global_vars["retry"] = True
        assert entry_no == 0


# 重试
def test_3_retry_or_not(init_app):
    retry = global_vars["retry"]
    if retry:
        print("失败后重试")
        one_task = globals()["current_task"]
        company_code = one_task.Company_Code
        api_code = one_task.API_Code
        entry_no = 0

        try:
            runner = globals()["runner"]
            entry_no = runner.main(company_code=company_code, api_code=api_code, retry=retry)
            assert entry_no != 0
            print("重试后，读取成功，Entry_No=%d" % entry_no)
            global_vars["entry_no"] = entry_no
            # 更新成功执行时间
            one_task.update_execute_time()

        except Exception as ex:
            print("重试后，依然失败")
            if one_task.api_task_setup.Fail_Handle == 3:
                # 重试后依然失败，如果Fail_Handle=3则发送提醒邮件
                global_vars["notify"] = True
                globals()["load_error"] = ex
    else:
        print("失败后不重试或第一次读取成功")


# 发送提醒邮件
def test_4_send_notification(init_app):
    notify = global_vars["notify"]
    if not notify:
        print("不发送提醒邮件")
    else:
        print("发送提醒邮件")
        one_task = globals()["current_task"]
        # 读取邮件列表
        notify_obj = Notification(one_task.Company_Code, one_task.API_Code)
        receivers = notify_obj.get_receiver_email()
        print(receivers)
        assert type(receivers) == list
        assert len(receivers) != 0
        # assert receivers[0].Activated or receivers[0].Receive_Notification
        # 发送邮件
        smtp_config = notify_obj.smtp_config
        assert smtp_config is not None
        assert smtp_config.Email_SMTP is not None
        assert smtp_config.Email_SMTP != ""

        nids = []
        for r in receivers:
            if (isinstance(r, NotificationUser) and r.Activated) \
                    or (isinstance(r, UserList) and r.Receive_Notification):
                notify_obj.add_receiver(r.Email_Address)

        email_title, email_content = notify_obj.get_notification_content(one_task.Task_Name, one_task.Company_Code, one_task.API_Code, error_message=load_error)

        assert email_content != ""
        result = notify_obj.send_mail(email_title, email_content)
        assert result
        # 写入提醒日志
        if result:
            nid = notify_obj.save_notification_log(",".join(notify_obj.receivers), email_title, email_content)
            assert nid is not None
            nids.append(nid)
        # 验证日志有记录
        app, db = init_app
        logs = db.session.query(NotificationLog).filter(NotificationLog.ID.in_(nids)).all()
        assert len(logs) > 0


# 验证写入的数据是否符合预期
def test_5_valid_data(init_app):
    entry_no = global_vars["entry_no"]
    if entry_no == 0:
        # 执行失败用例，不用验证
        print("接口读取失败，无数据写入")
        return True

    # 验证数据
    app, db = init_app
    db.session.expire_all()
    # 读取公司信息
    company_info = db.session.query(Company).filter(Company.Code == current_task.Company_Code).first()
    # 访问nav数据，需要修改数据库连接设置
    conn_str = company_info.get_nav_connection_string(app.config)
    app.config["SQLALCHEMY_BINDS"][
        "%s-nav" % company_info.NAV_Company_Code] = conn_str

    # interfaceInfo数据
    interfaceInfoClass = nav.dmsInterfaceInfo(company_info.NAV_Company_Code)
    interface_data = db.session.query(interfaceInfoClass).filter(interfaceInfoClass.Entry_No_ == entry_no).first()
    assert interface_data is not None
    assert type(interface_data.Type) == int
    print(interface_data.Type)
    # 根据type，验证对应数据
    if interface_data.Type == 0:
        custVendClass = nav.custVendBuffer(company_info.NAV_Company_Code)
        data_list = db.session.query(custVendClass).filter(custVendClass.Entry_No_ == entry_no).all()
        # 检查数据正确性
        assert interface_data.DMSCode == "7000320"
        assert interface_data.Customer_Vendor_Total_Count == 2
        assert len(data_list) > 0
        assert data_list[0].No_ == "835194"
        assert data_list[0].Type == 0
        assert data_list[1].No_ == "V00000002"
        assert data_list[1].Type == 1
    elif interface_data.Type == 1:
        faClass = nav.faBuffer(company_info.NAV_Company_Code)
        data_list = db.session.query(faClass).filter(faClass.Entry_No_ == entry_no).all()
        # 检查数据正确性
        assert interface_data.DMSCode == "28976"
        assert interface_data.FA_Total_Count == 1
        assert len(data_list) > 0
        assert data_list[0].FANo_ == "FA0001"
    elif interface_data.Type == 2:
        invoiceHeaderClass = nav.invoiceHeaderBuffer(company_info.NAV_Company_Code)
        invoiceLineClass = nav.invoiceLineBuffer(company_info.NAV_Company_Code)
        headerInfo = db.session.query(invoiceHeaderClass).filter(invoiceHeaderClass.Entry_No_ == entry_no).first()
        lineList = db.session.query(invoiceLineClass).filter(invoiceLineClass.Entry_No_ == entry_no).all()

        print(headerInfo)
        # 检查数据正确性
        assert interface_data.DMSCode == "7000320"
        assert interface_data.Invoice_Total_Count == 1
        assert headerInfo.InvoiceNo == "1183569670"
        assert len(lineList) > 0
        assert lineList[0].GLAccount == "6001040101"
        assert lineList[0].VIN == "WP1AB2920FLA58047"
        assert lineList[0].InvoiceNo == headerInfo.InvoiceNo
        assert lineList[1].GLAccount == "6001030104"
        assert lineList[1].VIN == "WP1AB2920FLA58047"
        assert lineList[1].InvoiceNo == headerInfo.InvoiceNo
    elif interface_data.Type == 3:
        # 检查数据正确性
        assert interface_data.DMSCode == "7000320"
        assert interface_data.Other_Transaction_Total_Count == 1
        otherClass = nav.otherBuffer(company_info.NAV_Company_Code)
        data_list = db.session.query(otherClass).filter(otherClass.Entry_No_ == entry_no).all()
        assert len(data_list) > 0
        assert data_list[0].DocumentNo_ == "XXXXX"
        assert data_list[0].SourceNo == "C0000001"
        assert data_list[1].SourceNo == "BNK_320_11_00003"

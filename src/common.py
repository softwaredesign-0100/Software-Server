from sanic import Sanic
import pandas as pd
from utils import *
from config import *
import smtplib
from email.mime.text import MIMEText

'''
:param
    data : {
        identify: '',
        account: '',
        password: ''
    }
:return
    {
        status: ''
    }

'''


def c_sign_up(data):
    sql = "insert into %s (account, password) values ('%s', '%s');"
    baser = DatabaseDeal()
    results, status = baser.insert_like(sql=sql % (map_table[data['identify']], data['account'], data['password']))
    print('sign in status: %d' % status)
    return results, status


'''
:param
    data: {
        identify: '',
        account: '',
        password: ''
    }

:return
    {
        status: ''
    }
'''


def c_sign_in(data):
    print('c sign in data: ', data)
    sql = "select password from %s where account = '%s'"
    baser = DatabaseDeal()
    results, status = baser.select(sql=sql % (map_table[data['identify']], data['account']))

    if results.shape[0] == 0:
        status = 404  # no such user
        return results, status
    elif results.iloc[0]['password'] != data['password']:
        status = 403  # password error
        return results, status

    sql_is_name = "select name from %s where account = '%s' and name is not null;"
    results, _ = baser.select(sql=sql_is_name % (map_table[data['identify']], data['account']))

    if results.shape[0] == 0:
        status = 401
    else:
        sql_is_name = "select name from %s where account = '%s' and name is not null;"
        results, _ = baser.select(sql=sql_is_name % (map_table[data['identify']], data['account']))
        if results.shape[0] == 0:
            status = 401
    print('sign in status: %d' % status)
    return results, status


'''
:param 
    data: {
        identify: '',
        account: '',
        old_password: '',
        new_password: ''
    }

:return
    {
        status: ''
    }
'''


def c_change_password(data):
    sql_get_pwd = "select password from %s where account = '%s';"
    baser = DatabaseDeal()

    results, status = baser.select(sql_get_pwd % (map_table[data['identify']], data['account']))

    if results.iloc[0]['password'] == data['old_password']:
        sql_change_pwd = "update %s set password = '%s' where account = '%s' and password = '%s';"
        results, status = baser.insert_like(
            sql_change_pwd % (map_table[data['identify']], data['account'], data['new_password'], data['old_password']))
    else:
        status = 403  # password error
        results = None
    return results, status


'''
发起取消预约
:params
    data: {
        identify: '',
        account: '',
        serial: '',
        reason: ''
    }

:return 
    {
        status
    }
'''


def c_initiate_cancel(data):
    print('c initiate cancel data: ', data)

    baser = DatabaseDeal()
    if data['identify'] == 'student':
        is_canceled = 2
    else:
        sql = "select s_account from ReservationInfo where serial = '%s';"
        results, status = baser.select(sql=sql % data['serial'])
        if results.iloc[0]['s_account'] is None:
            is_canceled = 3
            sql_delete = "delete from ReservationInfo where serial = '%s'"
            r_d, s_d = baser.insert_like(sql_delete % (data['serial']))
        else:
            is_canceled = 1

    # 更改状态
    if is_canceled != 3:
        sql = "update ReservationInfo set is_canceled = '%s', reason = '%s' where serial = '%s';"
        results, status = baser.insert_like(sql=sql % (is_canceled, data['reason'], data['serial']))
    else:
        results, status = None, 200
    print('c initiate cancel: status = %d | is_canceled = %d' % (status, is_canceled))

    # 发送邮件

    return results, status


'''
确认取消预约
:params
    data: {
        identify: '',
        account: '',
        serial: ''
    }

:return 
    {
        status: ''
    }
'''


def c_ensure_cancel(data):
    baser = DatabaseDeal()
    print('c ensure cancel data: ', data)
    # sql_select = "select concat(is_canceled) as is_canceled from ReservationInfo where serial = %d;"
    # r_select, _ = baser.select(sql_select % int(data['serial']))
    # # print('r_select: ', r_select)
    # is_canceled = int(r_select.iloc[0]['is_canceled'])

    if data['identify'] == 'teacher':
        sql = "update ReservationInfo set is_canceled = 0, is_selected = 0, s_name = null, s_account = null where serial = '%s';"
    if data['identify'] == 'student':
        sql = "delete from ReservationInfo where serial = '%s';"
    results, status = baser.insert_like(sql=sql % (data['serial']))
    print('c ensure cancel status: ', status, 'results: ', results)
    return results, status


'''
:params
    data: {
        email: '',
        code: ''
    }

:return
    {
        status:
    }
'''


def c_send_email(data):
    sender = SendEmail()
    print('c send email data: ', data)
    verify_code = data['code']
    receivers = [data['email']]

    codes = '您的验证码是<h3>%s</h3>请不要泄露哦' % verify_code

    try:
        status = sender.send_email(receivers=receivers, subject='校园预约系统邮箱验证', data=codes)
    except Exception as e:
        status = 500
        print('c send email error! ', e)

    # message = MIMEText(codes, 'plain', 'utf-8')
    # message['Subject'] = '校园预约系统邮箱验证'
    # message['From'] = mail_user
    # message['To'] = receivers[0]
    #
    # try:
    #     smtpObj = smtplib.SMTP()
    #     smtpObj.connect(mail_host, 25)
    #     smtpObj.login(user=mail_user, password=mail_password)
    #     smtpObj.sendmail(from_addr=mail_user, to_addrs=receivers[0], msg=message.as_string())
    #     smtpObj.quit()
    #     status = 200
    # except Exception as e:
    #     print('send email fail', e)
    #     status = 500

    print('c send eamil status: ', status)
    return 0, status


'''
:params
    data: {
        identify: ''
        account: '',
        ok: true
    }

:return 
    {
        status: 
    }
'''


def c_verify_email(data):
    print('c verify email data: ', data)
    baser = DatabaseDeal()
    sql = "insert into %s set email_verified = '1' where account = '%s';"
    try:
        results, status = baser.insert_like(sql % (map_table[data['identify']], data['account']))
    except Exception as e:
        print('update fail!', e)
        results, status = 0, 500
    return results, status


'''
:params 
    data: {
        identify: '',
        account: ''
    }

:return
    {
        verify_email: true or false,
        verify_phone: true,
        status: 
    }
'''


def c_get_verify_info(data):
    print('c get verify info data: ', data)
    baser = DatabaseDeal()
    sql = "select email_verified as verify_email, phone_verified as verify_phone from '%s' where account = '%s';"

    try:
        r, status = baser.select(sql=sql % (map_table[data['identify']], data['account']))
        results = {
            'verify_email': r.iloc[0]['verify_email'],
            'phone_verified': r.iloc[0]['phone_verified']
        }
    except Exception as e:
        results, status = None, 500
        print('select finish', e)

    return results, status


'''
:params 
    data: {
        identify: '',
        account: ''
    }

:return 
    {
        status: '',
        results: [
            {
                week: ''
                weekday: '', 
                reason: '',
                tips: '',
                segment: ''
                t_name: ''
                s_name: '',
                place: ''，
                score: ''
            },
            ...
        ]
    }
    
'''


def c_view_his_res(data):
    print('c view his res data: ', data)
    baser = DatabaseDeal()
    sql = "select week, weekday, segment, reason, tips, t_name, s_name, place, concat(serial) as serial, concat(score) as score " \
          "from ReservationInfo where %s = '%s' and is_finished = '1';"
    try:
        r, status = baser.select(sql % (map_field[data['identify']], data['account']))
        results = []
        for i in range(0, r.shape[0]):
            results.append(r.iloc[i].to_dict())
    except Exception as e:
        status = 500
        results = 0
        print('c view his results error!', e)

    print('c view his res results: ', results, 'status: ', status)
    return results, status


'''
11 删除考试

接口名
    delete_exam

:params 
    data: {
        account: '',
        serial: '',
        identify: ''
    }

:return 
    {
        status: ''
    }
'''


def c_delete_exam(data):
    print('c delete exam data: ', data)
    baser = DatabaseDeal()

    if data['identify'] == 'student':
        sql = "delete from StudentExam where s_account = '%s' and e_serial = '%s';"
    if data['identify'] == 'teacher':
        sql = "delete from ExamInfo where t_account = '%s' and serial = '%s'"

    try:
        results, status = baser.insert_like(sql % (data['account'], data['serial']))
    except Exception as e:
        print('c delete exam error!', e)
        results, status = None, 500
    return results, status


'''
10 完成预约

接口名
    finish_res

:params 
    data: {
        account: '',
        serial: '',
        score: int,
    }

:return 
    {
        status: ''
    }
'''


def c_finish_res(data):
    print('s s finish res data: ', data)
    baser = DatabaseDeal()
    sql = "update ReservationInfo set is_finished = '1', score = '%d' where serial = '%s';"
    try:
        results, status = baser.insert_like(sql % (data['score'], data['serial']))
    except Exception as e:
        print('s s finish res error!', e)
        results, status = 0, 0
    print('s s finish res results: ', results, 'status: ', status)
    return results, status

from sanic import Sanic
import pandas as pd
from deal_database import DatabaseDeal
from config import *

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
    sql = "select password from %s where account = '%s'"
    baser = DatabaseDeal()
    results, status = baser.select(sql=sql % (map_table[data['identify']], data['account']))

    if results.shape[0] == 0:
        status = 404  # no such user
    elif results.iloc[0]['password'] != data['password']:
        status = 403  # password error

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
        sql = "select s_name from ReservationInfo where serial = '%s';"
        results, status = baser.select(sql=sql % data['serial'])
        if results.iloc[0]['s_name'] is None:
            is_canceled = 3
        else:
            is_canceled = 1

    sql = "update ReservationInfo set is_canceled = '%s', reason = '%s' where serial = '%s';"
    results, status = baser.insert_like(sql=sql %(is_canceled, data['reason'], data['serial']))
    print('c initiate cancel: status = %d | is_canceled = %d' % (status, is_canceled))
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
    print('c ensure cancel data: ', data)
    sql = "update ReservationInfo set is_canceled = 3 where serial = '%s';"
    baser = DatabaseDeal()
    results, status = baser.insert_like(sql=sql % (data['serial']))
    print('c ensure cancel status: ', status, 'results: ', results)
    return results, status


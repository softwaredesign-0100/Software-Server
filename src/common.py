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
<<<<<<< HEAD

=======
>>>>>>> dev_mdy
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
<<<<<<< HEAD


    sql_is_name = "select name from %s where account = '%s' and name is not null;"
    results, _ = baser.select(sql=sql_is_name % (map_table[data['identify']], data['account']))
    if results.shape[0] == 0:
        status = 401
=======
    else:
        sql_is_name = "select name from %s where account = '%s' and name is not null;"
        results, _ = baser.select(sql=sql_is_name % (map_table[data['identify']], data['account']))
        if results.shape[0] == 0:
            status = 401
>>>>>>> dev_mdy
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

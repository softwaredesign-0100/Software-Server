import pandas as pd
import pymysql
from deal_database import DatabaseDeal
from config import *
from sanic.response import json

'''
:params:
    data: {
        "account: ""
    }

:return 
    {
        status: "",
        info: {
                name: "",
                phone: "",
                email: "",
                direction: "",
                classroom: '',
                department: '',
                number: ''
            }, 
    }
'''


def s_s_view_own_info(data):
    sql = "select name, number, email, phone, department, classroom, direction from StudentInfo where account = '%s';"
    baser = DatabaseDeal()
    results, status = baser.select(sql % (data['account']))
    results = results.iloc[0].to_dict()
    return results, status


'''
:params
    data: {
        name: "",
        phone: "",
        email: "",
        direction: "",
        classroom: '',
        department: '',
        number: ''
    }

:return 
    {
        status: ''
    }
'''


def s_s_submit_own_info(data):
    sql = "update StudentInfo set name = '%s', number = '%s', email = '%s', phone = '%s', department = '%s', " \
          "classroom = '%s', direction = '%s' where account = '%s';"
    baser = DatabaseDeal()
    results, status = baser.insert_like(sql=sql % (
        data['name'], data['number'], data['email'], data['phone'], data['department'], data['classroom'],
        data['direction'], data['account']))
    print(results, status)
    return results, status


'''
:params

:return 
    {
        status: '',
        ress: [
            {
                week: '',
                weekday: '',
                segment: '',
                t_name: '',
                place: '',
                tips: '',
                serial: 
            },
            ...
        ]
    }
'''


def s_seek_reservation(data):
    sql = "select week, weekday, segment, place, t_name, tips, concat(serial) as serial from ReservationInfo where s_account is null;"
    baser = DatabaseDeal()
    temp_ress, status = baser.select(sql=sql)
    print('temp_ress: ', temp_ress)
    ress = []
    for i in range(0, temp_ress.shape[0]):
        print(temp_ress.iloc[i].to_dict())
        ress.append(temp_ress.iloc[i].to_dict())
    print('ress: ', ress)
    return ress, status


'''
:params
    data: {
        account: '',
        serial: '',
        reason: ''
    }
    
:return 
    {
        status
    }
'''


def s_s_release_reservation(data):
    sql = "update ReservationInfo set s_account = '%s', reason = '%s' where serial = '%s';"
    baser = DatabaseDeal()
    results, status = baser.insert_like(sql=sql % (data['account'], data['reason'], data['serial']))
    if status == 201:
        return results, status
    sql_update_name = "update ReservationInfo set s_name = (select name from StudentInfo where account = " \
                      "ReservationInfo.s_account) where s_name is null;"
    results, status = baser.insert_like(sql_update_name)
    return results, status


'''
:params
    data: {
        account: ''
    }

:return 
    {
        'status': '',
        ress: [
            {
                week: '',
                weekday: '',
                segment: '',
                t_name: '',
                place: '',
                reason: '',
                tips: '',
            },
            ...
        ]
    }
'''


def s_s_view_reservation(data):
    sql = "select week, weekday, segment, concat(serial) as serial, t_name, place, reason, tips from ReservationInfo where s_account = '%s';"
    baser = DatabaseDeal()
    results, status = baser.select(sql % (data['account']))
    ress = []
    for i in range(0, results.shape[0]):
        ress.append(results.iloc[i].to_dict())
    return ress, status
import pandas as pd
import pymysql
from utils import DatabaseDeal
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
    print('s submit own info data: ', data)
    sql = "update StudentInfo set name = '%s', number = '%s', email = '%s', phone = '%s', department = '%s', " \
          "classroom = '%s', direction = '%s' where account = '%s';"
    baser = DatabaseDeal()
    results, status = baser.insert_like(sql=sql % (
        data['name'], data['number'], data['email'], data['phone'], data['department'], data['classroom'],
        data['direction'], data['account']))

    if status == 200:
        sql = "update ReservationInfo set s_name = (select name from StudentInfo where account = '%s') where s_account = '%s';"
        results, status = baser.insert_like(sql=sql % (data['account'], data['account']))
    print('s submit own info: status: ', status, 'results: ', results)
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
    sql = "select week, weekday, segment, place, t_name, t_email, t_phone, tips, concat(serial) as serial, concat(is_canceled) as is_canceled, " \
          "concat(is_finished) as is_finished from ReservationInfo where s_account is null and is_canceled != '3';"
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
    print('s view reservation data: ', data)
    sql = "select week, weekday, segment, concat(serial) as serial, t_name, place, reason, tips, concat(is_canceled) as is_canceled, concat(is_finished) as is_finished from ReservationInfo where s_account = '%s' and is_canceled != 3 and is_finished = 0 order by week asc, weekday asc, segment asc;"
    baser = DatabaseDeal()
    results, status = baser.select(sql % (data['account']))
    ress = []
    for i in range(0, results.shape[0]):
        ress.append(results.iloc[i].to_dict())
    print('s view reservation ress: ', ress, 'status: ', status)
    return ress, status


'''
学生查询考试情况

:params
    data: {
        
    }

:return 
    {
        status: '',
        exams: {
            {
                start: '',
                end: '',
                t_name: '',
                place: '',
                e_name: '' // 考试名称
            }
        }
    }
'''


def s_seek_exams(data):
    print('s_seek_exams data: ', data)
    sql = "select concat(serial) as serial, start, end, t_name, e_name, place, week, weekday from ExamInfo;"
    baser = DatabaseDeal()
    results, status = baser.select(sql=sql)
    exams = []
    for i in range(0, results.shape[0]):
        exams.append(results.iloc[i].to_dict())
    print('s seek exams exams: ', exams)
    return exams, status


'''
学生添加考试信息
:params
    data: {
        account: '', // student
        serial: '',  // exam
    }

:return 
    {
        status: ''
    }
'''


def s_add_exam(data):
    print('s add exam data: ', data)
    sql = "insert into StudentExam(s_account, e_serial) values ('%s', '%s');"
    baser = DatabaseDeal()
    results, status = baser.insert_like(sql=sql % (data['account'], data['serial']))
    print('s add exam status: ', status)
    return results, status


'''
学生查看自己的考试信息
:params
    data: {
        account: '' // student
    }

:return 
    {
        status: '',
        exams: [
            {
                start: '',
                end: '',
                t_name: '',
                e_name: '',
                place: '',
                serial: ''
            },
            ...
        ]
    }
'''


def s_view_own_exams(data):
    print('s view own exams data: ', data)
    sql = "select concat(ExamInfo.serial) as serial, week, weekday, e_name, t_name, start, end, place from ExamInfo inner join StudentExam on StudentExam.e_serial = ExamInfo.serial where StudentExam.s_account = '%s' and StudentExam.is_finished = '0' order by week asc, weekday asc, start asc;"
    baser = DatabaseDeal()
    results, status = baser.select(sql=sql % (data['account']))

    exams = []
    for i in range(0, results.shape[0]):
        exams.append(results.iloc[i].to_dict())
    print('s view own exams status: ', status, 'exams: ', exams)

    return exams, status


'''
12 完成考试

接口名
    s_finish_exam

:params 
    data: {
        account: '',
        serial: ''
    }

:return
    {
        status
    }
'''


def s_s_finish_exam(data):
    print('s s finish exam data: ', data)
    baser = DatabaseDeal()
    sql = "update StudentExam set is_finished = '1' where s_account = '%s' and e_serial = '%s';"
    try:
        results, status = baser.insert_like(sql % (data['account'], data['serial']))
    except Exception as e:
        results, status = None, 500
        print('s s finish exam error!', e)
    print('s s finish exam results: ', results, 'status: ', status)
    return results, status


'''
15 获取已完成的考试信息
接口名
    s_view_finish_exam

:params
    data: {
        account: ''
    }

:return 
    {
        status: '',
        exams: [
            {
                start: '',
                end: '',
                t_name: '',
                e_name: '',
                place: '',
                serial: ''
            },
            ...
        ]
    }
'''


def s_s_view_finish_exam(data):
    print('s s view finish exam data: ', data)
    baser = DatabaseDeal()
    sql = "select concat(ExamInfo.serial) as serial, week, weekday, e_name, t_name, start, end, place from" \
          " ExamInfo inner join StudentExam on StudentExam.e_serial = ExamInfo.serial where StudentExam.s_account = '%s'" \
          " and StudentExam.is_finished = '1' order by week asc, weekday asc, start asc;"
    results, status = baser.select(sql=sql % (data['account']))

    exams = []
    for i in range(0, results.shape[0]):
        exams.append(results.iloc[i].to_dict())
    print('s s view finish exams status: ', status, 'exams: ', exams)
    return exams, status






from config import *
from utils import DatabaseDeal

"""
:params:
    data: {
        "account: ""
    }

:return 
    {
        status: "",
        info : {
                name: "",
                phone: "",
                email: "",
                introduction: "",
                direction: "",
                workplace: ""
        }
    }
"""


def t_t_view_own_info(data):
    sql = "select name, phone, email, introduction, direction, workplace from TeacherInfo where account = '%s'"
    baser = DatabaseDeal()
    results, status = baser.select(sql=sql % (data['account']))
    result = results.iloc[0].to_dict()
    return result, status


'''
:params
    data: {
        name: '',
        email: '',
        direction: '',
        introduction: '',
        workplace: '',
        phone: '',
        account: ''
    }

:return 
    {
        status: ''
    }
'''


def t_t_submit_own_info(data):
    print('t submit own info data: ', data)
    sql = "update TeacherInfo set name = '%s', introduction = '%s', direction = '%s', email = '%s', phone = '%s', " \
          "workplace = '%s' where account = '%s';"
    baser = DatabaseDeal()
    results, status = baser.insert_like(sql=sql % (
        data['name'], data['introduction'], data['direction'], data['email'], data['phone'], data['workplace'],
        data['account']))
    if status == 200:
        sql = "update ReservationInfo set t_name = (select name from TeacherInfo where account = '%s') where t_account = '%s';"
        results, status = baser.insert_like(sql=sql % (data['account'], data['account']))

    return results, status


'''
    :params
        data: {
            account: '',
            reservations: [
                {
                    week: int,
                    weekday: int,
                    segment: int,
                    place: '',
                    tips: ''
                },
                ...
            ]
        }

    :return
        {
            status: ''
        }
'''


def t_t_release_reservation(data):
    sql_insert = "insert into ReservationInfo (t_account, week, weekday, segment, place, tips) values ('%s', '%s', '%s', '%s', '%s', '%s');"
    baser = DatabaseDeal()
    ress = data['reservations']
    results = None
    status = None
    for res in ress:
        results, status = baser.insert_like(
            sql_insert % (data['account'], res['week'], res['weekday'], res['segment'], res['place'], res['tips']))
        if status == 201:
            return results, status
    sql_update = "update ReservationInfo set t_name = (select name from TeacherInfo where TeacherInfo.account = ReservationInfo.t_account) where t_name is null;"
    results, status = baser.insert_like(sql=sql_update)
    return results, status


'''
:params:
    data: {
        account: ''
    }
    
    :return 
        {
            status: '',
            ress:  [
                {
                    week: '第1周',
                    weekday: '周五',
                    segment: '10:30 ~ 11:00',
                    student: '***',
                    place: '宋健一号院北***',
                    reason: '答疑',
                    score: str,
                    tips: '',
                },
                ...
            ]
        }
'''


def t_t_view_reservation(data):
    sql = "select week, weekday, segment, s_name as student, place, reason, tips, concat(is_canceled) as is_canceled, concat(is_finished) as is_finished, concat(serial) as serial, concat(score) as score from ReservationInfo where t_account = '%s' and is_canceled != 3 and is_finished = 0;"
    baser = DatabaseDeal()
    temp_ress, status = baser.select(sql=sql % data['account'])
    ress = []
    for i in range(0, temp_ress.shape[0]):
        ress.append(temp_ress.iloc[i].to_dict())
    print('t view reservation ress: ', ress)
    return ress, status


'''
教师发布考试信息

:params
    data: {
        account: '',
        week: '',
        weekday: '',
        e_name: '',
        start: '',
        end: '',
        place: '',
        tips: ''
    }

:return 
    {
        status: ''
    }
'''


def t_release_exam(data):
    print('t_release_exam: ', data)

    sql = "insert into ExamInfo (t_account, e_name, week, weekday, start, end, place, tips) values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');"
    baser = DatabaseDeal()
    results, status = baser.insert_like(
        sql=sql % (
            data['account'], data['e_name'], data['week'], data['weekday'],
            data['start'].replace('T', ' ').replace('.000Z', ''), data['end'].replace('T', '').replace('.000Z', ''),
            data['place'], data['tips']))

    if status == 200:
        # 更新，向表中插入姓名
        sql_update = "update ExamInfo set t_name = (select name from TeacherInfo where TeacherInfo.account = ExamInfo.t_account) where t_name = '';"
        results, status = baser.insert_like(sql=sql_update)
    print('t_release_exam status: ', status, '\n\tresults: ', results)
    return results, status


'''
教师查看自己发布的考试内容

:params
    data: {
        account: '' // 教师
    }

:return 
    {
        status: '',
        exams: [
            {
                'name': '', // 考试名
                'place': '',
                start: '',
                end: '',
                week: '',
                weekday: '',
                tips: ''
            }
        ]
    }

'''


def t_view_own_release_exams(data):
    print('t view own release exams data: ', data)
    baser = DatabaseDeal()
    sql = "select e_name as name, start, end, week, weekday, place, tips, concat(serial) as serial from ExamInfo where t_account = '%s' order by week asc, weekday asc, start asc;"
    results, status = baser.select(sql=sql % data['account'])

    exams = []
    for i in range(0, results.shape[0]):
        exams.append(results.iloc[i].to_dict())
    print('t view own release exams status: ', status, 'results', results)
    return exams, status


'''

14 修改发布的考试

接口名
    edit_exam

:params 
    data: {
        account: '',
        week: '',
        weekday: '',
        e_name: '',
        start: '',
        end: '',
        place: '',
        serial: ''
    }

:return 
    {
        status: ''
    }
'''


def t_edit_exam(data):
    print('t edit exam data: ', data)
    baser = DatabaseDeal()
    sql = "update ExamInfo set e_name = '%s', start = '%s', end = '%s', place = '%s', week = '%s', weekday = '%s', tips = '%s' where serial = '%s';"
    try:
        results, status = baser.insert_like(sql % (
        data['e_name'], data['start'], data['end'], data['place'], data['week'], data['weekday'], data['tips'],
        data['serial']))
    except Exception as e:
        results, status = None, 500
        print('t edit exam error!', e)

    return results, status

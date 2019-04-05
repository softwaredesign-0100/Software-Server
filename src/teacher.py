from config import *
from deal_database import DatabaseDeal

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
    sql = "update TeacherInfo set name = '%s', introduction = '%s', direction = '%s', email = '%s', phone = '%s', " \
          "workplace = '%s' where account = '%s';"
    baser = DatabaseDeal()
    results, status = baser.insert_like(sql=sql % (
        data['name'], data['introduction'], data['direction'], data['email'], data['phone'], data['workplace'],
        data['account']))
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
                    tips: '',
                },
                ...
            ]
        }
'''


def t_t_view_reservation(data):
    sql = "select week, weekday, segment, s_name as student, place, reason, tips from ReservationInfo where t_account = '%s';"
    baser = DatabaseDeal()
    temp_ress, status = baser.select(sql=sql % data['account'])
    ress = []
    for i in range(0, temp_ress.shape[0]):
        ress.append(temp_ress.iloc[i].to_dict())
    print('ress: ', ress)
    return ress, status



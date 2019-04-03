from sanic import Sanic
from sanic.response import text
from sanic.response import json
from sanic import response
import ssl
import pymysql
import collections
import json as js

app = Sanic()

'''
#create SSL passport --支持SSL证书 
app = Sanic()
context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain("./1_www.qidu1998.cn_bundle.crt", keyfile="./2_www.qidu1998.cn.key")
'''

def db_submit_per_info(data):
    print(data)
    print('there is submit_per_info')
    status = 201
    db = pymysql.connect("167.179.72.48","root","root","Software_Project" )
    cur = db.cursor()    
    if data["identify"] == "teacher":
        sql = "update TeacherInfo set t_name = '%s', t_workplace = '%s', \
            t_introduction = '%s', t_email = '%s',\
             t_direction = '%s', t_phone = '%s' where t_account = '%s'" % (data['name'], data['workplace'], data['introduction'], \
                 data['email'], data['direction'], data['phone'], data['account'])
    else:
        # sql = "update StudentInfo set s_name = '%s', s_introduction = '%s', s_classroom = '%s',\
        # s_number = '%s', s_email = '%s', s_direction = '%s', s_phone = '%s' where s_account = '%s'" % (\
            # data['name'], data['introduction'], data['classroom'], data['number'],\
            # data['email'], data['direction'], data['phone'], data['account'])
        sql = "update StudentInfo set s_name = '%s', s_classroom = '%s', s_number = '%s', s_email = '%s', s_direction = '%s', s_phone = '%s', s_department = '%s' where s_account = '%s'" % (data['name'], data['classroom'], data['number'], data['email'], data['direction'], data['phone'], data['department'], data['account'])
    print('submit_per_info sql: ', sql)

    try:
        cur.execute(sql)
        db.commit()
    except Exception as e:
        db.rollback()
        status = 500
        print(e)
    else:
        status = 200
    finally:
        db.close()
    print('sub per info finish ')
    return status, 0

# def db_submit_per_info(data):
#     print(data)
#     status = 201
#     db = pymysql.connect("167.179.72.48", "root", "root", "Software_Project" )
#     cur = db.cursor()    
#     if data["identify"] == "teacher":
#         sql = "update TeacherInfo set t_name = '%s', t_workplace = '%s', \
#             t_introduction = '%s', t_email = '%s',\
#              t_direction = '%s', t_phone = '%s' where t_account = '%s'" % (data['name'], data['workplace'], data['introduction'], \
#                  data['email'], data['direction'],data['phone'], data['account'])
#     else:
#         sql = "update StudentInfo set s_name = '%s', s_introduction = '%s', s_classroom = '%s',\
#         s_number = '%s', s_email = '%s', s_direction = '%s'，s_phone = '%s' where s_account = '%s'" % (\
#             data['name'], data['introduction'], data['classroom'], data['number'],\
#             data['email'], data['direction'], data['phone'], data['account'])

#     print('submit_per_info sql: ', sql)

#     try:
#         cur.execute(sql)
#         db.commit()
#     except Exception as e:
#         db.rollback()
#         status = 500
#         print(e)
#     else:
#         status = 200
#     finally:
#         db.close()
#     print('sub per info finish ')
#     return status, 0



def db_get_t_info(data):
    print('there is get t info')
    print(data)
    db = pymysql    
    status = 201
    db = pymysql.connect("167.179.72.48","root","root","Software_Project" )
    cur = db.cursor()    

    account = data['account']

    sql = "select t_name, t_phone, t_email, t_workplace, t_direction, t_introduction from TeacherInfo where t_account = '%s'" % account

    print('get t info sql: %s' %sql)

    results = {}
    try:
        cur.execute(sql)
        info = cur.fetchall()[0]
        results = {
            'name': info[0],
            'phone': info[1],
            'email': info[2],
            'workplace': info[3],
            'direction':info[4],
            'introduction': info[5]
        }
    except Exception as e:
        print('get t info error: ', e)
        status = 201
    else:
        status = 200
    finally:
        db.close()

    return status, results


def db_get_s_info(data):
    print('there is get s info')
    db = pymysql    
    status = 201
    db = pymysql.connect("167.179.72.48","root","root","Software_Project" )
    cur = db.cursor()    

    account = data['account']

    sql = "select s_name, s_phone, s_email, s_direction, s_number, s_classroom, s_department from StudentInfo where s_account = '%s'" % account

    print('get s info sql: %s' %sql)

    try:
        cur.execute(sql)
        info = cur.fetchall()[0]
        results = {
            'name': info[0],
            'phone': info[1],
            'email': info[2],
            'direction': info[3],
            'number': info[4],
            'classroom': info[5],
            'department': info[6]
        }
        status = 200
    except Exception as e:
        print('get t info error: ', e)
        status = 201
    finally:
        db.close()
    return status, results

    
def db_sign_up(data):
    status = 201
    db = pymysql.connect("167.179.72.48","root","root","Software_Project" )
    cur = db.cursor()
    if data["identify"] == "teacher":
        tablename = "TeacherInfo"
        id_name = "t_account"
        password_name = "t_password"
    else:
        tablename = "StudentInfo"
        id_name = "s_account"
        password_name = "s_password"
    sql = "insert into {0} ({1}, {2}) values ('{3}', '{4}')".format(tablename, id_name, password_name, data['account'], data['password'])
    print(sql)
    try:    
        cur.execute(sql)
        db.commit()
    except:
        db.rollback()
        status = 500
    else:
        status = 200

    finally:
        db.close()
    print(status)
    return status

def db_sign_in(data):
    status = 201
    db = pymysql.connect("167.179.72.48","root","root","Software_Project" )
    cur = db.cursor()
    if data["identify"] == "teacher":
        tablename = "TeacherInfo"
        id_name = "t_account"
        password_name = "t_password"
        name_name = "t_name"
    else:
        tablename = "StudentInfo"
        id_name = "s_account"
        password_name = "s_password"
        name_name = "s_name"
    sql = "select {0}, {1} from {2} where {3} = '{4}'".format(password_name, name_name, tablename, id_name, data["account"])
    print(sql)
    try:    
        cur.execute(sql)
        results = cur.fetchall()
        print(results)
    except:
        status = 500
    else:
        if len(results) == 0:
            status = 404
        else:
            password = results[0][0]
            name = results[0][1]
            if password != data["password"]:
                status = 403
            elif name == "":
                status = 401
            else:
                status = 200
    sql_get_name = "select %s from %s where %s = '%s'" % (name_name, tablename, id_name, data['account'])
    try:
        cur.execute(sql_get_name)
        results = cur.fetchall()
        target_name = results[0][0]
        if target_name is None:
            status = 401
    except Exception as e:
        print(e)
        db.rollback()

    finally:
        db.close()
    print('sign in statue: %d' % status)
    return status

def db_change_password(data):
    print('prepare change password')
    print(data)
    status = 201
    db = pymysql.connect("167.179.72.48","root","root","Software_Project" )
    cur = db.cursor()
    if data["identify"] == "teacher":
        tablename = "TeacherInfo"
        id_name = "t_account"
        password_name = "t_password"
    else:
        tablename = "StudentInfo"
        id_name = "s_account"
        password_name = "s_password"
    sql = "select {0} from {1} where {2} = '{3}'".format(password_name, tablename, id_name, data["account"])
    print(sql)
    try:
        cur.execute(sql)
        results = cur.fetchall()
    except:
        status = 500
    else:
        print(results)
        password = results[0][0]
        print(data['old_password'])
        print(password)
        print(password == data['old_password'])
        if password != data["old_password"]:
            status = 403
        else:
            sql = "update {0} set {1} = '{2}' where {3} = '{4}'".format(tablename, password_name, data["new_password"], id_name, data["account"])
            print(sql)
            try:    
                cur.execute(sql)
                db.commit()
            except:
                db.rollback()
            else:
                status = 200
    finally:
        db.close()
    print(status)
    return status

def db_person_info(data):
    status = 201
    db = pymysql.connect("127.0.0.1","root","123456","Software_Project" )
    cur = db.cursor()
    if data["identify"] == "teacher":
        tablename = "TeacherInfo"
        account_name = "t_id"
        name_name = "t_name"
        name_number = "t_number"
        name_department = "t_department"
        name_direction = "t_direction"
        name_email = "t_email"
        name_phone = "t_phone"
        name_workplace =  "t_workplace"
        name_introduction =  "t_introduction"
        sql = "update {0} set {1} = '{2}', \
            {3} = '{4}', {5} = '{6}', {7} = '{8}', \
            {9} = '{10}', {11} = '{12}', {13} = '{14}', \
            {15} = '{16}', where {17} = '{18}'".format(\
                tablename, \
                name_name, data['name'] , \
                name_number, data['number'] , \
                name_department, data['department'] , \
                name_direction, data['direction'] , \
                name_email, data['email'] , \
                name_phone, data['phone'] , \
                name_workplace, data['workplace'] , \
                name_introduction, data['introduction'], \
                account_name, data["account"])
        print(sql)
    else:
        tablename = "StudentInfo"
        account_name = "s_id"
        name_name = "s_name"
        name_number = "s_number"
        name_department = "s_department"
        name_direction = "s_direction"
        name_classroom = "s_classroom"
        name_email = "s_email"
        name_phone = "s_phone"
        name_workplace =  "s_workplace"
        name_introduction =  "s_introduction"        
        sql = "update {0} set {1} = '{2}', \
            {3} = '{4}', {5} = '{6}', {7} = '{8}', \
            {9} = '{10}', {11} = '{12}', {13} = '{14}', \
            {15} = '{16}', {17} = '{18}',  where {19} = '{20}'".format(\
                tablename, \
                name_name, data['name'] , \
                name_number, data['number'] , \
                name_department, data['department'] , \
                name_direction, data['direction'] , \
                name_classroom, data['classroom'] , \
                name_email, data['email'] , \
                name_phone, data['phone'] , \
                name_workplace, data['workplace'] , \
                name_introduction, data['introduction'], \
                account_name, data["account"])
        print(sql)
    try:    
        cur.execute(sql)
        db.commit()
    except:
        db.rollback()
        status = 500
    else:
        status = 200
    finally:
        db.close()
    print(status)
    return status

def db_show_t_info(data):
    status = 201
    db = pymysql.connect("167.179.72.48","root","root","Software_Project" )
    cur = db.cursor()
    if data["identify"] == "teacher":
        tablename = "TeacherInfo"
        id_name = "t_account"
        password_name = "t_password"
    else:
        tablename = "StudentInfo"
        id_name = "s_account"
        password_name = "s_password"
    sql = "select {0} from {1} where {2} = '{3}'".format(password_name, tablename, id_name, data["account"])
    print(sql)
    try:    
        cur.execute(sql)
        results = cur.fetchall()
        print(results)
    except:
        status = 500
    else:
        if len(results) == 0:
            status = 404
        else:
            password = results[0][0]
            print(password)
            print(password == data['password'])
            if password != data["password"]:
                status = 403
            else:
                status = 200
    finally:
        db.close()
    print(status)
    return status

def db_t_release_reservation(data):
    print(data)
    status = 201
    db = pymysql.connect("167.179.72.48","root","root","Software_Project" )
    cur = db.cursor()
    tablename = "TeacherInfo"
    id_name = "t_account"
    teacher_name = "t_name"
    week_name = "week"
    weekday_name = "weekday"
    segment_name = "segment"
    place_name = "place"
    tips_name = "tips"
    current_teacher_name = ""

    sql = "select {0} from {1} where {2} = '{3}'".format(\
        teacher_name, tablename, id_name, data['account'])
    print(sql)
    try:    
        cur.execute(sql)
        results = cur.fetchall()
    except Exception as e:
        print(e)
        status = 500
    else:
        if len(results) == 0:
            status = 404
        else:
            current_teacher_name = results[0][0]
            password = results[0][0]
            status = 200
    if status != 200:
        return status

    tablename = "ReservationInfo"
    reservations = data['reservations']
    status = 200
    for reservation in reservations:
        print(reservation)
        print(type(reservation))
        sql = "insert into {0} ({1}, {2}, {3}, {4}, {5}, {6}, {7}) \
        values ('{8}', '{9}', '{10}', '{11}', '{12}', '{13}', '{14}')".format(\
            tablename, id_name, teacher_name, week_name, weekday_name, segment_name, place_name, tips_name, \
            data['account'], current_teacher_name, reservation['week'], reservation['weekday'], reservation['segment'], reservation['place'], reservation['tips'])
        print(sql)
        try:    
            cur.execute(sql)
            db.commit()
        except Exception as e:
            print(e)
            db.rollback()
            status = 500
            status = 401
    db.close()
    print(status)
    return status

def db_s_release_reservation(data):
    status = 201
    db = pymysql.connect("167.179.72.48","root","root","Software_Project" )
    cur = db.cursor()

    sql = "update ReservationInfo set s_account = '%s', reason = '%s', s_name = '%s' where serial = %d" 

    sql_get_name = "select s_name from StudentInfo where s_account = '%s'" % data['account']

    try:
        cur.execute(sql_get_name)
        
        name = cur.fetchall()
        print('results: ', name)
        name = name[0][0]
        cur.execute(sql % (data['account'], data['reason'], name, data['serial']))
        print('name: ', name)
        print('s release sql: ', sql % (data['account'], data['reason'], name, data['serial']))
        db.commit()
    except Exception as e:
        status = 500
    else:
        status = 200
    finally:
        db.close()
    return status 
    # tablename = "ReservationInfo"
    # id_name = "s_account"
    # serial_name = "serial"
    # reason_name = "reason"

    # sql = "update {0} set {1} = '{2}', \
    # {3} = '{4}' where {5} = '{6}'".format(\
    #     tablename, id_name, data['account'], reason_name, data['reason'], serial_name, data['serial'])
    # print(sql)
    # try:    
    #     cur.execute(sql)
    #     db.commit()
    # except Exception as e:
    #     print(e)
    #     db.rollback()
    #     status = 500
    # else:
    #     status = 200
    # finally:
    #     db.close()
    # print(status)
    return status

def db_seek_reservation(data):
    status = 201
    db = pymysql.connect("167.179.72.48","root","root","Software_Project" )
    cur = db.cursor()
    tablename = "ReservationInfo"
    id_name_t = "t_account"
    id_name_s = "s_account"
    serial_name = "serial"
    week_name = "week"
    weekday_name = "weekday"
    segment_name = "segment"
    teacher_name = "t_name"
    place_name = "place"
    tips_name = "tips"
    results = []

    sql = 'select serial, week, weekday, segment, t_name, place, tips from ReservationInfo where s_name is null;'

    print('seek reservation sql: ', sql)

    try:
        cur.execute(sql)
        res = cur.fetchall()
        print('res: ', res)
        for i in res:
            results.append({
                'serial': i[0],
                'week': i[1],
                'weekday': i[2],
                'segment': i[3],
                't_name': i[4],
                'place': i[5],
                'tips': i[6]
            })
        status = 200
    except Exception as e:
        print(e)
        status = 500
    finally:
        db.close()
    return status, results

    # sql = "select {0}, {1}, {2}, {3}, {4}, {5}, {6} from {7} where {8} is not null".format(\
    #     serial_name, week_name, weekday_name, segment_name, teacher_name, place_name, tips_name, \
    #     tablename, id_name_s)
    # print(sql)
    # try:    
    #     cur.execute(sql)
    #     r_Info = cur.fetchall()
    #     r_Info = r_Info[0]
    # except Exception as e:
    #     print(e)
    #     status = 500
    # else:
    #     for r_info in r_Info:
    #         item = {}
    #         item[serial_name] = r_Info[0]
    #         item[week_name] = r_Info[1]
    #         item[weekday_name] = r_Info[2]
    #         item[segment_name] = r_Info[3]
    #         item[teacher_name] = r_Info[4]
    #         item[place_name] = r_Info[5]
    #         item[tips_name] = r_Info[6]
    #         results.append(item)
    #     status = 200
    # finally:
    #     db.close()
    # print(status)
    return status, results

def db_t_view_reservation(data):
    status = 201
    db = pymysql.connect("167.179.72.48","root","root","Software_Project" )
    cur = db.cursor()

    sql = "select week, weekday, segment, place, reason, s_name from ReservationInfo where t_account = '%s'" % data['account']

    results = {}
    try:
        cur.execute(sql)
        results = cur.fetchall()
        info = []
        for i in results:
            info.append({
                'week': i[0],
                'weekday': i[1],
                'segment': i[2],
                'place': i[3],
                'reason': i[4],
                'student': i[5]
            })
    except Exception as e:
        status = 500
    else:   
        status = 200
    finally:
        db.close()
    return status, info

    # tablename = "ReservationInfo"
    # serial_name = "serial"
    # week_name = "week"
    # weekday_name = "weekday"
    # segment_name = "segment"
    # t_account_name = "t_account"
    # s_account_name = "s_account"
    # s_name_name = "s_name"
    # s_number_name = "s_number"
    # s_department_name = "s_department"
    # s_direction_name = "s_direction"
    # s_classroom_name = "s_classroom"
    # s_email_name = "s_email"
    # s_phone_name = "s_phone"
    # reason_name = "reason"
    # place_name = "place"
    # request_cancel_name = "request_cancel"
    # results = []

    # sql = "select {}, {}, {}, {}, {}, {}, {} from {} where {} = '{}'".format(\
    #     serial_name, week_name, weekday_name, segment_name, reason_name, place_name, s_account_name, \
    #     tablename, t_account_name, data['account'])
    # print(sql)
    # try:    
    #     cur.execute(sql)
    #     r_Info = cur.fetchall()
    # except Exception as e:
    #     print(e)
    #     status = 500
    # else:
    #     tablename = "StudentInfo"
    #     for r_info in r_Info:
    #         if len(r_info) != 0:
    #             sql = "select {0}, {1}, {2}, {3}, {4}, {5}, {6} from {7} where {8} = '{9}'".format(\
    #                 s_name_name, s_number_name, s_department_name, s_direction_name, s_classroom_name, s_email_name, s_phone_name, \
    #                 tablename, s_account_name, r_info[6])
    #             print(sql)
    #             try:
    #                 cur.execute(sql)
    #                 s_Info = cur.fetchall()        
    #                 s_Info = s_Info[0]    
    #             except Exception as e:
    #                 print(e)
    #             else:
    #                 item={}
    #                 item[serial_name] = r_info[0]
    #                 item[week_name] = r_info[1]
    #                 item[weekday_name] = r_info[2]
    #                 item[segment_name] = r_info[3]
    #                 item[reason_name] = r_info[4]
    #                 item[place_name] = r_info[5]
    #                 item[s_name_name] = s_Info[0]
    #                 item[s_number_name] = s_Info[1]
    #                 item[s_department_name] = s_Info[2]
    #                 item[s_direction_name] = s_Info[3]
    #                 item[s_classroom_name] = s_Info[4]
    #                 item[s_email_name] = s_Info[5]
    #                 item[s_phone_name] = s_Info[6]
    #                 results.append(item)

    #     status = 200
    # finally:
    #     db.close()
    # print(status)


def db_s_view_reservation(data):
    status = 201
    db = pymysql.connect("167.179.72.48","root","root","Software_Project" )
    cur = db.cursor()
    tablename = "ReservationInfo"
    week_name = "week"
    weekday_name = "weekday"
    segment_name = "segment"
    s_account_name = "s_account"
    t_name_name = "t_name"
    reason_name = "reason"
    place_name = "place"
    tips_name = "tips"
    results = []

    sql = "select {}, {}, {}, {}, {}, {}, {} from {} where {} = '{}'".format(\
        week_name, weekday_name, segment_name, reason_name, place_name, tips_name, t_name_name, \
        tablename, s_account_name, data['account'])
    print(sql)
    try:    
        cur.execute(sql)
        r_Info = cur.fetchall()
    except Exception as e:
        print(e)
        status = 500
    else:
        for r_info in r_Info:
            if len(r_info) != 0:
                item={}
                item[week_name] = r_info[0]
                item[weekday_name] = r_info[1]
                item[segment_name] = r_info[2]
                item[reason_name] = r_info[3]
                item[place_name] = r_info[4]
                item[tips_name] = r_info[5]
                item[t_name_name] = r_info[6]
                results.append(item)
        status = 200
    finally:
        db.close()
    print(status)
    return status, results

@app.route("/sign_up", methods=['POST', 'GET'])
async def sign_up(request):
    data = request.json
    print(data)
    status = db_sign_up(data)
    return json({"status": status})

@app.route("/sign_in", methods=['POST', 'GET'])
async def sign_in(request):
    data = request.json
    status = db_sign_in(data)
    return json({"status": status})

@app.route("/change_password", methods=['POST', 'GET'])
async def change_password(request):
    data = request.json
    status = db_change_password(data)
    return json({"status": status})

@app.route("/person_info", methods=['POST', 'GET'])
async def person_info(request):
    data = request.json
    status = db_person_info(data)
    return json({"status": status})

@app.route("/show_t_info", methods=['POST', 'GET'])
async def show_t_info(request):
    data = request.json
    status = db_show_t_info(data)
    return json({"status": status})

@app.route("/t_release_reservation", methods=['POST', 'GET'])
async def t_release_reservation(request):
    data = request.json
    status = db_t_release_reservation(data)
    return json({"status": status})

@app.route("/s_release_reservation", methods=['POST', 'GET'])
async def s_release_reservation(request):
    data = request.json
    status = db_s_release_reservation(data)
    return json({"status": status})
    
@app.route("/seek_reservation", methods=['POST', 'GET'])
async def seek_reservation(request):
    data = request.json
    status, results = db_seek_reservation(data)
    return json({"status": status, "results": results})

@app.route("/t_view_reservation", methods=['POST', 'GET'])
async def t_view_reservation(request):
    data = request.json
    status, results = db_t_view_reservation(data)
    return json({"status": status, "results": results})

@app.route("/s_view_reservation", methods=['POST', 'GET'])
async def s_view_reservation(request):
    data = request.json
    status, results = db_s_view_reservation(data)
    return json({"status": status, "results": results})

@app.route("/get_t_info", methods=["POST", "GET"])
async def get_t_info(request):
    data = request.json
    status, results = db_get_t_info(data)
    return json({'status': status, 'info': results})

@app.route("/get_s_info", methods=["POST", "GET"])
async def get_s_info(request):
    data = request.json
    status, results = db_get_s_info(data)
    return json({'status': status, 'info': results})

@app.route('submit_per_info', methods=["POST", 'GET'])
async def submit_per_info(request):
    data = request.json
    status, results = db_submit_per_info(data)
    return json({'status': status, 'results': results})

if __name__ == "__main__":
    #app.run(host="0.0.0.0", port=3328, ssl=context)
    app.run(host="0.0.0.0", port=3328)
#nohup python3 /home/zhaodd/sanic/sanic_test.py >> /home/zhaodd/sanic/output.log 2>&1 &




from sanic import Sanic
from sanic.response import json
from sanic.response import text
from sanic import response
import ssl
import pymysql
import collections

from common import *
from student import *
from teacher import *

app = Sanic()


# ------------------------------------------- common --------------------------------------------#
@app.route('/sign_up', methods=['POST', 'GET'])
async def sign_up(request):
    data = request.json
    results, status = c_sign_up(data)
    return json({'status': status})


@app.route('/sign_in', methods=['POST', 'GET'])
async def sign_in(request):
    data = request.json
    results, status = c_sign_in(data)
    return json({'status': status})


@app.route('/change_password', methods=['POST', 'GET'])
async def change_password(request):
    data = request.json
    results, status = c_change_password(data)
    return json({'status': status})


@app.route('/initiate_cancel', methods=['POST', 'GET'])
async def initiate_cancel(requests):
    data = requests.json
    results, status = c_initiate_cancel(data)
    return json({'status': status})


@app.route('/ensure_cancel', methods=['POST', 'GET'])
async def ensure_cancel(requests):
    data = requests.json
    results, status = c_ensure_cancel(data)
    return json({'status': status})


# ------------------------------------------- teacher --------------------------------------------#
@app.route('/t_view_own_info', methods=['POST', 'GET'])
async def t_view_own_info(request):
    data = request.json
    results, status = t_t_view_own_info(data)
    return json({'info': results, 'status': status})


@app.route('/t_submit_own_info', methods=['POST', 'GET'])
async def t_submit_own_info(request):
    data = request.json
    results, status = t_t_submit_own_info(data)
    return json({'status': status})


@app.route('/t_release_reservation', methods=['POST', 'GET'])
async def t_release_reservation(request):
    data = request.json
    results, status = t_t_release_reservation(data)
    return json({'status': status})


@app.route('/t_view_reservation', methods=['POST', 'GET'])
async def t_view_reservation(request):
    data = request.json
    results, status = t_t_view_reservation(data)
    return json({'status': status, 'ress': results})


@app.route('/release_exam', methods=['POST', 'GET'])
async def release_exam(request):
    data = request.json
    results, status = t_release_exam(data)
    return json({'status': status})


@app.route('/view_own_release_exams', methods=['POST', 'GET'])
async def view_own_release_exams(request):
    data = request.json
    results, status = t_view_own_release_exams(data)
    return json({'status': status, 'exams': results})


# ------------------------------------------- student --------------------------------------------#
@app.route('/s_view_own_info', methods=['POST', 'GET'])
async def s_view_own_info(request):
    data = request.json
    results, status = s_s_view_own_info(data)
    return json({'status': status, 'info': results})


@app.route('/s_submit_own_info', methods=['POST', 'GET'])
async def s_submit_own_info(request):
    data = request.json
    results, status = s_s_submit_own_info(data)
    return json({'status': status})


@app.route('/seek_reservation', methods=['POST', 'GET'])
async def seek_reservation(request):
    data = request.json
    results, status = s_seek_reservation(data)
    return json({'status': status, 'ress': results})


@app.route('/s_release_reservation', methods=['POST', 'GET'])
async def s_release_reservation(request):
    data = request.json
    results, status = s_s_release_reservation(data)
    return json({'status': status})


@app.route('/s_view_reservation', methods=['POST', 'GET'])
async def s_view_reservation(request):
    data = request.json
    results, status = s_s_view_reservation(data)
    return json({'status': status, 'ress': results})


@app.route('/seek_exams', methods=['POST', 'GET'])
async def seek_exams(request):
    data = request.json
    results, status = s_seek_exams(data)
    return json({'status': status, 'exams': results})


@app.route('/add_exam', methods=['POST', 'GET'])
async def add_exam(request):
    data = request.json
    results, status = s_add_exam(data)
    return json({'status': status})


@app.route('/view_own_exams', methods=['POST', 'GET'])
async def view_own_exams(request):
    data = request.json
    results, status = s_view_own_exams(data)
    return json({'status': status, 'exams': results})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3328)

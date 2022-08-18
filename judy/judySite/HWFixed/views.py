from curses import noecho
from http import HTTPStatus
from django.shortcuts import render
from django.http import HttpResponse
import json
from .models import DiskChange, GpuChange, NodeChange, NodeFixed, DiskFixed, GpuFixed

import pymysql
import paramiko
import time
from DataParsig.main import AdminDB

# Create your views here.

change_table = None

# ssh 변수
ssh1 = None
ssh2 = None

admindb1 = None
admindb2 = None

cur = None
conn = None


def index(request):
    return HttpResponse("<p>HW Info<p>")


def HWFixedInfo(request):

    global admindb1
    global admindb2

    global conn

    connectDB()

    try:
        admindb1.fixed_insert_db()
        admindb2.fixed_insert_db()
        print("fixed insert done!")

    except:
        conn.close()
        print("Wrong")

    data = load_data(0)

    return render(request, 'HWFixed/HWFixedInfo.html', data)


def HWChangeInfo(request):
    global admindb1
    global admindb2

    global conn

    connectDB()

    try:
        while(True):
            admindb1.change_insert_db()
            admindb2.change_insert_db()
            print("fixed insert done!")

            time.sleep(5)

    except:
        conn.close()
        print("Wrong")

    data = load_data(1)

    return render(request, 'HWChange/HWChangeInfo.html', data)


def load_refresh(request):

    global change_table

    data = {
        'node_result': None,
        'disk_result': None,
        'gpu_result': None,
    }

    node_result = list(NodeChange.objects.all().order_by('created_at'))
    disk_result = list(DiskChange.objects.all().order_by('create_at'))
    gpu_result = list(GpuChange.objects.all().order_by('created_at'))

    if (change_table != None):
        if (len(change_table['node_result']) < len(node_result)):
            print("change_table_node: ", change_table['node_result'])
            difference = len(node_result) - len(change_table['node_result'])

            for i in range(difference):
                data['node_result'].append(node_result.pop())

            change_table['node_result'] = node_result

        if (len(change_table['disk_result']) < len(disk_result)):
            difference = len(disk_result) - len(change_table['disk_result'])

            for i in range(difference):
                data['disk_result'].append(disk_result.pop())

            change_table['disk_result'] = disk_result

        if (len(change_table['gpu_result']) < len(gpu_result)):
            difference = len(gpu_result) - len(change_table['gpu_result'])

            for i in range(difference):
                data['gpu_result'].append(gpu_result.pop())

            change_table['gpu_result'] = gpu_result

        print(data)

    else:
        print("Change Table is None!")
        return HttpResponse(HTTPStatus.CONFLICT)

    return HttpResponse(json.dumps(data, default=str), content_type="application/json")


def load_data(mode):

    if (mode == 0):  # fixed
        node_result = NodeFixed.objects.all().order_by('ip')
        gpu_result = GpuFixed.objects.all().order_by('ip')
        disk_result = DiskFixed.objects.all().order_by('ip')

        data = {
            'node_result': node_result,
            'gpu_result': gpu_result,
            'disk_result': disk_result
        }
        return data

    elif (mode == 1):  # change
        node_result = list(NodeChange.objects.all().order_by('created_at'))
        disk_result = list(DiskChange.objects.all().order_by('create_at'))
        gpu_result = list(GpuChange.objects.all().order_by('created_at'))

        data = {
            'node_result': node_result,
            'disk_result': disk_result,
            'gpu_result': gpu_result
        }

        global change_table
        change_table = data

        return data

    else:
        print("Wrong data")
        return


def connectDB():

    global ssh1
    global ssh2

    global admindb1
    global admindb2

    global cur
    global conn

    # 웹페이지에 들어가는 순간 값 받기 시작
    conn = pymysql.connect(host='localhost', user='root',
                                password='baro', db='judy', charset='utf8')
    cur = conn.cursor()

    ssh1 = paramiko.SSHClient()
    ssh1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh1.connect("192.168.20.114", port='22',  # 고객이 자신의 ip를 안다고 가정하에 '115'부분을 바꿈, 그러면 고객의 node에서 115로 가져올 수 있음, 지금은 115로 자기자신과 연결
                 username="oem", password='baro')  # customer

    ssh2 = paramiko.SSHClient()
    ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh2.connect("192.168.20.115", port='22',  # 고객이 자신의 ip를 안다고 가정하에 '115'부분을 바꿈, 그러면 고객의 node에서 115로 가져올 수 있음, 지금은 115로 자기자신과 연결
                 username="oem", password='baro')  # customer

    admindb1 = AdminDB(conn, cur, ssh1)
    admindb2 = AdminDB(conn, cur, ssh2)

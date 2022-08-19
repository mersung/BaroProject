from datetime import datetime
from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .models import DiskChange, GpuChange, NodeChange, NodeFixed, DiskFixed, GpuFixed

import pymysql
import paramiko
from DataParsig.main import AdminDB

# Create your views here.

# ssh 변수
ssh1 = None
ssh2 = None

admindb1 = None
admindb2 = None


def index(request):
    return HttpResponse("<p>HW Info<p>")


def HWFixedInfo(request):

    global admindb1
    global admindb2

    connectDB()

    try:
        admindb1.fixed_insert_db()
        admindb2.fixed_insert_db()
        print("fixed insert done!")

    except:
        print("FIXED Wrong")

    data = load_data(0)

    return render(request, 'HWFixed/HWFixedInfo.html', data)


def HWChangeInfo(request):
    if (ssh1 != None):
        ssh1.close()

    if (ssh2 != None):
        ssh2.close()

    connectDB()
    return render(request, 'HWChange/HWChangeInfo.html')


def load_refresh(request):

    client = request.GET.get('client')
    global admindb1
    global admindb2

    # print("[admindb1]: ", admindb1)
    # print("[admindb2]: ", admindb2)

    old_time = datetime.now()

    # 데이터 넣기
    admindb1.changed_insert_db()
    admindb2.changed_insert_db()

    # 데이터 갖고오기
    if (client != 'All Client'):
        node_result = list(NodeChange.objects.all().filter(
            created_at__gt=old_time, ip=client).order_by('created_at').values())
        disk_result = list(DiskChange.objects.all().filter(
            create_at__gt=old_time, ip=client).order_by('create_at').values())
        gpu_result = list(GpuChange.objects.all().filter(
            created_at__gt=old_time, ip=client).order_by('created_at').values())

    else:
        node_result = list(NodeChange.objects.all().filter(
            created_at__gt=old_time).order_by('created_at').values())
        disk_result = list(DiskChange.objects.all().filter(
            create_at__gt=old_time).order_by('create_at').values())
        gpu_result = list(GpuChange.objects.all().filter(
            created_at__gt=old_time).order_by('created_at').values())

    data = {
        'node_result': node_result,
        'gpu_result': gpu_result,
        'disk_result': disk_result
    }

    return HttpResponse(JsonResponse(data), content_type="application/json")


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

        return data

    else:
        print("Wrong data")
        return


def connectDB():

    global ssh1
    global ssh2

    global admindb1
    global admindb2

    # 웹페이지에 들어가는 순간 값 받기 시작
    conn = pymysql.connect(host='localhost', user='root',
                                password='baro', db='judy', charset='utf8')
    cur = conn.cursor()

    ssh1 = paramiko.SSHClient()
    ssh1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh1.connect("192.168.20.115", port='22',  # 고객이 자신의 ip를 안다고 가정하에 '115'부분을 바꿈, 그러면 고객의 node에서 115로 가져올 수 있음, 지금은 115로 자기자신과 연결
                 username="oem", password='baro')  # customer

    ssh2 = paramiko.SSHClient()
    ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh2.connect("192.168.20.114", port='22',  # 고객이 자신의 ip를 안다고 가정하에 '115'부분을 바꿈, 그러면 고객의 node에서 115로 가져올 수 있음, 지금은 115로 자기자신과 연결
                 username="oem", password='baro')  # customer

    admindb1 = AdminDB(conn, cur, ssh1)
    admindb2 = AdminDB(conn, cur, ssh2)

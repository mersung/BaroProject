from copy import deepcopy
from datetime import datetime

from django.shortcuts import render

from django.http import JsonResponse
from django.http import HttpResponse
import json

from .models import NodeFixed
from .models import NodeChange
from .models import GpuChange
from .models import GpuFixed
from .models import DiskChange
from .models import DiskFixed

from parsing.node import Node
from parsing.cpu import CPU
from parsing.disk import Disk
from parsing.gpu import Gpu
from parsing.main import AdminDB
import time
import pymysql
import paramiko



# Create your views here.
def index(request):
    conn = pymysql.connect(host='localhost', user='root',
                                password='baro', db='tony', charset='utf8')
    cur = conn.cursor()

    # 첫 번째 사용자
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("192.168.20.115", port='22',  # 고객이 자신의 ip를 안다고 가정하에 '115'부분을 바꿈, 그러면 고객의 node에서 115로 가져올 수 있음, 지금은 115로 자기자신과 연결
                username="oem", password='baro')  # customer
    admindb = AdminDB(conn, cur, ssh)

    # 두 번째 사용자
    ssh2 = paramiko.SSHClient()
    ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh2.connect("192.168.20.114", port='22',  # 고객이 자신의 ip를 안다고 가정하에 '115'부분을 바꿈, 그러면 고객의 node에서 115로 가져올 수 있음, 지금은 115로 자기자신과 연결
                username="oem", password='baro')  # customer
    admindb2 = AdminDB(conn, cur, ssh2)

    

    if request.method == "GET":
        current = datetime.now()
        try:
            admindb.fixed_insert_db()
        except:
            print("admin고정값은 한 번만 삽입")
        try:
            admindb2.fixed_insert_db()
        except:
            print("admin2 고정값은 한 번만 삽입")
        ssh.close()
        print("index ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")
        
        nodeFixed = NodeFixed.objects.all()
        nodeChange = NodeChange.objects.all().filter(created_at__gt=current)
        gpuChange = GpuChange.objects.all().filter(created_at__gt=current)
        gpuFixed = GpuFixed.objects.all()
        diskChange = DiskChange.objects.all().filter(create_at__gt=current)
        diskFixed = DiskFixed.objects.all()
        print("fixed 실행완료")
        return render(request, 'index.html', {"nodeFixed" : nodeFixed, "nodeChange" : nodeChange, "gpuChange" : gpuChange, "gpuFixed" : gpuFixed, "diskChange" : diskChange, "diskFixed" : diskFixed})

    if request.method == "POST":

        current = datetime.now()
    
        try:
            try:
                admindb.fixed_insert_db()
                admindb2.fixed_insert_db()
            except:
                print("고정값은 한 번만 삽입")

            try:
                admindb.changed_insert_db()
                admindb2.changed_insert_db()
            except:
                print("실패..?")

        except KeyboardInterrupt:
            conn.close()

        except:
            conn.close()
            print("Wrong")

        ssh.close()

        nodeFixed = NodeFixed.objects.all()
        nodeFixedCnt = nodeFixed.count()
        print(nodeFixedCnt)
        nodeChange = []
        nc = deepcopy(list(NodeChange.objects.all().filter(created_at__gt=current).order_by('ip').values()))
        for i in range(nodeFixedCnt):
            nodeChange.append(nc.pop())

        #GPU 개수만큼 뽑기
        gpuFixed = GpuFixed.objects.all()
        gpuFixedCnt = list(gpuFixed.values())
        print(gpuFixedCnt)
        print(len(gpuFixedCnt))
        gpuChange = []
        gc = deepcopy(list(GpuChange.objects.all().filter(created_at__gt=current).order_by('ip').values()))
        for j in range(0, len(gpuFixedCnt)):
            print("j:",  j)
            gpuChange.append(gc.pop())
        print("gpuchnage:",gpuChange)
        

        #DISK 개수만큼 뽑기
        diskFixed = DiskFixed.objects.all().filter()
        diskFixedCnt = diskFixed.count()
        diskChange = []
        print(diskFixedCnt)
        dc = deepcopy(list(DiskChange.objects.all().filter(create_at__gt=current).order_by('ip').values()))
        for i in range(0, diskFixedCnt):
            diskChange.append(dc.pop())
        
        data = {
            "nodeChange" : nodeChange, 
            "gpuChange" : gpuChange, 
            "diskChange" : diskChange, 
        }
        return HttpResponse(JsonResponse(data), content_type="application/json")


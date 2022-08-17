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
    print("index ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")
    nodeFixed = NodeFixed.objects.all()
    nodeChange = NodeChange.objects.all()
    gpuChange = GpuChange.objects.all()
    gpuFixed = GpuFixed.objects.all()
    diskChange = DiskChange.objects.all()
    diskFixed = DiskFixed.objects.all()

    return render(request, 'index.html', {"nodeFixed" : nodeFixed, "nodeChange" : nodeChange, "gpuChange" : gpuChange, "gpuFixed" : gpuFixed, "diskChange" : diskChange, "diskFixed" : diskFixed})

def load_data(request):
    conn = pymysql.connect(host='localhost', user='root',
                                password='baro', db='tony', charset='utf8')
    cur = conn.cursor()

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("192.168.20.115", port='22',  # 고객이 자신의 ip를 안다고 가정하에 '115'부분을 바꿈, 그러면 고객의 node에서 115로 가져올 수 있음, 지금은 115로 자기자신과 연결
                username="oem", password='baro')  # customer

    admindb = AdminDB(conn, cur, ssh)
    
    try:

        try:
            admindb.changed_insert_db()
        except:
            print("실패..?")

    except KeyboardInterrupt:
        conn.close()

    except:
        conn.close()
        print("Wrong")

    ssh.close()

    nodeFixed = NodeFixed.objects.all()
    nodeChange = NodeChange.objects.all()
    nodeChange = list(nodeChange.values()).pop()

    gpuChange = GpuChange.objects.all()
    gpuChange = list(gpuChange.values()).pop()
    
    gpuFixed = GpuFixed.objects.all()
    diskChange = DiskChange.objects.all()
    diskChange = list(diskChange.values()).pop()

    diskFixed = DiskFixed.objects.all()

    data = {
        "nodeChange" : nodeChange, 
        "gpuChange" : gpuChange, 
        "diskChange" : diskChange, 
    }
    return HttpResponse(JsonResponse(data), content_type="application/json")



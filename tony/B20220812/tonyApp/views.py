from copy import deepcopy
from datetime import datetime

from django.shortcuts import render

from django.http import JsonResponse
from django.http import HttpResponse

from .models import NodeFixed
from .models import NodeChange
from .models import GpuChange
from .models import GpuFixed
from .models import DiskChange
from .models import DiskFixed

from parsing.main import AdminDB
import pymysql
import paramiko



# Create your views here.
def index(request):

    current = datetime.now()

    if "ip" not in request.GET:
        return HttpResponse(status=404)
    ip_address = request.GET["ip"]

    conn = pymysql.connect(host='localhost', user='root',
                                password='baro', db='tony', charset='utf8')
    cur = conn.cursor()

    # 첫 번째 사용자
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip_address, port='22',  # 고객이 자신의 ip를 안다고 가정하에 '115'부분을 바꿈, 그러면 고객의 node에서 115로 가져올 수 있음, 지금은 115로 자기자신과 연결
                username="oem", password='baro')  # customer
    admindb = AdminDB(conn, cur, ssh)

    if request.method == "GET":
        try:
            admindb.fixed_insert_db()
        except:
            print("admin고정값은 한 번만 삽입")
        ssh.close()
        print("index ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")
        
        nodeFixed = NodeFixed.objects.all().filter(ip=ip_address)
        # nodeChange = NodeChange.objects.all().filter(created_at__gt=current)
        # gpuChange = GpuChange.objects.all().filter(created_at__gt=current)
        gpuFixed = GpuFixed.objects.all().filter(ip=ip_address)
        # diskChange = DiskChange.objects.all().filter(create_at__gt=current)
        diskFixed = DiskFixed.objects.all().filter(ip=ip_address)
        print("fixed 실행완료")
        return render(request, 'index.html', {"ip" : ip_address, "nodeFixed" : nodeFixed,   "gpuFixed" : gpuFixed, "diskFixed" : diskFixed})

    if request.method == "POST":

        
    
        try:
            try:
                admindb.changed_insert_db()
                # admindb2.changed_insert_db()
            except:
                print("실패..?")

        except KeyboardInterrupt:
            conn.close()

        except:
            conn.close()
            print("Wrong")

        ssh.close()

        nodeFixed = NodeFixed.objects.all().filter(ip=ip_address)
        nodeFixedCnt = nodeFixed.count()
        nodeChange = []
        nc = deepcopy(list(NodeChange.objects.all().filter(created_at__gt=current, ip=ip_address).values()))
        for i in range(nodeFixedCnt):
            nodeChange.append(nc.pop())

        #GPU 개수만큼 뽑기
        gpuFixed = GpuFixed.objects.all().filter(ip=ip_address)
        gpuFixedCnt = list(gpuFixed.values())
        gpuChange = []
        gc = deepcopy(list(GpuChange.objects.all().filter(created_at__gt=current, ip=ip_address).values()))
        for j in range(0, len(gpuFixedCnt)):
            gpuChange.append(gc.pop())
        
        #DISK 개수만큼 뽑기
        diskFixed = DiskFixed.objects.all().filter().filter(ip=ip_address)
        diskFixedCnt = diskFixed.count()
        diskChange = []
        dc = deepcopy(list(DiskChange.objects.all().filter(create_at__gt=current, ip=ip_address).values()))
        for i in range(0, diskFixedCnt):
            diskChange.append(dc.pop())
        
        data = {
            "ip" : ip_address,
            "nodeChange" : nodeChange, 
            "gpuChange" : gpuChange, 
            "diskChange" : diskChange, 
        }
        return HttpResponse(JsonResponse(data), content_type="application/json")

def mainpage(request):
    return render(request, "main.html")

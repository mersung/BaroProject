from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render

from .forms import GpuFixedForm, DiskFixedForm, NodeFixedForm, GpuChangedForm, DiskChangedForm, NodeChangedForm
from .models import DiskChanged, DiskFixed, GpuChanged, GpuFixed, NodeChanged, NodeFixed
from .utils import get_ssh

from parser.main import AdminDB

import paramiko
from datetime import datetime
import time

# 해당 컴퓨터의 자원 정보를 알아오기 위한 ssh 원격 접속
# try:
#     now = time.time()
#     ssh = paramiko.SSHClient()
#     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     ssh.connect("192.168.20.115", port='22',  # 고객이 자신의 ip를 안다고 가정하에 '115'부분을 바꿈, 그러면 고객의 node에서 115로 가져올 수 있음, 지금은 115로 자기자신과 연결
#                     username="oem", password='baro')
#     print(time.time()-now)
# except:
#     raise Exception("ssh 접속 에러")

def index(request):
    return render(request, 'base/index.html')


def fixed(request):
    # http가 get방식으로 오지 않을 경우
    if request.method != "GET":
        return HttpResponse("bad request")

    if "ip" not in request.GET:
        return HttpResponse(status=400)
    print(request.GET.get("ip"))
    
    # 전역변수로 선언한 ssh 사용
    # global ssh
    ip = request.GET.get("ip")
    ssh = get_ssh(ip)
    admindb = AdminDB(ssh)

    # 노드 정보 db에서 가져오기
    node = NodeFixed.objects.filter(ip=ip)
    # 없을경우 컴퓨터에서 새로 가져와 저장함
    if len(node) == 0:
        # nodefixed 가져와서 저장
        print(admindb.node_fixed_table)
        node = NodeFixedForm(admindb.node_fixed_table)
        if node.is_valid():
            node.save()
            print("node fixed ok")
        # 저장후 db에서 다시 가져오기
        node = NodeFixed.objects.filter(ip=ip)
        

    # 디스크 정보 db에서 가져오기
    disk = DiskFixed.objects.filter(ip=ip)
    if len(disk) == 0:
        # diskfixed 가져와서 저장
        for disk_fixed in admindb.disk_fixed_table:
            disk = DiskFixedForm(disk_fixed)
            if disk.is_valid():
                disk.save()
                print("disk fixed ok")
        # 저장후 db에서 다시 가져오기
        disk = DiskFixed.objects.filter(ip=ip)


    gpu = GpuFixed.objects.filter(ip=ip)
    if len(gpu) == 0:
        # gpufixed 가져와서 저장
        for gpu_fixed in admindb.gpu_fixed_table:
            gpu = GpuFixedForm(gpu_fixed)
            if gpu.is_valid():
                gpu.save()
                print("gpu fixed ok")
        # 저장후 db에서 다시 가져오기
        gpu = GpuFixed.objects.filter(ip=ip)

    # print(gpu[0].ip.ip) disk.ip.ip -> disk.ip는 nodefixed 객체임.

    # if len(node) == 0 or len(disk) == 0 or len(gpu):
    #     return HTTPResponse("bad")

    return render(request, 'base/fixed.html', {'gpus': gpu, 'disks': disk, 'node': node[0], 'ip': ip})


def changed(request):

    # 전역변수로 선언한 ssh 사용
    # global ssh
    ip = ""

    # http가 get 방식으로 오면 changed.html 리턴
    if request.method == "GET":
        if "ip" not in request.GET:
            return HttpResponse(status=400)

        ip = request.GET.get("ip")
        return render(request, 'base/changed.html', {"ip": ip})

    # ip를 받지 않았을 때
    if "ip" not in request.POST:
        print("test")
        return HttpResponse("no ip in post", status=400)

    ip = request.POST.get("ip")
    ssh = get_ssh(ip)
    admindb = AdminDB(ssh)

    # post 방식으로 오면 JsonResponse 리턴
    if request.method == "POST":
        
        """
        node_changed_table
        {   
            'node_changed_id': 32, 
            'ip_id': '192.168.20.115', 
            'total_gpu_memory_using_percent': 0.08, 
            'total_gpu_memory_using_MB': 20.0, 
            'free_disk_GB': 7857, 
            'free_memory_GB': 181, 
            'free_disk_percent': 94.573, 
            'total_memory_using_percent': 1.78, 
            'total_cpu_using_percent': 0.0, 
            'free_cpu_percent': 100.0, 
            'created_at': datetime.datetime(2022, 8, 18, 1, 16, 37, 320741, tzinfo=datetime.timezone.utc)
        }
        """

        # NodeChanged 저장후 가장 최근거 불러오기
        node = NodeChangedForm(admindb.node_change_table)
        # 클라이언트가 동시실행시 값을 더 많이 가져오는 문제가 발생할 수 있음.
        now_time = datetime.now()
        if node.is_valid():
            node.save()
            node_changed_table = NodeChanged.objects.filter(ip=ip, created_at__gt=now_time).values()[0]
            print("node changed ok")

        # DiskChanged 저장후 가장 최근거 불러오기
        disks_changed_table = []
        for disk_changed in admindb.disk_changed_table:
            # 클라이언트가 동시실행시 값을 더 많이 가져오는 문제가 발생할 수 있음.
            now_time = datetime.now()
            disk = DiskChangedForm(disk_changed)
            if disk.is_valid():
                disk.save()
                disks_changed_table.extend(DiskChanged.objects.filter(ip=ip, created_at__gt=now_time).values())
                print("disk changed ok")
            
        # GpuChanged 저장후 가장 최근거 불러오기
        gpus_changed_table = []
        for gpu_changed in admindb.gpu_changed_table:
            # 클라이언트가 동시실행시 값을 더 많이 가져오는 문제가 발생할 수 있음.
            now_time = datetime.now()
            gpu = GpuChangedForm(gpu_changed)
            if gpu.is_valid():
                gpu.save()
                gpus_changed_table.extend(GpuChanged.objects.filter(ip=ip, created_at__gt=now_time).values())
                print("gpu changed ok")

        context = {
            'node': node_changed_table,
            'disks': disks_changed_table,
            'gpus': gpus_changed_table
        }

        # if len(context['node']) == 0 or len(context['disks']) == 0 or len(context['gpus']) == 0:
        #     return HTTPResponse("bad", status=500)

        # node: { ... },
        # disks: [{ ... }, { ... }]
        # gpus: [{ ... }, { ... }]
        return JsonResponse(context)

    return HttpResponse("bad")

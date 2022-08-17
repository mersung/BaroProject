from http.client import HTTPResponse
from django.http import JsonResponse
from django.shortcuts import render

from .forms import GpuFixedForm, DiskFixedForm, NodeFixedForm, GpuChangedForm, DiskChangedForm, NodeChangedForm
from .models import DiskChanged, DiskFixed, GpuChanged, GpuFixed, NodeChanged, NodeFixed

from parser.main import AdminDB

import paramiko

# 해당 컴퓨터의 자원 정보를 알아오기 위한 ssh 원격 접속
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("192.168.20.115", port='22',  # 고객이 자신의 ip를 안다고 가정하에 '115'부분을 바꿈, 그러면 고객의 node에서 115로 가져올 수 있음, 지금은 115로 자기자신과 연결
                username="oem", password='baro')


# Create your views here.
def fixed(request):
    # http가 get방식으로 오지 않을 경우
    if request.method != "GET":
        return HTTPResponse("bad")

    print(request.__dict__)
    
    # 전역변수로 선언한 ssh 사용
    global ssh
    admindb = AdminDB(ssh)
    ip = "192.168.20.115"

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
        print(admindb.disk_fixed_table)
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
        print(admindb.gpu_fixed_table)
        for gpu_fixed in admindb.gpu_fixed_table:
            gpu = GpuFixedForm(gpu_fixed)
            if gpu.is_valid():
                gpu.save()
                print("gpu fixed ok")
        gpu = GpuFixed.objects.filter(ip=ip)

    # print(gpu[0].ip.ip) disk.ip.ip -> disk.ip는 nodefixed 객체임.

    return render(request, 'base/fixed.html', {'gpus': gpu, 'disks': disk, 'node': node[0]})


def changed(request):
    # http가 get 방식으로 오면 changed.html 리턴
    if request.method == "GET":
        return render(request, 'base/changed.html')

    # post 방식으로 오면 JsonResponse 리턴
    if request.method == "POST":
        # 전역변수로 선언한 ssh 사용
        global ssh
        admindb = AdminDB(ssh)
        ip = "192.168.20.115"
        
        node = NodeChangedForm(admindb.node_change_table)
        if node.is_valid():
            node.save()
            node_changed_table = admindb.node_change_table
            print("node changed ok")

        disks_changed_table = []
        for disk_changed in admindb.disk_changed_table:
            disk = DiskChangedForm(disk_changed)
            if disk.is_valid():
                disk.save()
                disks_changed_table.append(disk_changed)
                print("disk changed ok")
            
        gpus_changed_table = []
        for gpu_changed in admindb.gpu_changed_table:
            gpu = GpuChangedForm(gpu_changed)
            if gpu.is_valid():
                gpu.save()
                gpus_changed_table.append(gpu_changed)
                print("gpu changed ok")

        context = {
            'node': node_changed_table,
            'disks': disks_changed_table,
            'gpus': gpus_changed_table
        }

        return JsonResponse(context)

    return HTTPResponse("bad")


# def refresh(request):
#     # post 방식으로 오면 JsonResponse 리턴
#     if request.method == "GET":
#         # 전역변수로 선언한 ssh 사용
#         global ssh
#         admindb = AdminDB(ssh)
#         ip = "192.168.20.115"
        
#         node = NodeChangedForm(admindb.node_change_table)
#         if node.is_valid():
#             node.save()
#             node_changed_table = admindb.node_change_table
#             print("node changed ok")

#         disks_changed_table = []
#         for disk_changed in admindb.disk_changed_table:
#             disk = DiskChangedForm(disk_changed)
#             if disk.is_valid():
#                 disk.save()
#                 disks_changed_table.append(disk_changed)
#                 print("disk changed ok")
            
#         gpus_changed_table = []
#         for gpu_changed in admindb.gpu_changed_table:
#             gpu = GpuChangedForm(gpu_changed)
#             if gpu.is_valid():
#                 gpu.save()
#                 gpus_changed_table.append(gpu_changed)
#                 print("gpu changed ok")

#         context = {
#             'node': node_changed_table,
#             'disks': disks_changed_table,
#             'gpus': gpus_changed_table
#         }

#     return JsonResponse(context)

# def changed(request):
#     # http가 get 방식으로 오면 changed.html 리턴
#     # post 방식으로 오면 JsonResponse 리턴
#     # http가 get방식으로 오지 않을 경우
#     if request.method != "GET":
#         return HTTPResponse("bad")

#     # 전역변수로 선언한 ssh 사용
#     global ssh
#     admindb = AdminDB(ssh)
#     ip = "192.168.20.115"
    
#     node = NodeChangedForm(admindb.node_change_table)
#     if node.is_valid():
#         node.save()
#         print("node changed ok")

#     for disk_changed in admindb.disk_changed_table:
#         disk = DiskChangedForm(disk_changed)
#         if disk.is_valid():
#             disk.save()
#             print("disk changed ok")

#     for gpu_changed in admindb.gpu_changed_table:
#         gpu = GpuChangedForm(gpu_changed)
#         if gpu.is_valid():
#             gpu.save()
#             print("gpu changed ok")

#     node = NodeChanged.objects.all()
#     disk = DiskChanged.objects.all()
#     gpu = GpuChanged.objects.all()

#     return render(request, 'base/changed.html', {'gpus': gpu, 'disks': disk, 'nodes': node})
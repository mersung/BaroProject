from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest
import json
from django.core import serializers
from .models import DiskChange, GpuChange, NodeChange, NodeFixed, DiskFixed, GpuFixed

# Create your views here.


def index(request):
    return HttpResponse("<p>HW Fixed Info<p>")


def HWFixedInfo(request):
    node_result = NodeFixed.objects.all()
    gpu_result = GpuFixed.objects.all()
    disk_result = DiskFixed.objects.all()

    data = {
        'node_result': node_result,
        'gpu_result': gpu_result,
        'disk_result': disk_result
    }
    return render(request, 'HWFixed/HWFixedInfo.html', data)


def HWChangeInfo(request):
    node_result = NodeChange.objects.all()
    gpu_result = GpuChange.objects.all()
    disk_result = DiskChange.objects.all()

    data = {
        'node_result': node_result,
        'gpu_result': gpu_result,
        'disk_result': disk_result
    }
    return render(request, 'HWChange/HWChangeInfo.html', data)


def HWload(request):
    node_result = list(NodeChange.objects.all().values())
    # node_result = list(NodeChange.objects.all().values())
    # node_result = list(NodeChange.objects.all().values())

    return HttpResponse(node_result, content_type="application/json")

from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.

def index(request):
    nodeChange = NodeChange.objects.all().order_by('ip')
    NF = NodeFixed.objects.all().order_by('ip')
    GC = GpuChange.objects.all().order_by('ip')
    GF = GpuFixed.objects.all().order_by('ip')
    diskChange = DiskChange.objects.all()
    DF = DiskFixed.objects.all().order_by('ip')
    return render(request, 'index.html',{"nodeFixed" : NF, "nodeChange" : nodeChange, "gpuChange" : GC, "gpuFixed" : GF, "diskChange" : diskChange, "diskFixed" : DF})
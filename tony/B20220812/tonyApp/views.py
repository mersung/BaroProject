from django.shortcuts import render

from .models import NodeFixed
from .models import NodeChange
from .models import GpuChange
from .models import GpuFixed
from .models import DiskChange
from .models import DiskFixed

# Create your views here.
def index(request):
    nodeFixed = NodeFixed.objects.all()
    nodeChange = NodeChange.objects.all()
    gpuChange = GpuChange.objects.all()
    gpuFixed = GpuFixed.objects.all()
    diskChange = DiskChange.objects.all()
    diskFixed = DiskFixed.objects.all()
    
    return render(request, 'index.html', {"nodeFixed" : nodeFixed, "nodeChange" : nodeChange, "gpuChange" : gpuChange, "gpuFixed" : gpuFixed, "diskChange" : diskChange, "diskFixed" : diskFixed})


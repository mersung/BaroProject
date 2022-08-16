from django.contrib import admin

from .models import NodeChange
from .models import NodeFixed
from .models import GpuChange
from .models import DiskChange

# Register your models here.

admin.site.register(NodeChange)
admin.site.register(NodeFixed)

admin.site.register(GpuChange)

admin.site.register(DiskChange)


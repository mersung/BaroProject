from django.contrib import admin
from .models import NodeFixed
from .models import *
# Register your models here.

admin.site.register(NodeFixed)
admin.site.register(NodeChange)
admin.site.register(GpuChange)
admin.site.register(GpuFixed)
admin.site.register(DiskChange)
admin.site.register(DiskFixed)
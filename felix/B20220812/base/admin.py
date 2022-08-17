from django.contrib import admin

from .models import DiskChanged, DiskFixed, GpuChanged, GpuFixed, NodeChanged, NodeFixed


# Register your models here.
admin.site.register(NodeChanged)
admin.site.register(NodeFixed)
admin.site.register(GpuChanged)
admin.site.register(GpuFixed)
admin.site.register(DiskFixed)
admin.site.register(DiskChanged)
from django.contrib import admin


from .models import NodeChange,NodeFixed,GpuChange,GpuFixed,DiskChange,DiskFixed


# Register your models here.
admin.site.register(NodeChange)
admin.site.register(NodeFixed)
admin.site.register(GpuFixed)
admin.site.register(GpuChange)
admin.site.register(DiskFixed)
admin.site.register(DiskChange)
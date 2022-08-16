# Create your models here.
from django.db import models
# https://ssungkang.tistory.com/entry/Django-06pk-path-converter-getobjector404%EB%9E%80
class NODE_FIXED(models.Model):
    ip = models.CharField(max_length=20, primary_key=True)
    host_name = models.CharField(max_length=50)
    total_gpu_memory_capacity_MB = models.IntegerField()
    number_of_gpu = models.IntegerField()
    total_disk_capacity_GB = models.IntegerField()
    total_memory_capacity_GB = models.IntegerField()
    cpu_name = models.CharField(max_length=50)
    number_of_core = models.IntegerField()
    number_of_thread = models.IntegerField()

class DISK_FIXED(models.Model):
    disk_path = models.CharField(max_length=50, primary_key=True)
    ip = models.ForeignKey(NODE_FIXED, on_delete=models.CASCADE)
    each_total_disk_capacity_GB = models.IntegerField()

    class Meta:
        constraints = [models.UniqueConstraint(fields=['disk_path', 'ip'], name="DISK_FIXED_MIX")]

class GPU_FIXED(models.Model):
    gpu_index = models.IntegerField(primary_key=True)
    ip = models.ForeignKey(NODE_FIXED, on_delete=models.CASCADE)
    each_total_gpu_memory_capacity_MB = models.IntegerField()
    gpu_name = models.CharField(max_length=20)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['gpu_index', 'ip'], name="GPU_FIXED_MIX")]

class DISK_CHANGE(models.Model):
    create_at = models.DateTimeField(auto_now_add=True, primary_key=True)
    #db_column : 내 테이블에서 만들어질 이름, to_field : 조인할 컬럼 이름
    disk_path = models.ForeignKey(DISK_FIXED, on_delete=models.CASCADE, db_column="disk_path", to_field="disk_path")
    ip = models.ForeignKey(NODE_FIXED, on_delete=models.CASCADE, db_column="ip", to_field="ip")
    disk_using_GB = models.IntegerField()
    disk_using_percent = models.IntegerField()

    class Meta:
        constraints = [models.UniqueConstraint(fields=['create_at', 'disk_path', 'ip'], name="DISK_CHANGE_MIX")]

class NODE_CHANGE(models.Model):
    create_at = models.DateTimeField(auto_now_add= True, primary_key=True)
    ip = models.ForeignKey(NODE_FIXED, on_delete=models.CASCADE, db_column="ip", to_field="ip")
    total_gpu_memory_using_percent = models.FloatField()
    total_gpu_memory_using_MB = models.FloatField()
    free_disk_GB = models.IntegerField()
    free_memory_GB = models.IntegerField()
    free_disk_percent = models.FloatField()
    total_memory_using_percent = models.FloatField()
    total_cpu_using_percent = models.FloatField()
    free_cpu_percent = models.FloatField()

    class Meta:
        constraints = [models.UniqueConstraint(fields=['create_at', 'ip'], name="NODE_CHANGE_MIX")]

class GPU_CHANGE(models.Model):
    create_at = models.DateTimeField(auto_now_add=True, primary_key=True)
    gpu_index = models.ForeignKey(GPU_FIXED, on_delete=models.CASCADE, db_column="gpu_index", to_field="gpu_index")
    ip = models.ForeignKey(NODE_FIXED, on_delete=models.CASCADE, db_column="ip", to_field="ip")
    gpu_memory_using_MB = models.IntegerField()
    gpu_memory_using_percent = models.FloatField()

    class Meta:
        constraints = [models.UniqueConstraint(fields=['create_at', 'gpu_index', 'ip'], name="GPU_CHANGE_MIX")]
from django.db import models


# 노드 고정
class NodeFixed(models.Model):
    ip = models.CharField(max_length=20, primary_key=True)
    host_name = models.CharField(max_length=50)
    total_gpu_memory_capacity_MB = models.IntegerField()
    number_of_gpu = models.IntegerField()
    total_disk_capacity_GB = models.IntegerField()
    total_memory_capacity_GB = models.IntegerField()
    cpu_name = models.CharField(max_length=50)
    number_of_core = models.IntegerField()
    number_of_thread = models.IntegerField()


class DiskFixed(models.Model):
    disk_path = models.CharField(max_length=50, primary_key=True)
    ip = models.ForeignKey(NodeFixed, on_delete=models.CASCADE, db_column="ip")
    each_total_disk_capacity_GB = models.IntegerField()

    class Meta:
        constraints = [models.UniqueConstraint(fields=['disk_path', 'ip'], name="ip_disk_path")]


class DiskChanged(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, primary_key=True)
    disk_path = models.ForeignKey(DiskFixed, on_delete=models.CASCADE, db_column="disk_path", to_field="disk_path")
    ip = models.ForeignKey(NodeFixed, on_delete=models.CASCADE, db_column="ip", to_field="ip")
    disk_using_GB = models.IntegerField()
    disk_using_percent = models.IntegerField()

    class Meta:
        constraints = [models.UniqueConstraint(fields=['disk_path', 'ip', 'created_at'], name="ip_disk_path_created_at")]


class NodeChanged(models.Model):
    created_at = models.DateTimeField(auto_now_add= True, primary_key=True)
    ip = models.ForeignKey(NodeFixed, on_delete=models.CASCADE, db_column="ip", to_field="ip")
    total_gpu_memory_using_percent = models.FloatField()
    total_gpu_memory_using_MB = models.FloatField()
    free_disk_GB = models.IntegerField()
    free_memory_GB = models.IntegerField()
    free_disk_percent = models.FloatField()
    total_memory_using_percent = models.FloatField()
    total_cpu_using_percent = models.FloatField()
    free_cpu_percent = models.FloatField()

    class Meta:
        constraints = [models.UniqueConstraint(fields=['created_at', 'ip'], name="created_at_ip")]


class GPUFixed(models.Model):
    gpu_index = models.IntegerField(primary_key=True)
    ip = models.ForeignKey(NodeFixed, on_delete=models.CASCADE, db_column="ip")
    each_total_gpu_memory_capacity_MB = models.IntegerField()
    gpu_name = models.CharField(max_length=50)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['gpu_index', 'ip'], name="gpu_index_ip")]


class GPUChanged(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, primary_key=True)
    gpu_index = models.ForeignKey(GPUFixed, on_delete=models.CASCADE, db_column="gpu_index", to_field="gpu_index")
    ip = models.ForeignKey(NodeFixed, on_delete=models.CASCADE, db_column="ip", to_field="ip")
    gpu_memory_using_MB = models.IntegerField()
    gpu_memory_using_percent = models.FloatField()

    class Meta:
        constraints = [models.UniqueConstraint(fields=['gpu_index', 'ip', "created_at"], name="gpu_index_ip_created_at")]
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class DiskChange(models.Model):
    create_at = models.DateTimeField(primary_key=True)
    disk_path = models.ForeignKey('DiskFixed', models.CASCADE, db_column='disk_path', related_name="DiskChange1")
    ip = models.ForeignKey('NodeFixed', models.CASCADE, db_column='ip', related_name="DiskChange2")
    disk_using_gb = models.IntegerField(db_column='disk_using_GB')  # Field name made lowercase.
    disk_using_percent = models.FloatField()

    class Meta:
        managed = False
        db_table = 'DISK_CHANGE'
        constraints = [models.UniqueConstraint(fields=['create_at', 'disk_path', 'ip'], name="c_d_p_ip")]


class DiskFixed(models.Model):
    disk_path = models.CharField(primary_key=True, max_length=50)
    ip = models.ForeignKey('NodeFixed', models.CASCADE, db_column='ip', related_name="DiskFixed1")
    each_total_disk_capacity_gb = models.IntegerField(db_column='each_total_disk_capacity_GB')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DISK_FIXED'
        constraints = [models.UniqueConstraint(fields=['disk_path', 'ip'], name="d_p_ip")]


class GpuChange(models.Model):
    created_at = models.DateTimeField(primary_key=True)
    gpu_index = models.ForeignKey('GpuFixed', models.CASCADE, db_column='gpu_index', related_name="GpuChange1")
    ip = models.ForeignKey('NodeFixed', models.CASCADE, db_column='ip', related_name="GpuChange2")
    gpu_memory_using_mb = models.IntegerField(db_column='gpu_memory_using_MB')  # Field name made lowercase.
    gpu_memory_using_percent = models.FloatField()

    class Meta:
        managed = False
        db_table = 'GPU_CHANGE'
        constraints = [models.UniqueConstraint(fields=['created_at', 'gpu_index', 'ip'], name="c_gpu_index_ip")]


class GpuFixed(models.Model):
    gpu_index = models.IntegerField(primary_key=True)
    ip = models.ForeignKey('NodeFixed', models.CASCADE, db_column='ip', related_name="GpuFixed1")
    each_total_gpu_memory_capacity_mb = models.IntegerField(db_column='each_total_gpu_memory_capacity_MB')  # Field name made lowercase.
    gpu_name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'GPU_FIXED'
        constraints = [models.UniqueConstraint(fields=['gpu_index', 'ip'], name="gpu_index_ip")]


class NodeChange(models.Model):
    created_at = models.DateTimeField(primary_key=True)
    ip = models.ForeignKey('NodeFixed', models.CASCADE, db_column='ip', related_name="NodeChange1")
    total_gpu_memory_using_percent = models.FloatField()
    total_gpu_memory_using_mb = models.FloatField(db_column='total_gpu_memory_using_MB')  # Field name made lowercase.
    free_disk_gb = models.IntegerField(db_column='free_disk_GB')  # Field name made lowercase.
    free_memory_gb = models.IntegerField(db_column='free_memory_GB')  # Field name made lowercase.
    free_disk_percent = models.FloatField()
    total_memory_using_percent = models.FloatField()
    total_cpu_using_percent = models.FloatField()
    free_cpu_percent = models.FloatField()

    class Meta:
        managed = False
        db_table = 'NODE_CHANGE'
        constraints = [models.UniqueConstraint(fields=['created_at', 'ip'], name="c_ip")]



class NodeFixed(models.Model):
    ip = models.CharField(primary_key=True, max_length=20)
    host_name = models.CharField(max_length=50)
    total_gpu_memory_capacity_mb = models.IntegerField(db_column='total_gpu_memory_capacity_MB')  # Field name made lowercase.
    number_of_gpu = models.IntegerField()
    total_disk_capacity_gb = models.IntegerField(db_column='total_disk_capacity_GB')  # Field name made lowercase.
    total_memory_capacity_gb = models.IntegerField(db_column='total_memory_capacity_GB')  # Field name made lowercase.
    number_of_core = models.IntegerField()
    number_of_thread = models.IntegerField()
    cpu_name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'NODE_FIXED'

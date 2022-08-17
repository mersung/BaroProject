from tkinter import Widget
from django.db import models

# Create your models here.


class DiskChange(models.Model):
    create_at = models.DateTimeField(primary_key=True)
    disk_path = models.CharField(max_length=50)
    # foreign key인데 diskfixed에서 찾을때 같은 시간에 내뱉는게 여러개여서 문제인듯함
    # disk_path = models.ForeignKey(
    #     'DiskFixed', models.DO_NOTHING, db_column='disk_path', related_name='+')
    ip = models.ForeignKey('NodeFixed', models.DO_NOTHING,
                           db_column='ip', related_name='+')
    # Field name made lowercase.
    disk_using_gb = models.IntegerField(db_column='disk_using_GB')
    disk_using_percent = models.FloatField()

    class Meta:
        managed = False
        db_table = 'DISK_CHANGE'
        unique_together = (('create_at', 'disk_path', 'ip'),)


class DiskFixed(models.Model):
    disk_path = models.CharField(primary_key=True, max_length=50, unique=True)
    ip = models.ForeignKey('NodeFixed', models.DO_NOTHING,
                           db_column='ip', related_name='+')
    # Field name made lowercase.
    each_total_disk_capacity_gb = models.IntegerField(
        db_column='each_total_disk_capacity_GB')

    class Meta:
        managed = False
        db_table = 'DISK_FIXED'
        unique_together = (('disk_path', 'ip'),)


class GpuChange(models.Model):
    created_at = models.DateTimeField(primary_key=True)
    gpu_index = models.IntegerField()
    # foreign key인데 gpufixed에서 찾을때 같은 시간에 내뱉는게 여러개여서 문제인듯함
    # gpu_index = models.ForeignKey(
    #     'GpuFixed', models.DO_NOTHING, db_column='gpu_index', related_name='+')
    ip = models.ForeignKey('NodeFixed', models.DO_NOTHING,
                           db_column='ip', related_name='+')
    # Field name made lowercase.
    gpu_memory_using_mb = models.IntegerField(db_column='gpu_memory_using_MB')
    gpu_memory_using_percent = models.FloatField()

    class Meta:
        managed = False
        db_table = 'GPU_CHANGE'
        unique_together = (('created_at', 'gpu_index', 'ip'),)


class GpuFixed(models.Model):
    gpu_index = models.IntegerField(primary_key=True)
    ip = models.ForeignKey('NodeFixed', models.DO_NOTHING,
                           db_column='ip', related_name='+')
    each_total_gpu_memory_capacity_mb = models.IntegerField(
        db_column='each_total_gpu_memory_capacity_MB')  # Field name made lowercase.
    gpu_name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'GPU_FIXED'
        unique_together = (('gpu_index', 'ip'),)


class NodeChange(models.Model):
    created_at = models.DateTimeField(primary_key=True)
    ip = models.ForeignKey('NodeFixed', models.DO_NOTHING,
                           db_column='ip', related_name='+')
    total_gpu_memory_using_percent = models.FloatField()
    # Field name made lowercase.
    total_gpu_memory_using_mb = models.FloatField(
        db_column='total_gpu_memory_using_MB')
    # Field name made lowercase.
    free_disk_gb = models.IntegerField(db_column='free_disk_GB')
    # Field name made lowercase.
    free_memory_gb = models.IntegerField(db_column='free_memory_GB')
    free_disk_percent = models.FloatField()
    total_memory_using_percent = models.FloatField()
    total_cpu_using_percent = models.FloatField()
    free_cpu_percent = models.FloatField()

    class Meta:
        managed = False
        db_table = 'NODE_CHANGE'
        unique_together = (('created_at', 'ip'),)


class NodeFixed(models.Model):
    ip = models.CharField(primary_key=True, max_length=20)
    host_name = models.CharField(max_length=50)
    # Field name made lowercase.
    total_gpu_memory_capacity_mb = models.IntegerField(
        db_column='total_gpu_memory_capacity_MB')
    number_of_gpu = models.IntegerField()
    # Field name made lowercase.
    total_disk_capacity_gb = models.IntegerField(
        db_column='total_disk_capacity_GB')
    # Field name made lowercase.
    total_memory_capacity_gb = models.IntegerField(
        db_column='total_memory_capacity_GB')
    number_of_core = models.IntegerField()
    number_of_thread = models.IntegerField()
    cpu_name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'NODE_FIXED'

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class DiskChanged(models.Model):
    disk_changed_id = models.AutoField(primary_key=True)
    ip = models.ForeignKey('NodeFixed', models.CASCADE, db_column='ip')
    created_at = models.DateTimeField(auto_now_add=True)
    disk_using_GB = models.IntegerField(db_column='disk_using_GB')  # Field name made lowercase.
    disk_using_percent = models.FloatField()
    disk_path = models.CharField(max_length=50)


class DiskFixed(models.Model):
    disk_fixed_id = models.AutoField(primary_key=True)
    ip = models.ForeignKey('NodeFixed', models.CASCADE, db_column='ip')
    disk_path = models.CharField(max_length=50)
    each_total_disk_capacity_GB = models.IntegerField(db_column='each_total_disk_capacity_GB')  # Field name made lowercase.


class GpuChanged(models.Model):
    gpu_changed_id = models.AutoField(primary_key=True)
    ip = models.ForeignKey('NodeFixed', models.CASCADE, db_column='ip')
    created_at = models.DateTimeField(auto_now_add=True)
    gpu_memory_using_MB = models.IntegerField(db_column='gpu_memory_using_MB')  # Field name made lowercase.
    gpu_memory_using_percent = models.FloatField()
    gpu_index = models.IntegerField()


class GpuFixed(models.Model):
    gpu_fixed_id = models.AutoField(primary_key=True)
    ip = models.ForeignKey('NodeFixed', models.CASCADE, db_column='ip')
    gpu_name = models.CharField(max_length=50)
    gpu_index = models.IntegerField()
    each_total_gpu_memory_capacity_MB = models.IntegerField(db_column='each_total_gpu_memory_capacity_MB')  # Field name made lowercase.


class NodeChanged(models.Model):
    node_changed_id = models.AutoField(primary_key=True)
    ip = models.ForeignKey('NodeFixed', models.CASCADE, db_column='ip')
    total_gpu_memory_using_percent = models.FloatField()
    total_gpu_memory_using_MB = models.FloatField(db_column='total_gpu_memory_using_MB')  # Field name made lowercase.
    free_disk_GB = models.IntegerField(db_column='free_disk_GB')  # Field name made lowercase.
    free_memory_GB = models.IntegerField(db_column='free_memory_GB')  # Field name made lowercase.
    free_disk_percent = models.FloatField()
    total_memory_using_percent = models.FloatField()
    total_cpu_using_percent = models.FloatField()
    free_cpu_percent = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)


class NodeFixed(models.Model):
    ip = models.CharField(primary_key=True, max_length=50)
    host_name = models.CharField(max_length=50)
    total_gpu_memory_capacity_MB = models.IntegerField(db_column='total_gpu_memory_capacity_MB')  # Field name made lowercase.
    number_of_gpu = models.IntegerField()
    total_disk_capacity_GB = models.IntegerField(db_column='total_disk_capacity_GB')  # Field name made lowercase.
    total_memory_capacity_GB = models.IntegerField(db_column='total_memory_capacity_GB')  # Field name made lowercase.
    number_of_core = models.IntegerField()
    number_of_thread = models.IntegerField()
    cpu_name = models.CharField(max_length=50)

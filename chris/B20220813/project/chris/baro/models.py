
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
    disk_path = models.ForeignKey('DiskFixed', models.DO_NOTHING, db_column='disk_path', related_name ='+')
    ip = models.ForeignKey('NodeFixed', models.DO_NOTHING, db_column='ip')
    disk_using_gb = models.IntegerField(db_column='disk_using_GB')  # Field name made lowercase.
    disk_using_percent = models.FloatField()

    class Meta:
        managed = False
        db_table = 'DISK_CHANGE'
        unique_together = (('create_at', 'disk_path', 'ip'),)


class DiskFixed(models.Model):
    disk_path = models.CharField(primary_key=True, max_length=50)
    ip = models.ForeignKey('NodeFixed', models.DO_NOTHING, db_column='ip',related_name ='+')
    each_total_disk_capacity_gb = models.IntegerField(db_column='each_total_disk_capacity_GB')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DISK_FIXED'
        unique_together = (('disk_path', 'ip'),)


class GpuChange(models.Model):
    created_at = models.DateTimeField(primary_key=True)
    gpu_index = models.ForeignKey('GpuFixed', models.DO_NOTHING, db_column='gpu_index',related_name ='+')
    ip = models.ForeignKey('NodeFixed', models.DO_NOTHING, db_column='ip')
    gpu_memory_using_mb = models.IntegerField(db_column='gpu_memory_using_MB')  # Field name made lowercase.
    gpu_memory_using_percent = models.FloatField()

    class Meta:
        managed = False
        db_table = 'GPU_CHANGE'
        unique_together = (('created_at', 'gpu_index', 'ip'),)


class GpuFixed(models.Model):
    gpu_index = models.IntegerField(primary_key=True)
    ip = models.ForeignKey('NodeFixed', models.DO_NOTHING, db_column='ip', related_name ='+')
    each_total_gpu_memory_capacity_mb = models.IntegerField(db_column='each_total_gpu_memory_capacity_MB')  # Field name made lowercase.
    gpu_name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'GPU_FIXED'
        unique_together = (('gpu_index', 'ip'),)


class NodeChange(models.Model):
    created_at = models.DateTimeField(primary_key=True)
    ip = models.ForeignKey('NodeFixed', models.DO_NOTHING, db_column='ip', related_name ='+')
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
        unique_together = (('created_at', 'ip'),)


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


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING, related_name ='+')
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING, related_name ='+')

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, related_name ='+')
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class BaroDiskchanged(models.Model):
    created_at = models.DateTimeField(primary_key=True)
    disk_using_gb = models.IntegerField(db_column='disk_using_GB')  # Field name made lowercase.
    disk_using_percent = models.IntegerField()
    disk_path = models.ForeignKey('BaroDiskfixed', models.DO_NOTHING, db_column='disk_path')
    ip = models.ForeignKey('BaroNodefixed', models.DO_NOTHING, db_column='ip')

    class Meta:
        managed = False
        db_table = 'baro_diskchanged'
        unique_together = (('disk_path', 'ip', 'created_at'),)


class BaroDiskfixed(models.Model):
    disk_path = models.CharField(primary_key=True, max_length=50)
    each_total_disk_capacity_gb = models.IntegerField(db_column='each_total_disk_capacity_GB')  # Field name made lowercase.
    ip = models.ForeignKey('BaroNodefixed', models.DO_NOTHING, db_column='ip')

    class Meta:
        managed = False
        db_table = 'baro_diskfixed'
        unique_together = (('disk_path', 'ip'),)


class BaroGpuchanged(models.Model):
    created_at = models.DateTimeField(primary_key=True)
    gpu_memory_using_mb = models.IntegerField(db_column='gpu_memory_using_MB')  # Field name made lowercase.
    gpu_memory_using_percent = models.FloatField()
    gpu_index = models.ForeignKey('BaroGpufixed', models.DO_NOTHING, db_column='gpu_index')
    ip = models.ForeignKey('BaroNodefixed', models.DO_NOTHING, db_column='ip')

    class Meta:
        managed = False
        db_table = 'baro_gpuchanged'
        unique_together = (('gpu_index', 'ip', 'created_at'),)


class BaroGpufixed(models.Model):
    gpu_index = models.IntegerField(primary_key=True)
    each_total_gpu_memory_capacity_mb = models.IntegerField(db_column='each_total_gpu_memory_capacity_MB')  # Field name made lowercase.
    gpu_name = models.CharField(max_length=50)
    ip = models.ForeignKey('BaroNodefixed', models.DO_NOTHING, db_column='ip')

    class Meta:
        managed = False
        db_table = 'baro_gpufixed'
        unique_together = (('gpu_index', 'ip'),)


class BaroNodechanged(models.Model):
    created_at = models.DateTimeField(primary_key=True)
    total_gpu_memory_using_percent = models.FloatField()
    total_gpu_memory_using_mb = models.FloatField(db_column='total_gpu_memory_using_MB')  # Field name made lowercase.
    free_disk_gb = models.IntegerField(db_column='free_disk_GB')  # Field name made lowercase.
    free_memory_gb = models.IntegerField(db_column='free_memory_GB')  # Field name made lowercase.
    free_disk_percent = models.FloatField()
    total_memory_using_percent = models.FloatField()
    total_cpu_using_percent = models.FloatField()
    free_cpu_percent = models.FloatField()
    ip = models.ForeignKey('BaroNodefixed', models.DO_NOTHING, db_column='ip')

    class Meta:
        managed = False
        db_table = 'baro_nodechanged'
        unique_together = (('created_at', 'ip'),)


class BaroNodefixed(models.Model):
    ip = models.CharField(primary_key=True, max_length=20)
    host_name = models.CharField(max_length=50)
    total_gpu_memory_capacity_mb = models.IntegerField(db_column='total_gpu_memory_capacity_MB')  # Field name made lowercase.
    number_of_gpu = models.IntegerField()
    total_disk_capacity_gb = models.IntegerField(db_column='total_disk_capacity_GB')  # Field name made lowercase.
    total_memory_capacity_gb = models.IntegerField(db_column='total_memory_capacity_GB')  # Field name made lowercase.
    cpu_name = models.CharField(max_length=50)
    number_of_core = models.IntegerField()
    number_of_thread = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'baro_nodefixed'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
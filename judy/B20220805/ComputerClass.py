
class NodeInfo:
    def __init__(self) -> None:

        # Node 기본
        self.__ip = ""
        self.__hostname = ""

        # GPU
        self.__gpu_count = 0
        self.__total_gpu_memory_capacity = 0
        self.__total_gpu_memory_usage = 0
        self.__total_gpu_memory_usage_percent = 0

        # Memory
        self.__total_memory_capacity = 0
        self.__total_memory_usage_percent = 0
        self.__free_memory_capacity = 0

        # Disk
        self.__total_disk_capacity = 0
        self.__total_disk_free = 0

        # CPU
        self.__cpu_name = ""
        self.__total_thread_count = 0
        self.__total_core_count = 0
        self.__total_cpu_usage_percent = 0

    @property
    def ip(self):
        return self.__ip

    @ip.setter
    def ip(self, ip):
        self.__ip = ip

    @property
    def hostname(self):
        return self.__hostname

    @hostname.setter
    def hostname(self, hostname):
        self.__hostname = hostname

    @property
    def cpu_name(self):
        return self.__cpu_name

    @cpu_name.setter
    def cpu_name(self, name):
        self.__cpu_name = name

    @property
    def total_thread_count(self):
        return self.__total_thread_count

    @total_thread_count.setter
    def total_thread_count(self, thread):
        self.__total_thread_count = thread

    @property
    def total_core_count(self):
        return self.__total_core_count

    @total_core_count.setter
    def total_core_count(self, core):
        self.__total_core_count = core

    @property
    def total_cpu_usage_percent(self):
        return self.__total_cpu_usage_percent

    @total_cpu_usage_percent.setter
    def total_cpu_usage_percent(self, percent):
        self.__total_cpu_usage_percent = percent

    @property
    def total_disk_capcity(self):
        return self.__total_disk_capacity

    @total_disk_capcity.setter
    def total_disk_capacity(self, capacity):
        self.__total_disk_capacity = capacity

    @property
    def total_disk_free(self):
        return self.__total_disk_free

    @total_disk_free.setter
    def total_disk_free(self, free):
        self.__total_disk_free = free

    @property
    def total_memory_capacity(self):
        return self.__total_memory_capacity

    @total_memory_capacity.setter
    def total_memory_capacity(self, capacity):
        self.__total_memory_capacity = capacity

    @property
    def total_memory_usage_percent(self):
        return self.__total_memory_usage_percent

    @total_memory_usage_percent.setter
    def total_memory_usage_percent(self, percent):
        self.__total_memory_usage_percent = percent

    @property
    def free_memory_capacity(self):
        return self.__free_memory_capacity

    @free_memory_capacity.setter
    def free_memory_capacity(self, free):
        self.__free_memory_capacity = free

    @property
    def total_gpu_memory_capacity(self):
        return self.__total_gpu_memory_capacity

    @total_gpu_memory_capacity.setter
    def total_gpu_memory_capacity(self, capacity):
        self.__total_gpu_memory_capacity = capacity

    @property
    def total_gpu_memory_usage(self):
        return self.__total_gpu_memory_usage

    @total_gpu_memory_usage.setter
    def total_gpu_memory_usage(self, usage):
        self.__total_gpu_memory_usage = usage

    @property
    def total_gpu_memory_usage_percent(self):
        return self.__total_gpu_memory_usage_percent

    @total_gpu_memory_usage_percent.setter
    def total_gpu_memory_usage_percent(self, usage):
        self.__total_gpu_memory_usage_percent = usage

    @property
    def gpu_count(self):
        return self.__gpu_count

    @gpu_count.setter
    def gpu_count(self, count):
        self.__gpu_count = count


class DiskInfo:
    def __init__(self) -> None:
        self.__name = ""
        self.__usage = 0
        self.__usage_percent = 0

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def usage(self):
        return self.__usage

    @usage.setter
    def usage(self, usage):
        self.__usage = usage

    @property
    def usage_percent(self):
        return self.__usage_percent

    @usage_percent.setter
    def usage_percent(self, percent):
        self.__usage_percent = percent


class GPUInfo:
    def __init__(self) -> None:
        self.__name = ""
        self.__memory_capacity = 0
        self.__memory_usage = 0
        self.__memory_usage_percent = 0

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def memory_capacity(self):
        return self.__memory_capacity

    @memory_capacity.setter
    def memory_capacity(self, capacity):
        self.__memory_capacity = capacity

    @property
    def memory_usage(self):
        return self.__memory_usage

    @memory_usage.setter
    def memory_usage(self, usage):
        self.__memory_usage = usage

    @property
    def memory_usage_percent(self):
        return self.__memory_usage_percent

    @memory_usage_percent.setter
    def memory_usage_percent(self, usage):
        self.__memory_usage_percent = usage

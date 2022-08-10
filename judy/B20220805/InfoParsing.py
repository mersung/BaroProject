import os
from ComputerClass import NodeInfo, GPUInfo, DiskInfo
import AdminDB


def DiskInfoParsing(node: NodeInfo):

    # 터미널에서 디스크 정보 전부 가져오기
    disks_sd: list = os.popen("df | grep 'sd'").readlines()  # list 데이터값 표시 어찌함
    disks_hd: list = os.popen("df | grep 'hd'").readlines()
    disks_nvme: list = os.popen("df | grep 'nvme'").readlines()

    total_disk_capacity: int = 0
    total_disk_free: int = 0
    diskInfos: list[DiskInfo] = []

    for disk in disks_sd:

        infos: list[str] = disk.split()

        # 각 디스크 정보 넣기
        diskInfo = DiskInfo()
        diskInfo.name = infos[0]
        diskInfo.usage = round(int(infos[2]) / 1024**2)
        diskInfo.usage_percent = infos[4]
        diskInfos.append(diskInfo)

        # 총 디스크 정보 넣기
        total_disk_capacity += round(int(infos[1]) / 1024**2)
        total_disk_free += round(int(infos[3]) / 1024**2)
        node.total_disk_capacity = total_disk_capacity
        node.total_disk_free = total_disk_free

    for disk in disks_hd:

        infos: list[str] = disk.split()

        # 각 디스크 정보 넣기
        diskInfo = DiskInfo()
        diskInfo.name = infos[0]
        diskInfo.usage = round(int(infos[2]) / 1024**2)
        diskInfo.usage_percent = infos[4]
        diskInfos.append(diskInfo)

        # 총 디스크 정보 넣기
        total_disk_capacity += round(int(infos[1]) / 1024**2)
        total_disk_free += round(int(infos[3]) / 1024**2)
        node.total_disk_capacity = total_disk_capacity
        node.total_disk_free = total_disk_free

    for disk in disks_nvme:

        infos: list[str] = disk.split()

        # 각 디스크 정보 넣기
        diskInfo = DiskInfo()
        diskInfo.name = infos[0]
        diskInfo.usage = round(int(infos[2]) / 1024**2)
        diskInfo.usage_percent = infos[4]
        diskInfos.append(diskInfo)

        # 총 디스크 정보 넣기
        total_disk_capacity += round(int(infos[1]) / 1024**2)
        total_disk_free += round(int(infos[3]) / 1024**2)
        node.total_disk_capacity = total_disk_capacity
        node.total_disk_free = total_disk_free

    return diskInfos


def CPUInfoParsing(node: NodeInfo):

    # CPU 이름
    cpu_name: int = os.popen(
        "lscpu | grep -i -E 'model name'").read().split(":")[1]
    node.cpu_name = cpu_name

    # cpu당 thread 개수
    per_thread_count: int = int(
        os.popen("lscpu | grep -i -E 'thread'").read().split(":")[1])

    # 코어 개수
    # grep "cpu cores" /proc/cpuinfo | tail -1
    core_count: int = int(os.popen(
        "grep -c processor /proc/cpuinfo").read()) // per_thread_count  # 터미널 명령어 아님 > 불편
    node.total_core_count = core_count

    # 총 스레드 개수
    thread_count: int = core_count * per_thread_count
    node.total_thread_count = thread_count

    return


def MemoryInfoParsing(node: NodeInfo):

    # memory data
    memoryInfos: list[str] = os.popen(
        "free | grep -i -E 'Mem'").read().split(":")[1].split()[:3]

    # 총 메모리
    node.total_memory_capacity = int(memoryInfos[0]) // 1024**2

    # 사용 가능 메모리
    node.free_memory_capacity = int(memoryInfos[2]) // 1024**2

    # 총 메모리 사용량
    node.total_memory_usage_percent = round(
        int(memoryInfos[1]) / int(memoryInfos[0]) * 100, 2)

    return


def GPUInfoParsing(node: NodeInfo):

    # 총 개수
    gpu_count: int = int(os.popen("lspci | grep -i -c VGA").read())
    node.gpu_count = gpu_count

    total_capacity: int = 0
    total_usage: int = 0
    total_usage_percent: float = 0

    # 리스트
    gpuNames: list[str] = os.popen(
        "nvidia-smi --query-gpu=name --format=csv,noheader").read().split("\n")
    gpuUsages: list[str] = os.popen(
        "nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits").read().split("\n")
    gpuCapacities: list[str] = os.popen(
        "nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits").read().split("\n")
    # gpuFree: list[str] = os.popen(
    #     "nvidia-smi --query-gpu=memory.free --format=csv").readlines()[1:]

    # 저장할 리스트
    gpuList: list[gpuInfo] = []

    for idx in range(0, gpu_count):
        gpuInfo = GPUInfo()

        gpuInfo.name = gpuNames[idx]
        gpuInfo.memory_capacity = int(gpuCapacities[idx])
        gpuInfo.memory_usage = int(gpuUsages[idx])
        gpuInfo.memory_usage_percent = int(
            gpuUsages[idx]) / int(gpuCapacities[idx]) * 100
        gpuList.append(gpuInfo)

        total_usage += int(gpuUsages[idx])
        total_capacity += int(gpuCapacities[idx])

    total_usage_percent = total_usage / total_capacity * 100

    node.total_gpu_memory_capacity = total_capacity
    node.total_gpu_memory_usage = total_usage
    node.total_gpu_memory_usage_percent = total_usage_percent

    return gpuList


def NodeInfoParsing(node: NodeInfo):

    # 첫번째가 무조건 inet ip일지는 모르겠음
    ip: str = os.popen("hostname -I").read().split()[0]
    hostname: str = os.popen("hostname").read()

    node.ip = ip
    node.hostname = hostname


if __name__ == "__main__":

    node = NodeInfo()

    NodeInfoParsing(node)
    DiskInfos: list[DiskInfo] = DiskInfoParsing(node)
    CPUInfoParsing(node)
    MemoryInfoParsing(node)
    GPUInfos: list[GPUInfo] = GPUInfoParsing(node)

    AdminDB.ConnectDB()
    AdminDB.InsertDB("Node", node)

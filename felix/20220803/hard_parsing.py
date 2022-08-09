import os
import psutil


# cpu 제품 이름
def get_cpu_info() -> str:
    info = "[CPU]\n"

    # cpu 정보 [제품이름, 코어수, 스레드수, 사용률]
    cpu_info = []

    # cpu 제품 이름
    cpu_name: str = os.popen("cat /proc/cpuinfo | grep 'model name' | tail -1").read().split(":")[-1]
    info += "{:<20}:".format("model") + cpu_name
    # cpu 코어 수
    cpu_core: int = os.popen("cat /proc/cpuinfo | grep 'cpu cores' | tail -1").read().split(":")[-1]
    info += "{:<20}:".format("core") + cpu_core
    # cpu 스레드 수
    cpu_thread: int = os.popen("cat /proc/cpuinfo | grep 'siblings' | tail -1").read().split(":")[-1]
    info += "{:<20}:".format("thread") + cpu_thread
    # cpu 사용률
    cpu_percent: float = psutil.cpu_percent()
    info += "{:<20}: ".format("using") + str(cpu_percent) + " %\n\n"

    cpu_info.extend([cpu_name, cpu_core, cpu_thread, cpu_percent])

    return info, cpu_info


def get_memory_info() -> str:
    info = "[MEMORY]\n"

    # 메모리 총 용량, 사용가능 용량, 사용중 용량
    memory = psutil.virtual_memory()

    # 메모리 정보 [총용량, 사용가능 용량, 사용량]
    memory_info = []

    info += "{:<20}: ".format("total") + str(int(memory.total/1024**3)) + " GB \n"
    info += "{:<20}: ".format("available") + str(int(memory.available/1024**3)) + " GB \n"
    info += "{:<20}: ".format("using") + str(round(memory.used/memory.total*100, 3)) + " % \n\n"
    
    memory_info.extend([int(memory.total/1024**3), int(memory.available/1024**3), round(memory.used/memory.total*100, 3)])

    return info, memory_info


def get_disk_info() -> str:
    info = "[DISK]\n"

    # Disk 총 용량, 사용가능 용량, 사용중 용량
    disk = os.popen("df | grep -e /dev/nvme -e /dev/sd -e /dev/hd").read().strip().split('\n')

    disk_total = 0
    disk_usable_total = 0

    # 각 disk 정보 [[디스크이름, 디스크용량, 사용량(GB), 사용량(%)]]
    disks_info = []
    # 총 disk 정보 [총 디스크 용량, 사용가능 디스크 용량]
    disk_total_info = []

    for d in disk:
        d = d.split()
        print(d)
        disk_total += int(d[1])
        disk_usable_total += int(d[3])

        disk_info = []

        info += "{:<20}".format("name") + d[0] + "\n"
        info += "{:<20}".format("disk") + str(int(int(d[1])/1024**2)) + " GB \n"
        info += "{:<20}".format("using_disk") + str(int(int(d[2])/1024**2)) + " GB \n"
        info += "{:<20}".format("using_disk_percent") + str(round(int(d[2])/int(d[1])*100, 3)) + " % \n\n"

        disk_info.extend([d[0], int(int(d[1])/1024**2), int(int(d[2])/1024**2), round(int(d[2])/int(d[1])*100, 3)])

        disks_info.append(disk_info)

    info += "{:<20}".format("total_disk") + str(int(disk_total/1024**2)) + " GB \n"
    info += "{:<20}".format("total_usable_disk") + str(int(disk_usable_total/1024**2)) + " GB \n\n"

    disk_total_info.extend([int(disk_total/1024**2), int(disk_usable_total/1024**2)])

    return info, disks_info, disk_total_info


def get_gpu_info() -> str:
    info = "GPU\n"

    number_of_gpu = int(os.popen("nvidia-smi -q -d memory | grep 'Attached GPUs'").read().split(':')[1])
    gpu_memories = os.popen("nvidia-smi -q -d memory | grep 'Total'").read().strip().split('\n')
    gpu_using_memories = os.popen("nvidia-smi -q -d memory | grep 'Used'").read().strip().split('\n')
    gpu_models = os.popen("nvidia-smi -L").read().split('\n')
    gpu_total_memory = 0
    gpu_total_using_memory = 0

    # 각 gpu들 정보 [[이름, 메모리, 사용중인메모리, 사용률]]
    gpus_info = []
    # 총 gpu 정보 [개수, 메모리, 사용중인메모리, 사용률]
    gpu_total_info = []

    for i in range(number_of_gpu):
        gpu_model = gpu_models[i]

        gpu_info = []

        name: str = ' '.join(gpu_model.split()[2:-2])
        memory: int = int(gpu_memories[i*2].split(':')[-1].split()[0])
        using_memory: int = int(gpu_using_memories[i*2].split(':')[-1].split()[0])
        using_percent: float = round(int(gpu_using_memories[i*2].split(':')[-1].split()[0])/int(gpu_memories[i*2].split(':')[-1].split()[0])*100, 3)

        info += "{:<20}: ".format("GPU " + str(i)) + name + "\n"
        info += "{:<20}: ".format("memory") + str(memory) + " MB\n"
        info += "{:<20}: ".format("using_memory") + str(using_memory) + " MB\n"
        info += "{:<20}: ".format("using_percent") + str(using_percent) + " %\n\n"

        gpu_total_memory += memory
        gpu_total_using_memory += using_memory

        gpu_info.extend([name, memory, using_memory, using_percent])

        gpus_info.append(gpu_info)


    info += "{:<20}: ".format("number_of_gpu") + str(number_of_gpu) + "\n"
    info += "{:<20}: ".format("total_memory") + str(gpu_total_memory) + " MB\n"
    info += "{:<20}: ".format("total_using_memory") + str(gpu_total_using_memory) + " MB\n"
    info += "{:<20}: ".format("total_using_percent") + str(round(gpu_total_using_memory/gpu_total_memory*100, 3)) + " %\n"

    gpu_total_info.extend([number_of_gpu, gpu_total_memory, gpu_total_using_memory, round(gpu_total_using_memory/gpu_total_memory*100, 3)])


    return info, gpus_info, gpu_total_info


if __name__ == "__main__":
    # cpu 정보 [제품이름, 코어수, 스레드수, 사용률]
    info1, cpu_info = get_cpu_info()
    # 메모리 정보 [총용량, 사용가능 용량, 사용량]
    info2, memory_info = get_memory_info()
    # 각 disk 정보 [[디스크이름, 사용량(GB), 사용량(%)]]
    # 총 disk 정보 [총 디스크 용량, 사용가능 디스크 용량]
    info3, disks_info, disk_total_info = get_disk_info()
    # 각 gpu들 정보 [[이름, 메모리, 사용중인메모리, 사용률]]
    # 총 gpu 정보 [개수, 메모리, 사용중인메모리, 사용률]
    info4, gpus_info, gpu_total_info = get_gpu_info()

    # print(info)

    # 파일 저장
    with open('/home/oem/felix/20220803/device_info.txt', 'w') as f:
        f.write(info1)
        f.write(info2)
        f.write(info3)
        f.write(info4)

    # print(psutil.sensors_temperatures())
import os
import psutil

class Node:
    def get_fixed_info():
        #ip
        ip = os.popen("hostname -I").read().split()[0]
        #hostname
        host_name: str = os.popen("hostname").read().split()[0]
        #cpu
        cpu_name: str = os.popen("cat /proc/cpuinfo | grep 'model name' | tail -1").read().split(":")[-1].split("\n")[0]
        #gpu
        gpu_num = int(os.popen("nvidia-smi -q -d memory | grep 'Attached GPUs'").read().split(':')[1])
        gpu_memories = os.popen("nvidia-smi -q -d memory | grep 'Total'").read().strip().split('\n')
        all_gpu_mem = 0
        for i in range(gpu_num):
            memory: int = int(gpu_memories[i*2].split(':')[-1].split()[0])
            all_gpu_mem += memory
        #disk
        disk = os.popen("df | grep -e /dev/nvme -e /dev/sd -e /dev/hd").read().strip().split('\n')
        all_disk = 0
        for d in disk:
            d = d.split()
            all_disk += int(d[1])
        #memory
        memory = psutil.virtual_memory()
        all_mem =int(memory.total/1024**3)
        return {"ip":ip, "host_name":host_name, "cpu_name":cpu_name, "all_gpu_mem":all_gpu_mem, "gpu_num":gpu_num, "all_disk":all_disk,"all_mem":all_mem}

print(Node.get_fixed_info())
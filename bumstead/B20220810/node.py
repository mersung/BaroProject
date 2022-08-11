import os
import psutil

class Node:
    def __init__(self) -> None:
        self.node_fixed_info ={}
        self.node_changing_info ={}
        self.fixed_refresh()
        self.changing_refresh()

    def get_node_fixed_info(self):
        return self.node_fixed_info
    
    def get_node_changing_info(self):
        return self.node_changing_info

    def fixed_refresh(self):
        #ip
        ip: str = os.popen("hostname -I").read().split()[0]
        #hostname
        host_name: str = os.popen("hostname").read().split()[0]
        #memory
        memory = psutil.virtual_memory()
        all_mem :int =int(memory.total/1024**3)
        
        self.node_fixed_info["ip"] =ip
        self.node_fixed_info["host_name"] = host_name
        self.node_fixed_info["total_memory_capacity_GB"] = all_mem

    def changing_refresh(self):
        # memory 실시간
        memory = psutil.virtual_memory()
        self.node_changing_info["free_memory_GB"] : float = round(memory.available/1024**3, 3)
        self.node_changing_info["total_memory_using_percent"] : float = round(memory.used/memory.total*100, 3)

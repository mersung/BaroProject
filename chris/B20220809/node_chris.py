import os
import psutil

class Node:

    def __init__(self) -> None:
        self.node_fixed_info ={}
        self.fixed_refresh()

    def get_node_fixed_info(self):
        return self.node_fixed_info

    def fixed_refresh(self):
        #ip
        ip: str = os.popen("hostname -I").read().split()[0]
        #hostname
        host_name: str = os.popen("hostname").read().split()[0]
        #memory
        memory = psutil.virtual_memory()
        all_mem =int(memory.total/1024**3)
        
        self.node_fixed_info["ip"] =ip
        self.node_fixed_info["host_name"] = host_name
        self.node_fixed_info["all_mem"] = all_mem


if __name__ == "__main__":
    node = Node()
    print(node.get_node_fixed_info())
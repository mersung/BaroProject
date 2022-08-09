import os
import psutil

class Node:
    def __init__(self)->None:
        self.

    def node_changing(self):
        ## memory
        memory = psutil.virtual_memory()
        free_memory_GB= str(int(memory.available/1024**3)) 
        total_memory_using_percent = str(round(memory.used/memory.total*100, 3))


        return {"free_memory_GB":free_memory_GB, "total_memory_using_percent": total_memory_using_percent}

node = Node()
print(node.node_changing())

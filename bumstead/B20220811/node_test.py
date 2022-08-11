import os
import psutil
import paramiko

class Node:
    def __init__(self, ssh) -> None:
        self.node_fixed_info ={}
        self.node_changing_info ={}
        self.fixed_refresh(ssh)
        self.changing_refresh(ssh)
        self.ssh = ssh

    def get_node_fixed_info(self):
        return self.node_fixed_info
    
    def get_node_changing_info(self):
        return self.node_changing_info
    #stdin, stdout, stderr = ssh.exec_command()
    def fixed_refresh(self,ssh):
        #ip
        stdin, stdout, stderr = ssh.exec_command("hostname -I")
        ip: str = "".join(stdout.readlines()).split()[0].strip()
        #hostname
        stdin, stdout, stderr = ssh.exec_command("hostname ")
        host_name : str = "".join(stdout.readlines()).split()[0].strip()
        #memory
        stdin, stdout, stderr = ssh.exec_command("free -m | grep Mem")
        stdout = stdout.readline().split()
        all_mem :int =int(int(stdout[1])/1024)
        
        self.node_fixed_info["ip"] =ip
        self.node_fixed_info["host_name"] = host_name
        self.node_fixed_info["total_memory_capacity_GB"] = all_mem

    def changing_refresh(self,ssh):
        # memory 실시간
        stdin, stdout, stderr = ssh.exec_command("free -m | grep Mem")
        stdout = stdout.readline().split()
        free_mem = int(int(stdout[3])/1024)
        using_mem = int(stdout[2])/int(stdout[1])
        self.node_changing_info["free_memory_GB"] : int = free_mem
        self.node_changing_info["total_memory_using_percent"] : float = round(using_mem*100, 3)



if __name__ == "__main__":
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("192.168.20.115", port='22',  # 고객이 자신의 ip를 안다고 가정하에 '115'부분을 바꿈, 그러면 고객의 node에서 115로 가져올 수 있음, 지금은 115로 자기자신과 연결
                username="oem", password='baro')  # customer
    node = Node(ssh)
    print(node.get_node_fixed_info())
    print(node.get_node_changing_info())
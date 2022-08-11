import os
import psutil
import paramiko


ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("192.168.20.115", port='22',  # 고객이 자신의 ip를 안다고 가정하에 '115'부분을 바꿈, 그러면 고객의 node에서 115로 가져올 수 있음, 지금은 115로 자기자신과 연결
            username="oem", password='baro')  # customer
stdin, stdout, stderr = ssh.exec_command(
            "nvidia-smi -q -d memory | grep 'Attached GPUs'")
number_of_gpu = stdout.readline().strip().split(":")
print(number_of_gpu)
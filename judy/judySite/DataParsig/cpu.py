import os
import time
import paramiko


class CPU:

    # 생성자
    def __init__(self, ssh):
        self.fixed_cpu_info = {}
        self.changed_cpu_info = {}
        self.ssh = ssh
        self.fixed_data()

    # cpu 고정 정보 리턴
    def get_fixed_cpu_info(self):
        return self.fixed_cpu_info

    # cpu 변동 정보 리턴
    def get_changed_cpu_info(self):
        self.changed_data()
        return self.changed_cpu_info

    # cpu 고정 정보
    def fixed_data(self):
        # try:
        #     # cpu 제품 이름
        #     cpu_name: str = os.popen("cat /proc/cpuinfo | grep 'model name' | tail -1").read().split(":")[-1].strip()
        #     # cpu 코어 수
        #     cpu_core: int = int(os.popen("cat /proc/cpuinfo | grep 'cpu cores' | tail -1").read().split(":")[-1].strip())
        #     # cpu 스레드 수
        #     cpu_thread: int = int(os.popen("cat /proc/cpuinfo | grep 'siblings' | tail -1").read().split(":")[-1].strip())
        # except:
        #     raise Exception("fixed_data: shell 명령어 입력 에러")

        try:
            stdin, stdout, stderr = self.ssh.exec_command(
                "cat /proc/cpuinfo | grep 'model name' | tail -1")
            cpu_name: str = ''.join(stdout.readlines()).split(":")[-1].strip()

            stdin, stdout, stderr = self.ssh.exec_command(
                "cat /proc/cpuinfo | grep 'cpu cores' | tail -1")
            cpu_core: int = int(
                ''.join(stdout.readlines()).split(":")[-1].strip())

            stdin, stdout, stderr = self.ssh.exec_command(
                "cat /proc/cpuinfo | grep 'siblings' | tail -1")
            cpu_thread: int = int(
                ''.join(stdout.readlines()).split(":")[-1].strip())
        except:
            raise Exception("changed_data: shell 명령어 입력 에러")

        self.fixed_cpu_info["cpu_name"] = cpu_name
        self.fixed_cpu_info["number_of_core"] = cpu_core
        self.fixed_cpu_info["number_of_thread"] = cpu_thread

    # cpu 변동 정보
    def changed_data(self):
        # 총 CPU 사용량(%)
        # total_cpu_using_percent: float = round(psutil.cpu_percent(), 3)
        try:
            # "top -n1 | grep 'Cpu(s)'"
            # top -n2 -d 0.0000000001 | grep "Cpu(s)" | tail -1
            # 터미널 이용하면 앞에 이상한 바이너리가 붙어서 온다. 이를 삭제해 줘야한다.
            # top은 두번째 실행부터 제대로된 값을 뱉는데.. 이렇게 하는게 맞는지 의문임.
            usable_cpu = round(float(os.popen("top -n2 -d 0.00001 | grep 'Cpu(s)' | tail -1").read(
            ).split(",")[3].replace("\x1b(B\x1b[m\x1b[39;49m\x1b[1m", "").split()[0]), 3)
            # print("usablse :",usable_cpu)
        except:
            raise Exception("changed_data: shell 명령어 입력 에러")
        # 사용 가능한 CPU 사용량(%)
        using_cpu = round(100 - usable_cpu, 3)

        self.changed_cpu_info["total_cpu_using_percent"] = using_cpu
        self.changed_cpu_info["free_cpu_percent"] = usable_cpu

    def __str__(self):
        s = ""
        for c in self.fixed_cpu_info.values():
            s += str(c) + "\n"
        for c in self.changed_cpu_info.values():
            s += str(c) + "\n"
        return s


if __name__ == "__main__":
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("192.168.20.114", port='22',  # 고객이 자신의 ip를 안다고 가정하에 '115'부분을 바꿈, 그러면 고객의 node에서 115로 가져올 수 있음, 지금은 115로 자기자신과 연결
                username="oem", password='baro')  # customer
    cpu = CPU(ssh)
    while True:
        cpu.changed_data()
        time.sleep(0.5)
        print(cpu)

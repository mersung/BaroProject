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

        stdin, stdout, stderr = self.ssh.exec_command("cat /proc/cpuinfo | grep 'model name' | tail -1")
        print(''.join(stdout.readlines()))


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
            usable_cpu = float(os.popen("top -n2 -d 0.00001 | grep 'Cpu(s)' | tail -1").read().split(",")[3].strip().split()[-2])
            print(usable_cpu)
        except:
            raise Exception("changed_data: shell 명령어 입력 에러")
        # 사용 가능한 CPU 사용량(%)
        using_cpu = 100 - usable_cpu

        self.changed_cpu_info["total_cpu_using_percent"] = using_cpu
        self.changed_cpu_info["free_cpu_percent"] = usable_cpu

if __name__ == "__main__":
    cpu = CPU()
    while True:
        cpu.changed_data()
        time.sleep(0.8)

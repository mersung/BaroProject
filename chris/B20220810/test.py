import os
import time
import psutil


class CPU:

    # 생성자
    def __init__(self) -> None:
        self.fixed_cpu_info = {}
        self.changed_cpu_info = {}
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
        # cpu 제품 이름
        cpu_name: str = os.popen("cat /proc/cpuinfo | grep 'model name' | tail -1").read().split(":")[-1].strip()
        # cpu 코어 수
        cpu_core: int = int(os.popen("cat /proc/cpuinfo | grep 'cpu cores' | tail -1").read().split(":")[-1].strip())
        # cpu 스레드 수
        cpu_thread: int = int(os.popen("cat /proc/cpuinfo | grep 'siblings' | tail -1").read().split(":")[-1].strip())

        self.fixed_cpu_info["cpu_name"] = cpu_name
        self.fixed_cpu_info["number_of_core"] = cpu_core
        self.fixed_cpu_info["number_of_thread"] = cpu_thread

    # cpu 변동 정보
    def changed_data(self):
        # 총 CPU 사용량(%)
        total_using_cpu_percent: float = round(psutil.cpu_percent(), 3)

        # 사용 가능한 CPU 사용량(%)
        free_cpu_percent = 100 - total_using_cpu_percent

        self.changed_cpu_info["total_using_cpu_percent"] = total_using_cpu_percent
        self.changed_cpu_info["free_cpu_percent"] = free_cpu_percent


if __name__ == "__main__":
    cpu = CPU()
    n =10
    while n:
        print(cpu.get_fixed_cpu_info())
        print(cpu.get_changed_cpu_info())
        n-=1
        time.sleep(3)


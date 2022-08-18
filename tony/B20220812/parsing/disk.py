import time
import os
import paramiko

# Disk Class


class Disk:
    def __init__(self, ssh) -> None:

        self.ssh = ssh

        self.node_fixed_disk_info: dict = {}
        self.disk_fixed_list: list = []
        self.node_change_disk_info: dict = {}
        self.disk_change_list: list = []

        self.fixed_info()
        self.changing_info()

    # getter method
    def get_node_fixed_disk_info(self) -> dict:
        return self.node_fixed_disk_info

    def get_disk_fixed_list(self) -> list:
        self.changing_info()
        return self.disk_fixed_list

    def get_node_change_disk_info(self) -> dict:
        return self.node_change_disk_info

    def get_disk_change_list(self) -> list:
        self.changing_info()
        return self.disk_change_list

    # 고정값 받아오는 함수

    def fixed_info(self):

        try:
            # 원격에서 실행
            stdin, stdout, stderr = self.ssh.exec_command(
                "df | grep -e /dev/nvme -e /dev/sd -e /dev/hd")
            disk: list = "".join(stdout.readlines()).strip().split('\n')

            # Disk 총 용량, 사용가능 용량, 사용중 용량
            # disk = os.popen(
            #     "df | grep -e /dev/nvme -e /dev/sd -e /dev/hd").read().strip().split('\n')

            # 모든 Disk의 총 용량 -> NODE_FIXED에 들어감
            total_disk_capacity_GB: int = 0

            for d in disk:

                # 각 GPU의 정보를 넣을 Dictionary
                fixed_info: dict = {}

                d = d.split()

                # 모든 GPU의 총량 계산
                total_disk_capacity_GB += int(d[1])

                # 각 GPU의 정보 Dictionary 형태로 넣어줌
                fixed_info.update({"disk_path": d[0]})
                fixed_info.update(
                    {"each_total_disk_capacity_GB": round(int(d[1]) / 1024**2)})

                # GPU 리스트에 딕셔너리 넣기
                self.disk_fixed_list.append(fixed_info)

            # 모든 GPU 총량 딕셔너리에 넣기
            self.node_fixed_disk_info.update(
                {"total_disk_capacity_GB": round(total_disk_capacity_GB / 1024**2)})

        except:
            print("Problem with Parsing Disk: [Error] %s")

    # 변화하는 값 받아오는 함수
    def changing_info(self) -> list:

        # 초기화
        self.disk_change_list.clear()
        self.node_change_disk_info.clear()

        # 모든 Disk의 총 용량 -> NODE_FIXED에 들어감
        total_disk_capacity_GB: int = 0
        # 모든 Disk의 총 프리 -> NODE_FIXED에 들어감
        total_free_disk_GB: int = 0

        try:
            # 원격에서 실행
            stdin, stdout, stderr = self.ssh.exec_command(
                "df | grep -e /dev/nvme -e /dev/sd -e /dev/hd")
            disk: list = "".join(stdout.readlines()).strip().split('\n')

            # Disk 총 용량, 사용가능 용량, 사용중 용량
            # disk = os.popen(
            #     "df | grep -e /dev/nvme -e /dev/sd -e /dev/hd").read().strip().split('\n')

            for d in disk:

                # 각 GPU의 정보를 넣을 Dictionary
                chainging_info: dict = {}

                d = d.split()

                # 모든 DISK의 총량 계산
                total_disk_capacity_GB += int(d[1])
                # 모든 DISK의 사용량 계산
                total_free_disk_GB += int(d[3])

                chainging_info.update(
                    {"disk_using_GB": round(int(d[2]) / 1024**2)})
                chainging_info.update(
                    {"disk_using_percent": round(int(d[2])/int(d[1])*100, 3)})

                # GPU 리스트에 딕셔너리 넣기
                self.disk_change_list.append(chainging_info)

            self.node_change_disk_info.update(
                {"free_disk_GB": round(total_free_disk_GB / 1024**2)})
            self.node_change_disk_info.update({"free_disk_percent": round(
                (total_free_disk_GB / total_disk_capacity_GB) * 100, 3)})

        except:
            print("Problem with Parsing Disk: [Error] %s")


# if __name__ == "__main__":

#     ssh = paramiko.SSHClient()
#     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     ssh.connect("192.168.20.115", port='22',
#                 username="oem", password='baro')  # customer

#     disk = Disk(ssh)

#     print(disk.get_disk_fixed_list())
#     print(disk.get_node_fixed_disk_info())

#     while(True):
#         print(disk.get_disk_change_list())
#         print(disk.get_node_change_disk_info())
#         time.sleep(0.5)

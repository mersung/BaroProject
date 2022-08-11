import os
import psutil
import paramiko


class Gpu:
    def __init__(self,ssh) -> None:
        # 총량이기 때문에 dict로 한 번씩 빼줌
        self.node_fixed_gpu_info: dict = {}
        self.node_change_gpu_info: dict = {}
        # index가 4개까지 있기 때문에 list안에 dict들 넣어줌
        self.gpu_fixed_list: list = []
        self.gpu_change_list: list = []

        self.gpu_fixed()
        self.gpu_change()
        self.ssh = ssh

    # getter
    def get_node_fixed_gpu_info(self) -> dict:
        return self.node_fixed_gpu_info

    def get_node_change_gpu_info(self) -> dict:
        self.gpu_change()
        return self.node_change_gpu_info

    def get_gpu_fixed_list(self) -> list:
        return self.gpu_fixed_list

    def get_gpu_change_list(self) -> list:
        self.gpu_change()
        return self.gpu_change_list

    # gpu 고정 정보

    def gpu_fixed(self):
        # gpu_fixed 딕셔너리들을 담을 리스트
        #gpus_fixed = []
        # gpu 각각의 고정된 값을 담아줌, 메모리 총량, 이름, 인덱스, Ip
        gpu_fixed = {}
        # 총 GPU 메모리 총량을 더해줌
        #total_gpu = {}

        # info = "GPU\n"

        # gpu 개수(index 뽑기 용)
        # number_of_gpu = int(os.popen(
        #     "nvidia-smi -q -d memory | grep 'Attached GPUs'").read().split(':')[1])
        stdin, stdout, stderr = ssh.exec_command(
            "nvidia-smi -q -d memory | grep 'Attached GPUs'")
        number_of_gpu = stdout.readlines().split()
        print(number_of_gpu)
        # 노드고정에 들어갈 gpu개수
        self.node_fixed_gpu_info["number_of_gpu"] = number_of_gpu
        # 각 gpu 메모리 총량
        gpu_memories = os.popen(
            "nvidia-smi -q -d memory | grep 'Total'").read().strip().split('\n')
        # gpu 모델명
        gpu_models = os.popen("nvidia-smi -L").read().split('\n')

        # 노드 고정에 들어갈 총 메모리(MB)
        total_gpu_memory_capacity_MB = 0

        # # gpu 고정에 들어갈 것들
        # for i in range(number_of_gpu):
        #     gpu_model = gpu_models[i]

        #     gpu_info = []

        #     name: str = ' '.join(gpu_model.split()[2:-2])
        #     memory: int = int(gpu_memories[i*2].split(':')[-1].split()[0])

        #     total_gpu_memory_capacity_MB += memory

        #     gpu_fixed["gpu_index"] = i
        #     gpu_fixed["gpu_name"] = name
        #     gpu_fixed["each_total_gpu_memory_capacity_MB"] = memory

        #     # gpus_fixed.append(gpu_fixed)
        #     self.gpu_fixed_list.append(gpu_fixed)

        #     gpu_fixed = {}

        #total_gpu["total_gpu_memory_capacity_MB"] = total_gpu_memory_capacity_MB
        # 노드 고정에 들어갈 총 gpu 용량
        self.node_fixed_gpu_info.update(
            {"total_gpu_memory_capacity_MB": total_gpu_memory_capacity_MB})
        # gpus_fixed.append(total_gpu)

        # return gpus_fixed

    # 변하는 gpu 정보
    def gpu_change(self):
        # 초기화
        self.gpu_change_list.clear()
        self.node_change_gpu_info.clear()

        # 변하는 gpu 딕셔너리를 담을 리스트
        #gpus_change = []
        # 각 gpu 딕셔너리, 인덱스, ip, 각 gpu사용량(MB), 각 gpu사용률(%), ip는 나중에 따로
        gpu_change = {}

        gpu_using_memories = os.popen(
            "nvidia-smi -q -d memory | grep 'Used'").read().strip().split('\n')

        # gpu 개수(index 뽑기 용)
        number_of_gpu = int(os.popen(
            "nvidia-smi -q -d memory | grep 'Attached GPUs'").read().split(':')[1])
 
        # 각 gpu 메모리 총량
        gpu_memories = os.popen(
            "nvidia-smi -q -d memory | grep 'Total'").read().strip().split('\n')

        # 노드_변함에 들어갈 총 사용량
        total_gpu_memory_using_percent = 0
        total_gpu_memory_using_MB = 0
        for i in range(number_of_gpu):

            using_memory: int = int(
                gpu_using_memories[i*2].split(':')[-1].split()[0])
            total_gpu_memory_using_MB += using_memory

            using_percent: float = round(int(gpu_using_memories[i*2].split(':')[-1].split()[
                                         0])/int(gpu_memories[i*2].split(':')[-1].split()[0])*100, 3)
            total_gpu_memory_using_percent += using_percent

            # GPU변함에 들어갈 데이터
            gpu_change["gpu_index"] = i
            gpu_change["gpu_memory_using_MB"] = using_memory
            gpu_change["gpu_memory_using_percent"] = using_percent

            # gpus_change.append(gpu_change)
            self.gpu_change_list.append(gpu_change)
            gpu_change = {}
        # 노드_변함에 들어갈 총 사용량들
        self.node_change_gpu_info["total_gpu_memory_using_percent"] = total_gpu_memory_using_percent
        self.node_change_gpu_info["total_gpu_memory_using_MB"] = total_gpu_memory_using_MB
        # return gpus_change

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("192.168.20.115", port='22',  # 고객이 자신의 ip를 안다고 가정하에 '115'부분을 바꿈, 그러면 고객의 node에서 115로 가져올 수 있음, 지금은 115로 자기자신과 연결
            username="oem", password='baro')  # customer
Gpu = Gpu(ssh)
print(Gpu.gpu_fixed())
# print(Gpu().get_gpu_fixed_list())
# print(Gpu().get_gpu_change_list())
# print(Gpu().get_node_fixed_gpu_info())
# print(Gpu().get_node_change_gpu_info())
# print(Gpu.gpu_fixed())
# print(Gpu.gpu_change())

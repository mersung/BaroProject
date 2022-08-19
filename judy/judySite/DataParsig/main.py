from DataParsig.node import Node
from DataParsig.cpu import CPU
from DataParsig.disk_parsing import Disk
from DataParsig.gpu import Gpu
import time
import pymysql
import paramiko
import threading


class AdminDB:

    def __init__(self, conn, cur, ssh):
        # 원격 접속을 위한 ssh
        self.ssh = ssh

        self.node = Node(self.ssh)
        self.cpu = CPU(self.ssh)
        self.gpu = Gpu(self.ssh)
        self.disk = Disk(self.ssh)

        self.conn = conn
        self.cur = cur

        # 각 테이블에 들어가야 하는 데이터
        # Node
        self.node_fixed_table: dict = {}
        self.node_change_table: dict = {}

        # CPU
        self.cpu_table: dict = {}

        # GPU
        self.gpu_fixed_table: list = []
        self.gpu_changed_table: list = []

        # Disk
        self.disk_fixed_table: list = []
        self.disk_changed_table: list = []

        # FK로 쓰이는 값들
        self.cpu_name: dict = {'cpu_name': None}
        self.ip: dict = {'ip': None}
        self.gpu_index: list = []
        self.disk_path: list = []

        self.mergeFixedKey()
        self.mergeChangeKey()

    def mergeFixedKey(self):
        # node_fixed
        self.node_fixed_table.update(self.node.get_node_fixed_info())
        self.node_fixed_table.update(self.cpu.get_fixed_cpu_info())
        self.node_fixed_table.update(self.disk.get_node_fixed_disk_info())
        self.node_fixed_table.update(self.gpu.get_node_fixed_gpu_info())

        self.ip['ip'] = self.node_fixed_table.get('ip')

        # disk_fixed
        self.disk_fixed_table = self.disk.get_disk_fixed_list()
        for l in self.disk_fixed_table:
            l.update(self.ip)
            self.disk_path.append(l['disk_path'])  # disk_change에서 쓰는 FK 추출

        # gpu_fixed
        self.gpu_fixed_table = self.gpu.get_gpu_fixed_list()
        for l in self.gpu_fixed_table:
            l.update(self.ip)
            # gpu_change에서 쓰는 FK 추출 > 인덱스 맞추는거라 살짝 불안
            self.gpu_index.append(l['gpu_index'])

    def mergeChangeKey(self):

        # node_changed
        self.node_change_table.update(self.node.get_node_changing_info())
        self.node_change_table.update(self.cpu.get_changed_cpu_info())
        self.node_change_table.update(self.disk.get_node_change_disk_info())
        self.node_change_table.update(self.gpu.get_node_change_gpu_info())
        self.node_change_table.update(self.ip)

        # disk_change
        self.disk_changed_table = self.disk.get_disk_change_list()
        for i in range(0, len(self.disk_changed_table)):
            self.disk_changed_table[i].update(self.ip)
            self.disk_changed_table[i].update({'disk_path': self.disk_path[i]})

        # gpu_change
        self.gpu_changed_table = self.gpu.get_gpu_change_list()
        for i in range(0, len(self.gpu_changed_table)):
            self.gpu_changed_table[i].update(self.ip)
            self.gpu_changed_table[i].update({'gpu_index': self.gpu_index[i]})

    def makeSQL(self, table: str, data):
        # 넣을 data column
        columns_str: str = " ("

        # 넣을 data string
        values_str: str = "("

        # items만큼 돌리기
        for item in data.items():

            k: str = str(item[0]) + ","
            columns_str += k

            # value(data) 스트링의 경우 하나씩 ''로 묶어주기
            if (type(item[1]) == str):
                v: str = "'" + str(item[1]) + "',"
                values_str += v
            else:
                v: str = str(item[1])
                values_str += str(v) + ","

        # 마지막 ,제거 후 괄호 닫기
        columns_str = columns_str[:-1]
        values_str = values_str[:-1]
        sql = "INSERT INTO " + table + columns_str + ") VALUES " + values_str + ")"

        # DB Insert execute
        # print(sql)
        self.cur.execute(sql)
        self.conn.commit()

    def insertDB(self, table: str, data):

        # Dictionary인 경우
        if type(data) == dict:
            sql: str = self.makeSQL(table, data)

            # 리스트인 경우
        elif type(data) == list:

            # 딕셔너리인 경우처럼 리스트 수만큼 돌려주기
            for l in data:
                self.makeSQL(table, l)

    def changed_insert_db(self):
        self.mergeChangeKey()

        print("+++++++++++++++++++++++ Changed 값 ++++++++++++++++++++++")

        # 프로세스를 생성합니다
        # p1 = threading.Thread(target=self.insertDB, args=(
        #     "NODE_CHANGE", self.node_change_table))
        # p2 = threading.Thread(target=self.insertDB, args=(
        #     "DISK_CHANGE", self.disk_changed_table))
        # p3 = threading.Thread(target=self.insertDB, args=(
        #     "GPU_CHANGE", self.gpu_changed_table))

        # start로 각 프로세스를 시작합니다.
        # p1.start()
        # p2.start()
        # p3.start()

        # # join으로 각 프로세스가 종료되길 기다립니다 p1.join()이 끝난 후 p2.join()을 수행합니다
        # p1.join()
        # p2.join()
        # p3.join()

        # Node
        self.insertDB("NODE_CHANGE", self.node_change_table)

        # Disk
        self.insertDB("DISK_CHANGE", self.disk_changed_table)

        # GPU
        self.insertDB("GPU_CHANGE", self.gpu_changed_table)

        print("=================================")

    def fixed_insert_db(self):

        print("+++++++++++++++++++++++ fixed 값 ++++++++++++++++++++++")

        # 프로세스를 생성합니다
        # p1 = threading.Thread(target=self.insertDB, args=(
        #     "NODE_FIXED", self.node_fixed_table))
        # p2 = threading.Thread(target=self.insertDB, args=(
        #     "DISK_FIXED", self.disk_fixed_table))
        # p3 = threading.Thread(target=self.insertDB, args=(
        #     "GPU_FIXED", self.gpu_fixed_table))

        # # start로 각 프로세스를 시작합니다.
        # p1.start()
        # p2.start()
        # p3.start()

        # # join으로 프로세스 종료 대기. 선행 프로세스가 끝난 다음에 실행
        # p1.join()
        # p2.join()
        # p3.join()

        # Node
        self.insertDB("NODE_FIXED", self.node_fixed_table)

        # Disk
        self.insertDB("DISK_FIXED", self.disk_fixed_table)

        # GPU
        self.insertDB("GPU_FIXED", self.gpu_fixed_table)

    def extractDB(self, table):

        print("++++++++++++++++++++ %s Data ++++++++++++++++++++++++" %
              (table))

        # 저장할 리스트
        d_list: list = []

        sql = "SELECT * FROM " + table

        self.cur.execute(sql)
        result = self.cur.fetchall()

        for r in result:
            d_list.append(r)

        print(d_list)

        return d_list

    def get_fixed_DB(self):

        print("===================== FIXED 값 추출 ===========================")

        # 리턴할 모든 DATA를 담은 리스트
        f_list: list = []

        f_list.append(self.extractDB("NODE_FIXED"))
        f_list.append(self.extractDB("DISK_FIXED"))
        f_list.append(self.extractDB("GPU_FIXED"))

        return f_list

    def get_change_DB(self):
        print("===================== CHANGE 값 추출 ===========================")

        # 리턴할 모든 DATA를 담은 리스트
        c_list: list = []

        c_list.append(self.extractDB("NODE_CHANGE"))
        c_list.append(self.extractDB("DISK_CHANGE"))
        c_list.append(self.extractDB("GPU_CHANGE"))

        return c_list

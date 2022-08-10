from turtle import update
from chris.B20220809.node import Node
from felix.B20220809.cpu import CPU
from judy.B20220810.disk_parsing import Disk
from tony.B20220809.gpu import Gpu
import time
import pymysql


class AdminDB:

    def __init__(self, conn, cur):
        self.node = Node()
        self.cpu = CPU()
        self.gpu = Gpu()
        self.disk = Disk()

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

        self.mergeKey()

    def mergeKey(self):
        # 예외 처리 일단 제외

        # FK로 쓰이는 값들
        cpu_name: dict = {'cpu_name': None}
        ip: dict = {'ip': None}
        gpu_index: list = []
        disk_path: list = []

        # cpu
        self.cpu_table = self.cpu.get_fixed_cpu_info()

        cpu_name['cpu_name'] = self.cpu_table.get('cpu_name')

        # node_fixed
        self.node_fixed_table.update(self.node.get_node_fixed_info())
        self.node_fixed_table.update(self.disk.get_node_fixed_disk_info())
        self.node_fixed_table.update(self.gpu.get_node_fixed_gpu_info())
        self.node_fixed_table.update(cpu_name)

        ip['ip'] = self.node_fixed_table.get('ip')

        # node_changed
        self.node_change_table.update(self.node.get_node_changing_info())
        self.node_change_table.update(self.cpu.get_changed_cpu_info())
        self.node_change_table.update(self.disk.get_node_change_disk_info())
        self.node_change_table.update(self.gpu.get_node_change_gpu_info())
        self.node_change_table.update(ip)

        # disk_fixed
        self.disk_fixed_table = self.disk.get_disk_fixed_list()
        for l in self.disk_fixed_table:
            l.update(ip)
            disk_path.append(l['disk_path'])  # disk_change에서 쓰는 FK 추출

        # disk_change
        self.disk_changed_table = self.disk.get_disk_change_list()
        for i in range(0, len(self.disk_changed_table)):
            self.disk_changed_table[i].update(ip)
            self.disk_changed_table[i].update({'disk_path': disk_path[i]})

        # gpu_fixed
        self.gpu_fixed_table = self.gpu.get_gpu_fixed_list()
        for l in self.gpu_fixed_table:
            l.update(ip)
            # gpu_change에서 쓰는 FK 추출 > 인덱스 맞추는거라 살짝 불안
            gpu_index.append(l['gpu_index'])

        # gpu_change
        self.gpu_changed_table = self.gpu.get_gpu_change_list()
        for i in range(0, len(self.gpu_changed_table)):
            self.gpu_changed_table[i].update(ip)
            self.gpu_changed_table[i].update({'gpu_index': gpu_index[i]})

    def changed_insert_db(self):
        self.mergeKey()

        print("+++++++++++++++++++++++ Changed 값 ++++++++++++++++++++++")

        # Node
        self.insertDB("NODE_CHANGE", self.node_change_table)

        # Disk
        self.insertDB("DISK_CHANGE", self.disk_changed_table)

        # GPU
        self.insertDB("GPU_CHANGE", self.gpu_changed_table)

        print("=================================")

    def fixed_insert_db(self):

        print("+++++++++++++++++++++++ fixed 값 ++++++++++++++++++++++")

        # CPU
        self.insertDB("CPU", self.cpu_table)

        # Node
        self.insertDB("NODE_FIXED", self.node_fixed_table)

        # Disk
        self.insertDB("DISK_FIXED", self.disk_fixed_table)

        # GPU
        self.insertDB("GPU_FIXED", self.gpu_fixed_table)

    def makeSQL(self, table: str, data):
        # 넣을 data column
        columns_str: str = " ("

        # 넣을 data string
        values_str: str = "("

        # items만큼 돌리기
        for item in data.items():

            # key(column) 하나씩 ''로 묶어주기
            #k: str = "'" + str(item[0]) + "',"
            k: str = str(item[0]) + ","
            columns_str += k

            # value(data) 하나씩 ''로 묶어주기
            if (type(item[1]) == str):
                v: str = "'" + str(item[1]) + "',"
                values_str += v
            else:
                v: str = item[1]
                values_str += str(item[1]) + ","

        # 마지막 ,제거 후 괄호 닫기
        columns_str = columns_str[:-1]
        values_str = values_str[:-1]
        # sql = "INSERT INTO " + table + columns_str + ") VALUES " + values_str + ")"
        sql = "INSERT INTO " + table + columns_str + ") VALUES " + values_str + ")"

        # DB Insert execute
        print(sql)
        # self.cur.execute(sql)
        # self.conn.commit()

    def insertDB(self, table: str, data):

        # Dictionary인 경우
        if type(data) == dict:
            self.makeSQL(table, data)

            # 리스트인 경우
        elif type(data) == list:

            # 딕셔너리인 경우처럼 리스트 수만큼 돌려주기
            for l in data:
                self.makeSQL(table, l)


if __name__ == "__main__":

    # print("first: ", cpu.get_changed_cpu_info())
    # print("second: ", cpu.get_changed_cpu_info())

    conn = pymysql.connect(host='localhost', user='root',
                                password='baro', db='HWMonitoring', charset='utf8')
    cur = conn.cursor()

    admindb = AdminDB(conn, cur)

    try:
        admindb.fixed_insert_db()
        try:
            while True:
                admindb.changed_insert_db()
                time.sleep(1)
        except KeyboardInterrupt:
            conn.close()

    except:
        print("Wrong")

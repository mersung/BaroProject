from node import Node
from cpu import CPU
from disk import Disk
from gpu import Gpu
import time
import pymysql
import paramiko


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

    def changed_insert_db(self):
        self.mergeChangeKey()

        print("+++++++++++++++++++++++ Changed 값 ++++++++++++++++++++++")

        # Node
        self.insertDB("base_nodechanged", self.node_change_table)

        # Disk
        self.insertDB("base_diskchanged", self.disk_changed_table)

        # GPU
        self.insertDB("base_gpuchanged", self.gpu_changed_table)

        print("=================================")

    def fixed_insert_db(self):

        print("+++++++++++++++++++++++ fixed 값 ++++++++++++++++++++++")

        # Node
        self.insertDB("base_nodefixed", self.node_fixed_table)

        # Disk
        self.insertDB("base_diskfixed", self.disk_fixed_table)

        # GPU
        self.insertDB("base_gpufixed", self.gpu_fixed_table)

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
        print(sql)
        self.cur.execute(sql)
        self.conn.commit()

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

    conn = pymysql.connect(host='localhost', user='root',
                                password='baro', db='HWMonitoring', charset='utf8')
    cur = conn.cursor()

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("192.168.20.115", port='22',  # 고객이 자신의 ip를 안다고 가정하에 '115'부분을 바꿈, 그러면 고객의 node에서 115로 가져올 수 있음, 지금은 115로 자기자신과 연결
                username="oem", password='baro')  # customer

    admindb = AdminDB(conn, cur, ssh)
    

    try:
        admindb.fixed_insert_db()
        while True:
            admindb.changed_insert_db()
            time.sleep(2)

    except KeyboardInterrupt:
        conn.close()

    except:
        conn.close()
        print("Wrong")
    # stdin, stdout, stderr = ssh.exec_command('df -h')
    # print(''.join(stdout.readlines()))

    ssh.close()

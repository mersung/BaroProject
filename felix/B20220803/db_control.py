import pymysql
from hard_parsing import *

def create_table():
    pass

def insert_data(table_name, data):
    pass

if __name__ == "__main__":

    conn = pymysql.connect(host='localhost', user='root', password='baro', db='HWMonitoring', charset='utf8')
    cur = conn.cursor()

    # sql = "CREATE TABLE IF NOT EXISTS CPU (\
    #     cpu_name VARCHAR(50) NOT NULL PRIMARY KEY,\
    #     number_of_core SMALLINT NOT NULL,\
    #     number_of_thread SMALLINT NOT NULL);"

    # cur.execute(sql)

    # sql = "CREATE TABLE IF NOT EXISTS NODE(\
    #     ip VARCHAR(50) NOT NULL PRIMARY KEY,\
    #     cpu_name VARCHAR(50) NOT NULL,\
    #     FOREIGN KEY(cpu_name) REFERENCES CPU(cpu_name),\
    #     host_name VARCHAR(50) NOT NULL,\
    #     total_disk_GB FLOAT NOT NULL,\
    #     total_usable_disk_GB FLOAT NOT NULL,\
    #     number_of_disk SMALLINT NOT NULL,\
    #     total_memory_GB FLOAT NOT NULL,\
    #     total_usable_memory_GB FLOAT NOT NULL,\
    #     total_using_memory_percent FLOAT NOT NULL,\
    #     total_using_cpu_percent FLOAT NOT NULL,\
    #     total_gpu_memory_MB FLOAT NOT NULL,\
    #     total_using_gpu_memory_MB FLOAT NOT NULL,\
    #     total_using_gpu_memory_percent FLOAT NOT NULL,\
    #     number_of_gpu SMALLINT NOT NULL);"

    # cur.execute(sql)

    # sql = "CREATE TABLE IF NOT EXISTS GPU(\
    #     gpu_index_id SMALLINT NOT NULL,\
    #     ip VARCHAR(50) NOT NULL,\
    #     FOREIGN KEY(ip) REFERENCES NODE(ip),\
    #     each_gpu_memory_MB FLOAT NOT NULL,\
    #     each_using_gpu_memory_MB FLOAT NOT NULL,\
    #     each_using_gpu_memory_percent FLOAT NOT NULL,\
    #     gpu_name VARCHAR(50) NOT NULL,\
    #     primary key(gpu_index_id, ip));"

    # cur.execute(sql)

    # sql = "CREATE TABLE IF NOT EXISTS DISK(\
    #     disk_path_id VARCHAR(50) NOT NULL,\
    #     ip VARCHAR(50) NOT NULL,\
    #     each_using_disk_GB FLOAT NOT NULL,\
    #     each_using_disk_percent FLOAT NOT NULL,\
    #     name VARCHAR(50) NOT NULL,\
    #     primary key(disk_path_id, ip));"

    sql = "CREATE TABLE IF NOT EXISTS NODE_FIXED(\
        ip VARCHAR(20) NOT NULL PRIMARY KEY,\
        cpu_name VARCHAR(50) NOT NULL,\
        host_name VARCHAR(50) NOT NULL,\
        total_gpu_memory_capacity_MB INT NOT NULL,\
        number_of_gpu INT NOT NULL,\
        total_disk_capacity_GB INT NOT NULL,\
        total_memory_capacity_GB INT NOT NULL);"

    cur.execute(sql)

    sql = "CREATE TABLE IF NOT EXISTS DISK_FIXED(\
        disk_path VARCHAR(50) NOT NULL,\
        ip VARCHAR(20) NOT NULL,\
        total_disk_capacity_GB INT NOT NULL,\
        primary key(disk_path, ip));"

    cur.execute(sql)

    sql = 'ALTER TABLE DISK_FIXED ADD FOREIGN KEY(ip) REFERENCES NODE_FIXED(ip)'
    cur.execute(sql)

    # cpu 정보 [제품이름, 코어수, 스레드수, 사용률]
    # info1, cpu_info = get_cpu_info()
    # 메모리 정보 [총용량, 사용가능 용량, 사용량]
    # info2, memory_info = get_memory_info()
    # 각 disk 정보 [[디스크이름, 사용량(GB), 사용량(%)]]
    # 총 disk 정보 [총 디스크 용량, 사용가능 디스크 용량]
    # info3, disks_info, disk_total_info = get_disk_info()
    # 각 gpu들 정보 [[이름, 메모리, 사용중인메모리, 사용률]]
    # 총 gpu 정보 [개수, 메모리, 사용중인메모리, 사용률]
    # info4, gpus_info, gpu_total_info = get_gpu_info()
    # sql = "INSERT INTO CPU VALUES('" +\
    #     cpu_info[0] + "'," +\
    #     cpu_info[1] + "," +\
    #     cpu_info[2] + ");"

    # sql = "INSERT INTO CPU VALUES('{cpu_info[0]}',{cpu_info[1]},{cpu_info[2]});" 안됨

    # cur.execute(sql)

    # sql = "INSERT INTO NODE VALUES(\
    #     '127.0.0.1','" +\
    #     cpu_info[0] + "'," +\
    #     "'oem'," +\
    #     float(disk_total_info[0]) + "," +\
    #     float(disk_total_info[1]) + "," +\
    #     len(disks_info) + "," +\
    #     float(memory_info[0]) + "," +\
    #     float(memory_info[1]) + "," +\
    #     memory_info[2] + "," +\
    #     cpu_info[3] + "," +\
    #     gpu_total_info[1] + "," +\
    #     gpu_total_info[2] + "," +\
    #     gpu_total_info[0] + ");"

    # cur.execute(sql)

    # sql = "INSERT INTO NODE VALUES("
        

    conn.commit()

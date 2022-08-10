import pymysql
import sys
from ComputerClass import NodeInfo, GPUInfo, DiskInfo

conn = None
cur = None

# 연결


def ConnectDB():
    # Connect to MariaDB Platform
    try:
        global conn
        conn = pymysql.connect(
            user="root",
            password="baro",
            host="localhost",  # 192.168.20.114
            port=3306,
            database="judy"
        )

    except pymysql.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)


# 삽입
def InsertDB(table, node: NodeInfo = None, gpuInfos: list[GPUInfo] = None, diskInfos: list[DiskInfo] = None):

    if (conn != None):

        # Get Cursor
        global cur
        cur = conn.cursor()

        sql: str = "INSERT INTO " + table + \
            "VALUES(ip, hostname, total_gpu_memory_capacity, total_gpu_memory_used, total_gpu_memory_used_percent, total_memory_capacity, total_memory_used_percent, total_free_disk_capacity, total_thread_count, total_cpu_used_percent)"

        try:
            if (node != None):
                sql += "'" + node.ip + "', '"
                + node.hostname + "', '"
                + node.total_gpu_memory_capacity + "', '"
                + node.total_gpu_memory_usage + ", '"
                + node.total_gpu_memory_usage_percent + ", '"
                + node.total_memory_capacity + ", '"
                + node.total_memory_usage_percent + ", '"
                + node.total_disk_free + ", '"
                + node.total_thread_count + ", '"
                + node.total_cpu_usage_percent + "'"

            cur.excute(sql)
            conn.commit()

        except pymysql.Error as e:
            pass

    else:
        print("conn is None")

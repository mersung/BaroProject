import pymysql

conn = pymysql.connect(host='localhost', user='root',
                                password='baro', db='HWMonitoring', charset='utf8')
cur = conn.cursor()
fixnode = "SELECT * FROM NODE_FIXED"
cur.execute(fixnode)
node_fixed = cur.fetchall()
for record in node_fixed :
    print(record)
fixgpu = "SELECT * FROM GPU_FIXED"
cur.execute(fixgpu)
gpu_fixed = cur.fetchall()
for record in gpu_fixed :
    print(record)
fixdisk = "SELECT * FROM DISK_FIXED"
cur.execute(fixdisk)
disk_fixed = cur.fetchall()
for record in disk_fixed :
    print(record)
conn.close()
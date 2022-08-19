import time
import paramiko

def get_ssh(ip: str):
    # 해당 컴퓨터의 자원 정보를 알아오기 위한 ssh 원격 접속
    try:
        now = time.time()
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, port='22',  # 고객이 자신의 ip를 안다고 가정하에 '115'부분을 바꿈, 그러면 고객의 node에서 115로 가져올 수 있음, 지금은 115로 자기자신과 연결
                        username="oem", password='baro')
        # print(time.time()-now)
        return ssh
    except:
        raise Exception("ssh 접속 에러")

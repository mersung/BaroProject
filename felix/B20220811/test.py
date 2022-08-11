import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("192.168.20.115", port='22', username="oem", password='baro')

stdin, stdout, stderr = ssh.exec_command('df -h')
print(''.join(stdout.readlines()))
ssh.close()
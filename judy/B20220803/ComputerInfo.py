import platform
import os
import psutil
import torch
import shutil


def writeComputerInfo():

    # txt파일 출력 준비
    f = open("computerInfo.txt", "w")

    # CPU 정보
    f.write("CPU | Core counts: " + str(os.cpu_count()) + ", ")  # CPU 개수
    # CPU 모델 이름 터미널에서 가져옴
    f.write(os.popen("cat /proc/cpuinfo | grep 'model name' | head -1").read())

    # 메모리 정보
    f.write("Memory | Using Memory: " +
            str(psutil.virtual_memory().used // 1024**3) + "GB")
    f.write(", Total Memory: " +
            str(psutil.virtual_memory()[0] // 1024**3) + "GB")
    f.write("\n")

    # 디스크 정보
    # 라이브러리 사용
    # diskLabel = '/'
    # total, used, free = shutil.disk_usage(diskLabel)
    # print(total // 1000**3, used // 1000**3)

    diskInfo = os.statvfs('/')
    # 총량 = 디스크 블럭 하나의 사이즈 * 블럭 개수
    total = diskInfo.f_bsize * diskInfo.f_blocks // 1000**3
    # 사용중 = 디스크 블럭 하나의 사이즈 * (블럭 개수 - 일반 사용자가 사용 가능한 블럭 개수)
    used = diskInfo.f_bsize * \
        (diskInfo.f_blocks - diskInfo.f_bavail) // 1000**3
    f.write("Disk | Using Disk: " + str(used) + "GB")
    f.write(", Total Disk: " + str(total) + "GB")
    f.write("\n")

    # GPU 정보
    if (torch.cuda.is_available):
        f.write("GPU | Count: " + str(torch.cuda.device_count()))
        f.write(", Name: " + torch.cuda.get_device_name(torch.cuda.current_device()))
        # 사용중인 메모리 = total - free
        f.write(", Using Memory: " + str((torch.cuda.mem_get_info()
                                          [1] - torch.cuda.mem_get_info()[0]) // 1024**2) + "KB")

    # 파일 닫기
    f.close()
    return


if __name__ == "__main__":
    writeComputerInfo()

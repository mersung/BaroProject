import os

# Disk Class
class Disk:

    # 고정값 받아오는 함수
    def get_fixed_info(self):

        disk_fixed_list: list[dict] = []
    
        # Disk 총 용량, 사용가능 용량, 사용중 용량
        disk = os.popen("df | grep -e /dev/nvme -e /dev/sd -e /dev/hd").read().strip().split('\n')

        # 모든 Disk의 총 용량
        total_disk_capacity_GB: int = 0

        for d in disk:

            # 각 GPU의 정보를 넣을 Dictionary
            fixed_info: dict = {}

            d = d.split()
            
            # 모든 GPU의 총량 계산
            total_disk_capacity_GB += int(d[1])

            # 각 GPU의 정보 Dictionary 형태로 넣어줌
            fixed_info.update({"disk_path" : d[0]})
            fixed_info.update({"each_total_disk_capacity_GB" : round(int(d[1]) / 1024**2)})
            
            # GPU 리스트에 딕셔너리 넣기
            disk_fixed_list.append(fixed_info)

        # 모든 GPU 총량 dictionary 형태로 마나들기
        total_disk_capacity_info: dict = {"total_disk_capacity_GB":round(total_disk_capacity_GB / 1024**2)}

        # 고정된 디스크 값: [{각 디스크 경로, 각 디스크 총량}], 모든 디스크 총량
        return disk_fixed_list, total_disk_capacity_info

    # 변화하는 값 받아오는 함수
    def get_changing_info(self) -> list:
        
        # NODE_CHANGE에 들어갈 Disk 정보
        node_change_disk_info: dict = {}

        disk_chainging_list:list[dict] = []

        # Disk 총 용량, 사용가능 용량, 사용중 용량
        disk = os.popen("df | grep -e /dev/nvme -e /dev/sd -e /dev/hd").read().strip().split('\n')
        
        for d in disk:

            # 각 GPU의 정보를 넣을 Dictionary
            chainging_info: dict = {}

            d = d.split()

            # 각 GPU의 정보 Dictionary 형태로 넣어줌
            chainging_info.update({"disk_using_GB" : round(int(d[2]) / 1024**2)})
            chainging_info.update({"disk_using_percent" : round(int(d[2])/int(d[1])*100, 3)})
            
            
            node_change_disk_info.update({"free_disk_GB" : round(int(d[3]) / 1024**2)})
            node_change_disk_info.update({"free_disk_percent" : round(int(d[3]) / 1024**2)})

            # GPU 리스트에 딕셔너리 넣기
            disk_chainging_list.append(chainging_info)

        # 변화하는 값: [{각 디스크 사용량(GB), 각 디스크 사용량(%)}], 
        return disk_chainging_list, 

if __name__ == "__main__":
    disk = Disk()

    print(disk.get_changing_info())

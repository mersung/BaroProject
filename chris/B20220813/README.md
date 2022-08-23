# HWMonitoring
바로AI 회사 프로젝트

## 프로젝트명 
***
    Hardware Monitoring Service
####
    Baro AI의 자체 소프트웨어 인프라인 클러스터링 솔루션 'TIE" 내부에서 
    Node와 그에 따른 CPU, GPU, DISK, MEMORY등의 정보를 실시간으로 불러와서 모니터링 할 수 있는 프로그램
#



## 프로젝트 기간
    2022.08.03 ~ 2022.08.23
#

## ERD 구상
***
![image](https://user-images.githubusercontent.com/86938974/184828840-4e809d19-8a34-430c-8523-9ccdb122667d.png)
####

## 형상 관리
***
####
2022-08-08

    ERD 구상, 작성
#

####
2022-08-09
    
    Node 고정 클래스,모듈화
     
#

####
2022-08-10

    Node 고정 클래스,모듈화, makeSQL(), insert DB()작성

#

####
2022-08-11 

    ssh 연결을 위한 data parsing 재작업

#

####
2022-08-12

    Django 연결 및 models.py 작성

#

####
2022-08-16

    Django MVC 연결 및 view 초안 출력 
    
#

####
2022-08-17

    Changed Data 실시간 출력
    
#

####
2022-08-19

    다중 Node 입력 처리
    
#

####
2022-08-22

    예외처리 및 싱크 맞추기
    
#

## models.py 일부(테이블 생성)

![image](https://user-images.githubusercontent.com/86938974/184829408-c9af4e9d-b203-47a0-8ff0-9b875e973d67.png)

## 뷰와 url 연결 (urls.py 세팅)

![image](https://user-images.githubusercontent.com/86938974/184829688-fb55e631-f626-4748-b053-666f311f9474.png)

## html에 데이터 전달(views.py)

![image](https://user-images.githubusercontent.com/86938974/184830034-22c65fc2-dd91-48da-bf80-4a7fc961cfb2.png)

## 뷰로 출력(일부)

![image](https://user-images.githubusercontent.com/86938974/184830137-b161ace0-beb5-48ab-afa1-98410128a1ed.png)



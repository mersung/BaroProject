# BaroProject
바로AI 회사 프로젝트

## 프로젝트명 
***
    Hardware Monitoring Service
####
    Baro AI의 자체 소프트웨어 인프라인 클러스터링 솔루션 'TIE" 내부에서 
    Node와 그에 따른 CPU, GPU, DISK, MEMORY등의 정보를 실시간으로 불러와서 모니터링 할 수 있는 프로그램
#
## 팀원소개
***
    심대성(Tony), 김용후(Felix), 이아연(Judy), 이승준(Bumstead), 이원형(Chris)
#
## 프로젝트 기간
***
    2022.08.03 ~
#

## ERD 구상
***
![image](https://user-images.githubusercontent.com/86938974/184828840-4e809d19-8a34-430c-8523-9ccdb122667d.png)
####

## 형상 관리
***
####
2022-08-08

    심대성(tony) : Node 고정, Node 변함 ERD 구상, 작성
    
    이아연(judy) : Disk 고정, Disk 변함 ERD 구상, 작성
    
    김용후(felix) : Cpu, Gpu 고정, Gpu 변화 ERD 구상, 파싱코드, 작성
#

####
2022-08-09
    
    심대성(tony) : GPU 클래스,모듈화
    
    이아연(judy) : Disk 클래스,모듈화
    
    김용후(felix) : CPU 클래스,모듈화

    이승준(bumstead) : Node 변화 클래스,모듈화

    이원형(chris) : Node 고정 클래스,모듈화
     
    
#

####
2022-08-10

    심대성(tony) : GPU 클래스, 모듈화 수정, 테이블 수정, 오류 수정
    
    이아연(judy) : Admin DB 클래스 생성 후, __init__, mergeKey()작성, 고정 데이터 저장
     
    김용후(felix) : CPU 클래스, 모듈화 수정, 테이블 수정, 오류 수정

    이승준(bumstead) : Node 변화 클래스,모듈화, makeSQL(), insert DB()작성

    이원형(chris) : Node 고정 클래스,모듈화, makeSQL(), insert DB()작성

#

####
2022-08-11 

    심대성(tony) : ssh 연결을 위한 data parsing 재작업
    
    이아연(judy) : ssh 연결을 위한 data parsing 재작업
     
    김용후(felix) : ssh 연결을 위한 data parsing 재작업

    이승준(bumstead) : ssh 연결을 위한 data parsing 재작업

    이원형(chris) : ssh 연결을 위한 data parsing 재작업

#

####
2022-08-12

    심대성(tony) : Django 연결 및 models.py 작성
    
    이아연(judy) : Django 연결 및 models.py 작성
     
    김용후(felix) : Django 연결 및 models.py 작성

    이승준(bumstead) : Django 연결 및 models.py 작성

    이원형(chris) : Django 연결 및 models.py 작성

#

####
2022-08-16

    심대성(tony) : Django MVC 연결 및 view 초안 출력 

    이승준(bumstead) : Django MVC 연결 및 view 초안 출력 

    이원형(chris) : Django MVC 연결 및 view 초안 출력 
    
#

####
2022-08-17 ~ 2022-08-23

    심대성(tony) : url 요청에 의해 views.py에서 모듈화 해놓은 python 코드 실행, 데이터 삽입 후 VIEW로 json데이터 전달 확인, 오류 수정
                  실시간으로 데이터 삽입, 비동기 처리(Ajax)방식 사용하여 새로고침 없이 실시간 데이터 VIEW로 출력 성공 
                  관리자 입장에서 볼 수 있도록 IP를 나눠서 출력

    이아연(judy) : Django 이용한 백엔드 구성, html, ajax를 통한 프론트엔드 구성

    김용후(felix) : Django db 설정, views 작성, 파싱코드와 django 서버 연결
                    ssh 연결 재설정, html 작성, 데이터 올바르게 전달되는지 확인, 각종 오류 수정, 예외처리
                    실시간으로 데이터 삽입, 비동기 처리(Ajax)방식 사용하여 새로고침 없이 실시간 데이터 출력 성공
                    프로그래스 바를 이용하여 cpu, gpu, memory 상태 출력

    이승준(bumstead) : COVID-19 감염

    이원형(chris) : Django MVC 연결 및 view 초안 출력
                    Changed Data 실시간 출력
                    다중 Node 입력 처리
                    예외처리 및 싱크 맞추기
    
#


## models.py 일부(테이블 생성)

![image](https://user-images.githubusercontent.com/86938974/184829408-c9af4e9d-b203-47a0-8ff0-9b875e973d67.png)

## 뷰와 url 연결 (urls.py 세팅)

![image](tony/image/url.png)

## html에 데이터 전달(views.py)

![image](https://user-images.githubusercontent.com/86938974/184830034-22c65fc2-dd91-48da-bf80-4a7fc961cfb2.png)

## 뷰로 출력(일부)

![image](https://user-images.githubusercontent.com/86938974/184830137-b161ace0-beb5-48ab-afa1-98410128a1ed.png)

## Ajax 비동기 처리(실시간 데이터 출력용)

![image](tony/image/ajax.png)
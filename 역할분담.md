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
![바로AI 프로젝트 ERD ](https://user-images.githubusercontent.com/86938974/183346335-13bb400a-b4c6-4896-916a-d7f3f1907a13.png)
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

발표 자료
================================

### 데이터베이스 적용분야

> 도서 대출 프로그램


### 데이터베이스를 만들기 위한 요구사항 분석

* 요구사항
  1. 도서 정보 관리
  2. 회원 관리
  3. 도서 대출 관리
  4. 회원의 대출 이력 관리
  5. 연체 사항 관리
  6. 도서 예약
  7. 알림
  8. 도서 카테고리 관리
  9. 프로그램 인터페이스

* 쿼리문 10가지
  1. 모든 도서 목록 확인
  2. 대출 중인 도서 확인
  3. 특정 도서 대출 이력 검색
  4. 특정 학생의 대출 이력 검색
  5. 도서 연체 목록
  6. 도서 예약 목록 
  7. 도서 대출 통계 
  8. 도서 카테고리별 분류 
  9. 도서 대출 이력 보고서
  10. 도서 대출 가능한 도서 목록 

### ER 다이어그램 작성





파일 구조
================================

```txt
main.py: 메인 함수 코드. 프로그램 실행 시 이 파일 실행


modules/: ui와 연결되는 모듈이나 기타 파이썬(.py) 모듈들 모음 폴더
│
├─── MainWindow.py: main_window.ui 파일과 연결하여 메인 윈도우 창 구현
│
└─── functions.py: 각종 유용한 사용자 함수 모음 모듈


user_interfaces/: .ui 파일들 모음 폴더
│
└─── main_window.ui: 메인 윈도우의 ui를 구성하는 파일


defines/: 상수 값 모음 .py 파일들 모음 폴더
│
├─── strings.py: 프로그램에서 사용되는 문자열 지정
│
└─── paths.py: 각종 필요한 파일의 절대/상대 경로 지정


.gitignore: 깃허브에 업로드 되지 않는 파일들 지정


README.md: 도움말 파일
```


기능
================================

* ### 테이블/속성
| 테이블   | 속성                                                         |
|----------|--------------------------------------------------------------|
| 도서     | 도서번호P/도서명/저자/출판사/출판일자/카테고리/재고권수      |
| 회원     | 회원아이디P/비밀번호/회원명/전화번호/주소/이메일/회원등급    |
| 대출내역 | 대출번호P/회원아이디R/도서번호R/대출일/반납(예정)일/반납상태 |


### 도서 관리

**일반 회원**
* 도서 목록 확인 및 검색
* 도서 대출

**관리자**
* 도서 추가
* 도서 삭제
* 도서 정보 수정


### 회원 관리

**일반 회원**
* 내 정보 보기
* 내 정보 수정

**관리자**
* 회원 추가
* 회원 삭제
* 회원 정보 수정


### 도서 대출/반납

**일반 회원**
* 도서 대출 내역 확인
* 도서 반납
* 대출 연장

**관리자**
* 전체 대출/반납 현황
* 연체자 목록 확인




프로그램 사용 전 세팅들
================================

빌드하기
--------------------------------
* modules -> functions.py -> resourcePath 함수의 ["../" + ]를 먼저 제거할 것

* 빌드 시 pyinstaller -w --add-data="images/*;images" --add-data="uis/*;uis" main.py

MSSQL 초기 세팅
--------------------------------
SMMS 설정 https://freesugar.tistory.com/35

* B명은 BookManagement, 테이블 명은 Member, Book, Loan으로 아래 쿼리 실행 시 자동 적용
* 로그인 이름과 비밀번호는 pyuser, 1234로 할 것
* 사용자 매핑 시 BookManagement 지정


```sql
CREATE database BookManagement;
go

use BookManagement;

CREATE table Member
(
	uid				varchar(20)		NOT NULL		PRIMARY KEY,
	password		varchar(40)		NOT NULL,
	username		varchar(20)		NOT NULL,
	phone			varchar(20)		NULL,
	address			varchar(40)		NULL,
	email			varchar(20)		NULL,
	grade			varchar(20)		NOT NULL
);

go

CREATE table Book
(
	bid				int identity(1, 1)	NOT NULL	PRIMARY KEY,
	bookname		varchar(80)			NOT NULL,
	writer			varchar(20)			NOT NULL,
	publisher		varchar(40)			NULL,
	pubdate			date				NULL,
	category		varchar(20)			NULL,
	quantity		int					NOT NULL
);

go

CREATE table Loan
(
	lid				int identity(1, 1)	NOT NULL	PRIMARY KEY,
	uid				varchar(20)			NOT NULL	FOREIGN KEY REFERENCES Member (uid) ON DELETE NO ACTION,
	bid				int					NOT NULL	FOREIGN KEY REFERENCES Book (bid) ON DELETE NO ACTION,
	loandate		date				NOT NULL,
	returndate		date				NOT NULL,
	returnstatus	varchar(20)			NOT NULL,
);
```

> 필요 시 내용 추가하기
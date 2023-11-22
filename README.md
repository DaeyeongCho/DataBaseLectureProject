파일 구조
================================

```txt
main.py: 메인 함수 코드. 프로그램 실행 시 이 파일 실행


modules/: ui와 연결되는 모듈이나 기타 파이썬(.py) 모듈들 모음 폴더
│
├─── functions.py: 각종 유용한 사용자 함수 모음 모듈
│
├─── MainWindow.py: main_window.ui 파일과 연결하여 첫 화면 동작 구현
│
├──- MainWindowGeneral.py: 일반 회원 로그인 시 초기 화면 동작 구현
│
└─── MainWindowManager.py: 관리자 로그인 시 초기 화면 동작 구현


user_interfaces/: .ui 파일들 모음 폴더
│
├─── main_window.ui: 메인 윈도우의 ui를 구성하는 파일
│
├─── main_window_general.ui: 일반 회원 로그인 초기 화면 ui
│
└─── main_window_manager.ui: 관리자 로그인 초기 화면 ui


images/: 이미지, 아이콘 등 모음 폴더
│
└─── icon.ico 프로그램 아이콘


defines/: 상수 값 모음 .py 파일들 모음 폴더
│
├─── strings.py: 프로그램에서 사용되는 문자열들 지정
│
└─── paths.py: 각종 필요한 파일의 절대/상대 경로들 지정


temp/: 기타 파일들
│
├─── dbProjectQuery.sql: 데이터베이스 및 테이블 생성 쿼리
│
├─── .sql 확장자 파일들: 기타 쿼리들
│
└─── .drawio, .png 확장자 파일들: uml 관련 파일


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



실제 사용 쿼리
================================

### 회원 가입

**입력 값:** uid, password, username, phone, address, email, grade

```SQL
-- 입력한 아이디가 이미 존재하는 지 확인하는 쿼리 --
SELECT uid FROM Member WHERE uid = uid;

-- 새로운 회원 추가 --
INSERT INTO Member (uid, password, username, phone, address, email, grade) 
VALUES (uid, password, username, phone, address, email, grade);
```

### 로그인

**입력 값:** uid, password

```SQL
-- 아이디 존재 여부 확인 및 출력 --
SELECT * FROM Member WHERE uid = uid
```

### 도서 검색
```SQL
-- 도서 검색--
SELECT * 
FROM Book 
WHERE 컬럼명 LIKE '%입력값%'
[AND category = 입력값]
ORDER BY bookname ASC;

-- 도서 상세정보 --
SELECT *
FROM Book
WHERE bid = bid
```


프로그램 사용 전 세팅들
================================

MSSQL 초기 세팅
--------------------------------
* ### 반드시 해야 프로그램 정상 작동 함!

#### SMMS 설정 https://freesugar.tistory.com/35

* DB명은 BookManagement, 테이블 명은 Member, Book, Loan으로 아래 쿼리 실행 시 자동 적용
* 로그인 이름과 비밀번호는 pyuser, 1234로 할 것
* 사용자 매핑 시 BookManagement 지정


```sql
CREATE database BookManagement;
go

use BookManagement;

CREATE table Member
(
	uid				nvarchar(20)		NOT NULL		PRIMARY KEY,
	password		nvarchar(40)		NOT NULL,
	username		nvarchar(20)		NOT NULL,
	phone			nvarchar(20)		NULL,
	address			nvarchar(40)		NULL,
	email			nvarchar(20)		NULL,
	grade			nvarchar(20)		NOT NULL
);

go

CREATE table Book
(
	bid				int identity(1, 1)	NOT NULL	PRIMARY KEY,
	bookname		nvarchar(80)		NOT NULL,
	writer			nvarchar(20)		NOT NULL,
	publisher		nvarchar(40)		NOT NULL,
	pubdate			date				NOT NULL,
	category		nvarchar(20)		NULL,
	quantity		int					NOT NULL
);

go

CREATE table Loan
(
	lid				int identity(1, 1)	NOT NULL	PRIMARY KEY,
	uid				nvarchar(20)		NOT NULL	FOREIGN KEY REFERENCES Member (uid) ON DELETE NO ACTION,
	bid				int					NOT NULL	FOREIGN KEY REFERENCES Book (bid) ON DELETE NO ACTION,
	loandate		date				NOT NULL,
	returndate		date				NOT NULL,
	returnstatus	nvarchar(20)		NOT NULL,
);
```


ui 파일 꾸며주세요
================================

* main_window.ui
* main_window_general.ui
* main_window_manager.ui
* dialog_log_in.ui
* dialog_sign_up.ui
* widget_manager_book.ui


빌드하기
================================
* modules -> functions.py -> resourcePath 함수의 ["../" + ]를 먼저 제거할 것

* 빌드 시 pyinstaller -w --add-data="images/*;images" --add-data="uis/*;uis" main.py









> 필요 시 내용 추가하기
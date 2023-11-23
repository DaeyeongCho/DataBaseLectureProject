## database ##
HOST = 'localhost'
USER = 'pyuser'
PASSWORD = '1234'
DATABASE = 'BookManagement'
CHARSET = "utf8"

BOOK_DETAILS_TUPLE = ("bookname", "writer", "publisher", "pubdate", "category", "quantity") 
BOOK_DETAILS_TUPLE_MESSAGE = ("도서명", "저자", "출판사", "출판일", "카테고리", "재고수량")
BOOK_CATEGORY_TUPLE = ("전체", "소설", "시/에세이", "인문", "가정/육아", "요리", "건강", "취미/실용/스포츠", "경제/경영", "자기계발", "정치/사회", "역사/문화", "종교", "예술/대중문화", "중/고등참고서", "기술/공학", "외국어", "과학", "취업/수험서", "여행", "컴퓨터/IT", "잡지", "청소년")
ADD_BOOK_CATEGORY_TUPLE = ("없음", "소설", "시/에세이", "인문", "가정/육아", "요리", "건강", "취미/실용/스포츠", "경제/경영", "자기계발", "정치/사회", "역사/문화", "종교", "예술/대중문화", "중/고등참고서", "기술/공학", "외국어", "과학", "취업/수험서", "여행", "컴퓨터/IT", "잡지", "청소년")

## QMessageBox ##
WARNING_MESSAGE = "경고!"
INFORMATION_MESSAGE = "정보"

## mainWindow ##
GENERAL_MEMBER = "일반회원"
MANAGER_MEMBER = "관리자"

## signUp - mainWindow ##
SIGN_UP_ERROR_NO_INPUT = "필수 입력사항이 입력되지 않았습니다."
SIGN_UP_ERROR_ALREADY_EXIST = "이미 존재하는 아이디입니다."
SIGN_UP_SUCCESS = "가입 성공!"

## logIn - mainWindow ##
LOG_IN_ERROR_NO_USERID = "없는 아이디입니다."
LOG_IN_ERROR_WRONG_PASSWORD = "비밀번호가 틀렸습니다."

## mainWindowGeneral, mainWindowManager ##
LOG_IN_SUCCESS = "로그인 성공!"
LOG_IN_MESSAGE = "반갑습니다. %s회원님!"
LOG_OUT_MESSAGE_BOX_TITLE = "확인"
LOG_OUT_MESSAGE_BOX_CONTENT = "로그아웃 하시겠습니까?"

## dialogAddBook ##
ADD_BOOK_ERROR_NO_INPUT = "미입력 항목이 존재합니다."
ADD_BOOK_INFO_SAME_BOOK = "동일한 도서가 존재합니다. 그래도 추가하시겠습니까?"
ADD_BOOK_SUCCESS = "도서 추가 완료!"

## widgetManagerBook ##
DELETE_BOOK_QUESTION_MESSAGE = "정말 [%s]도서를 삭제하시겠습니까?"
DELETE_BOOK_ERROR_ON_LOAN = "해당 도서를 대여중인 회원이 있습니다!"
DELETE_SUCCESS_MESSAGE = "도서 삭제 완료!"
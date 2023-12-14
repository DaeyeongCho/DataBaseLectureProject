## database ##
HOST = 'localhost'
USER = 'pyuser'
PASSWORD = '1234'
DATABASE = 'BookManagement'
CHARSET = "utf8"

BOOK_DETAILS_TUPLE = ("bookname", "writer", "publisher", "pubdate", "category", "quantity") 
BOOK_DETAILS_TUPLE_MESSAGE = ("도서명", "저자", "출판사", "출판일", "카테고리", "재고수량")
BOOK_CATEGORY_TUPLE = ("전체", "소설", "시/에세이", "인문", "가정/육아", "요리", "건강", "취미/실용/스포츠", "경제/경영", "자기계발", "정치/사회", "역사/문화", "종교", "예술/대중문화", "기술/공학", "외국어", "과학", "여행", "컴퓨터/IT", "잡지", "청소년")
ADD_BOOK_CATEGORY_TUPLE = ("없음", "소설", "시/에세이", "인문", "가정/육아", "요리", "건강", "취미/실용/스포츠", "경제/경영", "자기계발", "정치/사회", "역사/문화", "종교", "예술/대중문화", "기술/공학", "외국어", "과학", "여행", "컴퓨터/IT", "잡지", "청소년")

## QMessageBox ##
WARNING_MESSAGE = "경고!"
INFORMATION_MESSAGE = "정보"

## mainWindow ##
GENERAL_MEMBER = "일반회원"
MANAGER_MEMBER = "관리자"

## signUp - mainWindow ##
SIGN_UP_ERROR_NO_INPUT = "필수 입력사항이 입력되지 않았습니다."
SIGN_UP_ERROR_SAME_PASSWORD = "비밀번호 확인이 잘못되었습니다."
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
HELLO_MESSAGE = "안녕하세요, %s 고객님!"

## widgetManagerBook ##
DELETE_BOOK_QUESTION_MESSAGE = "정말 [%s]도서를 삭제하시겠습니까?"
DELETE_BOOK_ERROR_ON_LOAN = "해당 도서를 대여중인 회원이 있습니다!"
DELETE_SUCCESS_MESSAGE = "도서 삭제 완료!"

## dialogAddBook ##
ADD_BOOK_ERROR_NO_INPUT = "미입력 항목이 존재합니다."
ADD_BOOK_INFO_SAME_BOOK = "동일한 도서가 존재합니다. 그래도 추가하시겠습니까?"
ADD_BOOK_SUCCESS = "도서 추가 완료!"

## dialogModifyBook ##
MODIFY_BOOK_QUESTION_MESSAGE = "수정하시겠습니까?"
MODIFY_BOOK_SUCCESS = "수정 완료!"

## widgetGeneralBook ##
LOAN_ERROR_ARREARS = "연체된 도서가 존재하여 대출 불가능합니다."
LOAN_ERROR_NO_QUANTITY = "해당 도서의 재고가 부족합니다."
LOAN_SUCCESS = "대출되었습니다."

## widgetGeneralLoan ##
LOAN_NOT_RETURN = "미반납"
LOAN_RETURNED = "반납됨"
LOAN_RETURN_QUESTION = "[%s] 도서를 반납하시겠습니까?"

## widgetGeneralUserInfo ##
USER_NAME_INTRODUCTION = "%s 회원님"
SET_USER_INFORMATION_QUESTION_MESSAGE = "회원님의 정보를 수정하시겠습니까?"
SET_USER_PASSWORD_QUESTION_MESSAGE = "회원님의 정보를 수정하시겠습니까?"
SET_USER_INFORMATION_SUCCESS = "회원님의 정보가 수정되었습니다."
SET_USER_PASSWORD_ERROR_NO_INPUT = "미입력된 항목이 존재합니다!"
SET_USER_PASSWORD_ERROR_DIFFERENT_INPUT = "비밀번호와 비밀번호 확인이 일치하지 않습니다!"
SET_USER_PASSWORD_SUCCESS = "비밀번호가 변경되었습니다."

## dialogProlongLoan ##
PROLONG_RETURN_DATE_MESSAGE = "연장되었습니다."

## widgetManagerUser ##
USER_DETAILS_LIST = ("회원 ID", "회원명", "전화번호", "주소", "이메일")
USER_DETAILS_FIELD_LIST = ("uid", "username", "phone", "address", "email")
INIT_PASSWORD_VALUE = '1111'
INIT_USER_PASSWORD_MESSAGE = "%s 회원님의 비밀번호를 초기화 하시겠습니까?"
INIT_USER_PASSWORD_SUCCESS = "%s 회원님의 비밀번호가 %s로 초기화 되었습니다."

## widgetManagerLoan
LOAN_DETAILS_LIST = ("회원명", "도서명", "대출일", "반납예정일")
LOAN_DETAILS_FIELD_LIST = ("username", "bookname", "loandate", "returndate")
LOAN_OVERDUE = "연체됨"
LOAN_NOT_OVERDUE = "연체되지 않음"
DELETE_OVERDUE_MESSAGE = "대출 연체를 해제 하시겠습니까?"
DELETE_OVERDUE_SUCCESS = "연체를 해제하였습니다."
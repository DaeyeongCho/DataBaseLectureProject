use BookManagement

INSERT INTO Member (uid, password, username, phone, address, email, grade) VALUES ('admin', '1234', '홍길동(관)', '010-1234-5678', '경상북도 경주시', 'abc@naver.com', '관리자');

INSERT INTO Member (uid, password, username, phone, address, email, grade) VALUES ('man1', '1234', '임꺽정', '010-1111-2222', '경상북도 포항시', 'aaa@naver.com', '일반회원');

INSERT INTO Book (bookname, writer, publisher, pubdate, category, quantity) VALUES ('데이터베이스 배움터', '홍의경', '생능출판', '2012-08-29', '기술/공학', 10);

INSERT INTO Book (bookname, writer, publisher, pubdate, category, quantity) VALUES ('해적의 시대를 건너는 법', '박웅현', '인티N', '2023-11-06', '인문', 5);
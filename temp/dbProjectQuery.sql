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
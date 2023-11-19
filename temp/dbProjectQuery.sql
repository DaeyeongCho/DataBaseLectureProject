CREATE database BookManagement;
go

use BookManagement;

CREATE table Member
(
	uid				varchar(20)		NOT NULL		PRIMARY KEY,
	password		varchar(20)		NOT NULL,
	username		varchar(20)		NOT NULL,
	phone			varchar(20)		NULL,
	address			varchar(20)		NULL,
	email			varchar(20)		NULL,
	grade			varchar(20)		NOT NULL
);

go

CREATE table Book
(
	bid				int identity(1, 1)	NOT NULL	PRIMARY KEY,
	bookname		varchar(20)			NOT NULL,
	writer			varchar(20)			NOT NULL,
	publisher		varchar(20)			NULL,
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
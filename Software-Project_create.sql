-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2019-04-07 14:27:06.703

-- init

drop table if exists StudentExam;
drop table if exists ExamInfo;
drop table if exists ReservationInfo;
drop table if exists StudentInfo;
drop table if exists TeacherInfo;


-- tables
-- Table: ExamInfo
CREATE TABLE ExamInfo (
    serial int NOT NULL AUTO_INCREMENT,
    t_account varchar(33) NOT NULL,
    t_name varchar(33) NOT NULL default '',
    e_name varchar(33) NOT NULL,
    start varchar(33) NOT NULL,
    end varchar(33) NOT NULL,
    place varchar(33) NOT NULL,
    week varchar(3) NOT NULL,
    weekday varchar(3) NOT NULL,
    tips varchar(99) NOT NULL,
    UNIQUE INDEX ExamInfo_ak_1 (start,place, week, weekday),
    UNIQUE INDEX ExamInfo_ak_2 (e_name, t_account),
    CONSTRAINT ExamInfo_pk PRIMARY KEY (serial)
);

-- Table: ReservationInfo
CREATE TABLE ReservationInfo (
    serial int NOT NULL AUTO_INCREMENT,
    t_account varchar(33) NOT NULL,
    s_account varchar(33) NULL,
    t_name varchar(33) NULL,
    s_name varchar(33) NULL,
    week varchar(3) NULL,
    weekday varchar(3) NULL,
    segment varchar(33) NULL,
    place varchar(33) NULL,
    reason varchar(33) NOT NULL default '',
    tips varchar(33) NULL default '',
    is_finished int NOT NULL DEFAULT 0,
    is_canceled int NOT NULL DEFAULT 0,
    UNIQUE INDEX ReservationInfo_ak_1 (t_account,week,weekday,segment),
    CONSTRAINT ReservationInfo_pk PRIMARY KEY (serial)
);

-- Table: StudentInfo
CREATE TABLE StudentInfo (
    account varchar(33) NOT NULL COMMENT '账号',
    password varchar(33) NULL,
    name varchar(33) NULL,
    number varchar(33) NULL,
    department varchar(33) NULL,
    classroom varchar(33) NULL,
    direction varchar(99) NULL,
    introduction varchar(666) NULL,
    email varchar(33) NULL,
    phone varchar(33) NULL,
    email_verified int NOT NULL DEFAULT 0,
    phone_verified int NOT NULL DEFAULT 0,
    CONSTRAINT account PRIMARY KEY (account)
) COMMENT '学生信息';

-- Table: TeacherInfo
CREATE TABLE TeacherInfo (
    account varchar(33) NOT NULL,
    password varchar(33) NOT NULL,
    name varchar(33) NULL,
    direction varchar(33) NULL,
    introduction varchar(33) NULL,
    workplace varchar(33) NULL,
    email varchar(33) NULL,
    phone varchar(33) NULL,
    email_verified int NOT NULL DEFAULT 0,
    phone_verified int NOT NULL DEFAULT 0,
    CONSTRAINT account PRIMARY KEY (account)
);

-- Table: student_exam
CREATE TABLE StudentExam (
    serial int NOT NULL AUTO_INCREMENT,
    s_account varchar(33) NOT NULL,
    e_serial int NOT NULL,
    is_finished int not null default 0,
    UNIQUE INDEX student_exam_ak_1 (s_account,e_serial),
    CONSTRAINT student_exam_pk PRIMARY KEY (serial)
);

-- foreign keys
-- Reference: ExamInfo_TeacherView (table: ExamInfo)
ALTER TABLE ExamInfo ADD CONSTRAINT ExamInfo_TeacherView FOREIGN KEY ExamInfo_TeacherView (t_account)
    REFERENCES TeacherInfo (account);

-- Reference: ReservationInfo_StudentView (table: ReservationInfo)
ALTER TABLE ReservationInfo ADD CONSTRAINT ReservationInfo_StudentView FOREIGN KEY ReservationInfo_StudentView (s_account)
    REFERENCES StudentInfo (account);

-- Reference: ReservationInfo_TeacherView (table: ReservationInfo)
ALTER TABLE ReservationInfo ADD CONSTRAINT ReservationInfo_TeacherView FOREIGN KEY ReservationInfo_TeacherView (t_account)
    REFERENCES TeacherInfo (account);

-- Reference: student_exam_StudentInfo (table: student_exam)
ALTER TABLE StudentExam ADD CONSTRAINT StudentExam_StudentInfo FOREIGN KEY StudentExam_StudentInfo (s_account)
    REFERENCES StudentInfo (account);

-- End of file.


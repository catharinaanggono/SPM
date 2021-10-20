DROP DATABASE IF EXISTS one_stop_lms;
CREATE DATABASE one_stop_lms;
USE one_stop_lms;

CREATE TABLE IF NOT EXISTS userTable(
    UserID INT NOT NULL AUTO_INCREMENT,
    UserName TEXT NOT NULL,
    UserType TEXT NOT NULL,
    PRIMARY KEY (UserID)
);

CREATE table if not exists course(
	CourseID INT NOT NULL AUTO_INCREMENT,
    CourseTitle VARCHAR(50) NOT NULL,
    CourseDescription TEXT NOT NULL,
    Badge TEXT NOT NULL,
    PRIMARY KEY (CourseID)
);

CREATE TABLE IF NOT EXISTS coursePrereq(
    CourseID INT NOT NULL,
    PrereqID INT NOT NULL,
    PRIMARY KEY (CourseID, PrereqID),
    FOREIGN KEY (CourseID) REFERENCES course(CourseID),
    FOREIGN KEY (PrereqID) REFERENCES course(CourseID)
);

CREATE TABLE IF NOT EXISTS LearnerCourse(
    LearnerID INT NOT NULL,
    CourseID INT NOT NULL,
    Status TEXT NOT NULL, -- completed, fail, ongoing
    PRIMARY KEY (LearnerID, CourseID),
    FOREIGN KEY (LearnerID) REFERENCES userTable(UserID),
    FOREIGN KEY (CourseID) REFERENCES course(CourseID)
    -- Should we also mention the class and the trainer?
);

CREATE table if not exists class(
    CourseID INT NOT NULL,
    ClassID INT NOT NULL AUTO_INCREMENT,
    StartDate DATETIME NOT NULL,
    EndDate DATETIME NOT NULL,
    ClassSize INT NOT NULL,
    RegistrationStartDate DATETIME NOT NULL,
    RegistrationEndDate DATETIME NOT NULL,
    PRIMARY KEY (ClassID),
    FOREIGN KEY (CourseID) REFERENCES course(CourseID)
);

CREATE TABLE IF NOT EXISTS classTrainer(
    CourseID INT NOT NULL,
    ClassID INT NOT NULL,
    TrainerID INT NOT NULL,
    PRIMARY KEY (ClassID, TrainerID),
    FOREIGN KEY (CourseID, ClassID) REFERENCES class(CourseID, ClassID),
    FOREIGN KEY (TrainerID) REFERENCES userTable(UserID)
);

CREATE TABLE IF NOT EXISTS classLearner(
    CourseID INT NOT NULL,
    ClassID INT NOT NULL,
    LearnerID INT NOT NULL,
    ApplicationStatus TEXT NOT NULL, -- self_enrolled, hr_enrolled, rejected, failed, ongoing, completed
    PRIMARY KEY (ClassID, CourseID, LearnerID),
    FOREIGN KEY (CourseID, ClassID) REFERENCES class(CourseID, ClassID),
    FOREIGN KEY (LearnerID) REFERENCES userTable(UserID) 
);

CREATE TABLE IF NOT EXISTS section(
    CourseID INT NOT NULL,
    ClassID INT NOT NULL,
    SectionID INT NOT NULL AUTO_INCREMENT,
    SectionName TEXT NOT NULL DEFAULT '',
    PRIMARY KEY (SectionID),
    FOREIGN KEY (CourseID) REFERENCES class(CourseID),
    FOREIGN KEY (ClassID) REFERENCES class(ClassID)
);

CREATE TABLE IF NOT EXISTS sectionMaterial(
    CourseID INT NOT NULL,
    ClassID INT NOT NULL,
    SectionID INT NOT NULL,
    MaterialContent VARCHAR(500) NOT NULL,
    PRIMARY KEY (CourseID, ClassID, SectionID, MaterialContent),
    FOREIGN KEY (CourseID) REFERENCES section(CourseID),
    FOREIGN KEY (ClassID) REFERENCES section(ClassID),
    FOREIGN KEY (SectionID) REFERENCES section(SectionID)
);

ALTER TABLE `sectionmaterial` ADD INDEX( `MaterialContent`);

CREATE TABLE IF NOT EXISTS quiz(
    CourseID INT NOT NULL,
    ClassID INT NOT NULL,
    SectionID INT NOT NULL,
    QuizID INT NOT NULL AUTO_INCREMENT,
    QuizTitle VARCHAR(50) NOT NULL,
    QuizTimer INT NOT NULL,
    PRIMARY KEY (QuizID),
    FOREIGN KEY (CourseID) REFERENCES section(CourseID),
    FOREIGN KEY (ClassID) REFERENCES section(ClassID),
    FOREIGN KEY (SectionID) REFERENCES section(SectionID)
);

CREATE TABLE IF NOT EXISTS finalQuiz(
    CourseID INT NOT NULL,
    QuizID INT NOT NULL AUTO_INCREMENT,
    QuizTitle VARCHAR(50) NOT NULL,
    QuizTimer INT NOT NULL,
    PRIMARY KEY (QuizID),
    FOREIGN KEY (CourseID) REFERENCES course(CourseID)
);


CREATE TABLE IF NOT EXISTS finalQuizQuestion(
    CourseID INT NOT NULL,
    QuizID INT NOT NULL,
    QuestionID INT NOT NULL AUTO_INCREMENT,
    QuestionContent TEXT NOT NULL,
    PRIMARY KEY (QuestionID),
    FOREIGN KEY (CourseID) REFERENCES finalQuiz(CourseID),
    FOREIGN KEY (QuizID) REFERENCES finalQuiz(QuizID)
);

CREATE TABLE IF NOT EXISTS finalQuizQuestionAnswer(
    CourseID INT NOT NULL,
    QuizID INT NOT NULL,
    QuestionID INT NOT NULL,
    AnswerID INT NOT NULL AUTO_INCREMENT,
    AnswerContent TEXT NOT NULL,
    Correct BOOLEAN NOT NULL,
    PRIMARY KEY (AnswerID),
    FOREIGN KEY (CourseID) REFERENCES finalQuizQuestion(CourseID),
    FOREIGN KEY (QuizID) REFERENCES finalQuizQuestion(QuizID),
    FOREIGN KEY (QuestionID) REFERENCES finalQuizQuestion(QuestionID)
);

CREATE TABLE IF NOT EXISTS finalStudentQuizResult(
    CourseID INT NOT NULL,
    ClassID INT NOT NULL,
    QuizID INT NOT NULL,
    LearnerID INT NOT NULL,
    Grade INT NOT NULL,
    AttemptID INT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (AttemptID),
    FOREIGN KEY (CourseID) REFERENCES finalQuiz(CourseID),
    FOREIGN KEY (QuizID) REFERENCES finalQuiz(QuizID),
    FOREIGN KEY (ClassID) REFERENCES class(ClassID),
    FOREIGN KEY (LearnerID) REFERENCES userTable(UserID)
);

CREATE TABLE IF NOT EXISTS question(
    CourseID INT NOT NULL,
    ClassID INT NOT NULL,
    SectionID INT NOT NULL,
    QuizID INT NOT NULL,
    QuestionID INT NOT NULL AUTO_INCREMENT,
    QuestionContent TEXT NOT NULL,
    PRIMARY KEY (QuestionID),
    FOREIGN KEY (CourseID) REFERENCES quiz(CourseID),
    FOREIGN KEY (ClassID) REFERENCES quiz(ClassID),
    FOREIGN KEY (SectionID) REFERENCES quiz(SectionID),
    FOREIGN KEY (QuizID) REFERENCES quiz(QuizID)
);

CREATE TABLE IF NOT EXISTS questionAnswer(
    CourseID INT NOT NULL,
    ClassID INT NOT NULL,
    SectionID INT NOT NULL,
    QuizID INT NOT NULL,
    QuestionID INT NOT NULL,
    AnswerID INT NOT NULL AUTO_INCREMENT,
    AnswerContent TEXT NOT NULL,
    Correct BOOLEAN NOT NULL,
    PRIMARY KEY (AnswerID),
    FOREIGN KEY (CourseID) REFERENCES question(CourseID),
    FOREIGN KEY (ClassID) REFERENCES question(ClassID),
    FOREIGN KEY (SectionID) REFERENCES question(SectionID),
    FOREIGN KEY (QuizID) REFERENCES question(QuizID),
    FOREIGN KEY (QuestionID) REFERENCES question(QuestionID)
);

CREATE TABLE IF NOT EXISTS studentQuizResult(
    CourseID INT NOT NULL,
    ClassID INT NOT NULL,
    SectionID INT NOT NULL,
    QuizID INT NOT NULL,
    LearnerID INT NOT NULL,
    Grade INT NOT NULL,
    AttemptID INT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (AttemptID),
    FOREIGN KEY (CourseID) REFERENCES quiz(CourseID),
    FOREIGN KEY (ClassID) REFERENCES quiz(ClassID),
    FOREIGN KEY (SectionID) REFERENCES quiz(SectionID),
    FOREIGN KEY (QuizID) REFERENCES quiz(QuizID),
    FOREIGN KEY (LearnerID) REFERENCES userTable(UserID)

);

CREATE TABLE IF NOT EXISTS studentAnswer(
    CourseID INT NOT NULL,
    ClassID INT NOT NULL,
    SectionID INT NOT NULL,
    QuizID INT NOT NULL,
    QuestionID INT NOT NULL,
    AnswerID INT NOT NULL,
    LearnerID INT NOT NULL,
    PRIMARY KEY (CourseID, ClassID, SectionID, QuizID, QuestionID,  LearnerID),
    FOREIGN KEY (CourseID) REFERENCES question(CourseID),
    FOREIGN KEY (ClassID) REFERENCES question(ClassID),
    FOREIGN KEY (SectionID) REFERENCES question(SectionID),
    FOREIGN KEY (QuizID) REFERENCES question(QuizID),
    FOREIGN KEY (AnswerID) REFERENCES questionAnswer(AnswerID),
    FOREIGN KEY (LearnerID) REFERENCES userTable(UserID)
);

CREATE TABLE IF NOT EXISTS MaterialProgress(
    CourseID INT NOT NULL,
    ClassID INT NOT NULL,
    SectionID INT NOT NULL,
    MaterialContent VARCHAR(500) NOT NULL,
    LearnerID INT NOT NULL,
    PRIMARY KEY (CourseID, ClassID, SectionID, MaterialContent, LearnerID),
    FOREIGN KEY (LearnerID) REFERENCES userTable(UserID),
    FOREIGN KEY (CourseID) REFERENCES sectionMaterial(CourseID),
    FOREIGN KEY (ClassID) REFERENCES sectionMaterial(ClassID),
    FOREIGN KEY (SectionID) REFERENCES sectionMaterial(SectionID),
    FOREIGN KEY (MaterialContent) REFERENCES sectionMaterial(MaterialContent)
);


CREATE TABLE IF NOT EXISTS courseForum(
    CourseID INT NOT NULL,
    ForumID INT AUTO_INCREMENT,
    ForumTitle TEXT NOT NULL,
    UserID INT NOT NULL,
    ForumDetails TEXT NOT NULL,
    ForumCreated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (ForumID),
    FOREIGN KEY (CourseID) REFERENCES course(CourseID),
    FOREIGN KEY (UserID) REFERENCES userTable(UserID)   
);

CREATE TABLE IF NOT EXISTS courseForumReply(
    ForumID INT NOT NULL,
    ReplyID INT AUTO_INCREMENT,
    ReplyContent TEXT NOT NULL,
    UserID INT NOT NULL,
    ReplyTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (ReplyID),
    FOREIGN KEY (ForumID) REFERENCES courseForum(ForumID),
    FOREIGN KEY (UserID) REFERENCES userTable(UserID)
);

CREATE TABLE IF NOT EXISTS publicForum(
    ForumID INT NOT NULL AUTO_INCREMENT,
    ForumTitle TEXT NOT NULL,
    UserID INT NOT NULL,
    ForumDetails TEXT NOT NULL,
    ForumCreated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (ForumID),
    FOREIGN KEY (UserID) REFERENCES userTable(UserID)
);

CREATE TABLE IF NOT EXISTS publicForumReply(
    ForumID INT NOT NULL,
    ReplyID INT AUTO_INCREMENT,
    ReplyContent TEXT NOT NULL,
    UserID INT NOT NULL,
    ReplyTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (ReplyID),
    FOREIGN KEY (ForumID) REFERENCES publicForum(ForumID),
    FOREIGN KEY (UserID) REFERENCES userTable(UserID)
);

FLUSH PRIVILEGES;
SET GLOBAL event_scheduler = ON;


DELIMITER $$
CREATE EVENT `UPDATE_ENROL_ONGOING` ON SCHEDULE EVERY 1 MINUTE STARTS '2021-10-14 13:02:26' ON COMPLETION NOT PRESERVE ENABLE DO update classLearner inner join class on class.classid = classlearner.classid set classLearner.ApplicationStatus = 'ongoing' where class.StartDate <= NOW() and (classLearner.ApplicationStatus = 'enrolled' or classlearner.ApplicationStatus = 'self_enrolled')
DELIMITER ;
-- create table if not exists course_forum();

-- create table if not exists public_forum(
--     topic
-- )

-- student

-- student_courses(
--     sid, cid, passed?
-- ) #test

use one_stop_lms;

insert into course(CourseTitle, CourseDescription, Badge) values ('SPM', 'This is a software project management module that will kill you and your social life', 'python_badge.png');
insert into course(CourseTitle, CourseDescription, Badge) values ('DB Management', 'Database Management', 'python_badge.png');
insert into course(CourseTitle, CourseDescription, Badge) values ('WAD 2', 'Web Application Management 2', 'python_badge.png');
insert into userTable(UserName, UserType) values ('Jhonny', 'Senior Engineer');
insert into userTable(UserName, UserType) values ('Julie', 'Senior Engineer');
insert into userTable(UserName, UserType) values ('Brenda', 'Junior Engineer');
insert into userTable(UserName, UserType) values ('Aaron', 'Junior Engineer');
insert into userTable(UserName, UserType) values ('Fred', 'Junior Engineer');
insert into class(CourseID, StartDate, EndDate, RegistrationStartDate, RegistrationEndDate, ClassSize) values (1, '2021-10-20 09:00:00', '2022-02-20 09:00:00', '2021-10-01 09:00:00', '2021-10-18 09:00:00', 50);
insert into class(CourseID, StartDate, EndDate, RegistrationStartDate, RegistrationEndDate, ClassSize) values (3, '2021-11-20 09:00:00', '2022-12-30 09:00:00', '2021-11-01 09:00:00', '2021-11-08 09:00:00', 45);
insert into classTrainer(CourseID, ClassID, TrainerID) values (1, 1, 1);
insert into classTrainer(CourseID, ClassID, TrainerID) values (3, 2, 2);
insert into LearnerCourse(CourseID, LearnerID, Status) values (1, 1, "completed");
insert into classLearner(ClassID, CourseID, LearnerID, ApplicationStatus) values (1, 1, 3, 'applied');
insert into classLearner(ClassID, CourseID, LearnerID, ApplicationStatus) values (2, 3, 4, 'applied');
insert into classLearner(ClassID, CourseID, LearnerID, ApplicationStatus) values (1, 1, 5, 'applied');
insert into classLearner(ClassID, CourseID, LearnerID, ApplicationStatus) values (1, 1, 4, 'enrolled');
insert into classLearner(ClassID, CourseID, LearnerID, ApplicationStatus) values (2, 3, 3, 'rejected');


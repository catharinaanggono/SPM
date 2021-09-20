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
    Status TEXT NOT NULL,
    PRIMARY KEY (LearnerID, CourseID),
    FOREIGN KEY (LearnerID) REFERENCES userTable(UserID),
    FOREIGN KEY (CourseID) REFERENCES course(CourseID)
    -- Should we also mention the class and the trainer?
);

CREATE table if not exists class(
    CourseID INT NOT NULL,
    ClassID INT NOT NULL AUTO_INCREMENT,
    TrainerID INT NOT NULL,
    StartDate DATE NOT NULL,
    EndDate DATE NOT NULL,
    ClassSize INT NOT NULL,
    PRIMARY KEY (ClassID),
    FOREIGN KEY (TrainerID) REFERENCES userTable(UserID),
    FOREIGN KEY (CourseID) REFERENCES course(CourseID)
);

CREATE TABLE IF NOT EXISTS classLearner(
    CourseID INT NOT NULL,
    ClassID INT NOT NULL,
    LearnerID INT NOT NULL,
    ApplicationStatus TEXT NOT NULL,
    PRIMARY KEY (ClassID, CourseID, LearnerID),
    FOREIGN KEY (CourseID, ClassID) REFERENCES class(CourseID, ClassID),
    FOREIGN KEY (LearnerID) REFERENCES userTable(UserID) 
);

CREATE TABLE IF NOT EXISTS section(
    CourseID INT NOT NULL,
    ClassID INT NOT NULL,
    SectionID INT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (SectionID),
    FOREIGN KEY (CourseID) REFERENCES class(CourseID),
    FOREIGN KEY (ClassID) REFERENCES class(ClassID)
);

CREATE TABLE IF NOT EXISTS sectionMaterial(
    CourseID INT NOT NULL,
    ClassID INT NOT NULL,
    SectionID INT NOT NULL,
    MaterialID INT NOT NULL AUTO_INCREMENT,
    MaterialContent TEXT NOT NULL,
    PRIMARY KEY (MaterialID),
    FOREIGN KEY (CourseID) REFERENCES section(CourseID),
    FOREIGN KEY (ClassID) REFERENCES section(ClassID),
    FOREIGN KEY (SectionID) REFERENCES section(SectionID)
);

CREATE TABLE IF NOT EXISTS quiz(
    CourseID INT NOT NULL,
    ClassID INT NOT NULL,
    SectionID INT NOT NULL,
    QuizID INT NOT NULL AUTO_INCREMENT,
    QuizTitle VARCHAR(50) NOT NULL,
    QuizTimer INT NOT NULL,
    PassingScore INT NOT NULL,
    PRIMARY KEY (QuizID),
    FOREIGN KEY (CourseID) REFERENCES section(CourseID),
    FOREIGN KEY (ClassID) REFERENCES section(ClassID),
    FOREIGN KEY (SectionID) REFERENCES section(SectionID)
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
    FOREIGN KEY (QuizID) REFERENCES question(QuizID)
);

CREATE TABLE IF NOT EXISTS studentQuizResult(
    CourseID INT NOT NULL,
    ClassID INT NOT NULL,
    SectionID INT NOT NULL,
    QuizID INT NOT NULL,
    LearnerID INT NOT NULL,
    Grade INT NOT NULL,
    PRIMARY KEY (CourseID, ClassID, SectionID, QuizID, LearnerID),
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
    MaterialID INT NOT NULL,
    LearnerID INT NOT NULL,
    STATUS BOOLEAN NOT NULL,
    PRIMARY KEY (CourseID, ClassID, SectionID, MaterialID, LearnerID),
    FOREIGN KEY (LearnerID) REFERENCES userTable(UserID),
    FOREIGN KEY (CourseID) REFERENCES sectionMaterial(CourseID),
    FOREIGN KEY (ClassID) REFERENCES sectionMaterial(ClassID),
    FOREIGN KEY (SectionID) REFERENCES sectionMaterial(SectionID),
    FOREIGN KEY (MaterialID) REFERENCES sectionMaterial(MaterialID)
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
-- create table if not exists course_forum();

-- create table if not exists public_forum(
--     topic
-- )

-- student

-- student_courses(
--     sid, cid, passed?
-- ) #test
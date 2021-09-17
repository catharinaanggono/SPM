DROP DATABASE IF EXISTS one_stop_lms;
CREATE DATABASE one_stop_lms;
USE one_stop_lms;

CREATE TABLE IF NOT EXISTS trainer(
    TrainerID INT NOT NULL AUTO_INCREMENT,
    TrainerName VARCHAR(65535) NOT NULL,
    PRIMARY KEY (TrainerID)
);

CREATE TABLE IF NOT EXISTS learner(
    LearnerID INT NOT NULL AUTO_INCREMENT,
    LearnerName VARCHAR(65535) NOT NULL,
    PRIMARY KEY (LearnerID)
    -- what else do we need to put in?
);

CREATE table if not exists course(
	CourseID INT NOT NULL AUTO_INCREMENT,
    CourseTitle VARCHAR(50) NOT NULL,
    CourseDescription VARCHAR(65535)NOT NULL,
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
    Status VARCHAR(65535) NOT NULL,
    PRIMARY KEY (LearnerID, CourseID),
    FOREIGN KEY (LearnerID) REFERENCES learner(LearnerID),
    FOREIGN KEY (CourseID) REFERENCES course(CourseID)
    -- Should we also mention the class and the trainer?
);

CREATE table if not exists class(
    CourseID INT NOT NULL,
    ClassID INT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (ClassID),
    FOREIGN KEY (CourseID) REFERENCES course(CourseID)
);

CREATE TABLE IF NOT EXISTS section(
    CourseID INT NOT NULL,
    ClassID INT NOT NULL,
    SectionID INT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (SectionID),
    FOREIGN KEY (CourseID) REFERENCES Class(CourseID),
    FOREIGN KEY (ClassID) REFERENCES Class(ClassID)
);

CREATE TABLE IF NOT EXISTS sectionMaterial(
    CourseID INT NOT NULL,
    ClassID INT NOT NULL,
    SectionID INT NOT NULL,
    MaterialID INT NOT NULL AUTO_INCREMENT,
    MaterialContent VARCHAR(65535) NOT NULL,
    PRIMARY KEY (MaterialID),
    FOREIGN KEY (CourseID) REFERENCES Section(CourseID),
    FOREIGN KEY (ClassID) REFERENCES Section(ClassID),
    FOREIGN KEY (SectionID) REFERENCES Section(SectionID)
);

CREATE TABLE IF NOT EXISTS quiz(
    CourseID INT NOT NULL,
    ClassID INT NOT NULL,
    SectionID INT NOT NULL,
    QuizID INT NOT NULL AUTO_INCREMENT,
    QuizTitle VARCHAR(50) NOT NULL,
    QuizTimer INT NOT NULL,
    PRIMARY KEY (QuizID),
    FOREIGN KEY (CourseID) REFERENCES Section(CourseID),
    FOREIGN KEY (ClassID) REFERENCES Section(ClassID),
    FOREIGN KEY (SectionID) REFERENCES Section(SectionID)
);

CREATE TABLE IF NOT EXISTS question(
    CourseID INT NOT NULL,
    ClassID INT NOT NULL,
    SectionID INT NOT NULL,
    QuizID INT NOT NULL,
    QuestionID INT NOT NULL AUTO_INCREMENT,
    QuestionContent VARCHAR(65535) NOT NULL,
    PRIMARY KEY (QuestionID),
    FOREIGN KEY (CourseID) REFERENCES QUIZ(CourseID),
    FOREIGN KEY (ClassID) REFERENCES QUIZ(ClassID),
    FOREIGN KEY (SectionID) REFERENCES QUIZ(SectionID),
    FOREIGN KEY (QuizID) REFERENCES QUIZ(QuizID)
);

CREATE TABLE IF NOT EXISTS questionAnswer(
    CourseID INT NOT NULL,
    ClassID INT NOT NULL,
    SectionID INT NOT NULL,
    QuizID INT NOT NULL,
    QuestionID INT NOT NULL,
    AnswerID INT NOT NULL AUTO_INCREMENT,
    AnswerContent VARCHAR(65535) NOT NULL,
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
    FOREIGN KEY (CourseID) REFERENCES QUIZ(CourseID),
    FOREIGN KEY (ClassID) REFERENCES QUIZ(ClassID),
    FOREIGN KEY (SectionID) REFERENCES QUIZ(SectionID),
    FOREIGN KEY (QuizID) REFERENCES QUIZ(QuizID),
    FOREIGN KEY (LearnerID) REFERENCES learner(LearnerID)

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
    FOREIGN KEY (LearnerID) REFERENCES learner(LearnerID)
);



-- create table if not exists course_forum();

-- create table if not exists public_forum(
--     topic
-- )

-- student

-- student_courses(
--     sid, cid, passed?
-- )
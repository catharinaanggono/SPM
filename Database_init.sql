-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Nov 09, 2021 at 10:38 AM
-- Server version: 10.3.31-MariaDB
-- PHP Version: 7.4.23

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `one_stop_lms`
--

-- --------------------------------------------------------

--
-- Table structure for table `class`
--

DROP DATABASE IF EXISTS one_stop_lms;

CREATE DATABASE one_stop_lms;

USE one_stop_lms;

CREATE TABLE `class` (
  `CourseID` int(11) NOT NULL,
  `ClassID` int(11) NOT NULL,
  `StartDate` datetime NOT NULL,
  `EndDate` datetime NOT NULL,
  `ClassSize` int(11) NOT NULL,
  `RegistrationStartDate` datetime NOT NULL,
  `RegistrationEndDate` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `class`
--

INSERT INTO `class` (`CourseID`, `ClassID`, `StartDate`, `EndDate`, `ClassSize`, `RegistrationStartDate`, `RegistrationEndDate`) VALUES
(1, 1, '2021-10-20 09:00:00', '2022-02-20 09:00:00', 50, '2021-10-01 09:00:00', '2021-10-18 09:00:00'),
(1, 2, '2021-11-30 09:00:00', '2022-03-31 09:00:00', 50, '2021-10-01 09:00:00', '2021-11-23 09:00:00'),
(3, 3, '2021-11-20 09:00:00', '2022-12-30 09:00:00', 45, '2021-11-01 09:00:00', '2021-11-08 09:00:00'),
(1, 4, '2021-11-30 22:06:00', '2021-12-30 22:07:00', 35, '2021-11-07 22:07:00', '2021-11-25 22:07:00'),
(4, 5, '2021-11-25 22:12:00', '2021-12-25 22:12:00', 55, '2021-11-07 22:13:00', '2021-11-17 22:13:00'),
(2, 6, '2021-11-30 22:21:00', '2021-12-30 22:21:00', 56, '2021-11-06 22:21:00', '2021-11-28 22:21:00'),
(3, 7, '2021-12-01 15:16:00', '2021-12-31 21:17:00', 0, '2021-11-01 15:17:00', '2021-11-30 15:17:00'),
(1, 8, '2021-11-25 17:41:00', '2021-12-30 17:42:00', 43, '2021-11-09 17:42:00', '2021-11-24 17:42:00'),
(1, 9, '2021-11-25 17:43:00', '2021-12-31 17:43:00', 46, '2021-11-10 17:43:00', '2021-11-24 17:43:00'),
(1, 10, '2021-11-22 17:48:00', '2021-12-24 17:48:00', 55, '2021-11-08 17:48:00', '2021-11-22 17:48:00'),
(1, 11, '2021-11-11 17:51:00', '2021-12-30 17:51:00', 40, '2021-11-09 17:51:00', '2021-11-10 17:52:00'),
(2, 12, '2021-11-25 17:54:00', '2021-12-30 17:55:00', 52, '2021-11-09 17:55:00', '2021-11-24 17:55:00');

-- --------------------------------------------------------

--
-- Table structure for table `classLearner`
--

CREATE TABLE `classLearner` (
  `CourseID` int(11) NOT NULL,
  `ClassID` int(11) NOT NULL,
  `LearnerID` int(11) NOT NULL,
  `ApplicationStatus` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `classLearner`
--

INSERT INTO `classLearner` (`CourseID`, `ClassID`, `LearnerID`, `ApplicationStatus`) VALUES
(1, 1, 1, 'hr_enrolled'),
(1, 1, 3, 'ongoing'),
(1, 1, 4, 'hr_enrolled'),
(1, 1, 5, 'ongoing'),
(3, 3, 1, 'completed'),
(2, 6, 1, 'rejected');

-- --------------------------------------------------------

--
-- Table structure for table `classTrainer`
--

CREATE TABLE `classTrainer` (
  `CourseID` int(11) NOT NULL,
  `ClassID` int(11) NOT NULL,
  `TrainerID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `classTrainer`
--

INSERT INTO `classTrainer` (`CourseID`, `ClassID`, `TrainerID`) VALUES
(1, 1, 1),
(1, 4, 1),
(1, 4, 2),
(1, 8, 2),
(1, 9, 2),
(1, 10, 2),
(1, 11, 2),
(2, 6, 2),
(2, 12, 1),
(3, 7, 2),
(4, 5, 1),
(4, 5, 2);

-- --------------------------------------------------------

--
-- Table structure for table `course`
--

CREATE TABLE `course` (
  `CourseID` int(11) NOT NULL,
  `CourseTitle` varchar(50) NOT NULL,
  `CourseDescription` text NOT NULL,
  `Badge` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `course`
--

INSERT INTO `course` (`CourseID`, `CourseTitle`, `CourseDescription`, `Badge`) VALUES
(1, 'SPM', 'This is a software project management module that will kill you and your social life', 'python_badge.png'),
(2, 'DB Management', 'Database Management', 'python_badge.png'),
(3, 'WAD 2', 'Web Application Management 2', 'python_badge.png'),
(4, 'Ethics', 'Class that makes you ethical', 'python_badge.png'),
(5, 'Analytics Foundation', 'Learn analytics!!!!', 'python_badge.png'),
(6, 'ESD', 'Enterprise Development', 'python_badge.png');

-- --------------------------------------------------------

--
-- Table structure for table `courseForum`
--

CREATE TABLE `courseForum` (
  `CourseID` int(11) NOT NULL,
  `ForumID` int(11) NOT NULL,
  `ForumTitle` text NOT NULL,
  `UserID` int(11) NOT NULL,
  `ForumDetails` text NOT NULL,
  `ForumCreated` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `courseForumReply`
--

CREATE TABLE `courseForumReply` (
  `ForumID` int(11) NOT NULL,
  `ReplyID` int(11) NOT NULL,
  `ReplyContent` text NOT NULL,
  `UserID` int(11) NOT NULL,
  `ReplyTime` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `coursePrereq`
--

CREATE TABLE `coursePrereq` (
  `CourseID` int(11) NOT NULL,
  `PrereqID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `coursePrereq`
--

INSERT INTO `coursePrereq` (`CourseID`, `PrereqID`) VALUES
(4, 1),
(4, 3);

-- --------------------------------------------------------

--
-- Table structure for table `finalQuiz`
--

CREATE TABLE `finalQuiz` (
  `CourseID` int(11) NOT NULL,
  `QuizID` int(11) NOT NULL,
  `QuizTitle` varchar(50) NOT NULL,
  `QuizTimer` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `finalQuiz`
--

INSERT INTO `finalQuiz` (`CourseID`, `QuizID`, `QuizTitle`, `QuizTimer`) VALUES
(1, 1, 'SPM Final Quiz', 1000),
(5, 3, 'Test Quiz 1', 60),
(6, 4, 'ESD Final Quiz', 10);

-- --------------------------------------------------------

--
-- Table structure for table `finalQuizQuestion`
--

CREATE TABLE `finalQuizQuestion` (
  `CourseID` int(11) NOT NULL,
  `QuizID` int(11) NOT NULL,
  `QuestionID` int(11) NOT NULL,
  `QuestionContent` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `finalQuizQuestion`
--

INSERT INTO `finalQuizQuestion` (`CourseID`, `QuizID`, `QuestionID`, `QuestionContent`) VALUES
(5, 3, 3, 'Test Question 1?'),
(5, 3, 4, 'What is 1 + 1?'),
(6, 4, 5, 'Do you like this course?');

-- --------------------------------------------------------

--
-- Table structure for table `finalQuizQuestionAnswer`
--

CREATE TABLE `finalQuizQuestionAnswer` (
  `CourseID` int(11) NOT NULL,
  `QuizID` int(11) NOT NULL,
  `QuestionID` int(11) NOT NULL,
  `AnswerID` int(11) NOT NULL,
  `AnswerContent` text NOT NULL,
  `Correct` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `finalQuizQuestionAnswer`
--

INSERT INTO `finalQuizQuestionAnswer` (`CourseID`, `QuizID`, `QuestionID`, `AnswerID`, `AnswerContent`, `Correct`) VALUES
(5, 3, 3, 6, 'Test Answer 1', 1),
(5, 3, 3, 7, 'Test Answer 2', 0),
(5, 3, 4, 8, '2', 1),
(5, 3, 4, 9, '4', 0),
(6, 4, 5, 10, 'Yes', 1),
(6, 4, 5, 11, 'No', 0);

-- --------------------------------------------------------

--
-- Table structure for table `finalStudentQuizResult`
--

CREATE TABLE `finalStudentQuizResult` (
  `CourseID` int(11) NOT NULL,
  `ClassID` int(11) NOT NULL,
  `QuizID` int(11) NOT NULL,
  `LearnerID` int(11) NOT NULL,
  `Grade` double NOT NULL,
  `AttemptID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `finalStudentQuizResult`
--

INSERT INTO `finalStudentQuizResult` (`CourseID`, `ClassID`, `QuizID`, `LearnerID`, `Grade`, `AttemptID`) VALUES
(1, 1, 1, 4, 90, 1);

-- --------------------------------------------------------

--
-- Table structure for table `LearnerCourse`
--

CREATE TABLE `LearnerCourse` (
  `LearnerID` int(11) NOT NULL,
  `CourseID` int(11) NOT NULL,
  `Status` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `LearnerCourse`
--

INSERT INTO `LearnerCourse` (`LearnerID`, `CourseID`, `Status`) VALUES
(1, 1, 'completed');

-- --------------------------------------------------------

--
-- Table structure for table `MaterialProgress`
--

CREATE TABLE `MaterialProgress` (
  `CourseID` int(11) NOT NULL,
  `ClassID` int(11) NOT NULL,
  `SectionID` int(11) NOT NULL,
  `MaterialID` int(11) NOT NULL,
  `LearnerID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `MaterialProgress`
--

INSERT INTO `MaterialProgress` (`CourseID`, `ClassID`, `SectionID`, `MaterialID`, `LearnerID`) VALUES
(1, 4, 1, 1, 1),
(1, 4, 1, 2, 1),
(1, 4, 1, 3, 1),
(1, 1, 4, 5, 1),
(1, 1, 4, 6, 1),
(1, 1, 4, 7, 1),
(1, 1, 4, 8, 1),
(1, 1, 4, 9, 1),
(1, 1, 6, 12, 1),
(1, 1, 6, 13, 1);

-- --------------------------------------------------------

--
-- Table structure for table `publicForum`
--

CREATE TABLE `publicForum` (
  `ForumID` int(11) NOT NULL,
  `ForumTitle` text NOT NULL,
  `UserID` int(11) NOT NULL,
  `ForumDetails` text NOT NULL,
  `ForumCreated` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `publicForum`
--

INSERT INTO `publicForum` (`ForumID`, `ForumTitle`, `UserID`, `ForumDetails`, `ForumCreated`) VALUES
(1, 'Forum Title 1', 4, 'Detail (Description) 1', '2021-11-08 15:53:47'),
(2, 'Forum Title 2', 5, 'How to do this?', '2021-11-08 16:00:40');

-- --------------------------------------------------------

--
-- Table structure for table `publicForumReply`
--

CREATE TABLE `publicForumReply` (
  `ForumID` int(11) NOT NULL,
  `ReplyID` int(11) NOT NULL,
  `ReplyContent` text NOT NULL,
  `UserID` int(11) NOT NULL,
  `ReplyTime` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `publicForumReply`
--

INSERT INTO `publicForumReply` (`ForumID`, `ReplyID`, `ReplyContent`, `UserID`, `ReplyTime`) VALUES
(1, 1, 'Test Reply 1', 1, '2021-11-08 23:59:01'),
(1, 2, 'Test Reply 2\n', 1, '2021-11-08 23:59:17');

-- --------------------------------------------------------

--
-- Table structure for table `question`
--

CREATE TABLE `question` (
  `CourseID` int(11) NOT NULL,
  `ClassID` int(11) NOT NULL,
  `SectionID` int(11) NOT NULL,
  `QuizID` int(11) NOT NULL,
  `QuestionID` int(11) NOT NULL,
  `QuestionContent` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `question`
--

INSERT INTO `question` (`CourseID`, `ClassID`, `SectionID`, `QuizID`, `QuestionID`, `QuestionContent`) VALUES
(1, 4, 2, 1, 1, 'What is the name of the section?'),
(1, 4, 2, 1, 2, 'What is the class?'),
(1, 4, 3, 3, 3, 'What is the link uploaded under section 3?'),
(1, 1, 4, 4, 4, 'Name?'),
(1, 1, 4, 4, 5, 'Day?'),
(1, 4, 1, 2, 6, 'What is your name?'),
(1, 4, 5, 5, 7, 'Name?'),
(1, 4, 5, 5, 8, 'Food?'),
(1, 1, 6, 6, 9, 'Which is the correct answer?');

-- --------------------------------------------------------

--
-- Table structure for table `questionAnswer`
--

CREATE TABLE `questionAnswer` (
  `CourseID` int(11) NOT NULL,
  `ClassID` int(11) NOT NULL,
  `SectionID` int(11) NOT NULL,
  `QuizID` int(11) NOT NULL,
  `QuestionID` int(11) NOT NULL,
  `AnswerID` int(11) NOT NULL,
  `AnswerContent` text NOT NULL,
  `Correct` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `questionAnswer`
--

INSERT INTO `questionAnswer` (`CourseID`, `ClassID`, `SectionID`, `QuizID`, `QuestionID`, `AnswerID`, `AnswerContent`, `Correct`) VALUES
(1, 4, 2, 1, 1, 1, 'Introduction to SPM', 1),
(1, 4, 2, 1, 1, 2, 'Introduction to ESD', 0),
(1, 4, 2, 1, 1, 3, 'Introduction to DBTT', 0),
(1, 4, 2, 1, 2, 4, '4', 1),
(1, 4, 2, 1, 2, 5, '0', 0),
(1, 4, 3, 3, 3, 6, 'Facebook', 1),
(1, 4, 3, 3, 3, 7, 'Youtube', 0),
(1, 1, 4, 4, 4, 8, 'Chris', 1),
(1, 1, 4, 4, 4, 9, 'Poskitt', 0),
(1, 1, 4, 4, 5, 10, 'Monday', 0),
(1, 1, 4, 4, 5, 11, 'Tuesday', 0),
(1, 1, 4, 4, 5, 12, 'Wednesday', 1),
(1, 4, 1, 2, 6, 13, 'This is correct', 1),
(1, 4, 1, 2, 6, 14, 'This is wrong', 0),
(1, 4, 5, 5, 7, 15, 'Hello', 0),
(1, 4, 5, 5, 7, 16, 'Hello 1', 1),
(1, 4, 5, 5, 8, 17, 'Burger', 0),
(1, 4, 5, 5, 8, 18, 'Chicken rice', 1),
(1, 1, 6, 6, 9, 19, 'This is correct.', 1),
(1, 1, 6, 6, 9, 20, 'This is wrong.', 0);

-- --------------------------------------------------------

--
-- Table structure for table `quiz`
--

CREATE TABLE `quiz` (
  `CourseID` int(11) NOT NULL,
  `ClassID` int(11) NOT NULL,
  `SectionID` int(11) NOT NULL,
  `QuizID` int(11) NOT NULL,
  `QuizTitle` varchar(50) NOT NULL,
  `QuizTimer` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `quiz`
--

INSERT INTO `quiz` (`CourseID`, `ClassID`, `SectionID`, `QuizID`, `QuizTitle`, `QuizTimer`) VALUES
(1, 4, 2, 1, 'Quiz 1', 30),
(1, 4, 1, 2, 'TEST', 60),
(1, 4, 3, 3, 'Lesson 3', 35),
(1, 1, 4, 4, 'Intro SPM ', 32),
(1, 4, 5, 5, 'Lesson 4 ', 45),
(1, 1, 6, 6, 'Test Quiz 2', 30);

-- --------------------------------------------------------

--
-- Table structure for table `section`
--

CREATE TABLE `section` (
  `CourseID` int(11) NOT NULL,
  `ClassID` int(11) NOT NULL,
  `SectionID` int(11) NOT NULL,
  `SectionName` text NOT NULL DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `section`
--

INSERT INTO `section` (`CourseID`, `ClassID`, `SectionID`, `SectionName`) VALUES
(1, 4, 1, 'Intro to SPM'),
(1, 4, 2, 'Introduction to SPM'),
(1, 4, 3, 'Lesson 3'),
(1, 1, 4, 'Intro SPM'),
(1, 4, 5, 'Lesson 4'),
(1, 1, 6, 'Lesson 2');

-- --------------------------------------------------------

--
-- Table structure for table `sectionMaterial`
--

CREATE TABLE `sectionMaterial` (
  `CourseID` int(11) NOT NULL,
  `ClassID` int(11) NOT NULL,
  `SectionID` int(11) NOT NULL,
  `MaterialID` int(11) NOT NULL,
  `MaterialTitle` text NOT NULL,
  `MaterialContent` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `sectionMaterial`
--

INSERT INTO `sectionMaterial` (`CourseID`, `ClassID`, `SectionID`, `MaterialID`, `MaterialTitle`, `MaterialContent`) VALUES
(1, 4, 1, 1, 'wk2-Kahoot-G1G2G6.pdf', 'wk2-Kahoot-G1G2G6.pdf'),
(1, 4, 1, 2, 'wk2-Kahoot-G1G2G6.pdf', 'wk2-Kahoot-G1G2G6.pdf'),
(1, 4, 1, 3, 'youtube', 'https://www.youtube.com/watch?v=9XkX6EGk_CA'),
(1, 1, 4, 5, 'youtube', 'https://youtube.com'),
(1, 1, 4, 6, 'Project Instructions.pdf', 'Project Instructions.pdf'),
(1, 1, 4, 7, 'Project Instructions.pdf', 'Project Instructions.pdf'),
(1, 1, 4, 8, 'ProjectClarificationV1.pdf', 'ProjectClarificationV1.pdf'),
(1, 1, 4, 9, '03-HA-Lab_1.pdf', '03-HA-Lab_1.pdf'),
(1, 4, 5, 10, 'Youtube', 'https://www.youtube.com/watch?v=lfWxMg5SOck'),
(1, 4, 5, 11, 'wk1-Kahoot-G1G2G6.pdf', 'wk1-Kahoot-G1G2G6.pdf'),
(1, 1, 6, 12, 'What Is Ethical Egoism.pdf', 'What Is Ethical Egoism.pdf'),
(1, 1, 6, 13, 'What Is Liberalism.pdf', 'What Is Liberalism.pdf');

-- --------------------------------------------------------

--
-- Table structure for table `studentAnswer`
--

CREATE TABLE `studentAnswer` (
  `CourseID` int(11) NOT NULL,
  `ClassID` int(11) NOT NULL,
  `SectionID` int(11) NOT NULL,
  `QuizID` int(11) NOT NULL,
  `AttemptID` int(11) NOT NULL,
  `QuestionID` int(11) NOT NULL,
  `AnswerID` int(11) NOT NULL,
  `LearnerID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `studentAnswer`
--

INSERT INTO `studentAnswer` (`CourseID`, `ClassID`, `SectionID`, `QuizID`, `AttemptID`, `QuestionID`, `AnswerID`, `LearnerID`) VALUES
(1, 4, 2, 1, 4, 1, 1, 1),
(1, 4, 2, 1, 4, 2, 4, 1),
(1, 1, 4, 4, 1, 4, 8, 1),
(1, 1, 4, 4, 2, 4, 8, 1),
(1, 1, 4, 4, 1, 5, 12, 1),
(1, 1, 4, 4, 2, 5, 12, 1),
(1, 4, 1, 2, 5, 6, 13, 1),
(1, 1, 6, 6, 6, 9, 19, 1);

-- --------------------------------------------------------

--
-- Table structure for table `studentQuizResult`
--

CREATE TABLE `studentQuizResult` (
  `CourseID` int(11) NOT NULL,
  `ClassID` int(11) NOT NULL,
  `SectionID` int(11) NOT NULL,
  `QuizID` int(11) NOT NULL,
  `LearnerID` int(11) NOT NULL,
  `Grade` double DEFAULT NULL,
  `AttemptID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `studentQuizResult`
--

INSERT INTO `studentQuizResult` (`CourseID`, `ClassID`, `SectionID`, `QuizID`, `LearnerID`, `Grade`, `AttemptID`) VALUES
(1, 1, 4, 4, 1, 0, 1),
(1, 1, 4, 4, 1, 0, 2),
(1, 4, 1, 2, 1, 0, 3),
(1, 4, 2, 1, 1, 0, 4),
(1, 4, 1, 2, 1, 0, 5),
(1, 1, 6, 6, 1, 0, 6);

-- --------------------------------------------------------

--
-- Table structure for table `userTable`
--

CREATE TABLE `userTable` (
  `UserID` int(11) NOT NULL,
  `UserName` text NOT NULL,
  `UserType` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `userTable`
--

INSERT INTO `userTable` (`UserID`, `UserName`, `UserType`) VALUES
(1, 'Jhonny', 'Senior Engineer'),
(2, 'Julie', 'Senior Engineer'),
(3, 'Brenda', 'Junior Engineer'),
(4, 'Aaron', 'Junior Engineer'),
(5, 'Fred', 'Junior Engineer');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `class`
--
ALTER TABLE `class`
  ADD PRIMARY KEY (`ClassID`),
  ADD KEY `CourseID` (`CourseID`);

--
-- Indexes for table `classLearner`
--
ALTER TABLE `classLearner`
  ADD PRIMARY KEY (`ClassID`,`LearnerID`),
  ADD KEY `CourseID` (`CourseID`,`ClassID`),
  ADD KEY `LearnerID` (`LearnerID`);

--
-- Indexes for table `classTrainer`
--
ALTER TABLE `classTrainer`
  ADD PRIMARY KEY (`ClassID`,`TrainerID`),
  ADD KEY `CourseID` (`CourseID`,`ClassID`),
  ADD KEY `TrainerID` (`TrainerID`);

--
-- Indexes for table `course`
--
ALTER TABLE `course`
  ADD PRIMARY KEY (`CourseID`);

--
-- Indexes for table `courseForum`
--
ALTER TABLE `courseForum`
  ADD PRIMARY KEY (`ForumID`),
  ADD KEY `CourseID` (`CourseID`),
  ADD KEY `UserID` (`UserID`);

--
-- Indexes for table `courseForumReply`
--
ALTER TABLE `courseForumReply`
  ADD PRIMARY KEY (`ReplyID`),
  ADD KEY `ForumID` (`ForumID`),
  ADD KEY `UserID` (`UserID`);

--
-- Indexes for table `coursePrereq`
--
ALTER TABLE `coursePrereq`
  ADD PRIMARY KEY (`CourseID`,`PrereqID`),
  ADD KEY `PrereqID` (`PrereqID`);

--
-- Indexes for table `finalQuiz`
--
ALTER TABLE `finalQuiz`
  ADD PRIMARY KEY (`QuizID`),
  ADD KEY `CourseID` (`CourseID`);

--
-- Indexes for table `finalQuizQuestion`
--
ALTER TABLE `finalQuizQuestion`
  ADD PRIMARY KEY (`QuestionID`),
  ADD KEY `CourseID` (`CourseID`),
  ADD KEY `QuizID` (`QuizID`);

--
-- Indexes for table `finalQuizQuestionAnswer`
--
ALTER TABLE `finalQuizQuestionAnswer`
  ADD PRIMARY KEY (`AnswerID`),
  ADD KEY `CourseID` (`CourseID`),
  ADD KEY `QuizID` (`QuizID`),
  ADD KEY `QuestionID` (`QuestionID`);

--
-- Indexes for table `finalStudentQuizResult`
--
ALTER TABLE `finalStudentQuizResult`
  ADD PRIMARY KEY (`AttemptID`),
  ADD KEY `CourseID` (`CourseID`),
  ADD KEY `QuizID` (`QuizID`),
  ADD KEY `ClassID` (`ClassID`),
  ADD KEY `LearnerID` (`LearnerID`);

--
-- Indexes for table `LearnerCourse`
--
ALTER TABLE `LearnerCourse`
  ADD PRIMARY KEY (`LearnerID`,`CourseID`),
  ADD KEY `CourseID` (`CourseID`);

--
-- Indexes for table `MaterialProgress`
--
ALTER TABLE `MaterialProgress`
  ADD PRIMARY KEY (`MaterialID`,`LearnerID`),
  ADD KEY `LearnerID` (`LearnerID`),
  ADD KEY `MaterialProgress_ibfk_2` (`CourseID`),
  ADD KEY `MaterialProgress_ibfk_3` (`ClassID`),
  ADD KEY `MaterialProgress_ibfk_4` (`SectionID`);

--
-- Indexes for table `publicForum`
--
ALTER TABLE `publicForum`
  ADD PRIMARY KEY (`ForumID`),
  ADD KEY `UserID` (`UserID`);

--
-- Indexes for table `publicForumReply`
--
ALTER TABLE `publicForumReply`
  ADD PRIMARY KEY (`ReplyID`),
  ADD KEY `ForumID` (`ForumID`),
  ADD KEY `UserID` (`UserID`);

--
-- Indexes for table `question`
--
ALTER TABLE `question`
  ADD PRIMARY KEY (`QuestionID`),
  ADD KEY `CourseID` (`CourseID`),
  ADD KEY `ClassID` (`ClassID`),
  ADD KEY `SectionID` (`SectionID`),
  ADD KEY `QuizID` (`QuizID`);

--
-- Indexes for table `questionAnswer`
--
ALTER TABLE `questionAnswer`
  ADD PRIMARY KEY (`AnswerID`),
  ADD KEY `CourseID` (`CourseID`),
  ADD KEY `ClassID` (`ClassID`),
  ADD KEY `SectionID` (`SectionID`),
  ADD KEY `QuizID` (`QuizID`),
  ADD KEY `QuestionID` (`QuestionID`);

--
-- Indexes for table `quiz`
--
ALTER TABLE `quiz`
  ADD PRIMARY KEY (`QuizID`),
  ADD KEY `CourseID` (`CourseID`),
  ADD KEY `ClassID` (`ClassID`),
  ADD KEY `SectionID` (`SectionID`);

--
-- Indexes for table `section`
--
ALTER TABLE `section`
  ADD PRIMARY KEY (`SectionID`),
  ADD KEY `CourseID` (`CourseID`),
  ADD KEY `ClassID` (`ClassID`);

--
-- Indexes for table `sectionMaterial`
--
ALTER TABLE `sectionMaterial`
  ADD PRIMARY KEY (`MaterialID`),
  ADD KEY `sectionMaterial_ibfk_1` (`CourseID`),
  ADD KEY `sectionMaterial_ibfk_2` (`ClassID`),
  ADD KEY `sectionMaterial_ibfk_3` (`SectionID`);

--
-- Indexes for table `studentAnswer`
--
ALTER TABLE `studentAnswer`
  ADD PRIMARY KEY (`CourseID`,`ClassID`,`SectionID`,`QuizID`,`QuestionID`,`LearnerID`,`AttemptID`),
  ADD KEY `ClassID` (`ClassID`),
  ADD KEY `SectionID` (`SectionID`),
  ADD KEY `QuizID` (`QuizID`),
  ADD KEY `AnswerID` (`AnswerID`),
  ADD KEY `LearnerID` (`LearnerID`),
  ADD KEY `AttemptID` (`AttemptID`);

--
-- Indexes for table `studentQuizResult`
--
ALTER TABLE `studentQuizResult`
  ADD PRIMARY KEY (`AttemptID`),
  ADD KEY `CourseID` (`CourseID`),
  ADD KEY `ClassID` (`ClassID`),
  ADD KEY `SectionID` (`SectionID`),
  ADD KEY `QuizID` (`QuizID`),
  ADD KEY `LearnerID` (`LearnerID`);

--
-- Indexes for table `userTable`
--
ALTER TABLE `userTable`
  ADD PRIMARY KEY (`UserID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `class`
--
ALTER TABLE `class`
  MODIFY `ClassID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `course`
--
ALTER TABLE `course`
  MODIFY `CourseID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `courseForum`
--
ALTER TABLE `courseForum`
  MODIFY `ForumID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `courseForumReply`
--
ALTER TABLE `courseForumReply`
  MODIFY `ReplyID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `finalQuiz`
--
ALTER TABLE `finalQuiz`
  MODIFY `QuizID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `finalQuizQuestion`
--
ALTER TABLE `finalQuizQuestion`
  MODIFY `QuestionID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `finalQuizQuestionAnswer`
--
ALTER TABLE `finalQuizQuestionAnswer`
  MODIFY `AnswerID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `finalStudentQuizResult`
--
ALTER TABLE `finalStudentQuizResult`
  MODIFY `AttemptID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `MaterialProgress`
--
ALTER TABLE `MaterialProgress`
  MODIFY `MaterialID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `publicForum`
--
ALTER TABLE `publicForum`
  MODIFY `ForumID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `publicForumReply`
--
ALTER TABLE `publicForumReply`
  MODIFY `ReplyID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `question`
--
ALTER TABLE `question`
  MODIFY `QuestionID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `questionAnswer`
--
ALTER TABLE `questionAnswer`
  MODIFY `AnswerID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `quiz`
--
ALTER TABLE `quiz`
  MODIFY `QuizID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `section`
--
ALTER TABLE `section`
  MODIFY `SectionID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `sectionMaterial`
--
ALTER TABLE `sectionMaterial`
  MODIFY `MaterialID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `studentQuizResult`
--
ALTER TABLE `studentQuizResult`
  MODIFY `AttemptID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `userTable`
--
ALTER TABLE `userTable`
  MODIFY `UserID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `class`
--
ALTER TABLE `class`
  ADD CONSTRAINT `class_ibfk_1` FOREIGN KEY (`CourseID`) REFERENCES `course` (`CourseID`);

--
-- Constraints for table `classLearner`
--
ALTER TABLE `classLearner`
  ADD CONSTRAINT `classLearner_ibfk_1` FOREIGN KEY (`CourseID`,`ClassID`) REFERENCES `class` (`CourseID`, `ClassID`),
  ADD CONSTRAINT `classLearner_ibfk_2` FOREIGN KEY (`LearnerID`) REFERENCES `userTable` (`UserID`);

--
-- Constraints for table `classTrainer`
--
ALTER TABLE `classTrainer`
  ADD CONSTRAINT `classTrainer_ibfk_1` FOREIGN KEY (`CourseID`,`ClassID`) REFERENCES `class` (`CourseID`, `ClassID`),
  ADD CONSTRAINT `classTrainer_ibfk_2` FOREIGN KEY (`TrainerID`) REFERENCES `userTable` (`UserID`);

--
-- Constraints for table `courseForum`
--
ALTER TABLE `courseForum`
  ADD CONSTRAINT `courseForum_ibfk_1` FOREIGN KEY (`CourseID`) REFERENCES `course` (`CourseID`),
  ADD CONSTRAINT `courseForum_ibfk_2` FOREIGN KEY (`UserID`) REFERENCES `userTable` (`UserID`);

--
-- Constraints for table `courseForumReply`
--
ALTER TABLE `courseForumReply`
  ADD CONSTRAINT `courseForumReply_ibfk_1` FOREIGN KEY (`ForumID`) REFERENCES `courseForum` (`ForumID`),
  ADD CONSTRAINT `courseForumReply_ibfk_2` FOREIGN KEY (`UserID`) REFERENCES `userTable` (`UserID`);

--
-- Constraints for table `coursePrereq`
--
ALTER TABLE `coursePrereq`
  ADD CONSTRAINT `coursePrereq_ibfk_1` FOREIGN KEY (`CourseID`) REFERENCES `course` (`CourseID`),
  ADD CONSTRAINT `coursePrereq_ibfk_2` FOREIGN KEY (`PrereqID`) REFERENCES `course` (`CourseID`);

--
-- Constraints for table `finalQuiz`
--
ALTER TABLE `finalQuiz`
  ADD CONSTRAINT `finalQuiz_ibfk_1` FOREIGN KEY (`CourseID`) REFERENCES `course` (`CourseID`);

--
-- Constraints for table `finalQuizQuestion`
--
ALTER TABLE `finalQuizQuestion`
  ADD CONSTRAINT `finalQuizQuestion_ibfk_1` FOREIGN KEY (`CourseID`) REFERENCES `finalQuiz` (`CourseID`),
  ADD CONSTRAINT `finalQuizQuestion_ibfk_2` FOREIGN KEY (`QuizID`) REFERENCES `finalQuiz` (`QuizID`);

--
-- Constraints for table `finalQuizQuestionAnswer`
--
ALTER TABLE `finalQuizQuestionAnswer`
  ADD CONSTRAINT `finalQuizQuestionAnswer_ibfk_1` FOREIGN KEY (`CourseID`) REFERENCES `finalQuizQuestion` (`CourseID`),
  ADD CONSTRAINT `finalQuizQuestionAnswer_ibfk_2` FOREIGN KEY (`QuizID`) REFERENCES `finalQuizQuestion` (`QuizID`),
  ADD CONSTRAINT `finalQuizQuestionAnswer_ibfk_3` FOREIGN KEY (`QuestionID`) REFERENCES `finalQuizQuestion` (`QuestionID`);

--
-- Constraints for table `finalStudentQuizResult`
--
ALTER TABLE `finalStudentQuizResult`
  ADD CONSTRAINT `finalStudentQuizResult_ibfk_1` FOREIGN KEY (`CourseID`) REFERENCES `finalQuiz` (`CourseID`),
  ADD CONSTRAINT `finalStudentQuizResult_ibfk_2` FOREIGN KEY (`QuizID`) REFERENCES `finalQuiz` (`QuizID`),
  ADD CONSTRAINT `finalStudentQuizResult_ibfk_3` FOREIGN KEY (`ClassID`) REFERENCES `class` (`ClassID`),
  ADD CONSTRAINT `finalStudentQuizResult_ibfk_4` FOREIGN KEY (`LearnerID`) REFERENCES `userTable` (`UserID`);

--
-- Constraints for table `LearnerCourse`
--
ALTER TABLE `LearnerCourse`
  ADD CONSTRAINT `LearnerCourse_ibfk_1` FOREIGN KEY (`LearnerID`) REFERENCES `userTable` (`UserID`),
  ADD CONSTRAINT `LearnerCourse_ibfk_2` FOREIGN KEY (`CourseID`) REFERENCES `course` (`CourseID`);

--
-- Constraints for table `MaterialProgress`
--
ALTER TABLE `MaterialProgress`
  ADD CONSTRAINT `MaterialProgress_ibfk_1` FOREIGN KEY (`LearnerID`) REFERENCES `userTable` (`UserID`),
  ADD CONSTRAINT `MaterialProgress_ibfk_2` FOREIGN KEY (`CourseID`) REFERENCES `sectionMaterial` (`CourseID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `MaterialProgress_ibfk_3` FOREIGN KEY (`ClassID`) REFERENCES `sectionMaterial` (`ClassID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `MaterialProgress_ibfk_4` FOREIGN KEY (`SectionID`) REFERENCES `sectionMaterial` (`SectionID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `MaterialProgress_ibfk_5` FOREIGN KEY (`MaterialID`) REFERENCES `sectionMaterial` (`MaterialID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `publicForum`
--
ALTER TABLE `publicForum`
  ADD CONSTRAINT `publicForum_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `userTable` (`UserID`);

--
-- Constraints for table `publicForumReply`
--
ALTER TABLE `publicForumReply`
  ADD CONSTRAINT `publicForumReply_ibfk_1` FOREIGN KEY (`ForumID`) REFERENCES `publicForum` (`ForumID`),
  ADD CONSTRAINT `publicForumReply_ibfk_2` FOREIGN KEY (`UserID`) REFERENCES `userTable` (`UserID`);

--
-- Constraints for table `question`
--
ALTER TABLE `question`
  ADD CONSTRAINT `question_ibfk_1` FOREIGN KEY (`CourseID`) REFERENCES `quiz` (`CourseID`),
  ADD CONSTRAINT `question_ibfk_2` FOREIGN KEY (`ClassID`) REFERENCES `quiz` (`ClassID`),
  ADD CONSTRAINT `question_ibfk_3` FOREIGN KEY (`SectionID`) REFERENCES `quiz` (`SectionID`),
  ADD CONSTRAINT `question_ibfk_4` FOREIGN KEY (`QuizID`) REFERENCES `quiz` (`QuizID`);

--
-- Constraints for table `questionAnswer`
--
ALTER TABLE `questionAnswer`
  ADD CONSTRAINT `questionAnswer_ibfk_1` FOREIGN KEY (`CourseID`) REFERENCES `question` (`CourseID`),
  ADD CONSTRAINT `questionAnswer_ibfk_2` FOREIGN KEY (`ClassID`) REFERENCES `question` (`ClassID`),
  ADD CONSTRAINT `questionAnswer_ibfk_3` FOREIGN KEY (`SectionID`) REFERENCES `question` (`SectionID`),
  ADD CONSTRAINT `questionAnswer_ibfk_4` FOREIGN KEY (`QuizID`) REFERENCES `question` (`QuizID`),
  ADD CONSTRAINT `questionAnswer_ibfk_5` FOREIGN KEY (`QuestionID`) REFERENCES `question` (`QuestionID`);

--
-- Constraints for table `quiz`
--
ALTER TABLE `quiz`
  ADD CONSTRAINT `quiz_ibfk_1` FOREIGN KEY (`CourseID`) REFERENCES `section` (`CourseID`),
  ADD CONSTRAINT `quiz_ibfk_2` FOREIGN KEY (`ClassID`) REFERENCES `section` (`ClassID`),
  ADD CONSTRAINT `quiz_ibfk_3` FOREIGN KEY (`SectionID`) REFERENCES `section` (`SectionID`);

--
-- Constraints for table `section`
--
ALTER TABLE `section`
  ADD CONSTRAINT `section_ibfk_1` FOREIGN KEY (`CourseID`) REFERENCES `class` (`CourseID`),
  ADD CONSTRAINT `section_ibfk_2` FOREIGN KEY (`ClassID`) REFERENCES `class` (`ClassID`);

--
-- Constraints for table `sectionMaterial`
--
ALTER TABLE `sectionMaterial`
  ADD CONSTRAINT `sectionMaterial_ibfk_1` FOREIGN KEY (`CourseID`) REFERENCES `section` (`CourseID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `sectionMaterial_ibfk_2` FOREIGN KEY (`ClassID`) REFERENCES `section` (`ClassID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `sectionMaterial_ibfk_3` FOREIGN KEY (`SectionID`) REFERENCES `section` (`SectionID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `studentAnswer`
--
ALTER TABLE `studentAnswer`
  ADD CONSTRAINT `studentAnswer_ibfk_1` FOREIGN KEY (`CourseID`) REFERENCES `question` (`CourseID`),
  ADD CONSTRAINT `studentAnswer_ibfk_2` FOREIGN KEY (`ClassID`) REFERENCES `question` (`ClassID`),
  ADD CONSTRAINT `studentAnswer_ibfk_3` FOREIGN KEY (`SectionID`) REFERENCES `question` (`SectionID`),
  ADD CONSTRAINT `studentAnswer_ibfk_4` FOREIGN KEY (`QuizID`) REFERENCES `question` (`QuizID`),
  ADD CONSTRAINT `studentAnswer_ibfk_5` FOREIGN KEY (`AnswerID`) REFERENCES `questionAnswer` (`AnswerID`),
  ADD CONSTRAINT `studentAnswer_ibfk_6` FOREIGN KEY (`LearnerID`) REFERENCES `userTable` (`UserID`),
  ADD CONSTRAINT `studentAnswer_ibfk_7` FOREIGN KEY (`AttemptID`) REFERENCES `studentQuizResult` (`AttemptID`);

--
-- Constraints for table `studentQuizResult`
--
ALTER TABLE `studentQuizResult`
  ADD CONSTRAINT `studentQuizResult_ibfk_1` FOREIGN KEY (`CourseID`) REFERENCES `quiz` (`CourseID`),
  ADD CONSTRAINT `studentQuizResult_ibfk_2` FOREIGN KEY (`ClassID`) REFERENCES `quiz` (`ClassID`),
  ADD CONSTRAINT `studentQuizResult_ibfk_3` FOREIGN KEY (`SectionID`) REFERENCES `quiz` (`SectionID`),
  ADD CONSTRAINT `studentQuizResult_ibfk_4` FOREIGN KEY (`QuizID`) REFERENCES `quiz` (`QuizID`),
  ADD CONSTRAINT `studentQuizResult_ibfk_5` FOREIGN KEY (`LearnerID`) REFERENCES `userTable` (`UserID`);

DELIMITER $$
--
-- Events
--
CREATE DEFINER=`root`@`%` EVENT `UPDATE_ENROL_ONGOING` ON SCHEDULE EVERY 1 MINUTE STARTS '2021-10-14 13:02:26' ON COMPLETION NOT PRESERVE ENABLE DO update classLearner inner join class on class.classid = classlearner.classid set classLearner.ApplicationStatus = 'ongoing' where class.StartDate <= NOW() and (classLearner.ApplicationStatus = 'hr_enrolled' or classlearner.ApplicationStatus = 'self_approved')$$

CREATE DEFINER=`root`@`%` EVENT `UPDATE_REJECT_FAILED` ON SCHEDULE EVERY 1 MINUTE STARTS '2021-10-14 13:02:26' ON COMPLETION NOT PRESERVE ENABLE DO update classLearner inner join class on class.classid = classlearner.classid set classLearner.ApplicationStatus = 'failed' where class.EndDate <= NOW() and (classLearner.ApplicationStatus = 'ongoing')$$

DELIMITER ;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

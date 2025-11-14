-- Database Setup for Talent Acquisition System
-- Created: 2023
-- Last Updated: 2025

CREATE DATABASE IF NOT EXISTS Final_Project;
USE Final_Project;

-- Table: Recruiter
-- Stores information about recruiters and their companies
CREATE TABLE IF NOT EXISTS Recruiter(
   ContactPerson  VARCHAR(255) NOT NULL PRIMARY KEY,
   Contact        VARCHAR(100) NOT NULL,
   Company        VARCHAR(255) NOT NULL,
   CompanyProfile TEXT
);

-- Table: Job
-- Stores job postings created by recruiters
CREATE TABLE IF NOT EXISTS Job (
   JobId INT PRIMARY KEY AUTO_INCREMENT,
   Location VARCHAR(255),
   Date VARCHAR(255),
   Experience VARCHAR(255),
   Skills TEXT,
   Title VARCHAR(255),
   ContactPerson VARCHAR(255),
   SalaryRange VARCHAR(255),
   FOREIGN KEY (ContactPerson) REFERENCES Recruiter(ContactPerson) ON DELETE CASCADE
);

-- Table: Candidate
-- Stores candidate information and their skills
CREATE TABLE IF NOT EXISTS Candidate (
   CandidateId INT PRIMARY KEY AUTO_INCREMENT,
   EdLevel VARCHAR(255),
   Gender VARCHAR(255),
   YearsCoded INT,
   Country VARCHAR(255),
   PreviousSalary INT,
   Skills TEXT
);

-- Table: Users
-- Stores user authentication information for the dashboard
CREATE TABLE IF NOT EXISTS Users (
   UserId INT PRIMARY KEY AUTO_INCREMENT,
   Username VARCHAR(100) NOT NULL UNIQUE,
   Password VARCHAR(255) NOT NULL,
   Role ENUM('admin', 'recruiter') NOT NULL DEFAULT 'recruiter',
   CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: Job_Audit
-- Stores audit trail for job salary updates
CREATE TABLE IF NOT EXISTS Job_Audit (
   AuditID INT PRIMARY KEY AUTO_INCREMENT,
   JobID INT NOT NULL,
   ActionType VARCHAR(50) NOT NULL,
   OldSalaryRange VARCHAR(255),
   NewSalaryRange VARCHAR(255),
   ModifiedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   FOREIGN KEY (JobID) REFERENCES Job(JobId) ON DELETE CASCADE
);

-- Trigger: Job Salary Update Audit
-- Automatically logs changes to job salary ranges
DELIMITER $$
CREATE TRIGGER IF NOT EXISTS job_salary_audit
AFTER UPDATE ON Job
FOR EACH ROW
BEGIN
   IF OLD.SalaryRange != NEW.SalaryRange THEN
      INSERT INTO Job_Audit (JobID, ActionType, OldSalaryRange, NewSalaryRange)
      VALUES (NEW.JobId, 'UPDATE', OLD.SalaryRange, NEW.SalaryRange);
   END IF;
END$$
DELIMITER ;

-- Display all tables
SHOW TABLES;
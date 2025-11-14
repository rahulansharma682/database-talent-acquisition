# Database Talent Acquisition System

**Course**: EN.601.615 - Database Systems
**Authors**: Shreya Jamsandekar, Rahul Anjani Nandana Sharma Chemitiganti
**Year**: 2023-2024

A comprehensive Streamlit-based web application for managing and analyzing talent acquisition data. This dashboard enables recruiters and administrators to manage job postings, track candidates, and perform advanced analytics on recruitment data using a MySQL database backend.

This project demonstrates practical application of database design, SQL queries, and web-based data visualization for real-world talent acquisition workflows.

## Table of Contents
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [User Guide](#user-guide)
- [Project Structure](#project-structure)
- [Contributing](#contributing)

## Features

### Core Functionality
- **User Authentication**: Secure login system with bcrypt password hashing
- **Role-Based Access Control**: Admin and recruiter roles with different permissions
- **CRUD Operations**: Add, view, and manage recruiters, jobs, and candidates
- **Advanced Analytics**: Multiple analytical dashboards and complex queries

### Analytics & Reporting
1. **Recruiter Performance Analytics**: Track total jobs posted by each recruiter
2. **Candidate Skills Matching**: Search and filter candidates by skills, education, and experience
3. **Salary Analytics**: Compute mean salaries by education level and skill set
4. **Job Market Insights**: Analyze in-demand skills with salary benchmarks
5. **Audit Trail**: Track all salary range updates with timestamps

### Complex Queries
- Top 3 most in-demand skills across all jobs
- Find recruiters posting jobs in specific locations
- Jobs offering competitive salaries for specific skills
- Jobs by recruiter with minimum experience requirements
- Compute mean salary by education level
- Compute mean salary by specific skill
- In-demand skills with salary benchmarks

## Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python 3.8+
- **Database**: MySQL 8.0+
- **Libraries**:
  - PyMySQL (Database connector)
  - bcrypt (Password hashing)
  - pandas (Data manipulation)
  - streamlit (Web framework)

## Prerequisites

- Python 3.8 or higher
- MySQL Server 8.0 or higher
- pip (Python package installer)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "Database Talent Acquisition"
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Database Setup

1. **Start MySQL Server**
   Ensure your MySQL server is running.

2. **Create the database schema**
   ```bash
   mysql -u root -p < SQL_Setup_MySQL.sql
   ```

   This will create:
   - `Recruiter` table: Stores recruiter and company information
   - `Job` table: Stores job postings
   - `Candidate` table: Stores candidate profiles
   - `Users` table: Stores authentication credentials
   - `Job_Audit` table: Stores audit trail for job updates
   - Trigger: Automatically logs salary range changes

3. **Import sample data** (optional)

   Sample data can be downloaded from the Kaggle sources listed in the [Data Sources](#data-sources) section. Once downloaded, import using:
   ```bash
   mysql -u root -p final_project < Recruiter.sql
   mysql -u root -p final_project < Job.sql
   mysql -u root -p final_project < Candidate.sql
   ```

4. **Create an initial admin user**
   Run the application and use the "Add User" feature, or manually insert:
   ```sql
   USE final_project;
   INSERT INTO Users (Username, Password, Role)
   VALUES ('admin', '$2b$12$hashedpasswordhere', 'admin');
   ```

## Configuration

1. **Update database credentials**

   Edit the `create_connection()` function in `dashboard.py` (lines 11-15):
   ```python
   connection = pymysql.connect(
       host="127.0.0.1",      # Your MySQL host
       user="your_username",   # Your MySQL username
       password="your_password", # Your MySQL password
       database="final_project"  # Database name
   )
   ```

   **Alternative**: Copy `config_template.py` to `config.py` and update credentials there.

## Running the Application

1. **Start the Streamlit application**
   ```bash
   streamlit run dashboard.py
   ```

2. **Access the dashboard**

   Open your browser and navigate to:
   ```
   http://localhost:8501
   ```

3. **Login**

   Use your admin or recruiter credentials to access the dashboard.

## User Guide

### For Administrators
- **Add Users**: Create new admin or recruiter accounts
- **Manage Data**: Full access to all CRUD operations
- **View Analytics**: Access to all analytical dashboards
- **Audit Logs**: Monitor salary range updates

### For Recruiters
- **Add Recruiters**: Register new recruiting companies
- **Post Jobs**: Create new job listings with details
- **Add Candidates**: Register candidate profiles
- **Search Candidates**: Find matching candidates by skills and experience
- **View Reports**: Access recruitment analytics

### Menu Options
1. **Add User**: Create new user accounts (admin only)
2. **Add Recruiter**: Register new recruiters
3. **Add Job**: Create job postings
4. **Add Candidate**: Register candidate profiles
5. **Recruiter Analysis**: View recruiter performance metrics
6. **Candidate Analysis**: Search and match candidates
7. **View Data**: Browse all recruiters, jobs, and candidates
8. **Audit Log Dashboard**: Track salary updates
9. **Update Job Salary**: Modify salary ranges (triggers audit)
10. **Complex Queries**: Run advanced analytical queries

## Project Structure

```
Database Talent Acquisition/
│
├── dashboard.py                        # Main Streamlit application
├── SQL_Setup_MySQL.sql                 # Database schema and setup
├── requirements.txt                    # Python dependencies
├── config_template.py                  # Configuration template
├── .gitignore                          # Git ignore rules
├── Database_FINAL_Project_2024.pdf     # Project documentation
└── README.md                           # This file

Note: Sample data files (Recruiter.sql, Job.sql, Candidate.sql) can be
downloaded from the Kaggle sources listed in the Data Sources section.
```

## Database Schema

### Tables
- **Recruiter**: ContactPerson (PK), Contact, Company, CompanyProfile
- **Job**: JobId (PK), Location, Date, Experience, Skills, Title, ContactPerson (FK), SalaryRange
- **Candidate**: CandidateId (PK), EdLevel, Gender, YearsCoded, Country, PreviousSalary, Skills
- **Users**: UserId (PK), Username, Password, Role, CreatedAt
- **Job_Audit**: AuditID (PK), JobID (FK), ActionType, OldSalaryRange, NewSalaryRange, ModifiedAt

### Triggers
- **job_salary_audit**: Automatically logs changes to Job.SalaryRange

## Security Notes

- Never commit `config.py` or files containing credentials
- Use strong passwords for database and user accounts
- Passwords are hashed using bcrypt before storage
- Regularly backup your database
- Use environment variables for production deployments

## Data Sources

This project uses two primary datasets:

1. **Job Descriptions Dataset**: Contains job postings across various industries with details about job titles, required skills, experience levels, and locations.
   - Source: [Kaggle - Job Description Dataset](https://www.kaggle.com/datasets/ravindrasinghrana/job-description-dataset)

2. **Job Applicants Dataset**: Provides data on 70,000+ job applicants including educational background, skills, years of experience, gender, previous salary, and country of origin.
   - Source: [Kaggle - 70k Job Applicants Data](https://www.kaggle.com/datasets/ayushtankha/70k-job-applicants-data-human-resource/data)

## Troubleshooting

**Database Connection Error**
- Verify MySQL server is running
- Check database credentials in `create_connection()`
- Ensure `final_project` database exists

**Login Failed**
- Verify user exists in Users table
- Check password is correctly hashed with bcrypt

**Import Error**
- Run `pip install -r requirements.txt`
- Verify Python version is 3.8+

## Contributing

This project was created in 2023 as a database management demonstration. Contributions for improvements are welcome!

## License

This project is for educational purposes.

---

**Last Updated**: November 2025


import streamlit as st
import pymysql
import bcrypt
import pandas as pd


# MySQL Database Connection Function
def create_connection():
    """Create and return a database connection."""
    try:
        connection = pymysql.connect(
            host="127.0.0.1",  # Update with your MySQL host
            user="root",       # Update with your MySQL username
            password="root",  # Update with your MySQL password
            database="final_project"  # Update with your database name
        )
        return connection
    except Exception as e:
        st.error(f"Database Connection Error: {e}")
        return None

# Insert Data into Recruiter Table
def insert_recruiter(contact_person, contact, company, company_profile):
    """Insert a new recruiter into the database."""
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                INSERT INTO Recruiter (ContactPerson, Contact, Company, CompanyProfile)
                VALUES (%s, %s, %s, %s)
            """, (contact_person, contact, company, company_profile))
            connection.commit()
            st.success("Recruiter added successfully!")
        except Exception as e:
            st.error(f"Error adding recruiter: {e}")
        finally:
            cursor.close()
            connection.close()

# Insert Data into Job Table
def insert_job(location, date, experience, skills, title, contact_person, salary_range):
    """Insert a new job posting into the database."""
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                INSERT INTO Job (Location, Date, Experience, Skills, Title, ContactPerson, SalaryRange)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (location, date, experience, skills, title, contact_person, salary_range))
            connection.commit()
            st.success("Job added successfully!")
        except Exception as e:
            st.error(f"Error adding job: {e}")
        finally:
            cursor.close()
            connection.close()

# Insert Data into Candidate Table
def insert_candidate(ed_level, gender, years_coded, country, previous_salary, skills):
    """Insert a new candidate into the database."""
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                INSERT INTO Candidate (EdLevel, Gender, YearsCoded, Country, PreviousSalary, Skills)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (ed_level, gender, years_coded, country, previous_salary, skills))
            connection.commit()
            st.success("Candidate added successfully!")
        except Exception as e:
            st.error(f"Error adding candidate: {e}")
        finally:
            cursor.close()
            connection.close()

# Function to Fetch Matching Candidates
def fetch_candidates(skill, ed_level, min_experience):
    """Fetch candidates matching specific criteria."""
    query = """
        SELECT CandidateID, EdLevel, Gender, YearsCoded, Country, PreviousSalary, Skills
        FROM Candidate
        WHERE Skills LIKE %s
        AND EdLevel = %s
        AND YearsCoded >= %s;
    """
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute(query, (f"%{skill}%", ed_level, min_experience))
            results = cursor.fetchall()
            return results
        except Exception as e:
            st.error(f"Error executing query: {e}")
            return None
        finally:
            cursor.close()
            connection.close()
    else:
        return None


# Function to validate user login
def validate_user(username, password):
    """Validate user credentials and return their role if valid."""
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT Password, Role FROM Users WHERE Username = %s", (username,))
            result = cursor.fetchone()
            if result and bcrypt.checkpw(password.encode('utf-8'), result[0].encode('utf-8')):
                return result[1]  # Return user role (admin/recruiter)
            else:
                return None
        except Exception as e:
            st.error(f"Login validation error: {e}")
            return None
        finally:
            cursor.close()
            connection.close()
    return None

# Streamlit Login Form
st.title("Talent Acquisition Dashboard")

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['role'] = None



if not st.session_state['logged_in']:
    st.header("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        role = validate_user(username, password)
        if role:
            st.session_state['logged_in'] = True
            st.session_state['role'] = role
            st.success(f"Welcome, {username}!")
            st.rerun()
        else:
            st.error("Invalid credentials. Please try again.")
else:
    st.sidebar.text(f"Logged in as: {st.session_state['role']}")
    if st.sidebar.button("Logout"):
        st.session_state['logged_in'] = False
        st.session_state['role'] = None
        st.rerun()



# Main Streamlit App Interface

# Sidebar Menu
menu = st.sidebar.selectbox("Menu", ["Add User","Add Recruiter", "Add Job", "Add Candidate","Recruiter Analysis","Candidate Analysis", "View Data","Audit Log Dashboard","Get Latest Job Salary Range Updates", "Complex Queries"])


# Function to insert a new user into the Users table
def add_new_user(username, password, role):
    """Add a new user to the Users table with hashed password."""
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            # Hash the password before saving it
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            cursor.execute("""
                INSERT INTO Users (Username, Password, Role)
                VALUES (%s, %s, %s)
            """, (username, hashed_password.decode('utf-8'), role))
            connection.commit()
            st.success(f"User '{username}' added successfully as {role}!")
        except Exception as e:
            st.error(f"Error adding user: {e}")
        finally:
            cursor.close()
            connection.close()


# Add User Menu (Admins Only)
if menu == "Add User":
    st.header("Add New User")
    new_username = st.text_input("Enter Username")
    new_password = st.text_input("Enter Password", type="password")
    role = st.selectbox("Select Role", ["admin", "recruiter"])
    
    if st.button("Create User"):
        if new_username and new_password and role:
            add_new_user(new_username, new_password, role)
        else:
            st.error("Please fill all the fields.")



if menu == "Add Recruiter":
    st.header("Add a New Recruiter")
    contact_person = st.text_input("Contact Person")
    contact = st.text_input("Contact")
    company = st.text_input("Company")
    company_profile = st.text_area("Company Profile")
    if st.button("Add Recruiter"):
        if contact_person and contact and company:
            insert_recruiter(contact_person, contact, company, company_profile)
        else:
            st.error("Please fill all required fields!")

elif menu == "Recruiter Analysis":
    st.header("Recruiter Performance Analytics")
    st.subheader("Total Jobs Posted by Each Recruiter")

    # Fetch Data
    connection = create_connection()
    if connection:
        try:
            # SQL query to fetch total jobs posted by each recruiter
            query = """
                SELECT r.ContactPerson, COUNT(DISTINCT j.JobID) AS TotalJobsPosted
                FROM Recruiter r
                LEFT JOIN Job j ON r.ContactPerson = j.ContactPerson
                GROUP BY r.ContactPerson
                ORDER BY TotalJobsPosted DESC;
            """
            cursor = connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()

            if results:
                # Convert results to a table format
                df = pd.DataFrame(results, columns=["Recruiter", "Total Jobs Posted"])

                # Display Table
                st.table(df)
            else:
                st.info("No data available.")

        except Exception as e:
            st.error(f"Error executing query: {e}")
        finally:
            cursor.close()
            connection.close()
    else:
        st.error("Failed to connect to the database.")

elif menu == "Candidate Analysis":
    st.header("Candidate Skills Search and Matching")
    st.subheader("Find Candidates by Skills, Education Level, and Experience")

    # Input Fields
    skill = st.text_input("Enter Skill (e.g., Python, SQL)")
    ed_level = st.selectbox("Select Education Level", ["Undergraduate", "Master", "PhD"])
    min_experience = st.number_input("Minimum Years of Coding Experience", min_value=0, step=1)

    # Search Button
    if st.button("Search Candidates"):
        if skill and ed_level and min_experience is not None:
            # Function to Fetch Candidates
            connection = create_connection()
            if connection:
                try:
                    query = """
                        SELECT CandidateID, EdLevel, Gender, YearsCoded, Country, PreviousSalary, Skills
                        FROM Candidate
                        WHERE Skills LIKE %s
                        AND EdLevel = %s
                        AND YearsCoded >= %s;
                    """
                    cursor = connection.cursor()
                    cursor.execute(query, (f"%{skill}%", ed_level, min_experience))
                    results = cursor.fetchall()

                    # Display Results
                    if results:
                        df = pd.DataFrame(results, columns=[
                            "CandidateID", "Education Level", "Gender", "Years Coded", "Country", "Previous Salary", "Skills"
                        ])
                        st.success("Matching Candidates Found:")
                        st.table(df)
                    else:
                        st.warning("No matching candidates found.")
                except Exception as e:
                    st.error(f"Error executing query: {e}")
                finally:
                    cursor.close()
                    connection.close()
        else:
            st.error("Please fill in all the fields.")


elif menu == "Add Job":
    st.header("Add a New Job")
    location = st.text_input("Location")
    date = st.text_input("Date")
    experience = st.text_input("Experience")
    skills = st.text_area("Skills")
    title = st.text_input("Job Title")
    contact_person = st.text_input("Contact Person")
    salary_range = st.text_input("Salary Range")
    if st.button("Add Job"):
        if location and date and experience and title and contact_person:
            insert_job(location, date, experience, skills, title, contact_person, salary_range)
        else:
            st.error("Please fill all required fields!")

elif menu == "Add Candidate":
    st.header("Add a New Candidate")
    ed_level = st.text_input("Education Level")
    gender = st.radio("Gender", ["Male", "Female", "Other"])
    years_coded = st.number_input("Years Coded", min_value=0)
    country = st.text_input("Country")
    previous_salary = st.number_input("Previous Salary", min_value=0)
    skills = st.text_area("Skills")
    if st.button("Add Candidate"):
        if ed_level and gender and country:
            insert_candidate(ed_level, gender, years_coded, country, previous_salary, skills)
        else:
            st.error("Please fill all required fields!")

elif menu == "View Data":
    st.header("Data")
    connection = create_connection()
    if connection:
        cursor = connection.cursor(pymysql.cursors.DictCursor)  # Use DictCursor
        try:
            st.subheader("Recruiters")
            cursor.execute("SELECT * FROM Recruiter")
            recruiters = cursor.fetchall()
            st.write(recruiters)

            st.subheader("Jobs")
            cursor.execute("SELECT * FROM Job")
            jobs = cursor.fetchall()
            st.write(jobs)

            st.subheader("Candidates")
            cursor.execute("SELECT * FROM Candidate")
            candidates = cursor.fetchall()
            st.write(candidates)
        except Exception as e:
            st.error(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()


elif menu == "Audit Log Dashboard":
    st.header("Audit Log Dashboard")
    st.subheader("View Changes Made to Job Entries")

    # Database Connection
    connection = create_connection()
    if connection:
        try:
            # SQL query to fetch audit log data
            query = """
                SELECT AuditID, JobID, ActionType, OldSalaryRange, NewSalaryRange, ModifiedAt
                FROM Job_Audit
                ORDER BY ModifiedAt DESC;
            """
            cursor = connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()

            # Display Results
            if results:
                df = pd.DataFrame(results, columns=[
                    "AuditID", "JobID", "Action Type", "Old Salary Range", "New Salary Range", "Modified At"
                ])
                st.success("Audit Log Entries:")
                st.table(df)
            else:
                st.info("No audit log entries found.")
        except Exception as e:
            st.error(f"Error executing query: {e}")
        finally:
            # Safe connection close
            if connection and connection.open:
                cursor.close()
                connection.close()
    else:
        st.error("Failed to connect to the database.")


elif menu == "Complex Queries":
    st.header("Run Complex Queries")
    query_option = st.selectbox(
        "Select a Query",
        [
            "Top 3 Most In-Demand Skills Across All Jobs",
            "Find Recruiters Posting Jobs in a Specific Location",
            "Find Jobs Offering Salary for a Specific Skill",
            "Jobs Available by Recruiter with a Minimum Experience Requirement",
            "Compute Mean Salary by Education Level",
            "Compute Mean Salary by Skill",
            "In-Demand Skills with Salary Benchmark",

        ]
    )
    connection = create_connection()
    if connection:
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        if query_option == "Top 3 Most In-Demand Skills Across All Jobs":
            st.subheader("Top 3 Most In-Demand Skills")
            try:
                cursor.execute("""
                    SELECT Skill, COUNT(*) AS SkillCount
                    FROM (
                        SELECT TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(Skills, ',', n.n), ',', -1)) AS Skill
                        FROM Job
                        CROSS JOIN (
                            SELECT a.N + b.N * 10 + 1 AS n
                            FROM (SELECT 0 AS N UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4) a,
                                 (SELECT 0 AS N UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4) b
                            ORDER BY n
                        ) n
                        WHERE n.n <= 1 + (LENGTH(Skills) - LENGTH(REPLACE(Skills, ',', '')))
                    ) AS SkillList
                    GROUP BY Skill
                    ORDER BY SkillCount DESC
                    LIMIT 3;
                """)
                results = cursor.fetchall()
                st.write(results)
            except Exception as e:
                st.error(f"Error: {e}")
        
        elif query_option == "Find Recruiters Posting Jobs in a Specific Location":
            st.subheader("Recruiters Posting Jobs in a Specific Location")
            location = st.text_input("Enter Location (e.g., Amsterdam)")

            if location and st.button("Run Query"):
                try:
                    query = """
                        SELECT r.ContactPerson, r.Company, j.Title, j.Location
                        FROM Recruiter r
                        JOIN Job j ON r.ContactPerson = j.ContactPerson
                        WHERE j.Location = %s;
                    """
                    cursor.execute(query, (location,))
                    results = cursor.fetchall()
                    if results:
                        st.write(results)
                    else:
                        st.info(f"No jobs found in {location}.")
                except Exception as e:
                    st.error(f"Error: {e}")

        elif query_option == "Find Jobs Offering Salary for a Specific Skill":
            st.subheader("Jobs with Salary for a Skill")
            skill = st.text_input("Enter Skill (e.g., Python)")
            if st.button("Run Query"):
                try:
                    cursor.execute("""
                        SELECT Title, Location, SalaryRange, Skills
                        FROM Job
                        WHERE Skills LIKE %s
                        ORDER BY CAST(SUBSTRING_INDEX(SalaryRange, '-', -1) AS UNSIGNED) DESC
                        LIMIT 5;
                    """, (f"%{skill}%",))
                    results = cursor.fetchall()
                    st.write(results)
                except Exception as e:
                    st.error(f"Error: {e}")
        
        elif query_option == "Compute Mean Salary by Education Level":
            st.subheader("Mean Salary of Candidates by Education Level")

            # Dropdown for selecting the education level
            ed_level = st.selectbox("Select Education Level", ["Undergraduate", "Master", "PhD"])

            if st.button("Run Query"):
                try:
                    query = """
                        SELECT AVG(PreviousSalary) AS MeanSalary
                        FROM Candidate
                        WHERE EdLevel = %s;
                    """
                    cursor.execute(query, (ed_level,))
                    result = cursor.fetchone()
                    mean_salary = result["MeanSalary"]

                    if mean_salary:
                        st.success(f"The mean salary for {ed_level} candidates is: ${mean_salary:.2f}")
                    else:
                        st.info(f"No {ed_level} candidates found in the database.")
                except Exception as e:
                    st.error(f"Error: {e}")

        elif query_option == "Compute Mean Salary by Skill":
            st.subheader("Mean Salary of Candidates by Skill")

            # Input field for skill
            skill = st.text_input("Enter Skill (e.g., Python, SQL, Java)")

            if skill and st.button("Run Query"):
                try:
                    query = """
                        SELECT AVG(PreviousSalary) AS MeanSalary
                        FROM Candidate
                        WHERE Skills LIKE %s;
                    """
                    cursor.execute(query, (f"%{skill}%",))
                    result = cursor.fetchone()
                    mean_salary = result["MeanSalary"]

                    if mean_salary:
                        st.success(f"The mean salary for candidates with '{skill}' skill is: ${mean_salary:.2f}")
                    else:
                        st.info(f"No candidates found with '{skill}' skill in the database.")
                except Exception as e:
                    st.error(f"Error: {e}")

        elif query_option == "Jobs Available by Recruiter with a Minimum Experience Requirement":
            st.subheader("Jobs by Recruiter with Minimum Experience")
            min_experience = st.number_input("Enter Minimum Experience (in years)", min_value=0, step=1)
            if st.button("Run Query"):
                try:
                    cursor.execute("""
                        SELECT r.ContactPerson, r.Company, j.Title, j.Experience
                        FROM Recruiter r
                        JOIN Job j ON r.ContactPerson = j.ContactPerson
                        WHERE CAST(SUBSTRING_INDEX(Experience, ' ', 1) AS UNSIGNED) >= %s;
                    """, (min_experience,))
                    results = cursor.fetchall()
                    st.write(results)
                except Exception as e:
                    st.error(f"Error: {e}")

        # Note: "Top Recruiters by Candidate Success" query removed
        # Reason: Candidate table has no JobID foreign key relationship in the actual schema
        # This feature was proposed in Phase 1 but couldn't be implemented due to data constraints

        elif query_option == "In-Demand Skills with Salary Benchmark":
            st.subheader("In-Demand Skills with Salary Benchmark")
            try:
                query = """
                    SELECT Skills, AVG(
                        CAST(SUBSTRING_INDEX(SalaryRange, '-', -1) AS UNSIGNED)
                    ) AS AverageSalary
                    FROM Job
                    GROUP BY Skills
                    ORDER BY AverageSalary DESC;
                """
                cursor.execute(query)
                results = cursor.fetchall()
                if results:
                    df = pd.DataFrame(results, columns=["Skill", "Average Salary"])
                    st.table(df)
                else:
                    st.info("No data found for this query.")
            except Exception as e:
                st.error(f"Error executing query: {e}")
              

        
           

        cursor.close()
        connection.close()


elif menu == "Get Latest Job Salary Range Updates":
    st.header("Update Job Salary Range")
    
    # Connect to fetch Job IDs
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            # Fetch all Job IDs and Titles for selection
            cursor.execute("SELECT JobID, Title FROM Job")
            jobs = cursor.fetchall()
            job_options = {f"{job[0]} - {job[1]}": job[0] for job in jobs}


            # Dropdown to select Job
            selected_job = st.selectbox("Select a Job to Update", list(job_options.keys()))
            new_salary = st.text_input("Enter New Salary Range (e.g., 120000-150000)")

            # Update Button
            if st.button("Update Salary Range"):
                job_id = job_options[selected_job]
                if new_salary:
                    # Execute the UPDATE statement
                    cursor.execute("""
                        UPDATE Job
                        SET SalaryRange = %s
                        WHERE JobID = %s
                    """, (new_salary, job_id))
                    connection.commit()
                    st.success(f"Job {job_id} updated successfully!")

                    # Display Audit Log
                    st.subheader("Audit Log (Job_Audit)")
                    cursor.execute("SELECT * FROM Job_Audit ORDER BY ModifiedAt DESC")
                    audit_log = cursor.fetchall()
                    st.write(audit_log)
                else:
                    st.error("Please enter a valid Salary Range.")
        except Exception as e:
            st.error(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()



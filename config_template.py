"""
Database Configuration Template
Copy this file to 'config.py' and update with your MySQL credentials.
DO NOT commit config.py to version control!
"""

# MySQL Database Configuration
DB_CONFIG = {
    'host': '127.0.0.1',  # MySQL host (usually localhost or 127.0.0.1)
    'user': 'root',       # Your MySQL username
    'password': 'your_password_here',  # Your MySQL password
    'database': 'final_project'  # Database name
}

# Optional: Application Settings
APP_CONFIG = {
    'debug_mode': False,
    'port': 8501
}

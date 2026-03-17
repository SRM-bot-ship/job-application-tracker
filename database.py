import mysql.connector

def get_db():
    return mysql.connector.connect(
        host='localhost',       # Database host
        user='root',            # Your MySQL username
        password='Jan@2025',  # Your MySQL password
        database='job_tracker'  # The name of the database you are connecting to
    )
import pandas as pd
import sqlite3
import os

# Define table names and corresponding CSV files
csv_files = {
    'bed': 'bed.csv',
    'doctor': 'doctor.csv',
    'Medical_record': 'Medical-record.csv',
    'medicine': 'medicine.csv',
    'Patient': 'Patient.csv',
    'staff': 'staff.csv'
}

# Create an in-memory SQLite database
conn = sqlite3.connect(':memory:')

# Load each CSV into the database
for table_name, file_name in csv_files.items():
    if os.path.exists(file_name):
        try:
            df = pd.read_csv(file_name)
            df.to_sql(table_name, conn, index=False, if_exists='replace')
        except Exception as e:
            print(f"Error loading {file_name}: {e}")

# Define queries
queries = [
    ("Female Patients > 20", "SELECT PatientID, Name, Age, Gender, Phone, Address FROM Patient WHERE Gender = 'Female' AND Age > 20"),
    ("Free General Beds", "SELECT BedNumber, WardType, Status FROM bed WHERE Status = 'Free' AND WardType = 'General'"),
    ("Doctors & Salaries", "SELECT Name, Specialty, Salary FROM staff WHERE Role = 'Doctor'"),
    ("Medicines > 100", "SELECT Medicine, Manufacturer, Price FROM medicine WHERE Price > 100 ORDER BY Price DESC"),
    ("Patient Diagnoses", "SELECT p.Name AS PatientName, m.Diagnosis, m.AdmissionDate FROM Patient p INNER JOIN Medical_record m ON p.PatientID = m.PatientID")
]

# Execute and print results
for title, sql in queries:
    print(f"=== {title} ===")
    try:
        result_df = pd.read_sql_query(sql, conn)
        if result_df.empty:
            print("(No records found matching the criteria)")
        else:
            print(result_df.to_string(index=False))
    except Exception as e:
        print(f"Error executing query: {e}")
    print("\n")

import sqlite3
import csv
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
cursor = conn.cursor()

# Load each CSV into the database
for table_name, file_name in csv_files.items():
    if os.path.exists(file_name):
        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                headers = next(reader)
                
                # Create table
                cols = ', '.join([f'"{h}" TEXT' for h in headers])
                cursor.execute(f'CREATE TABLE "{table_name}" ({cols})')
                
                # Insert data
                placeholders = ', '.join(['?' for _ in headers])
                cursor.executemany(f'INSERT INTO "{table_name}" VALUES ({placeholders})', list(reader))
        except Exception as e:
            print(f"Error loading {file_name}: {e}")

# Define queries
queries = [
    ("Female Patients > 20", "SELECT PatientID, Name, Age, Gender, Phone, Address FROM Patient WHERE Gender = 'Female' AND CAST(Age AS INTEGER) > 20"),
    ("Free General Beds", "SELECT BedNumber, WardType, Status FROM bed WHERE Status = 'Free' AND WardType = 'General'"),
    ("Doctors & Salaries", "SELECT Name, Specialty, Salary FROM staff WHERE Role = 'Doctor'"),
    ("Medicines > 100", "SELECT Medicine, Manufacturer, Price FROM medicine WHERE CAST(Price AS INTEGER) > 100 ORDER BY CAST(Price AS INTEGER) DESC"),
    ("Patient Diagnoses", "SELECT p.Name AS PatientName, m.Diagnosis, m.AdmissionDate FROM Patient p INNER JOIN Medical_record m ON p.PatientID = m.PatientID")
]

# Execute and print results
for title, sql in queries:
    print(f"=== {title} ===")
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        cols = [description[0] for description in cursor.description]
        
        if not rows:
            print("(No records found matching the criteria)")
        else:
            # Simple column alignment
            col_widths = [max(len(str(val)) for val in col) for col in zip(*([cols] + rows))]
            header_str = " | ".join(f"{str(col).ljust(width)}" for col, width in zip(cols, col_widths))
            print(header_str)
            print("-" * len(header_str))
            for row in rows:
                print(" | ".join(f"{str(val).ljust(width)}" for val, width in zip(row, col_widths)))
    except Exception as e:
        print(f"Error executing query: {e}")
    print("\n")

conn.close()

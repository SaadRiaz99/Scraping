import pyodbc
import pandas as pd

db_path = r"D:\python\project\Data_student\dbms_assignment.accdb"

conn_str = (
    r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
    rf"DBQ={db_path};"
)

conn = pyodbc.connect(conn_str)

table_name = "student_performance"

df = pd.read_sql(f"SELECT * FROM {table_name}", conn)

df.to_csv("dbms_data.csv", index=False)

conn.close()

print("CSV saved successfully!")
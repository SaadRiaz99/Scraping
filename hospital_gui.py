import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

DB_PATH = 'hospital_management.db'

class HospitalGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("HospitalManagement11 - Professional System")
        self.root.geometry("1200x850")
        
        # --- THEME COLORS (Hospital-Friendly Palette) ---
        self.clr_bg = "#f7f9fc"        # Soft White-Blue Background
        self.clr_header = "#2c3e50"    # Dark Slate for Main Header
        self.clr_primary = "#3498db"   # Modern Hospital Blue (Add/Save)
        self.clr_secondary = "#95a5a6" # Subtle Grey (Cancel/Print)
        self.clr_danger = "#e74c3c"    # Alert Red (Delete)
        self.clr_text = "#34495e"      # Deep Blue-Grey for Labels
        self.font_main = ("Segoe UI", 10)
        self.font_bold = ("Segoe UI", 11, "bold")
        self.font_header = ("Segoe UI", 26, "bold")

        self.root.configure(bg=self.clr_bg)

        # Database connection
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()

        self.setup_styles()
        self.setup_ui()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Notebook (Tabs) Styling
        style.configure("TNotebook", background=self.clr_bg, borderwidth=0)
        style.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"), padding=[15, 5])
        style.map("TNotebook.Tab", background=[("selected", self.clr_primary)], foreground=[("selected", "white")])

        # Treeview (Table) Styling
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=30, background="white")
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#ecf0f1")

    def setup_ui(self):
        # 1. Main System Header (Requirement 7)
        header_frame = tk.Frame(self.root, bg=self.clr_header, pady=25)
        header_frame.pack(side=tk.TOP, fill=tk.X)
        
        header_title = tk.Label(header_frame, text="HospitalManagement11", font=self.font_header, bg=self.clr_header, fg="white")
        header_title.pack()
        
        sub_title = tk.Label(header_frame, text="Patient Care & Medical Information System", font=("Segoe UI", 10), bg=self.clr_header, fg="#bdc3c7")
        sub_title.pack()

        # 2. Tab Control
        self.tab_control = ttk.Notebook(self.root)
        
        # Tabs for each form
        tabs = [
            ("Patients", "PatientForm", "PatientDetails"),
            ("Staff", "StaffForm", "StaffDetails"),
            ("Beds", "BedForm", "BedDetails"),
            ("Medical Records", "MedicalRecordForm", "RecordDetails"),
            ("Medicines", "MedicineForm", "MedicineDetails"),
            ("Prescriptions", "PrescriptionForm", "PrescriptionDetails")
        ]
        
        self.tab_frames = {}
        for text, form_name, internal_name in tabs:
            frame = ttk.Frame(self.tab_control)
            self.tab_control.add(frame, text=f"  {text}  ")
            self.tab_frames[internal_name] = frame

        self.tab_control.pack(expand=1, fill="both", padx=20, pady=20)

        # Initialize each tab
        self.setup_patient_tab()
        self.setup_staff_tab()
        self.setup_bed_tab()
        self.setup_medical_record_tab()
        self.setup_medicine_tab()
        self.setup_prescription_tab()

    def create_modern_form(self, parent, form_title, section_title, fields, table_cols, db_table, id_col, refresh_func):
        # Main Container
        container = tk.Frame(parent, bg=self.clr_bg)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # FORM HEADING (Requirement 1 & 7)
        heading_lbl = tk.Label(container, text=form_title, font=("Segoe UI", 24, "bold"), fg=self.clr_primary, bg=self.clr_bg)
        heading_lbl.pack(pady=(0, 20), anchor=tk.W)

        # Split layout: Left (Form) | Right (Table)
        content_frame = tk.Frame(container, bg=self.clr_bg)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # LEFT SIDE: Input Section (Requirement 2 & 5)
        input_container = tk.Frame(content_frame, bg="white", bd=1, relief=tk.SOLID, highlightbackground=self.clr_primary, highlightthickness=1)
        input_container.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        
        # Section Sub-header (Requirement 2)
        tk.Label(input_container, text=section_title, font=self.font_bold, bg="#ecf0f1", fg=self.clr_text, pady=10).pack(fill=tk.X)
        
        fields_frame = tk.Frame(input_container, bg="white", padx=20, pady=20)
        fields_frame.pack()

        vars = []
        for i, (txt, var, is_id) in enumerate(fields):
            # Label
            tk.Label(fields_frame, text=txt, font=self.font_main, bg="white", fg=self.clr_text).grid(row=i, column=0, sticky=tk.W, pady=8)
            
            # Entry (Requirement 3: Consistent size and alignment)
            e = tk.Entry(fields_frame, textvariable=var, font=self.font_main, width=30, bd=1, relief=tk.SOLID)
            if is_id: 
                e.config(state='readonly', readonlybackground="#f8f9fa")
            e.grid(row=i, column=1, pady=8, padx=(10, 0))
            vars.append(var)

        # BUTTONS (Requirement 1 & 4)
        btn_container = tk.Frame(input_container, bg="white", pady=20)
        btn_container.pack(fill=tk.X)

        # Row 1: Add & Save (Primary)
        tk.Button(btn_container, text="✚  Add New", command=lambda: self.add_record(db_table, [f[0].replace(':', '').strip() for f in fields if not f[2]], [v for v, f in zip(vars, fields) if not f[2]], refresh_func), 
                  bg=self.clr_primary, fg="white", font=self.font_bold, width=12, bd=0, cursor="hand2").pack(side=tk.LEFT, padx=(20, 10))
        
        tk.Button(btn_container, text="💾  Save", command=lambda: self.save_record(db_table, id_col, vars[0], [f[0].replace(':', '').strip() for f in fields if not f[2]], [v for v, f in zip(vars, fields) if not f[2]], refresh_func), 
                  bg=self.clr_primary, fg="white", font=self.font_bold, width=12, bd=0, cursor="hand2").pack(side=tk.LEFT)

        # Row 2: Delete & Print (Secondary)
        btn_row2 = tk.Frame(input_container, bg="white", pady=10)
        btn_row2.pack(fill=tk.X)
        
        tk.Button(btn_row2, text="🗑  Delete", command=lambda: self.delete_record(db_table, id_col, vars[0], refresh_func), 
                  bg=self.clr_danger, fg="white", font=self.font_bold, width=12, bd=0, cursor="hand2").pack(side=tk.LEFT, padx=(20, 10))
        
        tk.Button(btn_row2, text="🖨  Print Report", command=lambda: self.print_records(db_table), 
                  bg=self.clr_secondary, fg="white", font=self.font_bold, width=12, bd=0, cursor="hand2").pack(side=tk.LEFT)

        # RIGHT SIDE: Table Section (Requirement 5)
        table_container = tk.Frame(content_frame, bg="white", bd=1, relief=tk.SOLID)
        table_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        tree = ttk.Treeview(table_container, columns=table_cols, show="headings", style="Treeview")
        for c in table_cols: 
            tree.heading(c, text=c)
            tree.column(c, width=100, anchor=tk.CENTER)
        
        scrollbar = ttk.Scrollbar(table_container, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)
        
        tree.bind("<<TreeviewSelect>>", lambda e: self.on_select(tree, vars))
        return tree

    # --- TAB SETUPS ---
    def setup_patient_tab(self):
        self.p_vars = [tk.StringVar() for _ in range(6)]
        fields = [("Patient ID:", self.p_vars[0], True), ("Full Name:", self.p_vars[1], False), ("Age:", self.p_vars[2], False), 
                  ("Gender:", self.p_vars[3], False), ("Phone:", self.p_vars[4], False), ("Address:", self.p_vars[5], False)]
        self.p_table = self.create_modern_form(self.tab_frames["PatientDetails"], "PatientForm", "General Information", fields, ["ID", "Name", "Age", "Gender", "Phone", "Address"], "Patient", "PatientID", self.refresh_patient_table)
        self.refresh_patient_table()

    def setup_staff_tab(self):
        self.s_vars = [tk.StringVar() for _ in range(6)]
        fields = [("Staff ID:", self.s_vars[0], True), ("Name:", self.s_vars[1], False), ("Role:", self.s_vars[2], False), 
                  ("Specialty:", self.s_vars[3], False), ("Phone:", self.s_vars[4], False), ("Salary ($):", self.s_vars[5], False)]
        self.s_table = self.create_modern_form(self.tab_frames["StaffDetails"], "StaffForm", "Staff Record Details", fields, ["ID", "Name", "Role", "Specialty", "Phone", "Salary"], "Staff", "StaffID", self.refresh_staff_table)
        self.refresh_staff_table()

    def setup_bed_tab(self):
        self.b_vars = [tk.StringVar() for _ in range(3)]
        fields = [("Bed Number:", self.b_vars[0], False), ("Ward Type:", self.b_vars[1], False), ("Occupancy Status:", self.b_vars[2], False)]
        self.b_table = self.create_modern_form(self.tab_frames["BedDetails"], "BedForm", "Bed Allocation Status", fields, ["Bed #", "Ward Type", "Status"], "Bed", "BedNumber", self.refresh_bed_table)
        self.refresh_bed_table()

    def setup_medical_record_tab(self):
        self.m_vars = [tk.StringVar() for _ in range(7)]
        fields = [("Record ID:", self.m_vars[0], True), ("Patient ID:", self.m_vars[1], False), ("Staff ID:", self.m_vars[2], False), 
                  ("Bed Num:", self.m_vars[3], False), ("Admission Date:", self.m_vars[4], False), ("Discharge Date:", self.m_vars[5], False), ("Diagnosis:", self.m_vars[6], False)]
        self.m_table = self.create_modern_form(self.tab_frames["RecordDetails"], "MedicalRecordForm", "Clinical Information", fields, ["ID", "PID", "SID", "Bed", "Adm", "Dis", "Diagnosis"], "MedicalRecords", "RecordID", self.refresh_medical_record_table)
        self.refresh_medical_record_table()

    def setup_medicine_tab(self):
        self.med_vars = [tk.StringVar() for _ in range(5)]
        fields = [("Medicine ID:", self.med_vars[0], True), ("Name:", self.med_vars[1], False), ("Manufacturer:", self.med_vars[2], False), ("Price ($):", self.med_vars[3], False), ("Expiry Date:", self.med_vars[4], False)]
        self.med_table = self.create_modern_form(self.tab_frames["MedicineDetails"], "MedicineForm", "Pharmacy Inventory", fields, ["ID", "Name", "Manufacturer", "Price", "Expiry"], "Medicine", "MedicineID", self.refresh_medicine_table)
        self.refresh_medicine_table()

    def setup_prescription_tab(self):
        self.pr_vars = [tk.StringVar() for _ in range(6)]
        fields = [("Prescription ID:", self.pr_vars[0], True), ("Record ID:", self.pr_vars[1], False), ("Med ID:", self.pr_vars[2], False), ("Dosage:", self.pr_vars[3], False), ("Frequency:", self.pr_vars[4], False), ("Duration:", self.pr_vars[5], False)]
        self.pr_table = self.create_modern_form(self.tab_frames["PrescriptionDetails"], "PrescriptionForm", "Medication Plan", fields, ["ID", "RID", "MID", "Dosage", "Freq", "Duration"], "Prescription", "PrescriptionID", self.refresh_prescription_table)
        self.refresh_prescription_table()

    # --- CORE LOGIC (Maintained) ---
    def refresh_patient_table(self): self.refresh_table_data(self.p_table, "SELECT * FROM Patient")
    def refresh_staff_table(self): self.refresh_table_data(self.s_table, "SELECT * FROM Staff")
    def refresh_bed_table(self): self.refresh_table_data(self.b_table, "SELECT * FROM Bed")
    def refresh_medical_record_table(self): self.refresh_table_data(self.m_table, "SELECT * FROM MedicalRecords")
    def refresh_medicine_table(self): self.refresh_table_data(self.med_table, "SELECT * FROM Medicine")
    def refresh_prescription_table(self): self.refresh_table_data(self.pr_table, "SELECT * FROM Prescription")

    def refresh_table_data(self, table, query):
        for row in table.get_children(): table.delete(row)
        self.cursor.execute(query)
        for row in self.cursor.fetchall(): table.insert("", tk.END, values=row)

    def on_select(self, table, vars):
        item = table.focus()
        if item:
            vals = table.item(item, "values")
            for i, var in enumerate(vars): 
                if i < len(vals): var.set(vals[i])

    def add_record(self, table_name, columns, vars, refresh_cb):
        vals = [v.get() for v in vars]
        if not any(vals): messagebox.showwarning("Incomplete", "Please enter record details first."); return
        try:
            self.cursor.execute(f"INSERT INTO {table_name} ({','.join(columns)}) VALUES ({','.join(['?']*len(vals))})", vals)
            self.conn.commit(); refresh_cb(); messagebox.showinfo("Success", "New record added successfully.")
        except Exception as e: messagebox.showerror("Database Error", str(e))

    def save_record(self, table, id_col, id_var, columns, vars, refresh_cb):
        if not id_var.get(): messagebox.showwarning("Select Record", "Please select a record from the table to update."); return
        vals = [v.get() for v in vars] + [id_var.get()]
        clause = ",".join([f"{c}=?" for c in columns])
        try:
            self.cursor.execute(f"UPDATE {table} SET {clause} WHERE {id_col}=?", vals)
            self.conn.commit(); refresh_cb(); messagebox.showinfo("Success", "Record updated successfully.")
        except Exception as e: messagebox.showerror("Database Error", str(e))

    def delete_record(self, table, id_col, id_var, refresh_cb):
        if not id_var.get(): messagebox.showwarning("Select Record", "Please select a record from the table to delete."); return
        if messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this record? (Yes / No)"):
            try:
                self.cursor.execute(f"DELETE FROM {table} WHERE {id_col}=?", (id_var.get(),))
                self.conn.commit(); refresh_cb(); messagebox.showinfo("Success", "Record removed from system.")
            except Exception as e: messagebox.showerror("Database Error", str(e))

    def print_records(self, table):
        try:
            filename = f"{table.lower()}_report.csv"
            self.cursor.execute(f"SELECT * FROM {table}")
            rows = self.cursor.fetchall()
            with open(filename, "w", newline='') as f:
                writer = csv.writer(f)
                self.cursor.execute(f"PRAGMA table_info({table})")
                writer.writerow([h[1] for h in self.cursor.fetchall()])
                writer.writerows(rows)
            messagebox.showinfo("Report Exported", f"The report has been saved as: {filename}")
        except Exception as e: messagebox.showerror("Export Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalGUI(root)
    root.mainloop()

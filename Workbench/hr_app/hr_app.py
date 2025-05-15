#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import csv
import ast

app = Flask(__name__)


CSV_FILE = "initial_data.csv"

def init_db():
    """Initialize the database and populate it if empty."""
    conn = sqlite3.connect("/var/employees.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS employees (id INTEGER PRIMARY KEY, data TEXT)")

    # Check if the table is empty
    cursor.execute("SELECT COUNT(*) FROM employees")
    if cursor.fetchone()[0] == 0:
        populate_db_from_csv()  # Populate database if empty

    conn.commit()
    conn.close()

def populate_db_from_csv():
    # Read from CSV and insert into the database
    with open(CSV_FILE, "r") as file:
        reader = csv.DictReader(file, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
        conn = sqlite3.connect("/var/employees.db")
        cursor = conn.cursor()

        for row in reader:
            cursor.execute("INSERT INTO employees (data) VALUES (?)", (str(row),))
        conn.commit()
        conn.close()

init_db()

@app.route('/hr')
def index():
    employees = ()
    try:
        conn = sqlite3.connect("/var/employees.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employees")
        employees = [(emp[0], ast.literal_eval(emp[1])) for emp in cursor.fetchall()]
        conn.close()
    except Exception as e:
        return render_template("index.html", employees=employees, message=f"Listing All Users Failed: {str(e)} ❌")

    message = request.args.get("message", "")  # Get message from URL
    return render_template("index.html", employees=employees, message=message)

@app.route('/hr/add', methods=['POST'])
def add_employee():
    try:
        data = request.form.to_dict()

        conn = sqlite3.connect("/var/employees.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO employees (data) VALUES (?)", (str(data),))
        conn.commit()
        conn.close()
        return redirect(url_for("index", message="User Added Successfully! ✅"))
    except Exception as e:
        return redirect(url_for("index", message=f"Add Operation Failed: {str(e)} ❌"))

@app.route('/hr/edit', methods=['POST'])
def edit_employee():
    try:
        emp_id = request.form.get("emp_id")  # Get ID from form data
        data = request.form.to_dict()
        del data["emp_id"]  # Remove ID from data dictionary

        conn = sqlite3.connect("/var/employees.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE employees SET data = ? WHERE id = ?", (str(data), emp_id))
        conn.commit()
        conn.close()

        return redirect(url_for("index", message="User Updated Successfully! ✅"))
    except Exception as e:
        return redirect(url_for("index", message=f"Edit Operation Failed: {str(e)} ❌"))

@app.route('/hr/delete/<int:emp_id>')
def delete_employee(emp_id):
    try:
        conn = sqlite3.connect("/var/employees.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM employees WHERE id = ?", (emp_id,))
        conn.commit()
        conn.close()
        return redirect(url_for("index", message="User Deleted Successfully! ✅"))
    except Exception as e:
        return redirect(url_for("index", message=f"Delete Operation Failed: {str(e)} ❌"))

@app.route('/hr/export')
def export_csv():
    try:
        conn = sqlite3.connect("/var/employees.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employees")
        employees = [(emp[0], ast.literal_eval(emp[1])) for emp in cursor.fetchall()]
        conn.close()

        with open("./exported_data/hr_data.csv", "w", newline="") as file:
            writer = csv.writer(file, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
            writer.writerow(["employeenumber","ssn","firstname","surname","status","address","phone","emptype","job"])
            for emp_id, emp_data in employees:
                writer.writerow([emp_data.get('employeenumber', ''), emp_data.get('ssn', ''), emp_data.get('firstname', ''), emp_data.get('surname', ''), emp_data.get('status', ''), emp_data.get('address', ''), emp_data.get('phone', ''), emp_data.get('emptype', ''), emp_data.get('job', '')])

        return redirect(url_for("index", message="CSV Exported Successfully! ✅"))

    except Exception as e:
        return redirect(url_for("index", message=f"Export Operation Failed: {str(e)} ❌"))

if __name__ == '__main__':
    app.run()
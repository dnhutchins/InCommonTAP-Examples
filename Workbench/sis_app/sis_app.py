#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import csv
import ast

app = Flask(__name__)


CSV_FILE = "initial_data.csv"

def init_db():
    """Initialize the database and populate it if empty."""
    conn = sqlite3.connect("/var/students.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY, data TEXT)")

    # Check if the table is empty
    cursor.execute("SELECT COUNT(*) FROM students")
    if cursor.fetchone()[0] == 0:
        populate_db_from_csv()  # Populate database if empty

    conn.commit()
    conn.close()

def populate_db_from_csv():
    # Read from CSV and insert into the database
    with open(CSV_FILE, "r") as file:
        reader = csv.DictReader(file, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
        conn = sqlite3.connect("/var/students.db")
        cursor = conn.cursor()

        for row in reader:
            cursor.execute("INSERT INTO students (data) VALUES (?)", (str(row),))
        conn.commit()
        conn.close()

init_db()

@app.route('/sis')
def index():
    students = ()
    try:
        conn = sqlite3.connect("/var/students.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        students = [(std[0], ast.literal_eval(std[1])) for std in cursor.fetchall()]
        conn.close()
    except Exception as e:
        return render_template("index.html", students=students, message=f"Listing All Users Failed: {str(e)} ❌")

    message = request.args.get("message", "")  # Get message from URL
    return render_template("index.html", students=students, message=message)

@app.route('/sis/add', methods=['POST'])
def add_student():
    try:
        data = request.form.to_dict()

        conn = sqlite3.connect("/var/students.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (data) VALUES (?)", (str(data),))
        conn.commit()
        conn.close()
        return redirect(url_for("index", message="User Added Successfully! ✅"))
    except Exception as e:
        return redirect(url_for("index", message=f"Add Operation Failed: {str(e)} ❌"))

@app.route('/sis/edit', methods=['POST'])
def edit_student():
    try:
        std_id = request.form.get("std_id")  # Get ID from form data
        data = request.form.to_dict()
        del data["std_id"]  # Remove ID from data dictionary

        conn = sqlite3.connect("/var/students.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE students SET data = ? WHERE id = ?", (str(data), std_id))
        conn.commit()
        conn.close()

        return redirect(url_for("index", message="User Updated Successfully! ✅"))
    except Exception as e:
        return redirect(url_for("index", message=f"Edit Operation Failed: {str(e)} ❌"))

@app.route('/sis/delete/<int:std_id>')
def delete_student(std_id):
    try:
        conn = sqlite3.connect("/var/students.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE id = ?", (std_id,))
        conn.commit()
        conn.close()
        return redirect(url_for("index", message="User Deleted Successfully! ✅"))
    except Exception as e:
        return redirect(url_for("index", message=f"Delete Operation Failed: {str(e)} ❌"))

@app.route('/sis/export')
def export_csv():
    try:
        conn = sqlite3.connect("/var/students.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        students = [(std[0], ast.literal_eval(std[1])) for std in cursor.fetchall()]
        conn.close()

        with open("./exported_data/sis_data.csv", "w", newline="") as file:
            writer = csv.writer(file, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
            writer.writerow(["studentnumber","ssn","firstname","surname","status","address","phone","studytype", "alumni","field"])
            for std_id, std_data in students:
                writer.writerow([std_data.get('studentnumber', ''), std_data.get('ssn', ''), std_data.get('firstname', ''), std_data.get('surname', ''), std_data.get('status', ''), std_data.get('address', ''), std_data.get('phone', ''), std_data.get('studytype', ''), std_data.get('alumni', ''), std_data.get('field', '')])

        return redirect(url_for("index", message="CSV Exported Successfully! ✅"))

    except Exception as e:
        return redirect(url_for("index", message=f"Export Operation Failed: {str(e)} ❌"))

if __name__ == '__main__':
    app.run()
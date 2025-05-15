#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import csv
import ast

app = Flask(__name__)


CSV_FILE = "initial_data.csv"

def init_db():
    """Initialize the database and populate it if empty."""
    conn = sqlite3.connect("/var/guests.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS guests (id INTEGER PRIMARY KEY, data TEXT)")

    # Check if the table is empty
    cursor.execute("SELECT COUNT(*) FROM guests")
    if cursor.fetchone()[0] == 0:
        populate_db_from_csv()  # Populate database if empty

    conn.commit()
    conn.close()

def populate_db_from_csv():
    # Read from CSV and insert into the database
    with open(CSV_FILE, "r") as file:
        reader = csv.DictReader(file, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
        conn = sqlite3.connect("/var/guests.db")
        cursor = conn.cursor()

        for row in reader:
            cursor.execute("INSERT INTO guests (data) VALUES (?)", (str(row),))
        conn.commit()
        conn.close()

init_db()

@app.route('/gs')
def index():
    guests = ()
    try:
        conn = sqlite3.connect("/var/guests.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM guests")
        guests = [(guest[0], ast.literal_eval(guest[1])) for guest in cursor.fetchall()]
        conn.close()
    except Exception as e:
        return render_template("index.html", guests=guests, message=f"Listing All Users Failed: {str(e)} ❌")

    message = request.args.get("message", "")  # Get message from URL
    return render_template("index.html", guests=guests, message=message)

@app.route('/gs/add', methods=['POST'])
def add_guest():
    try:
        data = request.form.to_dict()

        conn = sqlite3.connect("/var/guests.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO guests (data) VALUES (?)", (str(data),))
        conn.commit()
        conn.close()
        return redirect(url_for("index", message="User Added Successfully! ✅"))
    except Exception as e:
        return redirect(url_for("index", message=f"Add Operation Failed: {str(e)} ❌"))

@app.route('/gs/edit', methods=['POST'])
def edit_guest():
    try:
        guest_id = request.form.get("guest_id")  # Get ID from form data
        data = request.form.to_dict()
        del data["guest_id"]  # Remove ID from data dictionary

        conn = sqlite3.connect("/var/guests.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE guests SET data = ? WHERE id = ?", (str(data), guest_id))
        conn.commit()
        conn.close()

        return redirect(url_for("index", message="User Updated Successfully! ✅"))
    except Exception as e:
        return redirect(url_for("index", message=f"Edit Operation Failed: {str(e)} ❌"))

@app.route('/gs/delete/<int:guest_id>')
def delete_guest(guest_id):
    try:
        conn = sqlite3.connect("/var/guests.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM guests WHERE id = ?", (guest_id,))
        conn.commit()
        conn.close()
        return redirect(url_for("index", message="User Deleted Successfully! ✅"))
    except Exception as e:
        return redirect(url_for("index", message=f"Delete Operation Failed: {str(e)} ❌"))

@app.route('/gs/export')
def export_csv():
    try:
        conn = sqlite3.connect("/var/guests.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM guests")
        guests = [(guest[0], ast.literal_eval(guest[1])) for guest in cursor.fetchall()]
        conn.close()

        with open("./exported_data/gs_data.csv", "w", newline="") as file:
            writer = csv.writer(file, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
            writer.writerow(["guestnumber","firstname","surname","address","phone","guesttype","expiration"])
            for guest_id, guest_data in guests:
                writer.writerow([guest_data.get('guestnumber', ''), guest_data.get('firstname', ''), guest_data.get('surname', ''), guest_data.get('address', ''), guest_data.get('phone', ''), guest_data.get('guesttype', ''), guest_data.get('expiration', '')])

        return redirect(url_for("index", message="CSV Exported Successfully! ✅"))

    except Exception as e:
        return redirect(url_for("index", message=f"Export Operation Failed: {str(e)} ❌"))

if __name__ == '__main__':
    app.run()
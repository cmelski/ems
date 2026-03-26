from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, Response
from dev.db import db_create
from dev.db.db_client import DBClient
import psycopg
import openpyxl
import pandas as pd
from sqlalchemy import create_engine, inspect

app = Flask(__name__)
db_create.create_db()
db_create.create_table()


def download_db_data():
    db_client = DBClient()
    data = db_client.get_table_data()
    wb = openpyxl.Workbook()
    wb.remove(wb.active)  # remove default empty sheet
    for sheet_name, rows in data.items():
        ws = wb.create_sheet(title=sheet_name)
        if rows:
            print(rows)
            # Write rows
            for row in rows:
                print(row)
                ws.append(row)

    wb.save('output.xlsx')


#download_db_data()

def upload_db_data():
    engine = create_engine("postgresql://postgres:password@localhost:5433/executor")

    xls = pd.ExcelFile("output.xlsx")
    inspector = inspect(engine)

    for table in xls.sheet_names:

        df = pd.read_excel(xls, sheet_name=table, header=None)

        # Skip empty sheets first
        if df.dropna(how="all").empty:
            print(f"Sheet '{table}' is empty, skipping.")
            continue

        cols = [c["name"] for c in inspector.get_columns(table)]

        df.columns = cols

        df.to_sql(table, engine, if_exists="append", index=False)

        print(f"Inserted {len(df)} rows into {table}")


#upload_db_data()


def get_tasks():
    db_client = DBClient()
    rows = db_client.get_tasks_from_db()
    return [
        {
            "id": r[0],
            "description": r[1],
            "category": r[2],
            "due_date": r[3],
            "priority": r[4],
            "status": r[5].lower()
        }
        for r in rows
    ]


@app.route('/api/tasks', methods=['GET'])
def fetch_tasks():
    tasks = get_tasks()
    return jsonify({
        "message": "Tasks returned successfully",
        "tasks": tasks
    })


def get_task_by_description(description):
    db_client = DBClient()
    row = db_client.get_task_by_description_from_db(description)
    return [
        {
            "id": row[0],
            "description": row[1],
            "category": row[2],
            "due_date": row[3],
            "priority": row[4],
            "status": row[5].lower()
        }
    ]


@app.route('/api/task', methods=['GET'])
def fetch_task_by_description():
    description = request.args.get("description")
    print(description)
    task = get_task_by_description(description)
    return jsonify({
        "message": "Task returned successfully",
        "task": task
    })


@app.route('/api/tasks', methods=['POST'])
def add_task():
    db_client = DBClient()
    try:
        print("Raw request data:", request.data)
        data = request.get_json(force=True)
        print("Parsed data:", data)

        if not data:
            return jsonify({"error": "No JSON received"}), 400

        task_details = []
        description = data['description']
        category = data['category']
        due_date = data['due_date']
        priority = data['priority']
        status = data['status'].lower()

        task_details.extend([description, category, due_date, priority, status])

        new_task = db_client.add_task_to_db(task_details)
        print(f'new task: {list(new_task)}')

        return jsonify({"message": "Task added successfully",
                        "task": {
                            "id": new_task[0],
                            "description": new_task[1],
                            "category": new_task[2],
                            "due_date": new_task[3],
                            "priority": new_task[4],
                            "status": new_task[5].lower()
                        }
                        }), 201

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task_by_task_id(task_id):
    print(f'task_id: {task_id}')
    db_client = DBClient()
    try:
        db_client.delete_task_by_task_id(task_id)
        return jsonify({"message": "Task deleted successfully"}), 200
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500


@app.route('/api/tasks/<int:task_id>', methods=['PATCH'])
def update_task_status_by_task_id(task_id):
    print("Raw request data:", request.data)
    data = request.get_json(force=True)
    print("Parsed data:", data)

    if not data:
        return jsonify({"error": "No JSON received"}), 400

    task_status = data['status']
    db_client = DBClient()
    try:
        db_client.update_task_status_by_task_id(task_id, task_status, data)
        return jsonify({"message": "Task updated successfully"}), 200
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500


@app.route('/api/tasks/row/<int:task_id>', methods=['PATCH'])
def update_task_row(task_id):
    print("Raw request data:", request.data)
    data = request.get_json(force=True)
    print("Parsed data:", data)

    if not data:
        return jsonify({"error": "No JSON received"}), 400

    db_client = DBClient()
    try:
        db_client.update_task_row(task_id, data)
        return jsonify({"message": "Task row updated successfully"}), 200
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500


def get_bills():
    db_client = DBClient()
    rows = db_client.get_bills_from_db()
    return [
        {
            "id": r[0],
            "description": r[1],
            "amount": r[2],
            "due_date": r[3],
            "bill_type": r[4],
            "status": r[5].lower()
        }
        for r in rows
    ]


@app.route('/api/bills', methods=['GET'])
def fetch_bills():
    bills = get_bills()
    return jsonify({
        "message": "Bills returned successfully",
        "bills": bills
    })


@app.route('/api/bills', methods=['POST'])
def add_bill():
    db_client = DBClient()
    try:
        print("Raw request data:", request.data)
        data = request.get_json(force=True)
        print("Parsed data:", data)

        if not data:
            return jsonify({"error": "No JSON received"}), 400

        bill_details = []
        description = data['description']
        amount = data['amount']
        due_date = data['due_date']
        bill_type = data['bill_type']
        status = data['status'].lower()

        bill_details.extend([description, amount, due_date, bill_type, status])

        new_bill = db_client.add_bill_to_db(bill_details)
        print(f'new bill: {list(bill_details)}')

        return jsonify({"message": "Bill added successfully",
                        "bill": {
                            "id": new_bill[0],
                            "description": new_bill[1],
                            "amount": new_bill[2],
                            "due_date": new_bill[3],
                            "type": new_bill[4],
                            "status": new_bill[5].lower()
                        }
                        }), 201

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500


@app.route('/api/bills/<int:bill_id>', methods=['DELETE'])
def delete_bill_by_bill_id(bill_id):
    print(f'bill_id: {bill_id}')
    db_client = DBClient()
    try:
        db_client.delete_bill_by_bill_id(bill_id)
        return jsonify({"message": "Bill deleted successfully"}), 200
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500


@app.route('/api/bills/<int:bill_id>', methods=['PATCH'])
def update_bill_status_by_bill_id(bill_id):
    print("Raw request data:", request.data)
    data = request.get_json(force=True)
    print("Parsed data:", data)

    if not data:
        return jsonify({"error": "No JSON received"}), 400

    bill_status = data['status']
    db_client = DBClient()
    try:
        db_client.update_bill_status_by_bill_id(bill_id, bill_status, data)
        return jsonify({"message": "Bill updated successfully"}), 200
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500


@app.route('/api/bills/row/<int:bill_id>', methods=['PATCH'])
def update_bill_row(bill_id):
    print("Raw request data:", request.data)
    data = request.get_json(force=True)
    print("Parsed data:", data)

    if not data:
        return jsonify({"error": "No JSON received"}), 400

    db_client = DBClient()
    try:
        db_client.update_bill_row(bill_id, data)
        return jsonify({"message": "Bill row updated successfully"}), 200
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500


def get_expenses():
    db_client = DBClient()
    rows = db_client.get_expenses_from_db()
    return [
        {
            "id": r[0],
            "description": r[1],
            "amount": r[2],
            "date_incurred": r[3],
            "category": r[4],
            "notes": r[5],
            "reimbursable": r[6],
            "status": r[7].lower()
        }
        for r in rows
    ]


@app.route('/api/expenses', methods=['GET'])
def fetch_expenses():
    expenses = get_expenses()
    print(f'expenses: {expenses}')
    return jsonify({
        "message": "Expenses returned successfully",
        "expenses": expenses
    })


@app.route('/api/expenses', methods=['POST'])
def add_expense():
    db_client = DBClient()
    try:
        print("Raw request data:", request.data)
        data = request.get_json(force=True)
        print("Parsed data:", data)

        if not data:
            return jsonify({"error": "No JSON received"}), 400

        expense_details = []
        description = data['description']
        amount = data['amount']
        date_incurred = data['date_incurred']
        category = data['category']
        notes = data['notes']
        reimbursable = data['reimbursable']

        if reimbursable == 'No':
            status = 'N/A'
        else:
            status = data['status'].lower()

        expense_details.extend([description, amount, date_incurred, category, notes,
                                reimbursable, status])

        new_expense = db_client.add_expense_to_db(expense_details)
        print(f'new expense: {list(expense_details)}')

        return jsonify({"message": "Expense added successfully",
                        "expense": {
                            "id": new_expense[0],
                            "description": new_expense[1],
                            "amount": new_expense[2],
                            "date_incurred": new_expense[3],
                            "category": new_expense[4],
                            "notes": new_expense[5],
                            "reimbursable": new_expense[6],
                            "status": new_expense[7].lower()
                        }
                        }), 201

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500


@app.route('/api/expenses/<int:expense_id>', methods=['DELETE'])
def delete_expense_by_expense_id(expense_id):
    print(f'expense_id: {expense_id}')
    db_client = DBClient()
    try:
        db_client.delete_expense_by_expense_id(expense_id)
        return jsonify({"message": "Expense deleted successfully"}), 200
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500


@app.route('/api/expenses/<int:expense_id>', methods=['PATCH'])
def update_expense_status_by_expense_id(expense_id):
    print("Raw request data:", request.data)
    data = request.get_json(force=True)
    print("Parsed data:", data)

    if not data:
        return jsonify({"error": "No JSON received"}), 400

    expense_status = data['status']
    db_client = DBClient()
    try:
        db_client.update_expense_status_by_expense_id(expense_id, expense_status, data)
        return jsonify({"message": "Expense updated successfully"}), 200
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500


def get_assets():
    db_client = DBClient()
    rows = db_client.get_assets_from_db()
    return [
        {
            "id": r[0],
            "name": r[1],
            "type": r[2],
            "value": r[3],
            "beneficiary": r[4],
            "location": r[5],
            "status": r[6].lower()
        }
        for r in rows
    ]


@app.route('/api/assets', methods=['GET'])
def fetch_assets():
    assets = get_assets()
    print(f'assets: {assets}')
    return jsonify({
        "message": "Assets returned successfully",
        "assets": assets
    })


@app.route('/api/assets', methods=['POST'])
def add_asset():
    db_client = DBClient()
    try:
        print("Raw request data:", request.data)
        data = request.get_json(force=True)
        print("Parsed data:", data)

        if not data:
            return jsonify({"error": "No JSON received"}), 400

        asset_details = []
        name = data['name']
        type = data['type']
        value = data['value']
        beneficiary = data['beneficiary']
        location = data['location']
        status = data['status'].lower()

        asset_details.extend([name, type, value, beneficiary, location,
                              status])

        new_asset = db_client.add_asset_to_db(asset_details)
        print(f'new asset: {list(asset_details)}')

        return jsonify({"message": "Asset added successfully",
                        "asset": {
                            "id": new_asset[0],
                            "name": new_asset[1],
                            "type": new_asset[2],
                            "value": new_asset[3],
                            "benificiary": new_asset[4],
                            "location": new_asset[5],
                            "status": new_asset[6].lower()
                        }
                        }), 201

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500


@app.route('/api/assets/<int:asset_id>', methods=['DELETE'])
def delete_asset_by_asset_id(asset_id):
    print(f'asset_id: {asset_id}')
    db_client = DBClient()
    try:
        db_client.delete_asset_by_asset_id(asset_id)
        return jsonify({"message": "Asset deleted successfully"}), 200
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500


@app.route('/api/assets/<int:asset_id>', methods=['PATCH'])
def update_asset_status_by_asset_id(asset_id):
    print("Raw request data:", request.data)
    data = request.get_json(force=True)
    print("Parsed data:", data)

    if not data:
        return jsonify({"error": "No JSON received"}), 400

    asset_status = data['status']
    db_client = DBClient()
    try:
        db_client.update_asset_status_by_asset_id(asset_id, asset_status, data)
        return jsonify({"message": "Asset updated successfully"}), 200
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500


def get_contacts():
    db_client = DBClient()
    rows = db_client.get_contacts_from_db()
    return [
        {
            "id": r[0],
            "name": r[1],
            "role": r[2],
            "phone": r[3],
            "email": r[4]
        }
        for r in rows
    ]


@app.route('/api/contacts', methods=['GET'])
def fetch_contacts():
    contacts = get_contacts()
    return jsonify({
        "message": "Contacts returned successfully",
        "contacts": contacts
    })


@app.route('/api/contacts', methods=['POST'])
def add_contacts():
    db_client = DBClient()
    try:
        print("Raw request data:", request.data)
        data = request.get_json(force=True)
        print("Parsed data:", data)

        if not data:
            return jsonify({"error": "No JSON received"}), 400

        contact_details = []
        name = data['name']
        role = data['role']
        phone = data['phone']
        email = data['email']

        contact_details.extend([name, role, phone, email])

        new_contact = db_client.add_contact_to_db(contact_details)
        print(f'new contact: {list(contact_details)}')

        return jsonify({"message": "Contact added successfully",
                        "contact": {
                            "id": new_contact[0],
                            "name": new_contact[1],
                            "role": new_contact[2],
                            "phone": new_contact[3],
                            "email": new_contact[4]
                        }
                        }), 201

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500


@app.route('/api/contacts/<int:contact_id>', methods=['DELETE'])
def delete_contact_by_contact_id(contact_id):
    print(f'contact_id: {contact_id}')
    db_client = DBClient()
    try:
        db_client.delete_contact_by_contact_id(contact_id)
        return jsonify({"message": "Contact deleted successfully"}), 200
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500


def get_notes():
    db_client = DBClient()
    rows = db_client.get_notes_from_db()
    return [
        {
            "id": r[0],
            "date": r[1],
            "title": r[2],
            "category": r[3],
            "content": r[4]
        }
        for r in rows
    ]


@app.route('/api/notes', methods=['GET'])
def fetch_notes():
    notes = get_notes()
    return jsonify({
        "message": "Notes returned successfully",
        "notes": notes
    })


@app.route('/api/notes', methods=['POST'])
def add_notes():
    db_client = DBClient()
    try:
        print("Raw request data:", request.data)
        data = request.get_json(force=True)
        print("Parsed data:", data)

        if not data:
            return jsonify({"error": "No JSON received"}), 400

        note_details = []
        date = data['date']
        title = data['title']
        category = data['category']
        content = data['content']

        note_details.extend([date, title, category, content])

        new_note = db_client.add_note_to_db(note_details)
        print(f'new note: {list(note_details)}')

        return jsonify({"message": "Note added successfully",
                        "note": {
                            "id": new_note[0],
                            "date": new_note[1],
                            "title": new_note[2],
                            "category": new_note[3],
                            "content": new_note[4]
                        }
                        }), 201

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500


@app.route('/api/notes/<int:note_id>', methods=['DELETE'])
def delete_note_by_note_id(note_id):
    print(f'note_id: {note_id}')
    db_client = DBClient()
    try:
        db_client.delete_note_by_note_id(note_id)
        return jsonify({"message": "Note deleted successfully"}), 200
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500


def get_settings():
    db_client = DBClient()
    rows = db_client.get_settings_from_db()
    return [
        {
            "id": r[0],
            "name": r[1],
            "dod": r[2],
            "executor": r[3],
            "ref": r[4]
        }
        for r in rows
    ]


@app.route('/api/settings', methods=['GET'])
def fetch_settings():
    settings = get_settings()
    print(settings)
    return jsonify({
        "message": "Settings returned successfully",
        "settings": settings
    })


@app.route('/api/settings', methods=['POST'])
def add_settings():
    db_client = DBClient()
    try:
        print("Raw request data:", request.data)
        data = request.get_json(force=True)
        print("Parsed data:", data)

        if not data:
            return jsonify({"error": "No JSON received"}), 400

        settings_details = []
        name = data['name']
        dod = data['dod']
        executor = data['executor']
        ref = data['ref']

        settings_details.extend([name, dod, executor, ref])

        new_settings = db_client.add_settings_to_db(settings_details)
        print(f'new settings: {list(settings_details)}')

        return jsonify({"message": "Settings added successfully",
                        "settingsDetails": {
                            "id": new_settings[0],
                            "name": new_settings[1],
                            "dod": new_settings[2],
                            "executor": new_settings[3],
                            "ref": new_settings[4]
                        }
                        }), 201

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500


@app.route('/api/settings/', methods=['PATCH'])
def update_settings():
    print("Raw request data:", request.data)
    data = request.get_json(force=True)
    print("Parsed data:", data)

    if not data:
        return jsonify({"error": "No JSON received"}), 400

    db_client = DBClient()
    try:
        db_client.update_settings(data)
        return jsonify({"message": "Settings updated successfully"}), 200
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500


def get_activity():
    db_client = DBClient()
    rows = db_client.get_activity_log()
    return [
        {
            "activity_id": r[0],
            "date": r[1],
            "category": r[2],
            "description": r[3],
            "detail": r[4],
            "status": r[5].lower(),
            "note": r[6]
        }
        for r in rows
    ]


@app.route('/api/activity', methods=['GET'])
def fetch_activity():
    activity = get_activity()
    print(f'activity loaded: {activity}')
    return jsonify({
        "message": "Activity returned successfully",
        "activity": activity
    })


@app.route('/')
def home():
    return render_template("index.html")


if __name__ == "__main__":
    # app.run(debug=app.config.get("DEBUG", False), port=5002)
    app.run(host="0.0.0.0", port=5002, debug=app.config.get("DEBUG", False))

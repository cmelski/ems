from dev.db.db_connect import DBConnect
from datetime import datetime

TABLES = ['asset', 'task', 'expense', 'bill', 'contact', 'note', 'settings', 'activity']


class DBClient:

    def __init__(self):
        self.connection = DBConnect()

    def get_user(self, user_id):
        cursor = self.connection.cursor
        cursor.execute("SELECT user_id, first_name, last_name, email, password "
                       "FROM users WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()
        return user

    def check_existing_user(self, email):
        cursor = self.connection.cursor
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        return user

    def check_user_executor(self, user_id):
        cursor = self.connection.cursor
        cursor.execute("""
                        SELECT s.*
                        FROM settings s
                        JOIN estate_users eu ON s.settings_id = eu.estate_id
                        WHERE eu.user_id = %s;
                        """, (user_id,))  # <-- pass as tuple
        result = cursor.fetchall()
        return result

    def register_user(self, user_info):
        cursor = self.connection.cursor
        cursor.execute("""
                    INSERT INTO users
                    (first_name, last_name, email, password)
                    VALUES (%s, %s, %s, %s)
                    RETURNING user_id, first_name, last_name, email, password;
                """, user_info)

        new_user = cursor.fetchone()
        self.connection.commit()
        return new_user

    def get_tasks_from_db(self):
        cursor = self.connection.cursor
        cursor.execute("SELECT * from task order by task_id desc;")
        tasks = cursor.fetchall()
        # print(tasks)
        cursor.close()
        return tasks

    def get_bills_from_db(self):
        cursor = self.connection.cursor
        cursor.execute("SELECT * from bill order by bill_id desc;")
        bills = cursor.fetchall()
        # print(bills)
        cursor.close()
        return bills

    def get_expenses_from_db(self):
        cursor = self.connection.cursor
        cursor.execute("SELECT * from expense order by expense_id desc;")
        expenses = cursor.fetchall()
        # print(expenses)
        cursor.close()
        return expenses

    def get_assets_from_db(self):
        cursor = self.connection.cursor
        cursor.execute("SELECT * from asset order by asset_id desc;")
        assets = cursor.fetchall()
        print(assets)
        cursor.close()
        return assets

    def get_contacts_from_db(self):
        cursor = self.connection.cursor
        cursor.execute("SELECT * from contact order by contact_id desc;")
        contacts = cursor.fetchall()
        # print(contacts)
        cursor.close()
        return contacts

    def get_notes_from_db(self):
        cursor = self.connection.cursor
        cursor.execute("SELECT * from note order by note_id desc;")
        notes = cursor.fetchall()
        # print(notes)
        cursor.close()
        return notes

    def get_settings_from_db(self):
        cursor = self.connection.cursor
        cursor.execute("SELECT * from settings order by settings_id desc;")
        settings = cursor.fetchall()
        # print(settings)
        cursor.close()
        return settings

    def get_task_by_id(self, task_id):
        cursor = self.connection.cursor
        cursor.execute("""
                           SELECT * FROM task
                           WHERE task_id = %s;
                       """, (task_id,))  # <-- pass as tuple
        task = cursor.fetchone()
        # print(task)
        return task

    def get_bill_by_id(self, bill_id):
        cursor = self.connection.cursor
        cursor.execute("""
                             SELECT * FROM bill
                             WHERE bill_id = %s;
                         """, (bill_id,))  # <-- pass as tuple
        bill = cursor.fetchone()
        # print(bill)
        return bill

    def get_expense_by_id(self, expense_id):
        cursor = self.connection.cursor
        cursor.execute("""
                              SELECT * FROM expense
                              WHERE expense_id = %s;
                          """, (expense_id,))  # <-- pass as tuple
        expense = cursor.fetchone()
        # print(expense)
        return expense

    def get_asset_by_id(self, asset_id):
        cursor = self.connection.cursor
        cursor.execute("""
                              SELECT * FROM asset
                              WHERE asset_id = %s;
                          """, (asset_id,))  # <-- pass as tuple
        asset = cursor.fetchone()
        # print(asset)
        return asset

    def get_contact_by_id(self, contact_id):
        cursor = self.connection.cursor
        cursor.execute("""
                           SELECT * FROM contact
                           WHERE contact_id = %s;
                       """, (contact_id,))  # <-- pass as tuple
        contact = cursor.fetchone()
        # print(contact)
        return contact

    def get_note_by_id(self, note_id):
        cursor = self.connection.cursor
        cursor.execute("""
                           SELECT * FROM note
                           WHERE note_id = %s;
                       """, (note_id,))  # <-- pass as tuple
        note = cursor.fetchone()
        # print(note)
        return note

    def get_settings_by_id(self, settings_id):
        cursor = self.connection.cursor
        cursor.execute("""
                              SELECT * FROM settings
                              WHERE settings_id = %s;
                          """, (settings_id,))  # <-- pass as tuple
        settings = cursor.fetchone()
        # print(settings)
        return settings

    def add_task_to_db(self, task_details):
        cursor = self.connection.cursor

        cursor.execute("""
            INSERT INTO task
            (description, category, due_date, priority, status)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING task_id, description, category, due_date, priority,
                      status;
        """, task_details)

        new_task = cursor.fetchone()
        # print(new_task)
        self.connection.commit()

        activity_log_list = []
        activity_id = list(new_task)[0]
        # date = datetime.now().strftime("%b %-d")
        description = list(new_task)[1]
        category = 'TASK'
        detail = list(new_task)[4] + ' Priority'
        status = list(new_task)[5]
        note = 'task added'
        activity_log_list.extend([activity_id, category, description,
                                  detail, status, note])
        # print(f'activity list: {activity_log_list}')
        self.add_activity_log_to_db(activity_log_list)
        cursor.close()
        # print(f'new task: {new_task}')
        return new_task

    def add_bill_to_db(self, bill_details):
        cursor = self.connection.cursor

        cursor.execute("""
                  INSERT INTO bill
                  (description, amount, due_date, type, status)
                  VALUES (%s, %s, %s, %s, %s)
                  RETURNING bill_id, description, amount, due_date, type,
                            status;
              """, bill_details)

        new_bill = cursor.fetchone()
        # print(new_bill)
        self.connection.commit()

        activity_log_list = []
        activity_id = list(new_bill)[0]
        description = list(new_bill)[1]
        category = 'BILL'
        detail = list(new_bill)[2]
        status = list(new_bill)[5]
        note = 'bill added'
        activity_log_list.extend([activity_id, category, description,
                                  detail, status, note])
        # print(f'activity list: {activity_log_list}')
        self.add_activity_log_to_db(activity_log_list)
        cursor.close()
        return new_bill

    def add_expense_to_db(self, expense_details):
        cursor = self.connection.cursor

        cursor.execute("""
                  INSERT INTO expense
                  (description, amount, date_incurred, category, notes, reimbursable, status)
                  VALUES (%s, %s, %s, %s, %s, %s, %s)
                  RETURNING expense_id, description, amount, date_incurred, category,
                            notes, reimbursable, status;
              """, expense_details)

        new_expense = cursor.fetchone()
        # print(new_expense)
        self.connection.commit()

        activity_log_list = []
        activity_id = list(new_expense)[0]
        description = list(new_expense)[1]
        category = 'EXPENSE'
        detail = list(new_expense)[2]
        status = list(new_expense)[7]
        note = 'expense added'
        activity_log_list.extend([activity_id, category, description,
                                  detail, status, note])
        # print(f'activity list: {activity_log_list}')
        self.add_activity_log_to_db(activity_log_list)
        cursor.close()
        return new_expense

    def add_asset_to_db(self, asset_details):
        cursor = self.connection.cursor

        cursor.execute("""
                  INSERT INTO asset
                  (asset_name, type, value, beneficiary, location_acct, status)
                  VALUES (%s, %s, %s, %s, %s, %s)
                  RETURNING asset_id, asset_name, type, value, beneficiary,
                            location_acct, status;
              """, asset_details)

        new_asset = cursor.fetchone()
        # print(new_asset)
        self.connection.commit()

        activity_log_list = []
        activity_id = list(new_asset)[0]
        asset_name = list(new_asset)[1]
        category = 'ASSET'
        detail = list(new_asset)[3]
        status = list(new_asset)[6]
        note = 'asset added'
        activity_log_list.extend([activity_id, category, asset_name,
                                  detail, status, note])
        # print(f'activity list: {activity_log_list}')
        self.add_activity_log_to_db(activity_log_list)
        cursor.close()
        return new_asset

    def add_contact_to_db(self, contact_details):
        cursor = self.connection.cursor

        cursor.execute("""
            INSERT INTO contact
            (contact_name, role, phone, email)
            VALUES (%s, %s, %s, %s)
            RETURNING contact_id, contact_name, role, phone, email;
        """, contact_details)

        new_contact = cursor.fetchone()
        # print(new_contact)
        self.connection.commit()

        activity_log_list = []
        activity_id = list(new_contact)[0]
        contact_name = list(new_contact)[1]
        category = 'CONTACT'
        detail = list(new_contact)[2]
        status = '-'
        note = 'contact added'
        activity_log_list.extend([activity_id, category, contact_name,
                                  detail, status, note])
        # print(f'activity list: {activity_log_list}')
        self.add_activity_log_to_db(activity_log_list)
        cursor.close()
        # print(f'new contact: {new_contact}')
        return new_contact

    def add_note_to_db(self, note_details):
        cursor = self.connection.cursor

        cursor.execute("""
            INSERT INTO note
            (date_added, title, category, content)
            VALUES (%s, %s, %s, %s)
            RETURNING note_id, date_added, title, category, content;
        """, note_details)

        new_note = cursor.fetchone()
        # print(new_note)
        self.connection.commit()

        activity_log_list = []
        activity_id = list(new_note)[0]
        title = list(new_note)[2]
        category = 'NOTE'
        detail = list(new_note)[3]
        status = '-'
        note = 'note added'
        activity_log_list.extend([activity_id, category, title,
                                  detail, status, note])
        # print(f'activity list: {activity_log_list}')
        self.add_activity_log_to_db(activity_log_list)
        cursor.close()
        # print(f'new note: {new_note}')
        return new_note

    def add_settings_to_db(self, settings_details):
        cursor = self.connection.cursor

        cursor.execute("""
               INSERT INTO settings
               (deceased_name, dod, executor, ref)
               VALUES (%s, %s, %s, %s)
               RETURNING settings_id, deceased_name, dod, executor, ref;
           """, settings_details)

        new_settings = cursor.fetchone()
        # print(new_settings)
        self.connection.commit()
        cursor.close()
        # print(f'new settings: {new_settings}')
        return new_settings

    def add_activity_log_to_db(self, item):
        cursor = self.connection.cursor

        cursor.execute("""
                    INSERT INTO activity
                    (activity_id, category, description, detail, status, note)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING activity_id, datetime, category, description, detail,
                              status, note;
                """, list(item))

        self.connection.commit()
        cursor.close()

    def get_activity_log(self):
        cursor = self.connection.cursor
        cursor.execute("SELECT * from activity order by datetime desc;")
        activities = cursor.fetchall()
        # print(activities)
        cursor.close()
        return activities

    def delete_task_by_task_id(self, task_id):
        task = self.get_task_by_id(task_id)
        # print(f'task deleted: {task}')

        cursor = self.connection.cursor  # <-- call the method
        cursor.execute("""
            DELETE FROM task
            WHERE task_id = %s;
        """, (task_id,))  # <-- pass as tuple
        self.connection.commit()

        # update activity log

        activity_log_list = []
        # date = datetime.now().strftime("%b %-d")
        description = task[1]
        status = task[5]
        detail = task[4] + ' Priority'
        activity_log_list.extend([task_id, 'TASK', description, detail, status, 'task deleted'])
        self.add_activity_log_to_db(activity_log_list)

        cursor.close()

    def delete_bill_by_bill_id(self, bill_id):
        bill = self.get_bill_by_id(bill_id)
        # print(f'bill deleted: {bill}')

        cursor = self.connection.cursor  # <-- call the method
        cursor.execute("""
            DELETE FROM bill
            WHERE bill_id = %s;
        """, (bill_id,))  # <-- pass as tuple
        self.connection.commit()

        # update activity log

        activity_log_list = []
        description = bill[1]
        status = bill[5]
        detail = bill[2]  # amount
        activity_log_list.extend([bill_id, 'BILL', description, detail, status, 'bill deleted'])
        self.add_activity_log_to_db(activity_log_list)

        cursor.close()

    def delete_expense_by_expense_id(self, expense_id):
        expense = self.get_expense_by_id(expense_id)
        # print(f'expense deleted: {expense}')

        cursor = self.connection.cursor  # <-- call the method
        cursor.execute("""
               DELETE FROM expense
               WHERE expense_id = %s;
           """, (expense_id,))  # <-- pass as tuple
        self.connection.commit()

        # update activity log

        activity_log_list = []
        description = expense[1]
        status = expense[7]
        detail = expense[2]  # amount
        activity_log_list.extend([expense_id, 'EXPENSE', description, detail, status, 'expense deleted'])
        self.add_activity_log_to_db(activity_log_list)

        cursor.close()

    def delete_asset_by_asset_id(self, asset_id):
        asset = self.get_asset_by_id(asset_id)
        # print(f'asset deleted: {asset}')

        cursor = self.connection.cursor  # <-- call the method
        cursor.execute("""
               DELETE FROM asset
               WHERE asset_id = %s;
           """, (asset_id,))  # <-- pass as tuple
        self.connection.commit()

        # update activity log

        activity_log_list = []
        asset_name = asset[1]
        status = asset[6]
        detail = asset[3]  # value
        activity_log_list.extend([asset_id, 'ASSET', asset_name, detail, status, 'asset deleted'])
        self.add_activity_log_to_db(activity_log_list)

        cursor.close()

    def delete_contact_by_contact_id(self, contact_id):
        contact = self.get_contact_by_id(contact_id)
        # print(f'contact deleted: {contact}')

        cursor = self.connection.cursor  # <-- call the method
        cursor.execute("""
            DELETE FROM contact
            WHERE contact_id = %s;
        """, (contact_id,))  # <-- pass as tuple
        self.connection.commit()

        # update activity log

        activity_log_list = []
        contact_name = contact[1]
        status = '-'
        detail = contact[2]
        activity_log_list.extend([contact_id, 'CONTACT', contact_name, detail, status, 'contact deleted'])
        self.add_activity_log_to_db(activity_log_list)

        cursor.close()

    def delete_note_by_note_id(self, note_id):
        note = self.get_note_by_id(note_id)
        # print(f'note deleted: {note}')

        cursor = self.connection.cursor  # <-- call the method
        cursor.execute("""
            DELETE FROM note
            WHERE note_id = %s;
        """, (note_id,))  # <-- pass as tuple
        self.connection.commit()

        # update activity log

        activity_log_list = []
        title = note[2]
        status = '-'
        detail = note[3]
        activity_log_list.extend([note_id, 'NOTE', title, detail, status, 'note deleted'])
        self.add_activity_log_to_db(activity_log_list)

        cursor.close()

    def update_task_status_by_task_id(self, task_id, task_status, data):
        cursor = self.connection.cursor
        cursor.execute(
            f'Update task '
            f'Set status = %s '
            f'WHERE task_id = %s;',
            (task_status, task_id,)
        )
        self.connection.commit()

        activity_log_list = []
        # date = datetime.now().strftime("%b %-d")
        description = data['description']
        detail = data['priority'] + ' Priority'
        activity_log_list.extend([task_id, 'TASK', description, detail, task_status, 'task status updated'])
        self.add_activity_log_to_db(activity_log_list)

        cursor.close()

    def update_task_row(self, task_id, data):
        description = data['description']
        category = data['category']
        due_date = data['due_date']
        priority = data['priority']
        status = data['status']
        cursor = self.connection.cursor
        cursor.execute("""
                          UPDATE task
                          SET description = %s,
                          category = %s,
                          due_date = %s,
                          priority = %s
                          WHERE task_id = %s;
                          """,
                       (description, category, due_date, priority, task_id))

        self.connection.commit()

        activity_log_list = []
        description = data['description']
        detail = data['priority'] + ' Priority'
        activity_log_list.extend([task_id, 'TASK', description, detail, status, 'task updated'])
        self.add_activity_log_to_db(activity_log_list)

        cursor.close()

    def update_bill_row(self, bill_id, data):
        description = data['description']
        bill_type = data['type']
        due_date = data['due_date']
        amount = data['amount']
        status = data['status']
        cursor = self.connection.cursor
        cursor.execute("""
                          UPDATE bill
                          SET description = %s,
                          type = %s,
                          due_date = %s,
                          amount = %s
                          WHERE bill_id = %s;
                          """,
                       (description, bill_type, due_date, amount, bill_id))

        self.connection.commit()

        activity_log_list = []
        activity_log_list.extend([bill_id, 'BILL', description, amount, status, 'bill updated'])
        self.add_activity_log_to_db(activity_log_list)

        cursor.close()

    def update_bill_status_by_bill_id(self, bill_id, bill_status, data):
        cursor = self.connection.cursor
        cursor.execute(
            f'Update bill '
            f'Set status = %s '
            f'WHERE bill_id = %s;',
            (bill_status, bill_id,)
        )
        self.connection.commit()

        activity_log_list = []
        description = data['description']
        detail = data['detail']
        activity_log_list.extend([bill_id, 'BILL', description, detail, bill_status, 'bill status updated'])
        self.add_activity_log_to_db(activity_log_list)

        cursor.close()

    def update_expense_status_by_expense_id(self, expense_id, expense_status, data):
        cursor = self.connection.cursor
        cursor.execute(
            f'Update expense '
            f'Set status = %s '
            f'WHERE expense_id = %s;',
            (expense_status, expense_id,)
        )
        self.connection.commit()

        activity_log_list = []
        description = data['description']
        detail = data['detail']
        activity_log_list.extend([expense_id, 'EXPENSE', description, detail, expense_status, 'expense status updated'])
        self.add_activity_log_to_db(activity_log_list)

        cursor.close()

    def update_expense_row(self, expense_id, data):
        expense_category = data['category']
        amount = data['amount']
        reimbursable = data['reimbursable']
        notes = data['notes']
        description = data['description']
        status = data['status']
        cursor = self.connection.cursor
        cursor.execute("""
                          UPDATE expense
                          SET category = %s,
                          amount = %s,
                          reimbursable = %s,
                          notes = %s
                          WHERE expense_id = %s;
                          """,
                       (expense_category, amount, reimbursable, notes, expense_id))

        self.connection.commit()

        activity_log_list = []
        activity_log_list.extend([expense_id, 'EXPENSE', description, amount, status, 'expense updated'])
        self.add_activity_log_to_db(activity_log_list)

        cursor.close()

    def update_asset_status_by_asset_id(self, asset_id, asset_status, data):
        cursor = self.connection.cursor
        cursor.execute(
            f'Update asset '
            f'Set status = %s '
            f'WHERE asset_id = %s;',
            (asset_status, asset_id,)
        )
        self.connection.commit()

        activity_log_list = []
        asset_name = data['name']
        detail = data['detail']
        activity_log_list.extend([asset_id, 'ASSET', asset_name, detail, asset_status, 'asset status updated'])
        self.add_activity_log_to_db(activity_log_list)

        cursor.close()

    def update_asset_row(self, asset_id, data):
        asset_type = data['type']
        amount = data['amount']
        beneficiary = data['beneficiary']
        location = data['location']
        name = data['name']
        status = data['status']
        cursor = self.connection.cursor
        cursor.execute("""
                          UPDATE asset
                          SET type = %s,
                          value = %s,
                          beneficiary = %s,
                          location_acct = %s
                          WHERE asset_id = %s;
                          """,
                       (asset_type, amount, beneficiary, location, asset_id))

        self.connection.commit()

        activity_log_list = []
        activity_log_list.extend([asset_id, 'ASSET', name, amount, status, 'asset updated'])
        self.add_activity_log_to_db(activity_log_list)

        cursor.close()

    def get_task_by_description_from_db(self, description):
        cursor = self.connection.cursor
        cursor.execute("""
                   SELECT * FROM task
                   WHERE description = %s;
               """, (description,))  # <-- pass as tuple
        task = cursor.fetchone()
        cursor.close()
        return task

    def update_settings(self, data):
        id = data['id']
        name = data['name']
        dod = data['dod']
        executor = data['executor']
        ref = data['ref']

        cursor = self.connection.cursor  # <-- call the method
        cursor.execute("""
                            UPDATE settings
                            SET deceased_name = %s,
                            dod = %s,
                            executor = %s,
                            ref = %s
                            WHERE settings_id = %s;
                            """,
                       (name, dod, executor, ref, id))
        self.connection.commit()
        cursor.close()

    def get_table_data(self):
        table_dict = dict()
        cursor = self.connection.cursor
        for table in TABLES:
            cursor.execute(f"SELECT * from {table};")
            rows = cursor.fetchall()
            table_dict[table] = rows

        cursor.close()
        # print(f'# of Tables loaded: {len(table_dict.keys())}')
        # print(table_dict)

        return table_dict

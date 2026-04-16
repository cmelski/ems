from dev.db.db_connect import DBConnect
from datetime import datetime

TABLES = ['asset', 'task', 'expense', 'bill', 'contact', 'note', 'settings', 'activity',
          'users', 'estate_users']


class DBClient:

    def __init__(self):
        self.connection = DBConnect()

    def get_user(self, user_id):
        cursor = self.connection.cursor
        cursor.execute("SELECT user_id, first_name, last_name, email, password, role "
                       "FROM users WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()
        return user

    def check_existing_user(self, email):
        cursor = self.connection.cursor
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        return user

    def check_estate_user(self, user_id):
        cursor = self.connection.cursor
        cursor.execute("""
                        SELECT s.*
                        FROM settings s
                        JOIN estate_users eu ON s.settings_id = eu.estate_id
                        WHERE eu.user_id = %s;
                        """, (user_id,))  # <-- pass as tuple
        result = cursor.fetchone()
        return result

    def register_request(self, user_info):
        cursor = self.connection.cursor
        cursor.execute("""
                SELECT setval(
                  pg_get_serial_sequence('register_requests', 'user_id'),
                  (SELECT MAX(user_id) FROM register_requests)
                );
                """)
        self.connection.commit()
        cursor.execute("""
                    INSERT INTO register_requests
                    (first_name, last_name, email, password, completed, date_requested)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING user_id, first_name, last_name, email, password, completed, date_requested;
                """, user_info)

        new_request = cursor.fetchone()
        self.connection.commit()
        return new_request

    def add_user(self, user_info):
        cursor = self.connection.cursor
        cursor.execute("""
                    INSERT INTO users
                    (user_id, first_name, last_name, email, password, role)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING user_id, first_name, last_name, email, password, role;
                """, user_info)

        new_user = cursor.fetchone()
        self.connection.commit()
        return new_user

    def add_user_estate(self, user_id, estate_id):
        cursor = self.connection.cursor
        cursor.execute("""
                    INSERT INTO estate_users
                    (user_id, estate_id)
                    VALUES (%s, %s)
                    RETURNING user_id, estate_id;
                """, (user_id, estate_id))

        self.connection.commit()


    def get_registration_requests_from_db(self):
        cursor = self.connection.cursor
        cursor.execute("""
                    SELECT * FROM register_requests
                    WHERE completed = 'no'
                    ORDER by date_requested DESC;
                    """)
        register_requests = cursor.fetchall()

        return register_requests

    def update_registration_request(self, user_id):
        completed = 'yes'
        cursor = self.connection.cursor
        cursor.execute(
            f'Update register_requests '
            f'Set completed = %s '
            f'WHERE user_id = %s;',
            (completed, user_id,)
        )

        self.connection.commit()


    def get_tasks_from_db(self, estate_id):
        cursor = self.connection.cursor
        cursor.execute("""
                    SELECT * FROM task
                    WHERE estate_id = %s
                    ORDER BY task_id desc;
                    """, (estate_id,))  # <-- pass as tuple
        # cursor.execute("SELECT * from task order by task_id desc;")
        tasks = cursor.fetchall()
        # print(tasks)
        cursor.close()
        return tasks


    def get_bills_from_db(self, estate_id):
        cursor = self.connection.cursor
        cursor.execute("""
                            SELECT * FROM bill
                            WHERE estate_id = %s
                            ORDER BY bill_id desc;
                            """, (estate_id,))  # <-- pass as tuple
        #cursor.execute("SELECT * from bill order by bill_id desc;")
        bills = cursor.fetchall()
        # print(bills)
        cursor.close()
        return bills

    def get_expenses_from_db(self, estate_id):
        cursor = self.connection.cursor
        cursor.execute("""
                            SELECT * FROM expense
                            WHERE estate_id = %s
                            ORDER BY expense_id desc;
                            """, (estate_id,))  # <-- pass as tuple
        #cursor.execute("SELECT * from expense order by expense_id desc;")
        expenses = cursor.fetchall()
        # print(expenses)
        cursor.close()
        return expenses

    def get_assets_from_db(self, estate_id):
        cursor = self.connection.cursor
        cursor.execute("""
                            SELECT * FROM asset
                            WHERE estate_id = %s
                            ORDER BY asset_id desc;
                            """, (estate_id,))  # <-- pass as tuple
        #cursor.execute("SELECT * from asset order by asset_id desc;")
        assets = cursor.fetchall()
        #print(assets)
        cursor.close()
        return assets

    def get_contacts_from_db(self, estate_id):
        cursor = self.connection.cursor
        cursor.execute("""
                            SELECT * FROM contact
                            WHERE estate_id = %s
                            ORDER BY contact_id desc;
                            """, (estate_id,))  # <-- pass as tuple
        #cursor.execute("SELECT * from contact order by contact_id desc;")
        contacts = cursor.fetchall()
        # print(contacts)
        cursor.close()
        return contacts

    def get_notes_from_db(self, estate_id):
        cursor = self.connection.cursor
        cursor.execute("""
                            SELECT * FROM note
                            WHERE estate_id = %s
                            ORDER BY note_id desc;
                            """, (estate_id,))  # <-- pass as tuple
        #cursor.execute("SELECT * from note order by note_id desc;")
        notes = cursor.fetchall()
        # print(notes)
        cursor.close()
        return notes

    def get_settings_from_db(self, estate_id):
        cursor = self.connection.cursor
        cursor.execute("""
                                   SELECT * FROM settings
                                   WHERE settings_id = %s;
                                   """, (estate_id,))  # <-- pass as tuple
        #cursor.execute("SELECT * from settings order by settings_id desc;")
        settings = cursor.fetchone()
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
                SELECT setval(
                  pg_get_serial_sequence('task', 'task_id'),
                  (SELECT MAX(task_id) FROM task)
                );
                """)
        self.connection.commit()

        cursor.execute("""
            INSERT INTO task
            (description, category, due_date, priority, status, estate_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING task_id, description, category, due_date, priority,
                      status, estate_id;
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
        estate_id = list(new_task)[6]
        activity_log_list.extend([activity_id, category, description,
                                  detail, status, note, estate_id])
        # print(f'activity list: {activity_log_list}')
        self.add_activity_log_to_db(activity_log_list)
        cursor.close()
        # print(f'new task: {new_task}')
        return new_task

    def add_bill_to_db(self, bill_details):
        cursor = self.connection.cursor
        cursor.execute("""
        SELECT setval(
          pg_get_serial_sequence('bill', 'bill_id'),
          (SELECT MAX(bill_id) FROM bill)
        );
        """)
        self.connection.commit()

        cursor.execute("""
                  INSERT INTO bill
                  (description, amount, due_date, type, status, estate_id, notes)
                  VALUES (%s, %s, %s, %s, %s, %s, %s)
                  RETURNING bill_id, description, amount, due_date, type,
                            status, estate_id, notes;
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
        estate_id = list(new_bill)[6]
        activity_log_list.extend([activity_id, category, description,
                                  detail, status, note, estate_id])
        # print(f'activity list: {activity_log_list}')
        self.add_activity_log_to_db(activity_log_list)
        cursor.close()
        return new_bill

    def add_expense_to_db(self, expense_details):
        cursor = self.connection.cursor
        cursor.execute("""
                SELECT setval(
                  pg_get_serial_sequence('expense', 'expense_id'),
                  (SELECT MAX(expense_id) FROM expense)
                );
                """)
        self.connection.commit()

        cursor.execute("""
                  INSERT INTO expense
                  (description, amount, date_incurred, category, notes, reimbursable, status, estate_id, receipt_path)
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                  RETURNING expense_id, description, amount, date_incurred, category,
                            notes, reimbursable, status, estate_id, receipt_path;
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
        estate_id = list(new_expense)[8]
        activity_log_list.extend([activity_id, category, description,
                                  detail, status, note, estate_id])
        # print(f'activity list: {activity_log_list}')
        self.add_activity_log_to_db(activity_log_list)
        cursor.close()
        return new_expense

    def add_asset_to_db(self, asset_details):
        cursor = self.connection.cursor
        cursor.execute("""
                SELECT setval(
                  pg_get_serial_sequence('asset', 'asset_id'),
                  (SELECT MAX(asset_id) FROM asset)
                );
                """)
        self.connection.commit()

        cursor.execute("""
                  INSERT INTO asset
                  (asset_name, type, value, beneficiary, location_acct, status, estate_id)
                  VALUES (%s, %s, %s, %s, %s, %s, %s)
                  RETURNING asset_id, asset_name, type, value, beneficiary,
                            location_acct, status, estate_id;
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
        estate_id = list(new_asset)[7]
        activity_log_list.extend([activity_id, category, asset_name,
                                  detail, status, note, estate_id])
        # print(f'activity list: {activity_log_list}')
        self.add_activity_log_to_db(activity_log_list)
        cursor.close()
        return new_asset

    def add_contact_to_db(self, contact_details):
        cursor = self.connection.cursor
        cursor.execute("""
                SELECT setval(
                  pg_get_serial_sequence('contact', 'contact_id'),
                  (SELECT MAX(contact_id) FROM contact)
                );
                """)
        self.connection.commit()

        cursor.execute("""
            INSERT INTO contact
            (contact_name, role, phone, email, estate_id)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING contact_id, contact_name, role, phone, email, estate_id;
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
        estate_id = list(new_contact)[5]
        activity_log_list.extend([activity_id, category, contact_name,
                                  detail, status, note, estate_id])
        # print(f'activity list: {activity_log_list}')
        self.add_activity_log_to_db(activity_log_list)
        cursor.close()
        # print(f'new contact: {new_contact}')
        return new_contact

    def add_note_to_db(self, note_details):
        cursor = self.connection.cursor
        cursor.execute("""
                SELECT setval(
                  pg_get_serial_sequence('note', 'note_id'),
                  (SELECT MAX(note_id) FROM note)
                );
                """)
        self.connection.commit()

        cursor.execute("""
            INSERT INTO note
            (date_added, title, category, content, estate_id)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING note_id, date_added, title, category, content, estate_id;
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
        estate_id = list(new_note)[5]
        activity_log_list.extend([activity_id, category, title,
                                  detail, status, note, estate_id])
        # print(f'activity list: {activity_log_list}')
        self.add_activity_log_to_db(activity_log_list)
        cursor.close()
        # print(f'new note: {new_note}')
        return new_note

    def add_settings_to_db(self, settings_details):
        cursor = self.connection.cursor
        cursor.execute("""
                SELECT setval(
                  pg_get_serial_sequence('settings', 'settings_id'),
                  (SELECT MAX(settings_id) FROM settings)
                );
                """)
        self.connection.commit()

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
                SELECT setval(
                  pg_get_serial_sequence('activity', 'activity_id'),
                  (SELECT MAX(activity_id) FROM activity)
                );
                """)
        self.connection.commit()

        cursor.execute("""
                    INSERT INTO activity
                    (activity_id, category, description, detail, status, note, estate_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING activity_id, datetime, category, description, detail,
                              status, note, estate_id;
                """, list(item))

        self.connection.commit()
        cursor.close()

    def get_activity_log(self, estate_id):
        cursor = self.connection.cursor
        cursor.execute("""
                            SELECT * FROM activity
                            WHERE estate_id = %s
                            ORDER BY datetime desc;
                            """, (estate_id,))  # <-- pass as tuple
        #cursor.execute("SELECT * from activity order by datetime desc;")
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
        estate_id = task[6]
        activity_log_list.extend([task_id, 'TASK', description, detail, status, 'task deleted', estate_id])
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
        estate_id = bill[6]
        activity_log_list.extend([bill_id, 'BILL', description, detail, status, 'bill deleted', estate_id])
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
        estate_id = expense[8]
        activity_log_list.extend([expense_id, 'EXPENSE', description, detail, status, 'expense deleted', estate_id])
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
        estate_id = asset[7]
        activity_log_list.extend([asset_id, 'ASSET', asset_name, detail, status, 'asset deleted', estate_id])
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
        estate_id = contact[5]
        activity_log_list.extend([contact_id, 'CONTACT', contact_name, detail, status, 'contact deleted', estate_id])
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
        estate_id = note[5]
        activity_log_list.extend([note_id, 'NOTE', title, detail, status, 'note deleted', estate_id])
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
        estate_id = data['estate_id']
        activity_log_list.extend([task_id, 'TASK', description, detail, task_status, 'task status updated', estate_id])
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
        estate_id = data['estate_id']
        activity_log_list.extend([task_id, 'TASK', description, detail, status, 'task updated', estate_id])
        self.add_activity_log_to_db(activity_log_list)

        cursor.close()

    def update_bill_row(self, bill_id, data):
        description = data['description']
        bill_type = data['type']
        due_date = data['due_date']
        amount = data['amount']
        status = data['status']
        estate_id = data['estate_id']
        notes = data['notes']
        cursor = self.connection.cursor
        cursor.execute("""
                          UPDATE bill
                          SET description = %s,
                          type = %s,
                          due_date = %s,
                          amount = %s,
                          notes = %s
                          WHERE bill_id = %s;
                          """,
                       (description, bill_type, due_date, amount, notes, bill_id))

        self.connection.commit()

        activity_log_list = []
        activity_log_list.extend([bill_id, 'BILL', description, amount, status, 'bill updated', estate_id])
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
        estate_id = data['estate_id']
        activity_log_list.extend([bill_id, 'BILL', description, detail, bill_status, 'bill status updated', estate_id])
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
        estate_id = data['estate_id']
        activity_log_list.extend([expense_id, 'EXPENSE', description, detail, expense_status, 'expense status updated', estate_id])
        self.add_activity_log_to_db(activity_log_list)

        cursor.close()

    def update_expense_row(self, expense_id, data):
        expense_category = data['category']
        amount = data['amount']
        reimbursable = data['reimbursable']
        notes = data['notes']
        description = data['description']
        status = data['status']
        estate_id = data['estate_id']
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
        activity_log_list.extend([expense_id, 'EXPENSE', description, amount, status, 'expense updated', estate_id])
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
        estate_id = data['estate_id']
        activity_log_list.extend([asset_id, 'ASSET', asset_name, detail, asset_status, 'asset status updated', estate_id])
        self.add_activity_log_to_db(activity_log_list)

        cursor.close()

    def update_asset_row(self, asset_id, data):
        asset_type = data['type']
        amount = data['amount']
        beneficiary = data['beneficiary']
        location = data['location']
        name = data['name']
        status = data['status']
        estate_id = data['estate_id']
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
        activity_log_list.extend([asset_id, 'ASSET', name, amount, status, 'asset updated', estate_id])
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

    def update_receipt(self, expense_id, receipt_path):
        cursor = self.connection.cursor
        cursor.execute(
            "UPDATE expense SET receipt_path = %s WHERE expense_id = %s",
            (receipt_path, expense_id)
        )
        self.connection.commit()

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

    def reset_db(self):
        cursor = self.connection.cursor
        for table in TABLES:
            cursor.execute(f"DELETE from {table};")
            self.connection.commit()
        cursor.close()


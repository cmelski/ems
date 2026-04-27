import os
import psycopg


class DBClient:

    def __init__(self):
        self.connection = psycopg.connect(
            dbname=os.environ.get('DB_NAME'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD'),
            host=os.environ.get('DB_HOST'),
            port=os.environ.get('DB_PORT')
        )

        self.host = os.getenv("DB_HOST")

        if not self.host:
            raise ValueError("DB_HOST is empty. Check your environment variables!")

        self.cursor = self.connection.cursor()

    def commit(self):
        """Commit current transaction"""
        self.connection.commit()

    def close(self):
        """Close cursor and connection"""
        self.cursor.close()
        self.connection.close()

    def clean_db_tables(self, tables):
        cursor = self.cursor

        for table in tables:
            cursor.execute(f"DELETE from {table};")
        self.connection.commit()

    def get_outstanding_tasks(self):
        cursor = self.cursor
        cursor.execute("SELECT * from task where status in ('pending', 'in-progress');")
        outstanding_tasks = cursor.fetchall()
        return outstanding_tasks

    def get_task_by_description(self, description):
        cursor = self.cursor
        cursor.execute("""
                   SELECT * FROM task
                   WHERE description = %s;
               """, (description,))  # <-- pass as tuple
        task = cursor.fetchone()
        print(task)
        return task

    def get_contacts(self):
        cursor = self.cursor
        cursor.execute("""
                           SELECT * FROM contact;
                       """)
        contacts = cursor.fetchall()
        return contacts

    def add_contact(self, contact_details):
        cursor = self.cursor
        # get estate_id
        cursor.execute("""
                    SELECT * FROM settings;
                    """)
        estate_id = cursor.fetchone()[0]
        contact_details.append(estate_id)

        cursor.execute("""
                    INSERT INTO contact
                    (contact_name, role, phone, email, estate_id)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING contact_id, contact_name, role, phone, email, estate_id;
                """, contact_details)

        new_contact = cursor.fetchone()
        self.connection.commit()
        return new_contact

    def get_estate_settings(self):
        cursor = self.cursor
        cursor.execute("""
                              SELECT * FROM settings;
                          """)
        settings = cursor.fetchone()
        return settings

    def add_task_to_db(self, task_details):
        cursor = self.cursor
        cursor.execute("""
                SELECT setval(
                  pg_get_serial_sequence('task', 'task_id'),
                  (SELECT MAX(task_id) FROM task)
                );
                """)
        self.connection.commit()

        cursor.execute("""
            INSERT INTO task
            (description, category, due_date, priority, status, estate_id, assignee)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING task_id, description, category, due_date, priority,
                      status, estate_id, assignee;
        """, task_details)

        new_task = cursor.fetchone()
        self.connection.commit()
        return new_task

    def get_task(self, task_id):
        cursor = self.cursor
        cursor.execute("""
                        SELECT * FROM task
                        WHERE task_id = %s;
                        """, (task_id,))  # <-- pass as tuple
        task = cursor.fetchone()
        return task

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

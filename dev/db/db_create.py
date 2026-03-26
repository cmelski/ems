import os
from pathlib import Path
import psycopg
from dotenv import load_dotenv

file_path = Path(__file__).parent.parent.parent / "test.env"
load_dotenv(file_path)


def create_db():
    try:
        # Connect to the default database (e.g. 'postgres')
        with psycopg.connect(
                host=os.environ.get('DB_HOST'),
                dbname=os.environ.get('DB_NAME_DEFAULT'),
                user=os.environ.get('DB_USER'),
                password=os.environ.get('DB_PASSWORD'),
                port=os.environ.get('DB_PORT')
        ) as conn:
            # Enable autocommit mode
            conn.autocommit = True

            with conn.cursor() as cur:
                db_name = os.environ.get('DB_NAME')
                cur.execute(f"CREATE DATABASE {db_name};")
                print("Database created successfully!")

    except psycopg.Error as e:
        print(f"Duplicate DB: {e}")


def create_table():
    # Connect to your target database
    with psycopg.connect(
            dbname=os.environ.get('DB_NAME'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD'),
            host=os.environ.get('DB_HOST'),
            port=os.environ.get('DB_PORT')
    ) as conn:
        conn.autocommit = True  # Apply changes immediately (no explicit commit needed)

        with conn.cursor() as cur:
            # task table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS task (
                    task_id SERIAL PRIMARY KEY,
                    description VARCHAR(250) NOT NULL,
                    category VARCHAR(30) NOT NULL,
                    due_date VARCHAR(10),
                    priority VARCHAR(20) NOT NULL,
                    status VARCHAR(20) NOT NULL
                );
            """)

            # bill table
            cur.execute("""
                      CREATE TABLE IF NOT EXISTS bill (
                          bill_id SERIAL PRIMARY KEY,
                          description VARCHAR(250) NOT NULL,
                          amount NUMERIC(12,2) NOT NULL,
                          due_date VARCHAR(10),
                          type VARCHAR(50) NOT NULL,
                          status VARCHAR(20) NOT NULL
                      );
                  """)

            # expense table
            cur.execute("""
                                CREATE TABLE IF NOT EXISTS expense (
                                    expense_id SERIAL PRIMARY KEY,
                                    description VARCHAR(250) NOT NULL,
                                    amount NUMERIC(12,2) NOT NULL,
                                    date_incurred VARCHAR(10),
                                    category VARCHAR(50) NOT NULL,
                                    notes VARCHAR(250),
                                    reimbursable VARCHAR(10) NOT NULL,
                                    status VARCHAR(20) NOT NULL
                                );
                            """)

            # expense table
            cur.execute("""
                                CREATE TABLE IF NOT EXISTS asset (
                                    asset_id SERIAL PRIMARY KEY,
                                    asset_name VARCHAR(250) NOT NULL,
                                    type VARCHAR(50) NOT NULL,
                                    value NUMERIC(12,2) NOT NULL,
                                    beneficiary VARCHAR(50),
                                    location_acct VARCHAR(250),
                                    status VARCHAR(20) NOT NULL
                                );
                            """)
            # contact table
            cur.execute("""
                                CREATE TABLE IF NOT EXISTS contact (
                                    contact_id SERIAL PRIMARY KEY,
                                    contact_name VARCHAR(50) NOT NULL,
                                    role VARCHAR(50) NOT NULL,
                                    phone VARCHAR(50) NOT NULL,
                                    email VARCHAR(50)
                                );
                            """)

            # note table
            cur.execute("""
                                CREATE TABLE IF NOT EXISTS note (
                                    note_id SERIAL PRIMARY KEY,
                                    date_added VARCHAR(10),
                                    title VARCHAR(250) NOT NULL,
                                    category VARCHAR(50) NOT NULL,
                                    content VARCHAR(500) NOT NULL
                                );
                            """)


            # settings table
            cur.execute("""
                                CREATE TABLE IF NOT EXISTS settings (
                                    settings_id SERIAL PRIMARY KEY,
                                    deceased_name VARCHAR(50) NOT NULL,
                                    dod VARCHAR(10),
                                    executor VARCHAR(50),
                                    ref VARCHAR(500)
                                );
                            """)

            # activity table
            cur.execute("""
                            CREATE TABLE IF NOT EXISTS activity (
                                activity_id INTEGER,
                                datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                category VARCHAR(100) NOT NULL,
                                description VARCHAR(250) NOT NULL,
                                detail VARCHAR(250) NOT NULL,
                                status VARCHAR(20) NOT NULL,
                                note VARCHAR(50) NOT NULL
                            );
                        """)

        print("✅ Tables created successfully!")

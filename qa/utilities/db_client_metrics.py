import os
import psycopg
from pathlib import Path


class DBClientMetrics:

    def __init__(self):
        self.connection = psycopg.connect(
            dbname=os.environ.get('DB_NAME_METRICS'),
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

    def load_test_cases(self, file_name="test_list.txt", test_type="automated"):
        cur = self.cursor

        project_root = Path(__file__).resolve().parents[2]

        file_path = project_root / file_name

        with open(file_path, "r") as f:
            lines = [line.strip() for line in f if line.strip()]

        rows = []

        for line in lines:
            # full pytest nodeid
            name = line

            # extract area from path
            # qa/tests/api/test_... -> api
            parts = line.split("::")[0].split("/")

            area = "unknown"
            if "tests" in parts:
                idx = parts.index("tests")
                if idx + 1 < len(parts):
                    area = parts[idx + 1]

            rows.append((name, test_type, area))

        cur.executemany("""
                INSERT INTO test_cases (name, type, area)
                VALUES (%s, %s, %s)
                ON CONFLICT (name) DO NOTHING
            """, rows)

        self.commit()
        self.close()
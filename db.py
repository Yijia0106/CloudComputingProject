import sys

import psycopg2

conn_args = {
    'host': 'yj-db.c1p3vanozzul.us-east-1.rds.amazonaws.com',
    'user': 'postgres',
    'password': 'crossjoin',
    'database': 'cloud_computing',
    'port': '5432',
}


class DatabaseOp:
    def __init__(self):
        self.conn = None

    def connect(self):
        try:
            conn = psycopg2.connect(**conn_args)
            self.conn = conn
            return True
        except Exception as e:
            print(e)
            return False

    def get_admin_info(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT * "
                           "FROM admin_data.user_cred_info "
                           "WHERE type = 'a'")
            res = cursor.fetchone()
            print(res)
            return True
        except Exception as e:
            print(e)
            return False

    def insert_into_user_info(self, the_type, email, username, password):
        cursor = self.conn.cursor()
        try:
            query = "INSERT INTO admin_data.user_cred_info (username, email, pwd, type) VALUES (%s, %s, %s, %s);"
            cursor.execute(query, (username, email, password, the_type))
            self.conn.commit()
            return True

        except Exception as e:
            print(e)
            return False

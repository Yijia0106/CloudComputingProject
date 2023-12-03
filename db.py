import logging
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
        self.logger = logging.getLogger()

    def connect(self):
        try:
            conn = psycopg2.connect(**conn_args)
            self.conn = conn
            return True
        except Exception as e:
            self.logger.error(e)
            return False

    def get_admin_info(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT * "
                           "FROM admin_data.user_cred_info "
                           "WHERE type = 'a'")
            res = cursor.fetchone()
            return res
        except Exception as e:
            self.logger.error(e)
            # self.exit_gracefully()

    def insert_into_user_info(self, the_type, email, username, password):
        cursor = self.conn.cursor()
        try:
            query = "INSERT INTO admin_data.user_cred_info (username, email, pwd, type) VALUES ('{}', '{}', '{}', '{}');"
            cursor.execute(query.format(username, email, password, the_type))
            self.conn.commit()
            self.logger.info("A new entry inserted into the admin_data.user_cred_info table")
            return True

        except Exception as e:
            self.logger.error(e)
            # self.exit_gracefully()

    def select_from_user_info_by_email(self, email):
        cursor = self.conn.cursor()
        try:
            query = "SELECT * FROM admin_data.user_cred_info WHERE email = '{}'".format(email)
            cursor.execute(query)
            res = cursor.fetchall()
            return res

        except Exception as e:
            self.logger.error(e)
            # self.exit_gracefully()

    def exit_gracefully(self):
        self.conn.commit()
        self.conn.close()
        self.logger.info("The database connection is closed. System is exiting...")
        sys.exit(0)

    def insert_into_activities(self, user_id, action):
        cursor = self.conn.cursor()
        try:
            query = "INSERT INTO admin_data.activities (user_id, action) VALUES ('{}', '{}');"
            cursor.execute(query.format(user_id, action))
            self.conn.commit()
            self.logger.info("A new entry inserted into the admin_data.activities table")
            return True

        except Exception as e:
            self.logger.error(e)
            # self.exit_gracefully()

    def select_from_user_info(self, where_clause):
        cursor = self.conn.cursor()
        try:
            query = ("SELECT * FROM admin_data.user_cred_info WHERE '{}'".format(where_clause).replace("'", "")
                     .replace("**", "'"))
            cursor.execute(query)
            res = cursor.fetchall()
            return res

        except Exception as e:
            self.logger.error(e)
            # self.exit_gracefully()

    def update_user_status(self, email, change_to):
        cursor = self.conn.cursor()
        try:
            query = "UPDATE admin_data.user_cred_info SET is_blocked = '{}' WHERE email = '{}'"
            cursor.execute(query.format(change_to, email))
            self.conn.commit()
            self.logger.info("A entry got updated in the admin_data.user_cred_info table")
            return True

        except Exception as e:
            self.logger.error(e)
            # self.exit_gracefully()

    def delete_a_user(self, email):
        cursor = self.conn.cursor()
        try:
            query = "DELETE FROM admin_data.user_cred_info WHERE email = '{}'"
            cursor.execute(query.format(email))
            self.conn.commit()
            self.logger.info("A entry got deleted in the admin_data.user_cred_info table")
            return True

        except Exception as e:
            self.logger.error(e)
            # self.exit_gracefully()

    def insert_into_transaction(self, buyer_email, seller_email, product_id, product_name, price, quantity):
        cursor = self.conn.cursor()
        try:
            query = "INSERT INTO admin_data.transactions (buyer_email, seller_email, product_id, product_name, price, quantity) VALUES ('{}', '{}','{}', '{}', '{}', '{}');"
            cursor.execute(query.format(buyer_email, seller_email, product_id, product_name, price, quantity))
            self.conn.commit()
            self.logger.info("A new entry inserted into the admin_data.transactions table")
            return True

        except Exception as e:
            self.logger.error(e)
            # self.exit_gracefully()

    def select_from_user_info_with_pagination(self, where_clause, offset, limit):
        cursor = self.conn.cursor()
        try:
            query = (
                "SELECT * FROM admin_data.user_cred_info WHERE '{}' LIMIT '{}' OFFSET '{}'".format(where_clause, limit,
                                                                                                   offset).replace("'",
                                                                                                                   "")
                .replace("**", "'"))
            cursor.execute(query)
            res = cursor.fetchall()
            return res

        except Exception as e:
            self.logger.error(e)
            # self.exit_gracefully()

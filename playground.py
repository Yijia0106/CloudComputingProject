import db

database_op = db.DatabaseOp()
database_op.connect()

database_op.insert_into_user_info('s', 'yw3936@columbia.edu', 'testseller', '000000')
# database_op.get_admin_info()

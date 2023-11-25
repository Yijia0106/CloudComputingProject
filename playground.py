import db

database_op = db.DatabaseOp()
database_op.connect()

database_op.insert_into_activities('05212f13-f4ad-4932-9ddf-e02e7d3dc96e', 'login')

# database_op.get_admin_info()

# import db
#
# database_op = db.DatabaseOp()
# database_op.connect()
#
# database_op.insert_into_activities('05212f13-f4ad-4932-9ddf-e02e7d3dc96e', 'login')
#
# # database_op.get_admin_info()

import json
import boto3
import datetime
import boto3

s3 = boto3.client('s3')
msg = {'H':'L'}
ts = datetime.datetime.now().timestamp()
bucket_name = "demo-bucket-yijia0106"
file_name = f"/{ts}.json"

json_str = json.dumps(msg)
print(json_str)
s3.put_object(
    Bucket=bucket_name,
    Key=file_name,
    Body=json_str,
)
print(msg)

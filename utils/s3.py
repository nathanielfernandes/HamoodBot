import os
import asyncio
import aiobotocore


try:
    AWS_ACCESS_KEY_ID = os.environ.get("AWSACCESSKEYID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWSSECRETKEY")

except KeyError:
    from dotenv import load_dotenv

    load_dotenv()
    AWS_ACCESS_KEY_ID = os.environ.get("AWSACCESSKEYID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWSSECRETKEY")


class S3:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.session = aiobotocore.get_session()

    async def upload(self, filename: str):
        key = os.path.basename(filename)

        async with self.session.create_client(
            "s3",
            region_name="us-east-2",
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
        ) as client:
            await client.put_object(
                Bucket=self.bucket_name, Key=key, Body=open(filename, "rb")
            )
        return "https://hamoodbucket.s3.us-east-2.amazonaws.com/" + key

    async def delete(self, filename: str):
        key = filename
        async with self.session.create_client(
            "s3",
            region_name="us-east-2",
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
        ) as client:
            await client.delete_object(Bucket=self.bucket_name, Key=key)


# example to manage all objects in bucket
# async def deleteAll():
#     bucket = 'testfoolish'

#     session = aiobotocore.get_session()
#     async with session.create_client('s3', region_name='us-east-1',
#                                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
#                                    aws_access_key_id=AWS_ACCESS_KEY_ID) as client:
#                         x = await client.list_objects(Bucket=bucket)
#                         for y in x['Contents']:
#                             filename = y['Key']
#                             await delete(filename)

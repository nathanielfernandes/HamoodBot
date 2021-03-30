import os, random, requests, json
import boto3
from boto3 import Session
from botocore.exceptions import ClientError
from threading import Thread


def create_presigned_post(
    bucket_name, object_name, fields=None, conditions=None, expiration=3600
):
    """Generate a presigned URL S3 POST request to upload a file

    :param bucket_name: string
    :param object_name: string
    :param fields: Dictionary of prefilled form fields
    :param conditions: List of conditions to include in the policy
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Dictionary with the following keys:
        url: URL to post to
        fields: Dictionary of form fields and values to submit with the POST
    :return: None if error.
    """
    # Generate a presigned S3 POST URL
    s3_client = boto3.client("s3")
    try:
        response = s3_client.generate_presigned_post(
            bucket_name,
            object_name,
            Fields=fields,
            Conditions=conditions,
            ExpiresIn=expiration,
        )
    except ClientError as e:
        return None
    return response


class S3:
    def __init__(self, bucket_name, bot_token):
        self.bucket_name = bucket_name
        self.headers = {
            "Authorization": f"Bot {bot_token}",
            "User-Agent": "Hamood",
            "Content-Type": "application/json",
        }

    def gen_key(self, ext="png"):
        return "".join(random.choice("123456789") for i in range(12)) + "." + ext

    def get_key(self, filepath: str):
        return os.path.basename(filepath)

    def upload_bytes_to_S3(self, file_bytes, key):
        # file_bytes.seek(0)
        files = {"file": (key, file_bytes)}
        response = create_presigned_post(self.bucket_name, key)
        r = requests.post(response["url"], data=response["fields"], files=files)

        return "https://hamoodtempbucket.s3.amazonaws.com/" + key

    def upload_to_S3(self, filepath, key, delete_file):
        response = create_presigned_post(self.bucket_name, key)
        with open(filepath, "rb") as f:
            files = {"file": (key, f)}
            r = requests.post(response["url"], data=response["fields"], files=files)

        if delete_file:
            os.remove(filepath)

        return "https://hamoodtempbucket.s3.amazonaws.com/" + key

    def upload_to_discord_bytes(
        self, file_bytes, ext, channel_id: int, content: str = "", embed: dict = None
    ):
        key = self.gen_key(ext)
        img_url = self.upload_bytes_to_S3(file_bytes, key)
        embed["image"]["url"] = img_url

        msg = json.dumps({"content": content, "embed": embed})

        r = requests.post(
            f"https://discordapp.com/api/channels/{channel_id}/messages",
            headers=self.headers,
            data=msg,
        )

    def upload_to_discord(
        self,
        filepath: str,
        channel_id: int,
        content: str = "",
        embed: dict = None,
        delete_file=True,
    ):
        key = self.get_key(filepath)
        img_url = self.upload_to_S3(filepath, key, delete_file)

        embed["image"]["url"] = img_url

        msg = json.dumps({"content": content, "embed": embed})

        r = requests.post(
            f"https://discordapp.com/api/channels/{channel_id}/messages",
            headers=self.headers,
            data=msg,
        )

    def schedule_upload(
        self,
        filepath: str,
        channel_id: int,
        content: str = "",
        embed: dict = None,
        delete_file=True,
    ):
        p = Thread(
            target=self.upload_to_discord,
            args=(filepath, channel_id, content, embed, delete_file),
        )
        p.start()

    def schedule_upload_bytes(
        self,
        file_bytes: str,
        ext: str,
        channel_id: int,
        content: str = "",
        embed: dict = None,
    ):
        p = Thread(
            target=self.upload_to_discord_bytes,
            args=(file_bytes, ext, channel_id, content, embed),
        )
        p.start()

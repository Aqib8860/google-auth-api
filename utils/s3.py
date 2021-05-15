from boto3 import client, resource

from server.settings import AWS

class S3:
    def __init__(self):
        self.c = client('s3', aws_access_key_id=AWS.ACCESS_KEY,
               aws_secret_access_key=AWS.SECRET_ACCESS_KEY)

    def download_file(self, cloud_file, local_path):
        return self.c.download_file(
            AWS.STORAGE_BUCKET_NAME,
            cloud_file,
            local_path
        )

    def upload_fileobj(self, cloud_file: str, file: object):
        self.c.upload_fileobj(file, AWS.STORAGE_BUCKET_NAME, cloud_file, ExtraArgs={"ACL": AWS.DEFAULT_ACL, })

        return "https://{0}.s3.amazonaws.com/{1}".format(
                    AWS.STORAGE_BUCKET_NAME,
                    cloud_file
                )

    def upload_file(self, cloud_file: str, file_name: str):
        return self.c.upload_file(file_name, AWS.STORAGE_BUCKET_NAME, cloud_file, ExtraArgs={"ACL": "public-read"})

    def get_bucket_url(self):
        return self.c.meta.endpoint_url
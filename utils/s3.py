from boto3 import client, resource
import json
import firebase_admin
from firebase_admin import credentials, db
from server.settings import AWS, FIREBASE

class SNS:
    def __init__(self):
        self.sns_client = client('sns',
                aws_access_key_id = AWS.ACCESS_KEY,
                aws_secret_access_key = AWS.SECRET_ACCESS_KEY,
                region_name = AWS.REGION_NAME,
        )
        self.sns_resource = resource('sns',
                aws_access_key_id = AWS.ACCESS_KEY, 
                aws_secret_access_key = AWS.SECRET_ACCESS_KEY, 
                region_name = AWS.REGION_NAME, 
        )

    def add_token(self, user):

        # Login Firebase, get firebase json file
        if not firebase_admin._apps:
            cred = credentials.Certificate(FIREBASE.CERTIFICATE)

            firebase_admin.initialize_app(cred,{
                'databaseURL': FIREBASE.DATABASE_URL
            })

    
        # Get User Token from firbase

        token = db.reference('/user/'+user+'/token').get()
        
        platform_application = "arn:aws:sns:ap-south-1:151342635097:app/GCM/Cessini"

        # Get All Users of Sns 
        res = self.sns_client.list_endpoints_by_platform_application(
                PlatformApplicationArn=platform_application
        )

        # Check User Already Exist

        user_already_exist = False
        user_arn = ""

        for i in res["Endpoints"]:
            if i["Attributes"]["UserId"]==user:
                user_already_exist = True
                user_arn = i["EndpointArn"]
                break

        # Update User Token
        if user_already_exist is True:
            platform_endpoint = self.sns_resource.PlatformEndpoint(user_arn)
            response = platform_endpoint.set_attributes(
                Attributes={
                    'Token': token,
                    'Enabled': 'True',
                }
            )

        # Add User if not Exist
        else:
            response = self.sns_client.create_platform_endpoint(
                PlatformApplicationArn = platform_application,
                Token = token,
                CustomUserData = user,
                Attributes = {
                    'UserId': user,
                    'Enabled': 'True',
                }
            )
    

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
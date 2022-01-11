import datetime

class DBInfo(object):
    MONGO_USER = "myworld"
    MONGO_PASSWORD = "hgrhtAAeybVuuHCc"

    @staticmethod
    def get_url():
        return f"mongodb+srv://aiworld:i6TO1DZbtBzckOnx@mydb.xci1l.mongodb.net/mydb?retryWrites=true&w=majority"
        #return f"mongodb+srv://{DBInfo.MONGO_USER}:{DBInfo.MONGO_PASSWORD}@cluster0.jzv7p.mongodb.net/myworld?authSource=admin&replicaSet=atlas-39hn0j-shard-0&w=majority&readPreference=primary&appname=MongoDB%20Compass&retryWrites=true&ssl=true"
 
class AWS:
    ACCESS_KEY = 'AKIASGPFZLBMQV5ACHCL'
    SECRET_ACCESS_KEY = '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'
    REGION_NAME = 'ap-south-1'

    # AWS BUCKET
    STORAGE_BUCKET_NAME = 'new-myworld-bucket'
    DEFAULT_ACL = 'public-read'

    # AWS SNS 
    PLATFORM_APPLICATION = "arn:aws:sns:ap-south-1:151342635097:app/GCM/Cessini"

class FIREBASE:
    CERTIFICATE = 'firebase.json'
    DATABASE_URL = 'https://myworld-311307-default-rtdb.asia-southeast1.firebasedatabase.app/'

    
    

class SERVER:
    DEBUG = True

    HOST = "127.0.0.1"
    PORT = 8000

    NUMBER_OF_VIDEOS_TO_SEND = 3
    NUMBER_OF_STORIES_TO_SEND = 3


class SECURITY:
    SECRET_KEY = 'i#%%(nqkzw#3xrkwj8f_#+yl4wz91_=#=u-8j1v-pbho_(r(u7'
    JWT_SECRET_KEY = 'i#%%(nqkzw#3xrkwj8f_#+yl4wz91_=#=u-8j1v-pbho_(r(u7'
    JWT_ACCESS_TOKEN_EXPIRY = datetime.timedelta(days=1)
    JWT_REFRESH_TOKEN_EXPIRY = datetime.timedelta(days=3)

#class FCM:
    #API_KEY="AAAA06zBFVA:APA91bEzn2_SeZTRipMpqImpLc3otatgjRKfxj84W-oWuLCD7R7gYx8PR4PTfSiMjs08ddGvtB2S319QXzNDapVbGJEQNIdZdRc8XA3e6tZzAtcphM7YLuYe_nZgQIy487Xr0pJTC3Vj"


class SOCIAL:
    GOOGLE_CLIENT_ID =  [
        '909136434512-cca9i6u7cjo19l8583l6ho5q6c5h7ccf.apps.googleusercontent.com',  # Android
        '1047620411446-dltsdc36bvb5ui0883m55emk0id55350.apps.googleusercontent.com'  # Web
    ]
    SOCIAL_SECRET = 'E9JOBS3i-JPX2o1wZs-9cQ6F'

    FACEBOOK_APP_ID = '800430383906982'
    FACEBOOK_SECRET = "119276e4178d7754d0abf81d3e946ad5"
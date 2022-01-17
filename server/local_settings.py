import datetime

class DBInfo(object):
    MONGO_USER = ""
    MONGO_PASSWORD = ""

    @staticmethod
    def get_url():
        return f"mongodb+srv://aiworld:i6TO1DZbtBzckOnx@mydb.xci1l.mongodb.net/mydb?retryWrites=true&w=majority"
        #return f"mongodb+srv://{DBInfo.MONGO_USER}:{DBInfo.MONGO_PASSWORD}@cluster0.jzv7p.mongodb.net/myworld?authSource=admin&replicaSet=atlas-39hn0j-shard-0&w=majority&readPreference=primary&appname=MongoDB%20Compass&retryWrites=true&ssl=true"
 
class AWS:
    ACCESS_KEY = ''
    SECRET_ACCESS_KEY = ''
    REGION_NAME = ''

    # AWS BUCKET
    STORAGE_BUCKET_NAME = ''
    DEFAULT_ACL = 'public-read'

    # AWS SNS 
    PLATFORM_APPLICATION = ""

class FIREBASE:
    CERTIFICATE = ''
    DATABASE_URL = ''

    
    

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
        '',  # Android
        ''  # Web
    ]
    SOCIAL_SECRET = ''

    FACEBOOK_APP_ID = ''
    FACEBOOK_SECRET = ""

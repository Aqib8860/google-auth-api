import datetime

class DBInfo(object):
    MONGO_USER = "myworld"
    MONGO_PASSWORD = "hgrhtAAeybVuuHCc"

    @staticmethod
    def get_url():
        return f"mongodb://{DBInfo.MONGO_USER}:{DBInfo.MONGO_PASSWORD}@docdb-2021-08-31-04-49-08.cluster-cnx3ni4ekzmn.ap-south-1.docdb.amazonaws.com:27017/?replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false"
        #return f"mongodb+srv://{DBInfo.MONGO_USER}:{DBInfo.MONGO_PASSWORD}@cluster0.jzv7p.mongodb.net/myworld?authSource=admin&replicaSet=atlas-39hn0j-shard-0&w=majority&readPreference=primary&appname=MongoDB%20Compass&retryWrites=true&ssl=true"

class AWS:
    ACCESS_KEY = 'AKIAWRTFIBNT2IPD7SUN'
    SECRET_ACCESS_KEY = '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'
    STORAGE_BUCKET_NAME = 'myworld-bucket-new'
    DEFAULT_ACL = 'public-read'

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

class FCM:
    API_KEY="AAAA06zBFVA:APA91bEzn2_SeZTRipMpqImpLc3otatgjRKfxj84W-oWuLCD7R7gYx8PR4PTfSiMjs08ddGvtB2S319QXzNDapVbGJEQNIdZdRc8XA3e6tZzAtcphM7YLuYe_nZgQIy487Xr0pJTC3Vj"

class SOCIAL:
    GOOGLE_CLIENT_ID =  [
        '909136434512-cca9i6u7cjo19l8583l6ho5q6c5h7ccf.apps.googleusercontent.com',  # Android
        '1047620411446-dltsdc36bvb5ui0883m55emk0id55350.apps.googleusercontent.com'  # Web
    ]
    SOCIAL_SECRET = 'E9JOBS3i-JPX2o1wZs-9cQ6F'

    FACEBOOK_APP_ID = '800430383906982'
    FACEBOOK_SECRET = "119276e4178d7754d0abf81d3e946ad5"
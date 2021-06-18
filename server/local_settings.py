import datetime

class DBInfo(object):
    MONGO_USER = "myworld"
    MONGO_PASSWORD = "hgrhtAAeybVuuHCc"
    MONGO_DB = "profile"

    @staticmethod
    def get_url():
        return f"mongodb+srv://{DBInfo.MONGO_USER}:{DBInfo.MONGO_PASSWORD}@cluster0.jzv7p.mongodb.net/?retryWrites=true&w=majority"

class AWS:
    ACCESS_KEY = 'AKIAUHZ3VLC5ZPVEAOXI'
    SECRET_ACCESS_KEY = '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'
    STORAGE_BUCKET_NAME = 'myworld2021'
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


class SOCIAL:
    GOOGLE_CLIENT_ID =  [
        '909136434512-cca9i6u7cjo19l8583l6ho5q6c5h7ccf.apps.googleusercontent.com',  # Android
        '1047620411446-dltsdc36bvb5ui0883m55emk0id55350.apps.googleusercontent.com'  # Web
    ]
    SOCIAL_SECRET = 'E9JOBS3i-JPX2o1wZs-9cQ6F'

    FACEBOOK_APP_ID = '800430383906982'
    FACEBOOK_SECRET = "119276e4178d7754d0abf81d3e946ad5"
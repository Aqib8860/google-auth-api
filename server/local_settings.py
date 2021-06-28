import datetime

class DBInfo(object):
    MONGO_USER = "myworld"
    MONGO_PASSWORD = "hgrhtAAeybVuuHCc"

    @staticmethod
    def get_url():
        # return f"mongodb://{DBInfo.MONGO_USER}:{DBInfo.MONGO_PASSWORD}@docdb-2021-06-21-08-18-34.cluster-cmmlvhwuwqnu.ap-south-1.docdb.amazonaws.com:27017/?ssl=true&ssl_ca_certs=rds-combined-ca-bundle.pem&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false"
        return f"mongodb://{DBInfo.MONGO_USER}:{DBInfo.MONGO_PASSWORD}@docdb-2021-06-22-07-54-11.cluster-cmmlvhwuwqnu.ap-south-1.docdb.amazonaws.com:27017/?ssl=true&ssl_ca_certs=rds-combined-ca-bundle.pem&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false"


class AWS:
    ACCESS_KEY = 'AKIARET4LDLNAFC546LY'
    SECRET_ACCESS_KEY = '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'
    STORAGE_BUCKET_NAME = 'myworld-bucket'
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
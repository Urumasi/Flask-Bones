import os


class base_config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')

class test_config(base_config):
    TESTING = True
    WTF_CSRF_ENABLED = False

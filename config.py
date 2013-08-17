import os

CSRF_ENABLED = True
SECRET_KEY = "\xfag}\xedA\xa0\xbd|(\x1b\xec\xaf\xfbx03yx16x00\xd8+x98>\x9f[x05"

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
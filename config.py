import os

CSRF_ENABLED = False
SECRET_KEY = "\xfag}\xedA\xa0\xbd|(\x1b\xec\xaf\xfbx03yx16x00\xd8+x98>\x9f[x05"

RESULTS_PER_PAGE = 4

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:tiger@localhost/wtblog_db'
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
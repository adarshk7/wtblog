import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = "\xfag}\xedA\xa0\xbd|(\x1b\xec\xaf\xfbx03yx16x00\xd8+x98>\x9f[x05"

SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:tiger@localhost/wtblog_db'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
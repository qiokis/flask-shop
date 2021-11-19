from app import db, app
from app.models import User
import config
from flask_login import current_user
from flask import redirect, url_for
from hashlib import md5
import os


def folders_setup():
    folders = ['app\\static', 'app\\static\\images']

    folders.extend([f'{folders[1]}\\category',
                    f'{folders[1]}\\product',
                    f'{folders[1]}\\post'])
    for folder in folders:
        if not os.path.exists(folder):
            os.mkdir(folder)


def check_user_existence(username='', email=''):
    if username:
        u = User.query.filter_by(username=username).first()
        return True if u else False
    elif email:
        u = User.query.filter_by(email=email).first()
        return True if u else False


def allowed_file(filename):
    return '.' in filename and filename.split('.')[-1] in app.config['ALLOWED_EXTENSIONS']


def generate_filename(filename, file_id, addition):
    ext = filename.split('.')[-1]
    filename = md5(f'{file_id}-{filename}'.encode()).hexdigest()
    filename += f'.{ext}'
    return filename, os.path.join(app.config['UPLOAD_FOLDER']+f'\\{addition}', filename)
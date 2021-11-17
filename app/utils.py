from app import db, app
from app.models import User


def check_user_existence(username='', email=''):
    if username:
        u = User.query.filter_by(username=username).first()
        return True if u else False
    elif email:
        u = User.query.filter_by(email=email).first()
        return True if u else False


if __name__ == '__main__':
    test = 'qioki'
    print(check_user_existence(email='qioki@example.com'))
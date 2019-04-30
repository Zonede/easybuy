from functools import wraps

from flask import session, url_for
from werkzeug.utils import redirect

#可以接收多个参数
def is_login(func):
    @wraps(func)
    def check():
        user_id=session.get('user_id')
        if user_id:
            return func()
        else:
            return redirect(url_for('back.login'))


    return check
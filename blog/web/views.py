from flask import Blueprint,render_template

web_blueprint=Blueprint('web',__name__)


@web_blueprint.route('/index/',methods=['GET','POST'])
def index():
    return render_template('web/index.html')
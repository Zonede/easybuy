from flask import Blueprint, render_template, \
    request, redirect, url_for, session

from back.funtion1 import is_login
from back.models import User, db
from werkzeug.security import generate_password_hash,check_password_hash

back_blueprint=Blueprint('back',__name__)

#
# @back_blueprint.route('/register/',methods=['GET','POST'])
# def register():
#     if request.method == 'GET':
#         return render_template('back/register.html')
#     if request.methods=='POST':
#         return redirect(url_for('back.login'))



@back_blueprint.route('/index/',methods=['GET'])
@is_login
def index():
    return render_template('/back/index.html')


@back_blueprint.route('/register/',methods=['GET','POST'])
def register():
    if request.method=='GET':
        return render_template('back/register.html')
    if request.method=='POST':
        username=request.form.get('username')
        password = request.form.get('userpwd')
        password1 = request.form.get('userpwd1')

        print(username,password,password1)
        if username and password :
            #判断账号是否被注册过
            user=User.query.filter(User.username==username).first()
            if user:
                error='该账号已注册,请更换账号'
                return render_template('back/register.html',error=error)
            elif password1==password:
                user=User()
                user.username=username
                user.password=generate_password_hash(password)
                user.save()
                return render_template('back/login.html')
            elif password !=password1:

                return render_template('back/register.html',)

        else:
            error='请填写完整的信息 '
            return render_template('back/register.html',error=error)


#在数据库建立数据
@back_blueprint.route('/create_db/',methods=['get'])
def create_db():
    db.create_all()
    return '创建表成功'



@back_blueprint.route('/login/',methods=['GET','POST'])
def login():
    if request.method =='GET':
        return render_template('back/login.html')

    if request.method =='POST':
        username=request.form.get('username')
        password=request.form.get('password')

        if username and password:
            user=User.query.filter(User.username==username).first()
            if not user:
                error='该账号不存在'
                return render_template('back/login.html',error=error)
            if not check_password_hash(user.password,password):
                error='密码错误,请重新输入'
                return render_template('back/login.html', error=error)
            session['user_id']=user.id
            return redirect(url_for('back.index'))

        else:
            error='请填写完整的信息'
            return render_template('back/login.html',error=error)



@back_blueprint.route('/article',methods=['GET'])
def index_article():
    return render_template('/back/article.html')



# @back_blueprint.route('/index/report',methods=['GET'])
# def index_report():
#     return render_template('/back/report.html')
#
# 退出
# @back_blueprint.route('/logout/', methods=['GET'])
# @is_login
# def logout():
#     del session['user_id']
#     return redirect(url_for('back.login'))




# 文章修改
@back_blueprint.route('/update-article/', methods=['GET', 'POST'])
def update_article():
    if request.method == 'GET':
        return render_template('back/update-article.html')


# 公告
@back_blueprint.route('/notice/', methods=['GET', 'POST'])
def notice():
    if request.method == 'GET':
        return render_template('back/notice.html')


# 评论
@back_blueprint.route('/comment/', methods=['GET', 'POST'])
def comment():
    if request.method == 'GET':
        return render_template('back/comment.html')


# 栏目
@back_blueprint.route('/category/', methods=['GET', 'POST'])
def category():
    if request.method == 'GET':
        return render_template('back/category.html')


# 友情链接
@back_blueprint.route('/flink/', methods=['GET', 'POST'])
def flink():
    if request.method == 'GET':
        return render_template('back/flink.html')


# 访问记录
@back_blueprint.route('/loginlog/', methods=['GET', 'POST'])
def loginlog():
    if request.method == 'GET':
        return render_template('back/loginlog.html')


# 管理用户
@back_blueprint.route('/manage-user/', methods=['GET', 'POST'])
def manage_user():
    if request.method == 'GET':
        return render_template('back/manage-user.html')

# 基本设置
@back_blueprint.route('/setting/', methods=['GET', 'POST'])
def setting():
    if request.method == 'GET':
        return render_template('back/setting.html')


# 用户设置
@back_blueprint.route('/readset/', methods=['GET', 'POST'])
def readset():
    if request.method == 'GET':
        return render_template('back/readset.html')
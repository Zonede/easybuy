import pymysql
from flask import Blueprint, render_template, request, redirect, url_for, session, make_response, Response
from werkzeug.security import generate_password_hash, check_password_hash

from back.functions import is_login
from back.models import User, db, Article, Notice, ArticleType, iPdengLu

back_blue = Blueprint('back', __name__)



@back_blue.route('/index/', methods=['GET'])
@is_login
def index():
    # 获取session，通过id 拿到用户名  渲染到前端页面
    # Article.query.filter_by(id=id).first()
    user_id = session.get('user_id')
    user = User.query.filter(User.id == user_id).first()
    username = user.username  # bug:如果没有注册过这里会报错

    # 读取登陆者 ip
    ip = session.get('user_ip')
    # 登录次数
    num1 = len(iPdengLu.query.filter(iPdengLu.name == username).all())
    # 获取上次登录时间和ip
    if num1 > 1 :
        scip = iPdengLu.query.filter(iPdengLu.name == username).all()[len(iPdengLu.query.filter(iPdengLu.name == username).all())-1]
    else:
        scip = '无记录'

    wz = len(Article.query.all())
    rs = len(User.query.all())
    ylq = str(request.user_agent).split(')')

    return render_template('back/index.html', username=username,
                           ip=ip,ylq=ylq,rs=rs,wz=wz,scip=scip,num1=num1)


# request

# 注册
@back_blue.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('back/register.html')

    if request.method == 'POST':
        # 获取数据
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        if username and password and password2:
            # 是否注册过
            user = User.query.filter(User.username == username).first()
            if user:
                error = '该账户已被注册'
                return render_template('back/register.html', error=error)
            else:
                if password2 == password:
                    user = User()
                    user.username = username
                    user.password = generate_password_hash(password)
                    user.save()
                    return redirect(url_for('back.login'))
                else:
                    error = '两次密码不一致，请重新填写'
                    return render_template('back/register.html', error=error)
        else:
            error = '请填写完整的信息'
            return render_template('back/register.html', error=error)


# 登录

@back_blue.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('back/login.html')

    if request.method == 'POST':
        # 获取数据
        username = request.form.get('username')
        password = request.form.get('password')
        ip = request.form.get('ip')

        if username and password:
            user = User.query.filter(User.username == username).first()
            if not user:
                error = '账号不存在，请先注册'
                return render_template('back/login.html', error=error)
            if not check_password_hash(user.password, password):
                error = '密码错误'
                return render_template('back/login.html', error=error)
            # 登录成功，保存状态，跳转首页
            session['user_id'] = user.id
            session['user_name'] = username
            session['user_ip'] = ip
            # response = Response('')
            # response.set_cookie('%s'%username, '%s'%password,max_age=100)


            # 保存登陆者 ip
            iPdengLu().saveip(ip, username)

            return redirect(url_for('back.index'))
        else:
            error = '请填写完整登录信息'
            return render_template('back/login.html', error=error)


# 退出
@back_blue.route('/logout/', methods=['GET'])
@is_login
def logout():
    del session['user_id']
    return redirect(url_for('back.login'))


# 登录记录
@back_blue.route('/loginlog/', methods=['GET', 'POST'])
def loginlog():
    if request.method == 'GET':
        uip = iPdengLu.query.all()
        lens = len(iPdengLu.query.all())
        return render_template('back/loginlog.html', uip=uip,lens=lens)

# 单行删除
@back_blue.route('/del_loginlogs/<int:id>', methods=['GET', 'POST'])
def del_loginlogs(id):
    if request.method == 'GET':
        u = iPdengLu.query.filter_by(id=id).first()
        db.session.delete(u)
        db.session.commit()
        return redirect(url_for('back.loginlog'))

# 自己
@back_blue.route('/dels_loginlog/', methods=['GET', 'POST'])
def dels_loginlog():
    if request.method == 'GET':
        name = session['username']
        names = iPdengLu.query.filter(iPdengLu.name == name).all()
        lens = len(iPdengLu.query.filter(iPdengLu.name == name).all())
        list1 = []
        for i in range(lens):
            list1.append(names[i].id)
        for i in list1:
            u = iPdengLu.query.filter(iPdengLu.id == i).first()
            db.session.delete(u)
            db.session.commit()
        return redirect(url_for('back.loginlog'))

# 全部删除
@back_blue.route('/dels_loginlogs/', methods=['GET', 'POST'])
def dels_loginlogs():
    if request.method == 'GET':
        lens = len(iPdengLu.query.all())
        names = iPdengLu.query.all()
        list1 = []
        for i in range(lens):
            list1.append(names[i].id)
        for i in list1:
            u = iPdengLu.query.filter(iPdengLu.id == i).first()
            db.session.delete(u)
            db.session.commit()
        return redirect(url_for('back.loginlog'))
        return redirect(url_for('back.loginlog'))


########################【 文章 】##############################

# 文章
@back_blue.route('/active/', methods=['GET', 'POST'])
@is_login
def article():
    if request.method == 'GET':
        articles = Article.query.all()
        wz = len(Article.query.all())
        return render_template('back/article.html', articles=articles, wz=wz)


# 新增文章
@back_blue.route('/add-active/', methods=['GET', 'POST'])
def add_article():
    if request.method == 'GET':
        lanMu = ArticleType.query.all()
        return render_template('back/add-article.html', lanMu=lanMu)
    if request.method == 'POST':
        a = Article()
        Article().saveDB(a)
        return redirect(url_for('back.article'))


# 文章修改
@back_blue.route('/update-article/<int:id>', methods=['GET', 'POST'])
def update_article(id):
    if request.method == 'GET':
        u = Article.query.filter_by(id=id).first()
        lanMu = ArticleType.query.all()
        return render_template('back/update-article.html', u=u, lanMu=lanMu)

    if request.method == 'POST':
        Article().updateDB(id)
        return redirect(url_for('back.article'))


# 删除文章
@back_blue.route('/deldate-article/<int:id>',methods=['GET', 'POST'])
def deldate_article(id):
    if request.method == 'GET':
        u = Article.query.filter_by(id=id).first()
        db.session.delete(u)
        db.session.commit()
        return redirect(url_for('back.article'))

# 删除所选文章
@back_blue.route('/del-article/',methods=['GET', 'POST'])
def del_article():
    if request.method == 'GET':
        return redirect(url_for('back.article'))
    if request.method == 'POST':
        u = dict(request.form)
        k = list(u.values())
        u = k[0]
        for id in u:
            i = Article.query.filter_by(id=id).first()
            print(id,i)
            db.session.delete(i)
            db.session.commit()



        return redirect(url_for('back.article'))






########################【  公告   】###########################

# 公告
@back_blue.route('/notice/', methods=['GET', 'POST'])
@is_login
def notice():
    if request.method == 'GET':
        conn = pymysql.connect(host='127.0.0.1', user='root', password='123456', db='back001', charset='utf8')
        sql = "SELECT * FROM notice"
        cur = conn.cursor()
        cur.execute(sql)
        u = cur.fetchall()
        conn.close()
        gg = len(Notice.query.all())
        return render_template('back/notice.html', u=u, gg=gg)

    # 修改


@back_blue.route('/update-notice/<int:id>', methods=['GET', 'POST'])
def update_notice(id):
    if request.method == 'GET':
        conn = pymysql.connect(host='127.0.0.1', user='root', password='123456', db='back001', charset='utf8')
        sql = "SELECT * FROM notice where id=%d" % id
        cur = conn.cursor()
        cur.execute(sql)
        u = cur.fetchall()
        conn.close()
        print(u)
        return render_template('back/update-notice.html', u=u)
    if request.method == 'POST':
        Notice().update(id)
        return redirect(url_for('back.notice'))


# 新增
@back_blue.route('/add-notice/', methods=['GET', 'POST'])
def add_notice():
    if request.method == 'GET':
        return render_template('back/add-notice.html')
    if request.method == 'POST':
        a = Notice()
        Notice().saveNot(a)
        print(a)
        return redirect(url_for('back.notice'))


# 删除
@back_blue.route('/deldate-notice/<int:id>')
@is_login
def deldate_notice(id):
    u = Notice.query.filter_by(id=id).first()
    db.session.delete(u)
    db.session.commit()
    return redirect(url_for('back.notice'))

#####################【  栏目 】########################
# 分类相关（显示分类列表）  category.html
@back_blue.route('/a_type/', methods=['GET', 'POST'])
@is_login
def a_type():
    if request.method == 'GET':
        # 获取所有分类信息
        types = ArticleType.query.all()
        # 渲染到页面
        return render_template('back/category.html', types=types)


# 添加分类,保存信息，然后跳转回分类页面，分类页面获取所有信息
@back_blue.route('/add-category/', methods=['GET', 'POST'])
def add_category():
    if request.method == 'GET':
        return render_template('back/add-category.html')
    if request.method == 'POST':
        atype = request.form.get('atype')
        if atype:
            # 保存分类信息
            art_type = ArticleType()
            art_type.t_name = atype
            db.session.add(art_type)
            db.session.commit()
            return redirect(url_for('back.a_type'))

        else:
            error = '请填写分类信息'
            return render_template('back/add-category.html')


# 更新
@back_blue.route('/update-category/<int:id>/', methods=['GET', 'POST'])
def update_category(id):
    if request.method == 'GET':
        return render_template('back/update-category.html')
    if request.method == 'POST':
        atype = ArticleType.query.get(id)
        g_name = request.form.get('g_name')
        if g_name:
            atype.t_name = g_name
            atype.save()
            return redirect(url_for('back.a_type'))


# 删除分类
@back_blue.route('/del_type/<int:id>/', methods=['GET', 'POST'])
@is_login
def del_type(id):
    atype = ArticleType.query.get(id)
    db.session.delete(atype)
    db.session.commit()
    return redirect(url_for('back.a_type'))


######################################################
# 友情链接
@back_blue.route('/flink/', methods=['GET', 'POST'])
@is_login
def flink():
    if request.method == 'GET':
        return render_template('back/flink.html')

# 管理用户
@back_blue.route('/manage-user/', methods=['GET', 'POST'])
@is_login
def manage_user():
    if request.method == 'GET':
        return render_template('back/manage-user.html')


# 基本设置
@back_blue.route('/setting/', methods=['GET', 'POST'])
@is_login
def setting():
    if request.method == 'GET':
        return render_template('back/setting.html')


# 用户设置
@back_blue.route('/readset/', methods=['GET', 'POST'])
@is_login
def readset():
    if request.method == 'GET':
        return render_template('back/readset.html')

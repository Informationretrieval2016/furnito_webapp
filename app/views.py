from flask import Flask, render_template, request, session, redirect, url_for, escape
from app import app
from app import db
from models import Comments, Clicks, User
from common import Common
from search import Search
from match import Match
from vsm import VSM
import math

#start view controller
com = Common()
search = Search()
mth = Match()
vsm = VSM()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    username = request.form['username']
    password = request.form['password']
    user_data = User.query.filter_by(username = username).all()
    for user in user_data:
        if username == user.username and password == user.password:
            session['current_user'] = username
            session['age'] = user.age
            session['favoritestyle'] = user.favoritestyle
            session['gender'] = user.gender
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            return render_template('login.html', message = 'login failed, please check your passowrd')
    return render_template('login.html', message = 'login failed, username is invalid')

@app.route('/newuser', methods=['GET', 'POST'])
def newuser():
    password = request.form['password']
    repetpassword = request.form['repetpassword']
    if not password == repetpassword:
        return render_template('register.html', message = 'repet password wrong')
    else:
        username = request.form['username']
        if len(User.query.filter_by(username = username).all()) == 0:
            gender = request.form['gender']
            favoritestyle = request.form['favoritestyle']
            age = request.form['age']
            one_user = User(username, password, age, favoritestyle, gender)
            db.session.add(one_user)
            db.session.commit()
            session['current_user'] = username
            session['age'] = age
            session['favoritestyle'] = favoritestyle
            session['gender'] = gender
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            return render_template('register.html', message = 'username already exist')


@app.route('/result/<int:page>', methods=['GET', 'POST'])
def result(page):
    datas = []
    term_per_page = 15
    session['current_page'] = page
    furniture_list = []
    search_query = ''
    if request.method == 'POST':
        search_query = request.form['srch-term']
        session['search_query'] = search_query
    else:
        search_query = session['search_query']
    furniture_list = search.search_bm25(search_query)
    total_pages = int(math.ceil(float(len(furniture_list)) / term_per_page))
    if total_pages <= 0:
        return render_template('result.html',search_query = search_query,datas = [], total_pages = 1)
    if page < 1:
        return redirect(url_for('result', page=1))
    if page > total_pages:
        return redirect(url_for('result', page=total_pages))
    print total_pages
    lower_limit = (page-1)*term_per_page
    upper_limit = min(page*term_per_page, len(furniture_list))
    for i in range(lower_limit,upper_limit):
        data = com.readJSON(furniture_list[i])
        data['name'] = data['name'].replace('_',' ')
        if len(data['description']) >= 100:
            data['description'] = data['description'][:100] + '...'
        datas.append(data)

    return render_template('result.html', search_query = search_query, datas = datas, total_pages = total_pages)

@app.route('/show', methods=['GET', 'POST'])
def show():
    name = request.args.get('name').replace(' ','_')
    age = None
    favoritestyle = None
    gender = None
    try:
        if escape(session['logged_in']): 
            last_name = request.args.get('last_name').replace(' ','_')
            age = str(escape(session['age']))
            favoritestyle = str(escape(session['favoritestyle']))
            gender = str(escape(session['gender']))
            one_click = Clicks(last_name,name,age,favoritestyle,gender)
            db.session.add(one_click)
            db.session.commit()
        else:
            pass
    except:
        pass
    data = com.getJSONData(name)
    related_data = []
    commentlist = []
    comments = Comments.query.filter_by(furniture_name = name).all()
    for comment in comments:
        commentlist.append(comment.comment)
    related_list = mth.match_furniture(name,age,favoritestyle,gender)
    for related in related_list:
        related_data.append(com.readJSON(related))
    return render_template('show.html', commentlist = commentlist, name = name.replace('_',' '), img_url = data['img_url'][0], description = data['description'], price = data['price'], related_data = related_data)


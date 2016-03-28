from flask import Flask, render_template, request, session, redirect, url_for
from app import app
from models import Comments, Clicks
from common import Common
from search import Search
from match import Match
import math

#start view controller
com = Common()
search = Search()
mth = Match()

@app.route('/')
def index():
    return render_template('index.html')

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
    furniture_list = search.search_hardmatch(search_query)
    total_pages = int(math.ceil(float(len(furniture_list)) / term_per_page))
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
    data = com.getJSONData(name)
    related_data = []
    commentlist = []
    comments = Comments.query.filter_by(furniture_name = name).all()
    for comment in comments:
        commentlist.append(comment.comment)
    related_list = mth.match_test()
    for related in related_list:
        related_data.append(com.readJSON(related))
    return render_template('show.html', commentlist = commentlist, name = name, img_url = data['img_url'][0], description = data['description'], related_data = related_data)


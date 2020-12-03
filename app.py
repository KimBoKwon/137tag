import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from flask import Flask, request, render_template, session, url_for, abort, redirect
import dbdb

app = Flask(__name__)
app.secret_key = "ABCDEFG"

@app.route('/', methods=['GET', 'POST'])
def new():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        baseUrl = "https://www.tagsfinder.com/ko-kr/related/"
        inputUrl = request.form['name']
        url = baseUrl + inputUrl + '/'
        source = requests.get(url).text
        bsObject = BeautifulSoup(source, "html.parser")
        hotKey = bsObject.find_all(attrs={'rel':'nofollow'})
        index = 31
        key1 = []
        for key in hotKey:
            index -= 1
            key1.append(key.text[1:])
            if index <= 0:
                break
        session['cache'] = inputUrl
        return render_template("list.html", data = key1)

@app.route('/list')
def lis():
    baseUrl = "https://www.tagsfinder.com/ko-kr/related/"
    inputUrl = session['cache']
    url = baseUrl + inputUrl + '/'
    source = requests.get(url).text
    bsObject = BeautifulSoup(source, "html.parser")
    hotKey = bsObject.find_all(attrs={'rel':'nofollow'})
    index = 31
    key1 = []
    for key in hotKey:
        index -= 1
        key1.append(key.text[1:])
        if index <= 0:
            break
    return render_template('list.html', data = key1)

@app.route('/wordcloud')
def wordcloud():
    baseUrl = "https://www.tagsfinder.com/ko-kr/related/"
    inputUrl = session['cache']
    url = baseUrl + inputUrl + '/'
    source = requests.get(url).text
    bsObject = BeautifulSoup(source, "html.parser")
    hotKey = bsObject.find_all(attrs={'rel':'nofollow'})
    index = 31
    value1 = ""
    for key in hotKey:
        index -= 1
        value1 += (" " + key.text[1:]) * index
        if index <= 10:
            break
    return render_template("wordcloud.html", data = value1)

@app.route('/bargraph')
def bargraph():
    baseUrl = "https://www.tagsfinder.com/ko-kr/related/"
    inputUrl = session['cache']
    url = baseUrl + inputUrl + '/'
    source = requests.get(url).text
    bsObject = BeautifulSoup(source, "html.parser")
    hotKey = bsObject.find_all(attrs={'rel':'nofollow'})
    index = 31
    index1 = 0
    key1 = []
    for key in hotKey:
        index -= 1
        key1.append(key.text[1:])
        if index <= 20:
            break
    return render_template("bargraph.html", data = key1)

@app.route('/piegraph')
def piegraph():
    baseUrl = "https://www.tagsfinder.com/ko-kr/related/"
    inputUrl = session['cache']
    url = baseUrl + inputUrl + '/'
    source = requests.get(url).text
    bsObject = BeautifulSoup(source, "html.parser")
    hotKey = bsObject.find_all(attrs={'rel':'nofollow'})
    index = 31
    key1 = []
    for key in hotKey:
        index -= 1
        key1.append(key.text[1:])
        if index <= 20:
            break
    return render_template("piegraph.html", data = key1)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        email = request.form['email']
        pw = request.form['password']
        ret = dbdb.select_user(email, pw)
        if ret != None:
            session['user'] = email
            return redirect(url_for('new'))
        else:
            return render_template('index.html')
@app.route('/join', methods=['POST'])
def join():
    email = request.form['email']
    password = request.form['password']
    name = request.form['name']
    print(email)
    print(password)
    print(name)
    ret = dbdb.check_email(email)
    if ret != None:
        # return render_template('errid.html')
        return '아이디있다'
    dbdb.insert_user(email, password, name)
    # return redirect(url_for('login'))
    return redirect(url_for('new'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('new'))

if __name__ == '__main__':
    app.run(debug=True)
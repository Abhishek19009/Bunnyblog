from flask import Flask, render_template, request, redirect, url_for, json, session, jsonify
from datetime import datetime
import sqlite3
import smtplib
import os
import sys
from email.message import EmailMessage


app = Flask(__name__)


@app.route('/')
def home():
  return render_template('home.jinja2')

@app.route('/signin')
def signin():
  return render_template('signin.jinja2')

@app.route('/signindata', methods= ['POST'])
def signinfodata():
    username = request.form.get('username')
    password = request.form.get('password')

    connection = sqlite3.connect('data/userprofiles.db')
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS userprofs(username text, password text, email text)')
    cursor.execute('SELECT * FROM userprofs')
    users = cursor.fetchall()
    connection.close()

    for user in users:
        if username == user[0] and password == user[1]:
            return redirect(url_for('userpage', username= username))
    return render_template('signinerror.jinja2')


@app.route('/forget-password', methods= ['GET', 'POST'])
def forgetpass():
  if request.method == "POST":
      email = request.form.get('resetemail')

      connection = sqlite3.connect('data/userprofiles.db')
      cursor = connection.cursor()
      cursor.execute('CREATE TABLE IF NOT EXISTS userprofs(username text, password text, email text)')
      cursor.execute('SELECT * FROM userprofs')
      users = cursor.fetchall()
      connection.close()

      for user in users:
        if user[2] == email:
            email = EmailMessage()
            content = f'''
            We understand that you have forget your password, but worry not 
            your username along with password is here,

            username =   '{user[0]}'

            password =   '{user[1]}'

            Please understand these data are confidential, so immediately delete 
            this message after reading,

            Thank you for your support............
            '''
            email['From'] = 'heddyrogue@gmail.com'
            email['To'] = user[2]
            email['Subject'] = 'BunnyBlog - Reset mail'
            email.set_content(content)

            smtp_connector = smtplib.SMTP(host='smtp.gmail.com', port=587)

            smtp_connector.starttls()

            smtp_connector.login('heddyrogue@gmail.com', 'abhi.kuriyal')

            smtp_connector.send_message(email)
            smtp_connector.quit()

            executable = 'Message has been sent successfully to your registered email..........'
            break
      else:
          executable = 'This mail is not registered with us, please enter registered email.........'
      return render_template('forgetpassmessage.jinja2', executable= executable)
  return render_template('forgetpass.jinja2')

@app.route('/register')
def register():
  return render_template('register.jinja2')

@app.route('/registerdata', methods= ['POST'])
def registerinfodata():
      username = request.form.get('username')
      password= request.form.get('password')
      email = request.form.get('email')

      if username != None  and password != None and email != None:
        connection = sqlite3.connect('data/userprofiles.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM userprofs')
        allusers = cursor.fetchall()
        for users in allusers:
            if username in users:
                executable = "This username already exists please try another......."
                return render_template('registererror.jinja2', executable= executable)
        else:
            cursor.execute('INSERT INTO userprofs VALUES(?, ?, ?)', (username, password, email))
            connection.commit()
            connection.close()

      return redirect(url_for('userpage', username= username))



@app.route('/<string:username>-blogpage', methods= ['GET'])
def userpage(username):
    #All data of the user is to be extracted here userpage will just display it.
    session['username'] = username
    connection = sqlite3.connect('data/userblogdata.db')
    cursor = connection.cursor()
    username = str(username)
    cursor.execute('CREATE TABLE IF NOT EXISTS "{}"(title text, tags text, content text, date text, id integer)'.replace("{}", username))
    connection.commit()
    cursor.execute('SELECT * FROM "{}"'.replace("{}", username))
    userdata = cursor.fetchall()
    userdata = json.dumps(userdata)
    connection.close()
    return render_template('userpage.jinja2', username=username, userdata=userdata)

@app.route('/blogdata', methods = ['GET', 'POST'])
def blogdata():
    if request.method == 'POST':
        username = session.get('username', 'Hello baby')
        title = request.form.get('blogstitleinput')
        taglist = request.form.getlist('blogstag')
        tags = ",".join(taglist)
        content = request.form.get('blogscontentinput')
        date = datetime.now().strftime('%d-%m-%Y    %H:%M:%S')
        connection = sqlite3.connect('data/userblogdata.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM "{}" ORDER BY id DESC LIMIT 1'.replace("{}", username))
        lastrow = cursor.fetchall()
        print(lastrow)
        if len(lastrow) != 0:
            lastid = lastrow[0][4]
        else:
            lastid = 1
        cursor.execute('INSERT INTO "{}" VALUES(?, ?, ?, ?, ?)'.replace("{}", username), (title, tags, content, date, lastid+1))
        connection.commit()
        connection.close()
        jsondata = json.dumps({'Status': 'OK', 'title': title, 'tags': tags, 'content': content, 'date':date , 'id': lastid, 'username': username})
        return jsondata

@app.route('/myblogs')
def myblogs():
    userbloglist = []
    username = session.get('username')
    connection = sqlite3.connect('data/userblogdata.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM "{}"'.replace("{}", username))
    userdata = cursor.fetchall()
    connection.commit()
    connection.close()
    userdata = reversed(userdata)
    for userblog in userdata:
        userblogdata = {'title':userblog[0], 'tags':userblog[1], 'content':userblog[2], 'date':userblog[3], 'id':userblog[4], 'username': username}
        userbloglist.append(userblogdata)
    return json.dumps(userbloglist)

@app.route('/sharedblogs')
def sharedblogs():
    userbloglist = []
    username = session.get('username')
    connection = sqlite3.connect('data/userblogsharedata.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM "{}"'.replace("{}", username))
    userdata = cursor.fetchall()
    connection.commit()
    connection.close()
    userdata = reversed(userdata)
    for userblog in userdata:
        userblogdata = {'title': userblog[0], 'tags': userblog[1], 'content': userblog[2], 'date': userblog[3],
                        'id': userblog[4], 'username': username}
        userbloglist.append(userblogdata)
    return json.dumps(userbloglist)

@app.route('/allblogs')
def allblogs():
    userbloglist = []
    connection = sqlite3.connect('data/userblogsharedata.db')
    cursor = connection.cursor()
    cursor.execute('SELECT name FROM sqlite_master WHERE type = "table"')
    usernamelist = cursor.fetchall()
    connection.commit()
    for username in usernamelist:
        cursor.execute('SELECT * FROM "{}"'.replace("{}", username[0]))
        userdata = cursor.fetchall()
        for userblog in userdata:
            userblogdata = {'title': userblog[0], 'tags': userblog[1], 'content': userblog[2], 'date': userblog[3],
                            'id': userblog[4], 'username': username}
            userbloglist.append(userblogdata)

    return json.dumps(userbloglist)

@app.route('/shareblog', methods = ['GET','POST'])
def shareblog():
    if request.method == "POST":
        username = session.get('username')
        id = request.get_json()
        id = int(id['id'])
        connection = sqlite3.connect('data/userblogdata.db')
        cursor = connection.cursor()
        cursor.execute(f'SELECT * FROM "username" WHERE id == {id}'.replace("username", username))
        sharedata = cursor.fetchall()
        indata = sharedata[0]
        connection.close()
        connection = sqlite3.connect('data/userblogsharedata.db')
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS "{}"(title text, tags text, content text, date text, id integer)'.replace("{}", username))
        cursor.execute('INSERT INTO "{}" VALUES(?, ?, ?, ?, ?)'.replace("{}", username), (indata[0], indata[1], indata[2], indata[3], indata[4]))
        connection.commit()
        connection.close()
        return json.dumps({'success':True})

@app.route('/deleteblog', methods = ['POST'])
def deleteblog():
    username = session.get('username')
    id = request.get_json()
    id = int(id['id'])
    connection = sqlite3.connect('data/userblogdata.db')
    cursor = connection.cursor()
    cursor.execute(f'DELETE FROM "username" WHERE id == {id}'.replace("username", username))
    connection.commit()
    connection.close()

    connection = sqlite3.connect('data/userblogsharedata.db')
    cursor = connection.cursor()
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS "{}"(title text, tags text, content text, date text, id integer)'.replace("{}",
                                                                                                              username))
    cursor.execute(f'DELETE FROM "username" WHERE id == {id}'.replace("username", username))
    connection.commit()
    connection.close()
    return json.dumps({'success': True})

@app.route('/searchblog', methods = ['POST'])
def searchblog():
    tagstring = ''
    result = request.get_json()
    tags = ['Educational', 'Inspirational', 'Religious', 'Comic', 'Factual', 'News', 'Family', 'Any']

    for tag in tags:
        if result['suggestion'] == '':
            return json.dumps({'result':'Educational,Inspirational,Religious,Comic,Factual,News,Family,Any'})
        elif result['suggestion'] in tag:
            tagstring += tag+','
        elif result['suggestion'] not in tag:
            continue
    if tagstring == '':
        return json.dumps({'result':'No suggestions found....'})
    else:
        return json.dumps({'result': tagstring})

@app.route('/searchresult', methods = ['POST'])
def searchresult():
    jsdata = request.get_json()
    searchstring = jsdata['result']

    userbloglist = []
    connection = sqlite3.connect('data/userblogsharedata.db')
    cursor = connection.cursor()
    cursor.execute('SELECT name FROM sqlite_master WHERE type = "table"')
    usernamelist = cursor.fetchall()
    connection.commit()

    for username in usernamelist:
        cursor.execute(f'SELECT * FROM "username" WHERE tags LIKE "%{searchstring.title()}%"'.replace("username", username[0]))
        userdata = cursor.fetchall()
        userdata = reversed(userdata)
        for userblog in userdata:
            userblogdata = {'title': userblog[0], 'tags': userblog[1], 'content': userblog[2], 'date': userblog[3],
                            'id': userblog[4], 'username': username}
            userbloglist.append(userblogdata)

    return json.dumps(userbloglist)

@app.route('/news')
def newsblock():
  return render_template('news.jinja2', news= news)

@app.route('/blog_of_day')
def blog_of_day():
  return render_template('blog_of_day.jinja2')

@app.route('/instructions')
def instructions():
  return render_template('instructions.jinja2')


@app.route('/help', methods= ['GET', 'POST'])
def help():
    if request.method == 'POST':
        querymail = request.form.get('querymail')
        querycontent = request.form.get('querycontent')
        querytitle = request.form.get('querytitle')

        email = EmailMessage()
        email['From'] = 'heddyrogue@gmail.com'
        email['To'] = 'heddyrogue@gmail.com'
        email['Subject'] = "FEEDBACK & DISCORD MESSAGE"
        content = f'''
        '{querymail}' has given you following mail under '{querytitle}' title:-

        {querycontent}

        '''
        email.set_content(content)

        smtp_connector = smtplib.SMTP(host='smtp.gmail.com', port=587)

        smtp_connector.starttls()

        smtp_connector.login('heddyrogue@gmail.com', 'abhi.kuriyal')

        smtp_connector.send_message(email)
        smtp_connector.quit()

        return render_template('helpinfo.jinja2')

    return render_template('help.jinja2')


@app.route('/contact')
def contact():
  return render_template('contact.jinja2')

@app.route('/privacypolicy')
def privacypolicy():
  return render_template('privacypolicy.jinja2')

@app.route('/termsofservice')
def termsofservice():
  return render_template('termsofservice.jinja2')

@app.route('/about')
def about():
  return render_template('about.jinja2')


if __name__ == "__main__":
    app.run(debug =True)
    app.config['SECRET_KEY'] = "long long secret key"




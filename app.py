from flask import Flask, render_template, session, g, json, request, redirect, url_for, flash
from flaskext.mysql import MySQL
# from werkzeug import generate_password_hash, check_password_hash #Do I need this anymore?


mysql = MySQL()
app = Flask(__name__, static_url_path='/static')
#Don't store the secret key this way (always store in separate)
app.secret_key = 'tobeornottobeasecretkey'


# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'shaun'
app.config['MYSQL_DATABASE_PASSWORD'] = '1234'
app.config['MYSQL_DATABASE_DB'] = 'twitter'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


app.config['UPLOAD_FOLDER'] = 'static/Uploads'


@app.route('/', methods = ['GET'])
def main():
	return render_template('index.html')


#Do I need this anymore?
@app.route('/showUserPage')
def showUserPage():
	#add code here to show blank or existing user page????
	return render_template('user-page.html')


#From Kenso's twitter app
# @app.route("/")
# def server_frontpage():
# 	tweets = model.Tweet.publ()
# 	return render_template("index.html", tweets = tweets)


@app.route('/addPost', methods=['POST'])
def addPost():
	try:
		if session.get('username'):
			# _username = session.get('username')
			_user_id = session.get('user_id')
			_title = request.form['inputTitle']
			_text = request.form['inputDescription']

			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.callproc('sp_addPost',(_user_id, _title, _text))
			data = cursor.fetchall()

			if len(data) is 0:
				conn.commit()
				return redirect('/showUserPage')
			else:
				return render_template('error.html',error = 'An error occurred!')
		else:
			return render_template('error.html',error = 'Unauthorized Access')
	except Exception as e:
		return render_template('error.html',error = str(e))
	else:
		cursor.close()
		conn.close()


@app.route('/getUsername')
def getUsername():
	_username = session.get('username')
	uname = {
		'Username': _username
	}
	uname_dict =[]
	uname_dict.append(uname)
	return json.dumps(uname_dict)


@app.route('/getPostsByUser')
def getPostsByUser():
	try:
		if session.get('user_id'):
			_username = session.get('username')
			_user_id = session.get('user_id')

			con = mysql.connect()
			cursor = con.cursor()
			cursor.callproc('sp_getPostsByUser',(_user_id,))
			posts = cursor.fetchall()

			posts_dict = []
			for post in reversed(posts):
				post_dict = {
					'Id': post[0],
					'Title': post[3],
					'Text': post[4],
					'Date': post[2]
				}
				posts_dict.append(post_dict)

			return json.dumps(posts_dict)
		else:
			return render_template('error.html', error = 'Unauthorized Access')
	except Exception as e:
		return render_template('error.html', error = str(e))


# @app.route('/getpost',methods=['POST'])
# def getpost():
# 	try:
# 		if session.get('user'):
# 			_user = session.get('user')
# 			_limit = pageLimit
# 			_offset = request.form['offset']
# 			_total_records = 0

# 			con = mysql.connect()
# 			cursor = con.cursor()
# 			cursor.callproc('sp_GetpostByUser',(_user,_limit,_offset,_total_records))
# 			postes = cursor.fetchall()
# 			cursor.close()

# 			cursor = con.cursor()
# 			cursor.execute('SELECT @_sp_GetpostByUser_3');
# 			outParam = cursor.fetchall()

# 			response = []
# 			postes_dict = []
# 			for post in postes:
# 			    post_dict = {
# 			            'Id': post[0],
# 			            'Title': post[1],
# 			            'Description': post[2],
# 			            'Date': post[4]}
# 			    postes_dict.append(post_dict)
# 			response.append(postes_dict)
# 			response.append({'total':outParam[0][0]}) 

# 			return json.dumps(response)
# 		else:
# 			return render_template('error.html', error = 'Unauthorized Access')
# 	except Exception as e:
# 		return render_template('error.html', error = str(e))


#This just enters user info into the DB
@app.route('/signUp', methods=['POST','GET'])
def signUp():
	try:
		_username = request.form['inputUsername']

		# validate the received values
		if _username:
			# All Good, let's call MySQL
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.callproc('sp_validateLogin',(_username,))
			data = cursor.fetchall()

			if len(data) > 0:
				session['username'] = _username
				session['user_id'] = data[0][0]
				cursor.close()
				conn.close()
				return redirect('/showUserPage')

			elif len(data) is 0:
				cursor.callproc('sp_createUser',(_username,))
				conn.commit()
				cursor.callproc('sp_validateLogin',(_username,))
				data = cursor.fetchall()
				session['username'] = _username
				session['user_id'] = data[0][0]
				cursor.close()
				conn.close()
				return redirect('/showUserPage')

			else:
				return json.dumps({'error':str(data[0])})
		else:
			return json.dumps({'html':'<span>Enter the required fields</span>'})
	except Exception as e:
		return json.dumps({'error':str(e)})
	else:
		cursor.close()
		conn.close()


if __name__ == "__main__":
	app.run(host = '127.0.0.1', port = 5000)



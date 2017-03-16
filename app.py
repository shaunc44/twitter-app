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


# @app.route('/addPost', methods=['POST'])
# def addPost():
# 	# try:
# 	if session.get('username'):
# 		_title = request.form['inputTitle']
# 		_description = request.form['inputDescription']
# 		_username = session.get('username')
# 		# if request.form.get('filePath') is None:
# 		# 	_filePath = ''
# 		# else:
# 		# 	_filePath = request.form.get('filePath')

# 		conn = mysql.connect()
# 		cursor = conn.cursor()
# 		cursor.callproc('sp_addPost',(_title,_description,_username))
# 		data = cursor.fetchall()

	# 		if len(data) is 0:
	# 			conn.commit()
	# 			# return render_template('user-page.html')
	# 			return redirect('/addPost')
	# 		else:
	# 			return render_template('error.html',error = 'An error occurred!')
	# 	else:
	# 		return render_template('error.html',error = 'Unauthorized Access')
	# except Exception as e:
	# 	return render_template('error.html',error = str(e))
	# else:
	# 	cursor.close()
	# 	conn.close()


@app.route('/addPost', methods=['POST'])
def addPost():
	try:
		if session.get('username'):
			_title = request.form['inputTitle']
			_text = request.form['inputDescription']
			_username = session.get('username')
			_user_id = session.get('user_id')

			conn = mysql.connect()
			cursor = conn.cursor()
			# _user
			cursor.callproc('sp_addPost',(_user_id, _title, _text))
			data = cursor.fetchall()

			if len(data) is 0:
				conn.commit()
				# return render_template('user-page.html')
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
				session['user'] = _username
				session['user_id'] = data[0][0]
				cursor.close()
				conn.close()
				return redirect('/showUserPage')

			elif len(data) is 0:
				cursor.callproc('sp_createUser',(_username,))
				conn.commit()
				cursor.callproc('sp_validateLogin',(_username,))
				data = cursor.fetchall()
				session['user'] = _username
				session['user_id'] = data[0][0]
				cursor.close()
				conn.close()
				return redirect('/showUserPage')
				# user_id = cursor.execute('SELECT user_id FROM users WHERE username = ?;', (_username,))
				# session['user_id'] = user_id
				# session['user_id'] = cursor.lastrowid
			#this is not right
		# elif len(data) is 0:
		# 	conn.commit()
		# 	session['username'] = data[0][0]
		# 	return redirect('/showUserPage')
		# elif len(data) > 0:
		# 	session['username'] = data[0][0]
		# 	return redirect('/showUserPage')
			else:
				return json.dumps({'error':str(data[0])})
		else:
			return json.dumps({'html':'<span>Enter the required fields</span>'})
	except Exception as e:
		return json.dumps({'error':str(e)})
	else:
		cursor.close()
		conn.close()


#WORKING VERSION
#This just enters user info into the DB
# @app.route('/signUp', methods=['POST','GET'])
# def signUp():
# 	try:
# 		_username = request.form['inputUsername']

# 		# validate the received values
# 		if _username:
# 			# All Good, let's call MySQL
# 			conn = mysql.connect()
# 			cursor = conn.cursor()
# 			cursor.callproc('sp_createUser',(_username,))
# 			data = cursor.fetchall()
# 			# print (data)
# 			session['username'] = data[0][0]
# 			# user_id = cursor.execute('SELECT user_id FROM users WHERE username = ?;', (_username,))
# 			session['user_id'] = user_id
# 			# session['user_id'] = cursor.lastrowid

# 			#this is not right
# 			if len(data) is 0:
# 				conn.commit()
# 				return redirect('/showUserPage')
# 			elif len(data) > 0:
# 				return redirect('/showUserPage')
# 			else:
# 				return json.dumps({'error':str(data[0])})
# 		else:
# 			return json.dumps({'html':'<span>Enter the required fields</span>'})
# 	except Exception as e:
# 		return json.dumps({'error':str(e)})
# 	else:
# 		cursor.close()
# 		conn.close()



# MAYBE CREATE A NEW STORED PROCEDURE FOR THIS ????
# 1. Verify username to `users` table of DB
#	a. query `users` table of DB for username
#	b. if username DOES NOT exists
#		i.  add username to DB
#		ii. send user to their blank user page
#	c. username DOES exists
#		i.  retrieve user posts from `posts` table of DB
#		ii. send user to existing user page


#POST signup data to the signup method
# @app.route('/logIn', methods = ['POST'])
# def logIn():

# 	_username = request.form['inputUsername']

# 	conn = mysql.connect()
# 	cursor = conn.cursor()
# 	cursor.callproc('sp_createUser',(_username,))
# 	#maybe change createUser to validateUser???
# 	data = cursor.fetchall()

# 	if len(data) is 0:
# 		conn.commit()
# 		return json.dumps({'message':'User created successfully !'})
# 	elif len(data) > 0:
# 		session['user'] = data[0][0]
# 		return redirect('/showUserPage')
# 		#how to link valid user to `posts` table ???????
# 	else:
# 		return json.dumps({'html':'<span>Enter the required fields</span>'})

# 	cursor.close()
# 	conn.close()


if __name__ == "__main__":
	app.run(host = '127.0.0.1', port = 5000)



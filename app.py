from flask import Flask, render_template, session, g, json, request, redirect, url_for, flash
from flaskext.mysql import MySQL
# from werkzeug import generate_password_hash, check_password_hash #Do I need this anymore?


mysql = MySQL()
app = Flask(__name__, static_url_path='/static')


# MySQL configurations
app.config['MYSQL_DATABASE_USERNAME'] = 'shaunc44'
mysql.init_app(app)

@app.route('/', methods = ['GET'])
def main():
	return render_template('index.html')

#Do I need this anymore?
@app.route('/showUserPage')
def showUserPage():
	#add code here to show blank or existing user page????
	return render_template('user-page.html')


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
@app.route('/logIn', methods = ['POST', 'GET'])
def logIn():
	try:
		_username = request.form['inputUsername']

		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.callproc('sp_createUser',(_username,)) #maybe change createUser to validateUser???
		data = cursor.fetchall()

		if len(data) > 0:
			session['user'] = data[0][0]
			return redirect('/showUserPage')
			#how to link valid user to `posts` table ???????
		else:
			return json.dumps({'html':'<span>Enter the required fields</span>'})
	finally:
		cursor.close()
		conn.close()


		# if _name and _email and _password:
	# 	if _username:
	# 		#Call MySQL
	# 		conn = mysql.connect()
	# 		cursor = conn.cursor()
	# 		cursor.callproc('sp_createUser',(_username,))
	# 		data = cursor.fetchall()

	# 		if len(data) is 0:
	# 			conn.commit()
	# 			return json.dumps({'message':'User created successfully !'})
	# 		else:
	# 			return json.dumps({'error':str(data[0])})
	# 	else:
	# 		return json.dumps({'html':'<span>Enter the required fields</span>'})
	# except Exception as e:
	# 	return json.dumps({'error':str(e)})
	# else:
	# 	cursor.close()
	# 	conn.close()



#POST signup data to the signup method
# @app.route('/logIn', methods = ['POST', 'GET'])
# def logIn():
# 	try:
# 		_username = request.form['inputUsername']

# 		# if _name and _email and _password:
# 		if _username:
# 			#Call MySQL
# 			conn = mysql.connect()
# 			cursor = conn.cursor()
# 			cursor.callproc('sp_createUser',(_username))
# 			data = cursor.fetchall()

# 			if len(data) is 0:
# 				conn.commit()
# 				return json.dumps({'message':'User created successfully !'})
# 			else:
# 				return json.dumps({'error':str(data[0])})
# 		else:
# 			return json.dumps({'html':'<span>Enter the required fields</span>'})
# 	except Exception as e:
# 		return json.dumps({'error':str(e)})
# 	else:
# 		cursor.close()
# 		conn.close()


if __name__ == "__main__":
	app.run(host = '127.0.0.1', port = 5000)



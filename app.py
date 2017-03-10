from flask import Flask, render_template, json, request
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash #Do I need this anymore?


mysql = MySQL()
app = Flask(__name__)


# MySQL configurations
app.config['MYSQL_DATABASE_USERNAME'] = 'shaunc44'
# app.config['MYSQL_DATABASE_PASSWORD'] = '1234'
# app.config['MYSQL_DATABASE_DB'] = 'BucketList'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route("/")
def main():
	return render_template('index.html')


@app.route("/showHomePage")
def showHomePage():
	return render_template('home-page.html')


#POST signup data to the signup method
@app.route("/signUp", methods = ['POST', 'GET'])
def signUp():
	try:
		#read posted values from the UI
		_username = request.form['inputUserName']
		# _email = request.form['inputEmail']
		# _password = request.form['inputPassword']

		# validate the received values
		# if _name and _email and _password:
		if _username:
			#Call MySQL
			conn = mysql.connect()
			cursor = conn.cursor()
			# _hashed_password = generate_password_hash(_password)
			# print (_hashed_password)
			cursor.callproc('sp_createUser2',(_name,_email,_hashed_password))
			# cursor.callproc('sp_createUser2',(_name,_email,_hashed_password))
			data = cursor.fetchall()

			if len(data) is 0:
				conn.commit()
				return json.dumps({'message':'User created successfully !'})
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



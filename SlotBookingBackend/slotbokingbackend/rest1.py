import pymysql
from app import app
from db_config import mysql
from flask import jsonify, request, session
from werkzeug.security import check_password_hash, generate_password_hash
		
@app.route('/')
def home():
	if 'phonenumber' in session:
		phonenumber = session['phonenumber']
		return jsonify({'message' : 'You are already logged in', 'phonenumber' : phonenumber})
	else:
		resp = jsonify({'message' : 'Unauthorized'})
		resp.status_code = 401
		return resp

@app.route('/register' , methods=['POST'])
def register():
    conn = None;
    cursor = None;
    
    try:
        json = request.json
        name = json['name']
        phonenumber = json['phonenumber']
        password = json['password']
		# validate the received values
        if name and phonenumber and password:
            conn = mysql.connect()
            cursor = conn.cursor()
            sql = "SELECT * FROM customer WHERE phonenumber=%s"
            sql_where = (phonenumber,)
            cursor.execute(sql, sql_where)
            row = cursor.fetchone()
            if row:
                resp = jsonify({'message' : 'User already exists'})
                resp.status_code = 409
                return resp
            else:
                hashed_password = generate_password_hash(password)
                sql = "INSERT INTO customer(phonenumber, name, password) VALUES(%s, %s, %s)"
                sql_data = (phonenumber, name, hashed_password)
                cursor.execute(sql, sql_data)
                conn.commit()
                resp = jsonify({'message' : 'User created successfully'})
                resp.status_code = 201
                return resp
        else:
            resp = jsonify({'message' : 'Bad Request - invalid credendtials'})
            resp.status_code = 400
            return resp

    # except Exception as e:
    #     print(e)

    finally:
        if cursor and conn:
            cursor.close()
            conn.close()

@app.route('/login', methods=['POST'])
def login():
	conn = None;
	cursor = None;
	
	try:
		_json = request.json
		_phonenumber = _json['phonenumber']
		_password = _json['password']
		
		# validate the received values
		if _phonenumber and _password:
			#check user exists			
			conn = mysql.connect()
			cursor = conn.cursor()
			
			sql = "SELECT * FROM customer WHERE phonenumber=%s"
			sql_where = (_phonenumber,)
			
			cursor.execute(sql, sql_where)
			row = cursor.fetchone()
			
			if row:
				if check_password_hash(row[2], _password):
					session['phonenumber'] = row[1]
					#cursor.close()
					#conn.close()
					return jsonify({'message' : 'You are logged in successfully'})
				else:
					resp = jsonify({'message' : 'Bad Request - invalid password'})
					resp.status_code = 400
					return resp
		else:
			resp = jsonify({'message' : 'Bad Request - invalid credendtials'})
			resp.status_code = 400
			return resp

	except Exception as e:
		print(e)

	finally:
		if cursor and conn:
			cursor.close()
			conn.close()
		
@app.route('/logout')
def logout():
	if 'phonenumber' in session:
		session.pop('phonenumber', None)
	return jsonify({'message' : 'You successfully logged out'})
		
if __name__ == "__main__":
    app.run(debug=True, port=4000)

# BEGIN: yz18d9bcejpp
from flask import Flask, request, jsonify, session, redirect, url_for
from flask_session import Session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import razorpay

app = Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SECRET_KEY'] = '123#$'

# Initialize Flask-Session
Session(app)

# MySQL database configuration
db_config = {
    'host': 'localhost',
    'user': 'manu',
    'password': '*@Manu2002@*',
    'database': 'parking_reservaton',
    'port': 3300
}

# Create a MySQL connection
db_connection = mysql.connector.connect(**db_config)
cursor = db_connection.cursor()

# Register route
@app.route('/register', methods=['POST'])
def register():
    if 'phonenumber' in session:
        return jsonify({'message': 'Already logged in'}), 400
    data = request.get_json()
    phonenumber = data.get('phonenumber')
    name= data.get('name')
    password = data.get('password')

    if not phonenumber or not password:
        return jsonify({'message': 'Both phonenumber, name and password are required'}), 400

    # Check if the username already exists
    cursor.execute("SELECT * FROM customer WHERE phonenumber = %s", (phonenumber,))
    existing_user = cursor.fetchone()

    if existing_user:
        return jsonify({'message': 'phonenumber already exists'}), 400

    # Hash the password before storing it
    hashed_password = generate_password_hash(password, method='sha256')

    # Insert a new user into the database
    cursor.execute("INSERT INTO customer (phonenumber,name, password) VALUES (%s,%s, %s)", (phonenumber, name,hashed_password))
    db_connection.commit()

    return jsonify({'message': 'User registered successfully'}), 201

# Login route
@app.route('/login', methods=['POST'])
def login():
    if 'phonenumber' in session:
        return jsonify({'message': 'Already logged in'}), 400
    data = request.get_json()
    phonenumber = data.get('phonenumber')
    password = data.get('password')

    if not phonenumber or not password:
        return jsonify({'message': 'Both phonenumber and password are required'}), 400

    # Retrieve the user from the database
    cursor.execute("SELECT * FROM customer WHERE phonenumber = %s", (phonenumber,))
    user = cursor.fetchone()

    if not user or not check_password_hash(user[3], password):  # Assuming password_hash is in the third column
        return jsonify({'message': 'Invalid phonenumber or password'}), 401
    session['phonenumber'] = user[1]

    return jsonify({'message': 'Login successful'}), 200

# Logout route
@app.route('/logout')
def logout():
    if 'phonenumber' in session:
        session.pop('phonenumber')
        return jsonify({'message': 'Logged out successfully'}), 200

    return jsonify({'message': 'Not logged in'}), 400

# Seat selection route
@app.route('/select-seats', methods=['POST'])
def select_seats():
    # if 'phonenumber' not in session:
    #     return jsonify({'message': 'Not logged in'}), 401

    data = request.get_json()
    selected_seats = data.get('selected_seats')
    print(selected_seats)

    if not selected_seats:
        return jsonify({'message': 'No seats selected'}), 400

    # Print the selected seats
    print('Selected seats:', selected_seats)

    # Insert the selected seats into the database
    for seat in selected_seats:
        cursor.execute("INSERT INTO parking_slot (rowI, colI) VALUES (%s, %s)", (seat['rowI'], seat['colI']))
    db_connection.commit()

    return jsonify({'message': 'Seats selected successfully'}), 200

# Get selected seats route
@app.route('/get-selected-seats', methods=['GET'])
def get_selected_seats():
    if 'phonenumber' not in session:
        return jsonify({'message': 'Not logged in'}), 401

    # Retrieve the selected seats from the database
    cursor.execute("SELECT rowI, colI FROM parking_slot")
    selected_seats = cursor.fetchall()

    return jsonify({'selected_seats': selected_seats}), 200

# Razorpay payment gateway configuration
razorpay_client = razorpay.Client(auth=('rzp_test_QU92zSHk7fBUv1', 'kJr2zUSXVLOBgvS43fw77z1C'))

# Razorpay payment success handler
def handle_payment_success(response):
    print('Payment success: {}'.format(response['payment_id']))

# Razorpay payment error handler
def handle_payment_error(response):
    print('Payment error: {}'.format(response['error']['description']))

# Razorpay external wallet handler
def handle_external_wallet(response):
    print('External Wallet: {}'.format(response['wallet']))

# Payment route
@app.route('/pay', methods=['POST'])
def pay():
    if 'phonenumber' not in session:
        return jsonify({'message': 'Not logged in'}), 401

    data = request.get_json()
    amount = data.get('amount')

    if not amount:
        return jsonify({'message': 'Amount not provided'}), 400

    # Create a Razorpay order
    order_amount = amount * 100  # Razorpay accepts amount in paise
    order_currency = '100'
    order_receipt = 'order_rcptid_11'
    notes = {'phonenumber': session['phonenumber']}
    razorpay_order = razorpay_client.order.create(dict(amount=order_amount, currency=order_currency, receipt=order_receipt, notes=notes))

    # Return the Razorpay order ID to the client
    return jsonify({'order_id': razorpay_order['id']}), 200

# Razorpay payment success route
@app.route('/payment-success', methods=['POST'])
def payment_success():
    response = request.get_json()
    handle_payment_success(response)
    return jsonify({'message': 'Payment successful'}), 200

# Razorpay payment error route
@app.route('/payment-error', methods=['POST'])
def payment_error():
    response = request.get_json()
    handle_payment_error(response)
    return jsonify({'message': 'Payment error'}), 400

# Razorpay external wallet route
@app.route('/external-wallet', methods=['POST'])
def external_wallet():
    response = request.get_json()
    handle_external_wallet(response)
    return jsonify({'message': 'External wallet'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=4000)
# END: yz18d9bcejpp

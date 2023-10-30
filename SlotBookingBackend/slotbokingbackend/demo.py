# Import necessary packages and files
from flask import Flask, jsonify, request, render_template
import mysql.connector

# Initialize the Flask app
app = Flask(__name__)

# Connect to the MySQL database
db = mysql.connector.connect(
  host="localhost",
  user="yourusername",
  password="yourpassword",
  database="yourdatabase"
)

# Define the slot selection page route
@app.route('/slot-selection')
def slot_selection():
  # Fetch the available slots from the database
  cursor = db.cursor()
  cursor.execute("SELECT * FROM slots")
  slots = cursor.fetchall()
  # Render the slot selection page with the available slots
  return render_template('slot_selection.html', slots=slots)

# Define the route to handle the AJAX request for slot selection
@app.route('/select-slot', methods=['POST'])
def select_slot():
  # Get the selected slot information from the AJAX request
  slot_id = request.form['slot_id']
  slot_time = request.form['slot_time']
  # Insert the selected slot into the database
  cursor = db.cursor()
  cursor.execute("INSERT INTO selected_slots (slot_id, slot_time) VALUES (%s, %s)", (slot_id, slot_time))
  db.commit()
  # Return a success message
  return jsonify({'message': 'Slot selected successfully'})

# Run the Flask app
if __name__ == '__main__':
  app.run(debug=True)
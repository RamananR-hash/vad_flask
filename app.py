from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from flask_session import Session
import csv
import os
from datetime import datetime
from keras.models import load_model  
from PIL import Image, ImageOps  
import numpy as np
from flask import send_file
from werkzeug.utils import secure_filename
from plant_remidies import remedies
app = Flask(__name__)
np.set_printoptions(suppress=True)
model = load_model("model/Tomato_model.h5", compile=False)
class_names = open("model/labels.txt", "r").readlines()

data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

# Configure Flask-Session to use filesystem-based sessions
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Define the path to 
# the CSV file where user data will be stored.
csv_file_path = "db/user_data.csv"

# Check if the CSV file exists, and create it if it doesn't.
if not os.path.exists(csv_file_path):
    with open(csv_file_path, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(["Full Name", "Email", "Farmer ID", "Password", "Full Address", "Mobile Number", "Adhar Card Number"])

# Configure an "uploads" folder to store uploaded images
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed file extensions for image uploads
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

# Function to check if a filename has an allowed file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function for disease detection (you will need to implement this)
def detect_disease(image_path):
    image = Image.open(image_path).convert("RGB")
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    image_array = np.asarray(image)

    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    data[0] = normalized_image_array

    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    return str(class_name[2:]), confidence_score



@app.route('/')
def index():
    return render_template('index.html')

# ... (your other routes, including signup, login, dashboard, etc.)

@app.route('/signup', methods=['POST'])
def signup():
    full_name = request.form['fullName']
    email = request.form['signupEmail']
    farmer_id = request.form['farmerIdSignup']
    password = request.form['passwordSignup']
    full_address = request.form['fullAddress']
    mobile_number = request.form['mobileNumber']
    adhar_card_number = request.form['adharCardNumber']

    # Append the user data to the CSV file.
    with open(csv_file_path, 'a', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow([full_name, email, farmer_id, password, full_address, mobile_number, adhar_card_number])

    return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    farmer_id = request.form['farmerId']
    password = request.form['password']

    # Check if the provided farmer ID and password match any record in the CSV file.
    with open(csv_file_path, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            if row[2] == farmer_id and row[3] == password:
                # Successful login, set session variable and redirect to dashboard
                session['logged_in'] = True
                session['user_id'] = farmer_id
                return redirect(url_for('dashboard'))

    # If login fails, you can render an error message or redirect back to the login page.
    return render_template("invaliduserpass.html")

@app.route('/dashboard')
def dashboard():
    # Check if the user is logged in
    if session.get('logged_in'):
        user_id = session['user_id']
        
        # Search for the user's full name in the CSV file
        with open(csv_file_path, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip the header row
            for row in csv_reader:
                if row[2] == user_id:
                    user_full_name = row[0]  # Get the full name of the user
                    return render_template('dashboard.html', user_full_name=user_full_name)
        
        # If the user is not found in the CSV, you can handle this case as needed
        return render_template("nodbfound.html")
    else:
        return render_template("nologin.html")

@app.route('/logout')
def logout():
    # Clear the session and redirect to the login page
    session.clear()
    return redirect(url_for('index'))

@app.route('/weather')
def weather():
    # Check if the user is logged in
    if session.get('logged_in'):
        user_id = session['user_id']
        
        # Search for the user's full name in the CSV file
        with open(csv_file_path, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip the header row
            for row in csv_reader:
                if row[2] == user_id:
                    user_full_name = row[0]  # Get the full name of the user
                    return render_template('weather.html', user_full_name=user_full_name)
        
        # If the user is not found in the CSV, you can handle this case as needed
        return render_template("nodbfound.html")
    else:
        return render_template("nologin.html")

@app.route('/select_crop')
def select_crop():
    # Check if the user is logged in
    if session.get('logged_in'):
        user_id = session['user_id']
        
        # Search for the user's full name in the CSV file
        with open(csv_file_path, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip the header row
            for row in csv_reader:
                if row[2] == user_id:
                    user_full_name = row[0]  # Get the full name of the user
                    return render_template('selectcrop.html', user_full_name=user_full_name)
        
        # If the user is not found in the CSV, you can handle this case as needed
        return render_template("nodbfound.html")
    else:
        return render_template("nologin.html")

@app.route('/affected_crop')
def affected_crop():
    # Check if the user is logged in
    if session.get('logged_in'):
        user_id = session['user_id']
        
        # Search for the user's full name in the CSV file
        with open(csv_file_path, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip the header row
            for row in csv_reader:
                if row[2] == user_id:
                    user_full_name = row[0]  # Get the full name of the user
                    return render_template('affectedcrop.html', user_full_name=user_full_name)
        
        # If the user is not found in the CSV, you can handle this case as needed
        return render_template("nodbfound.html")
    else:
        return render_template("nologin.html")
@app.route('/buyers_details')
def buyers_details():
    # Check if the user is logged in
    if session.get('logged_in'):
        user_id = session['user_id']
        
        # Search for the user's full name in the CSV file
        with open(csv_file_path, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip the header row
            for row in csv_reader:
                if row[2] == user_id:
                    user_full_name = row[0]  # Get the full name of the user
                    return render_template('buyers_details.html', user_full_name=user_full_name)
        
        # If the user is not found in the CSV, you can handle this case as needed
        return render_template("nodbfound.html")
    else:
        return render_template("nologin.html")

@app.route('/machine_requirements')
def machine_requirements():
    # Check if the user is logged in
    if session.get('logged_in'):
        user_id = session['user_id']
        
        # Search for the user's full name in the CSV file
        with open(csv_file_path, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip the header row
            for row in csv_reader:
                if row[2] == user_id:
                    user_full_name = row[0]  # Get the full name of the user
                    return render_template('machine_requirements.html', user_full_name=user_full_name)
        
        # If the user is not found in the CSV, you can handle this case as needed
        return render_template("nodbfound.html")
    else:
        return render_template("nologin.html")
@app.route('/soil_info')
def soil_info():
    # Check if the user is logged in
    if session.get('logged_in'):
        user_id = session['user_id']

        # Search for the user's full name in the CSV file
        with open(csv_file_path, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip the header row
            for row in csv_reader:
                if row[2] == user_id:
                    user_full_name = row[0]  # Get the full name of the user

        return render_template('soil_info.html', user_full_name=user_full_name)

    # If the user is not logged in, redirect to the login page
    return redirect(url_for('index'))
@app.route('/tomato_disease_detection', methods=['GET', 'POST'])
def tomato_disease_detection():
 # Check if the user is logged in
    if session.get('logged_in'):
        user_id = session['user_id']
        with open(csv_file_path, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip the header row
            for row in csv_reader:
                if row[2] == user_id:
                    user_full_name = row[0]
        # Handle image upload
        if request.method == 'POST':
            # Check if the post request has the file part
            if 'file' not in request.files:
                return render_template('tomato_disease_detection.html', error='No file part')

            file = request.files['file']

            # Check if the file is submitted without selecting a file
            if file.filename == '':
                return render_template('tomato_disease_detection.html', error='No selected file')

            # Check if the file is allowed
            if file and allowed_file(file.filename):
                # Generate a unique filename based on date and time
                now = datetime.now()
                timestamp = now.strftime("%Y%m%d%H%M%S")
                filename = f"{timestamp}_{secure_filename(file.filename)}"

                # Save the file to the upload folder
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)

                # Perform disease detection
                disease, confidence = detect_disease(file_path)
                disease_remedies = remedies(disease=disease)
                print(disease_remedies)

# Display the result on the HTML page
            return render_template('tomato_disease_detection.html', user_full_name=user_full_name,
                       filename=filename, disease=disease, confidence=confidence, disease_remedies=disease_remedies)
        return render_template('tomato_disease_detection.html', user_full_name=user_full_name)

    # If the user is not logged in, redirect to the login page
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

       
if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0')
    except:
        app.run(debug=True,host='0.0.0.0')
        

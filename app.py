from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory, Response
from twilio.rest import Client
from googlesearch import search
from flask_socketio import SocketIO, emit
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import time
import base64
import smtplib
from flask import send_file
import boto3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import threading
from flask_sqlalchemy import SQLAlchemy
import getpass
# from flask_cors import CORS
import cv2
import numpy as np
from io import BytesIO
from PIL import Image
import io
import os
import pywhatkit
import pyautogui
# import pyttsx3
# import speech_recognition as sr
# import dlib
from werkzeug.utils import secure_filename
from uuid import uuid4 as uuid
import uuid  # Ensure this import is at the top of your file
from dotenv import load_dotenv
import urllib.parse
from werkzeug.utils import secure_filename
from cvzone.HandTrackingModule import HandDetector
from instagrapi import Client as InstaClient
from flask_socketio import SocketIO, emit
from botocore.exceptions import NoCredentialsError, ClientError
from geopy.geocoders import Nominatim

load_dotenv()
app = Flask(__name__)

account_sid = os.getenv('your_sid')
auth_token = os.getenv('your_auth_token')
twilio_number = os.getenv('your_twillio_number')
app.secret_key = 'your_secret_key'

client = Client(account_sid, auth_token)

@app.route('/')
def index():
    return render_template('index.html')

        # ------------------------------call someone-------------
        
# Initialize Background Scheduler
scheduler = BackgroundScheduler()
scheduler.start()

@app.route('/call', methods=['POST'])
def call():
    number = request.form['number']
    from_number = request.form['from_number']
    delay_minutes = request.form.get('delay_minutes', type=int)

    if delay_minutes and delay_minutes > 0:
        delay_time = datetime.now() + timedelta(minutes=delay_minutes)
        scheduler.add_job(make_call, 'date', run_date=delay_time, args=[number, from_number])
        return jsonify(status='success', message=f"Call scheduled successfully in {delay_minutes} minutes!")
    else:
        try:
            call = client.calls.create(
                to=number,
                from_=from_number,
                url='http://demo.twilio.com/docs/voice.xml'  # Replace with your TwiML URL
            )
            return jsonify(status='success', message="Call Success!", call_sid=call.sid)
        except Exception as e:
            return jsonify(status='danger', message=str(e))

def make_call(number, from_number):
    try:
        call = client.calls.create(
            to=number,
            from_=from_number,
            url='http://demo.twilio.com/docs/voice.xml'  # Replace with your TwiML URL
        )
        print(f"Call made successfully, SID: {call.sid}")
    except Exception as e:
        print(f"Error making the call: {str(e)}")      
    #    -----------------SMS---------------- 
app.secret_key = 'your_secret_key'

client = Client("your_sid", "your_auth_toke")

scheduler = BackgroundScheduler()
scheduler.start()

from_number = 'your_twillio_number'

def send_sms(number, message):
    try:
        sent_message = client.messages.create(
            body=message,
            from_=from_number,  
            to=number
        )
        return {'status': 'success', 'sid': sent_message.sid}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

def send_delayed_sms(number, message):
    return send_sms(number, message)

@app.route('/handle_sms', methods=['POST'])
def handle_sms():
    data = request.json
    number = data.get('number')
    message = data.get('message')
    delay_minutes = int(data.get('delay_minutes', 0))

    if not number:
        return jsonify({'status': 'error', 'message': 'Phone number is required.'})
    if not message:
        return jsonify({'status': 'error', 'message': 'Message is required.'})

    if delay_minutes > 0:
        # Schedule the SMS
        delay_time = datetime.now() + timedelta(minutes=delay_minutes)
        scheduler.add_job(send_delayed_sms, 'date', run_date=delay_time, args=[number, message])
        return jsonify({'status': 'success', 'message': f'SMS scheduled successfully in {delay_minutes} minutes!'})
    else:
        # Send SMS immediately
        result = send_sms(number, message)
        return jsonify(result)


# -----------------Google Search----------------

def home():
    return render_template('index.html')

@app.route('/google_search', methods=['POST'])
def google_search_route():
    data = request.get_json()
    query = data.get('query')
    
    if not query:
        return jsonify({'results': []}), 400
    
    try:
        # Perform a Google search and retrieve the top 5 results
        results = [url for url in search(query, num_results=5)]
    except Exception as e:
        print(f"Error during Google search: {e}")
        results = []
    
    return jsonify({'results': results})

# ------------------Search Google Query----------------


@app.route('/search/google', methods=['POST'])
def search_google():
    query = request.form.get('query')
    query = urllib.parse.quote(query)
    return redirect(f'https://www.google.com/search?q={query}')




# -----------------Search Bing Query----------------

@app.route('/search/bing', methods=['POST'])
def search_bing():
    query = request.form.get('query')
    query = urllib.parse.quote(query)
    return redirect(f'https://www.bing.com/search?q={query}')

# --------------------------Ip Camera----------------


# Folder to save captured images
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Function to capture a frame from the IP camera
def capture_frame(ip):
    cap_ip = cv2.VideoCapture(f"http://{ip}/video")
    success, frame = cap_ip.read()
    cap_ip.release()
    if success:
        filename = f"{uuid.uuid4()}.jpg"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        cv2.imwrite(filepath, frame)
        return filename
    return None

# Function to generate frames for video streaming
def generate_frames(ip):
    cap_ip = cv2.VideoCapture(f"http://{ip}/video")
    while True:
        success, frame = cap_ip.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Route to capture a photo
@app.route('/capture_photo', methods=['POST'])
def capture_photo():
    data = request.get_json()
    ip = data.get('ip')
    if ip:
        filename = capture_frame(ip)
        if filename:
            return jsonify(message=f"Photo captured and saved as {filename}")
        else:
            return jsonify(message="Failed to capture photo"), 500
    return jsonify(message="IP address not provided"), 400

# Route for video streaming
@app.route('/video_feed/<ip>')
def video_feed(ip):
    return Response(generate_frames(ip),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Route to serve captured images
@app.route('/image/<filename>')
def get_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)
# -------------Send Email----------------
def send_email_task(smtp_user, smtp_password, from_email, to_email, subject, body):
    try:
        message = MIMEMultipart()
        message['From'] = from_email
        message['To'] = to_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain', 'utf-8'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(from_email, to_email, message.as_string())
        server.quit()
        return {'status': 'success', 'message': 'Email sent successfully!'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

@app.route('/send_email', methods=['POST'])
def send_email():
    data = request.json
    smtp_user = os.getenv('SMTP_USER')
    smtp_password = os.getenv('SMTP_PASSWORD')
    from_email = smtp_user
    to_email = data.get('to_email')
    subject = data.get('subject')
    body = data.get('body')

    response = send_email_task(smtp_user, smtp_password, from_email, to_email, subject, body)
    return jsonify(response)

@app.route('/send_delayed_email', methods=['POST'])
def send_delayed_email():
    data = request.json
    smtp_user = os.getenv('SMTP_USER')
    smtp_password = os.getenv('SMTP_PASSWORD')
    from_email = smtp_user
    to_email = data.get('to_email')
    subject = data.get('subject')
    body = data.get('body')
    delay_seconds = int(data.get('delay_seconds', 0))

    if delay_seconds > 0:
        def delayed_send():
            time.sleep(delay_seconds)
            send_email_task(smtp_user, smtp_password, from_email, to_email, subject, body)
        thread = threading.Thread(target=delayed_send)
        thread.start()
        return jsonify({'status': 'success', 'message': f'Email scheduled successfully in {delay_seconds} seconds!'})
    else:
        response = send_email_task(smtp_user, smtp_password, from_email, to_email, subject, body)
        return jsonify(response)




# ----------------------------------instagram ---------------------------------------
from instagrapi import Client
from PIL import Image
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def index():
    return 'Instagram Post Upload'

@app.route('/insta', methods=['POST'])
def insta():
    # Initialize Instagram client
    cl = Client()
    cl.login("its.ankita25", "rahul1824")

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        filename = secure_filename(file.filename)
        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(photo_path)
        
        caption = request.form.get('caption', '')

        try:
            with Image.open(photo_path) as img:
                img.verify()  # Check if the image is corrupted
            cl.photo_upload(photo_path, caption)
            return jsonify({'success': 'Photo posted successfully!'})
        except (IOError, SyntaxError) as e:
            return jsonify({'error': f'An error occurred while processing the image: {e}'}), 500
        except Exception as e:
            return jsonify({'error': f'An error occurred: {e}'}), 500
      
        # --------------------------------face crop ------------------------------------

UPLOAD_FOLDER = 'uploads/'
OUTPUT_FOLDER = 'static/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Ensure upload and output directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# @app.route('/')
def index():
    return render_template('index.html')

@app.route('/facecrop', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        output_image_path = process_image(file_path)
        return jsonify({'output_image': output_image_path})
    return 'No file uploaded', 400

def process_image(image_path):
    image = cv2.imread(image_path)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) > 0:
        (x, y, w, h) = faces[0]
        cropped_face = image[y:y+h, x:x+w]

        # Optionally resize the cropped face
        resized_face = cv2.resize(cropped_face, (100, 100))

        # Save the cropped face image
        output_image_path = os.path.join(app.config['OUTPUT_FOLDER'], os.path.basename(image_path))
        cv2.imwrite(output_image_path, resized_face)
    else:
        output_image_path = image_path  # If no face detected, return the original image path

    return os.path.basename(output_image_path)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)



# -----------------Filter on image----------------
UPLOAD_FOLDER = 'uploads'
FILTERED_FOLDER = 'filtered'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(FILTERED_FOLDER, exist_ok=True)

def apply_color_filter(image_path, filter_color, output_path):
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Could not load image.")
        return

    filtered_image = image.copy()

    if filter_color.lower() == 'red':
        filtered_image[:, :, 0] = 0
        filtered_image[:, :, 1] = 0
    elif filter_color.lower() == 'green':
        filtered_image[:, :, 0] = 0
        filtered_image[:, :, 2] = 0
    elif filter_color.lower() == 'blue':
        filtered_image[:, :, 1] = 0
        filtered_image[:, :, 2] = 0
    else:
        print("Invalid color filter.")
        return

    cv2.imwrite(output_path, filtered_image)


@app.route('/uploadfilter', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    filter_color = request.form.get('filter_color')

    if file.filename == '':
        return "No selected file", 400

    if file:
        filename = file.filename
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        output_path = os.path.join(FILTERED_FOLDER, filename)
        apply_color_filter(file_path, filter_color, output_path)
        return send_from_directory(FILTERED_FOLDER, filename)

@app.route('/filterImg', methods=['POST'])
def capture_image():
    filter_color = request.form.get('filter_color')

    # Capture image from webcam
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        return "Error capturing image", 500

    filename = 'captured_image.jpg'
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    cv2.imwrite(file_path, frame)
    output_path = os.path.join(FILTERED_FOLDER, filename)
    apply_color_filter(file_path, filter_color, output_path)
    return send_from_directory(FILTERED_FOLDER, filename)




# ------------------------speak---------------------------- 

# engine = pyttsx3.init()

# def speak():
#     return render_template('index.html')


# @app.route('/speak', methods=['POST'])
# def speak():
#     text = request.form['text']
#     if text:
#         try:
#             engine.say(text)
#             engine.runAndWait()
#             return jsonify(success=True)
#         except Exception as e:
#             print(f"Error: {e}")
#             return jsonify(success=False)
#     else:
#         return jsonify(success=False)

# --------------------------sunglass set------------------------- 
# Load the face detection classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Define paths to accessory images
hat_path = 'old-fedora-hat-removebg-preview.png'
sunglasses_path = 'sunglasses.jpg'

def add_accessory(frame, accessory_path, face_rect, scale=1, position_offset=(0, 0)):
    accessory = cv2.imread(accessory_path, cv2.IMREAD_UNCHANGED)
    if accessory is None:
        print("Error: Could not load accessory.")
        return frame

    accessory_width = int(face_rect[2] * scale)
    accessory_height = int(accessory_width * accessory.shape[0] / accessory.shape[1])
    accessory_resized = cv2.resize(accessory, (accessory_width, accessory_height), interpolation=cv2.INTER_LINEAR)

    if accessory_resized.shape[2] == 4:
        alpha_channel = accessory_resized[:, :, 3] / 255.0
        accessory_resized = accessory_resized[:, :, :3]
    else:
        alpha_channel = np.ones(accessory_resized.shape[:2])

    x, y, w, h = face_rect
    y = y - accessory_height // 2 + position_offset[1]
    x = x + w // 2 - accessory_width // 2 + position_offset[0]

    if y < 0 or x < 0 or y + accessory_height > frame.shape[0] or x + accessory_width > frame.shape[1]:
        print("Error: Accessory position out of bounds.")
        return frame

    for c in range(3):
        frame[y:y+accessory_height, x:x+accessory_width, c] = (1 - alpha_channel) * frame[y:y+accessory_height, x:x+accessory_width, c] + alpha_channel * accessory_resized[:, :, c]

    return frame

@app.route('/add_accessory', methods=['POST'])
def add_accessory_route():
    data = request.json
    image_data = data['image'].split(',')[1]
    accessory = data['accessory']

    image = np.frombuffer(base64.b64decode(image_data), dtype=np.uint8)
    frame = cv2.imdecode(image, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    for face_rect in faces:
        if accessory == 'hat':
            frame = add_accessory(frame, hat_path, face_rect, scale=1, position_offset=(0, -face_rect[3] // 4))
        elif accessory == 'sunglasses':
            frame = add_accessory(frame, sunglasses_path, face_rect, scale=1, position_offset=(0, face_rect[3] // 5))

    _, buffer = cv2.imencode('.jpg', frame)
    frame_encoded = base64.b64encode(buffer).decode('utf-8')

    return jsonify({'image': frame_encoded})
# ---------------------------whastsapp message------------------- 

# @app.route('/')

# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  
def what():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():
    number = request.form['number']
    message = request.form['message']

    pywhatkit.sendwhatmsg_instantly(number, message, wait_time=10, tab_close=True, close_time=10)
    time.sleep(10)
    pyautogui.press('enter')

    return 'Message sent!'

# ---------------------------------------custom image-----------------------

@app.route('/CustomImg', methods=['GET', 'POST'])
def image():
    if request.method == 'POST':
        try:
            # Read form data
            width = int(request.form['width'])
            height = int(request.form['height'])
            shape = request.form['shape'].strip().lower()
            start_x = int(request.form['start_x'])
            start_y = int(request.form['start_y'])
            end_x = int(request.form['end_x'])
            end_y = int(request.form['end_y'])
            color_b = int(request.form['color_b'])
            color_g = int(request.form['color_g'])
            color_r = int(request.form['color_r'])

            # Create image
            image = np.zeros((height, width, 3), dtype=np.uint8)
            color = (color_b, color_g, color_r)

            if shape == 'rectangle':
                cv2.rectangle(image, (start_x, start_y), (end_x, end_y), color, -1)
            elif shape == 'line':
                thickness = int(request.form.get('thickness', 1))  # Default to 1 if not provided
                cv2.line(image, (start_x, start_y), (end_x, end_y), color, thickness)
            elif shape == 'circle':
                radius = int(request.form.get('radius', 0))  # Default to 0 if not provided
                cv2.circle(image, (start_x, start_y), radius, color, -1)
            else:
                return render_template('index.html', error="Shape not recognized. Please enter 'rectangle', 'line', or 'circle'.")

            # Convert the image to a format Flask can send
            _, img_encoded = cv2.imencode('.png', image)
            img_io = io.BytesIO(img_encoded.tobytes())
            return send_file(img_io, mimetype='image/png', as_attachment=True, download_name='custom_image.png')
        except ValueError as e:
            return render_template('index.html', error="Invalid input. Please ensure all fields are filled correctly.")
    return render_template('index.html')


# -------------geolocation-------------------

# Initialize the geolocator with a unique user agent
geolocator = Nominatim(user_agent="my_geolocation_app")

# Geolocation route
@app.route('/geolocate', methods=['POST'])
def geolocate():
    data = request.get_json()
    address = data.get('address')

    if not address:
        return jsonify({'error': 'Please provide an address'}), 400

    try:
        location = geolocator.geocode(address)
        if location:
            return jsonify({
                'address': location.address,
                'latitude': location.latitude,
                'longitude': location.longitude
            }), 200
        else:
            return jsonify({'error': 'Location not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)
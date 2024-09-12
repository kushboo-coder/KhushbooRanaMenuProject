import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify, send_file
import numpy as np
import cv2
from PIL import Image, ImageDraw


def send_email(sender_email, sender_password, receiver_email, subject, message):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        return "Email sent successfully!"
    except Exception as e:
        return str(e)
    

from twilio.rest import Client

def send_sms(account_sid, auth_token, from_phone, to_phone, message):
    client = Client(account_sid, auth_token)
    try:
        message = client.messages.create(
            body=message,
            from_=from_phone,
            to=to_phone
        )
        return f"Message sent successfully! SID: {message.sid}"
    except Exception as e:
        return str(e)


import requests
from bs4 import BeautifulSoup

def scrape_google(query):
    url = f"https://www.google.com/search?q={query}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(url, headers=headers)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    results = []
    
    for item in soup.select('div.yuRUbf'):
        title = item.find('h3').get_text()
        link = item.find('a')['href']
        results.append({'title': title, 'link': link})
        if len(results) >= 5:
            break
    
    return results


import geocoder

def get_geo_coordinates():
    g = geocoder.ip('me')
    return {'latitude': g.latlng[0], 'longitude': g.latlng[1], 'location': g.city}


from gtts import gTTS
import os

def text_to_audio(text, language='en'):
    tts = gTTS(text=text, lang=language)
    filename = "output.mp3"
    tts.save(filename)
    return filename


from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume

def set_volume(volume_level):
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        volume.SetMasterVolume(volume_level, None)
    return f"Volume set to {volume_level * 100}%"


from twilio.rest import Client

def send_sms_via_mobile(account_sid, auth_token, from_phone, to_phone, message):
    client = Client(account_sid, auth_token)
    try:
        message = client.messages.create(
            body=message,
            from_=from_phone,
            to=to_phone
        )
        return f"Message sent successfully via mobile! SID: {message.sid}"
    except Exception as e:
        return str(e)


def send_bulk_email(sender_email, sender_password, recipient_list, subject, message):
    for receiver_email in recipient_list:
        result = send_email(sender_email, sender_password, receiver_email, subject, message)
        print(f"Sending email to {receiver_email}: {result}")
    return "Bulk email sending completed!"





from flask import Flask, request, jsonify
from your_functions_module import send_email, send_sms, scrape_google, get_geo_coordinates, text_to_audio, set_volume, send_sms_via_mobile, send_bulk_email

app = Flask(__name__)

@app.route('/send_email', methods=['POST'])
def send_email_route():
    data = request.json
    result = send_email(data['sender_email'], data['sender_password'], data['receiver_email'], data['subject'], data['message'])
    return jsonify({"message": result})

@app.route('/send_sms', methods=['POST'])
def send_sms_route():
    data = request.json
    result = send_sms(data['account_sid'], data['auth_token'], data['from_phone'], data['to_phone'], data['message'])
    return jsonify({"message": result})

@app.route('/scrape_google', methods=['POST'])
def scrape_google_route():
    query = request.json['query']
    results = scrape_google(query)
    return jsonify(results)

@app.route('/get_geo', methods=['GET'])
def get_geo_route():
    result = get_geo_coordinates()
    return jsonify(result)

@app.route('/text_to_audio', methods=['POST'])
def text_to_audio_route():
    text = request.json['text']
    filename = text_to_audio(text)
    return jsonify({"file": filename})

@app.route('/set_volume', methods=['POST'])
def set_volume_route():
    volume_level = request.json['volume_level']
    result = set_volume(volume_level)
    return jsonify({"message": result})

@app.route('/send_sms_via_mobile', methods=['POST'])
def send_sms_via_mobile_route():
    data = request.json
    result = send_sms_via_mobile(data['account_sid'], data['auth_token'], data['from_phone'], data['to_phone'], data['message'])
    return jsonify({"message": result})

@app.route('/send_bulk_email', methods=['POST'])
def send_bulk_email_route():
    data = request.json
    recipient_list = data['recipient_list']
    result = send_bulk_email(data['sender_email'], data['sender_password'], recipient_list, data['subject'], data['message'])
    return jsonify({"message": result})

app = Flask(__name__)

# Endpoint for automated data processing
@app.route('/data_processing', methods=['POST'])
def data_processing():
    dataset_url = request.json.get('dataset_url')
    # Here you'd download and process the dataset from the given URL
    # For simplicity, we'll just return a success message
    return jsonify({"message": "Dataset processed successfully!"})

# Endpoint for model integration with web app
@app.route('/model_integration', methods=['POST'])
def model_integration():
    model_type = request.json.get('model_type')
    web_app_url = request.json.get('web_app_url')
    # Here you'd integrate the model with the web app
    # For simplicity, we'll just return a success message
    return jsonify({"message": f"Model '{model_type}' integrated with web app at {web_app_url}!"})

# Endpoint for face detection and cropping
@app.route('/face_detection', methods=['POST'])
def face_detection():
    file = request.files['image']
    image = np.array(Image.open(file))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
        face = image[y:y+h, x:x+w]
    
    if faces == ():
        return jsonify({"message": "No face detected."})
    
    face_image = Image.fromarray(face)
    face_image.save('cropped_face.jpg')

    return send_file('cropped_face.jpg', mimetype='image/jpeg')

# Endpoint for applying image filters
@app.route('/apply_filters', methods=['POST'])
def apply_filters():
    file = request.files['image']
    filter_type = request.form.get('filter_type')
    image = np.array(Image.open(file))

    if filter_type == 'gray':
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif filter_type == 'blur':
        image = cv2.GaussianBlur(image, (15, 15), 0)
    else:
        return jsonify({"message": "Filter type not recognized."})

    filtered_image = Image.fromarray(image)
    filtered_image.save('filtered_image.jpg')

    return send_file('filtered_image.jpg', mimetype='image/jpeg')

# Endpoint for custom image generation with numpy
@app.route('/generate_image', methods=['POST'])
def generate_image():
    dimensions = request.json.get('dimensions')
    try:
        dims = tuple(map(int, dimensions.split(',')))
        if len(dims) == 3:
            array = np.random.rand(*dims) * 255
            image = Image.fromarray(array.astype('uint8')).convert('RGB')
            image.save('custom_image.jpg')
            return send_file('custom_image.jpg', mimetype='image/jpeg')
        else:
            return jsonify({"message": "Invalid dimensions, should be in format: height,width,channels"})
    except Exception as e:
        return jsonify({"message": str(e)})

# Endpoint for applying fun image filters
@app.route('/apply_fun_filters', methods=['POST'])
def apply_fun_filters():
    file = request.files['image']
    image = Image.open(file)
    draw = ImageDraw.Draw(image)

    # Example filter: Adding sunglasses to the face (for simplicity, we'll just draw black rectangles)
    draw.rectangle([100, 100, 200, 150], fill="black")

    image.save('fun_filtered_image.jpg')
    return send_file('fun_filtered_image.jpg', mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)

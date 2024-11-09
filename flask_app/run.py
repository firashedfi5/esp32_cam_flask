from flask import Flask, request
import numpy as np
import cv2
import os
from multiprocessing import Value

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'sdfhj43uop23opjuhjg234jghds8'

# Initialize counter variable
counter = Value('i', 0)

# Directory to save images
img_dir = 'C:\\Users\\firas\\OneDrive\\Desktop\\Projet_Tutore_3eme\\Code\\esp32_cam_flask\\flask_app\\esp32_imgs'
if not os.path.isdir(img_dir):
    os.mkdir(img_dir)

# Function to save the image
def save_img(img):
    with counter.get_lock():
        counter.value += 1
        count = counter.value
    cv2.imwrite(os.path.join(img_dir, f"img_{count}.jpg"), img)

# Route for index
@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    return "ESP32-CAM Flask Server", 200

# Route for image upload
@app.route('/upload', methods=['POST'])
def upload():
    if 'imageFile' in request.files:
        file = request.files['imageFile']
        # Convert string of image data to uint8
        nparr = np.frombuffer(file.read(), np.uint8)
        # Decode image
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        save_img(img)
        return "[SUCCESS] Image Received", 201
    else:
        return "[FAILED] Image Not Received", 204

# Run the server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

import os
from flask import Blueprint, render_template, request, send_file
from PIL import Image
import pillow_heif

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']

    if uploaded_file and uploaded_file.filename.lower().endswith('.heic'):
        try:
            pillow_heif.register_heif_opener()
            image = Image.open(uploaded_file.stream)

            original_filename = os.path.splitext(uploaded_file.filename)[0]
            output_filename = f"{original_filename}_converted.jpg"
            output_path = os.path.join(os.path.dirname(__file__), output_filename)
            image.save(output_path, "JPEG")

            return send_file(output_path, as_attachment=True)
        except Exception as e:
            print(f"{e}")
            return render_template('index.html', error="Failed to convert the file. Please try again.")
    else:
        return render_template('index.html', error="Invalid file format. Please try again.")
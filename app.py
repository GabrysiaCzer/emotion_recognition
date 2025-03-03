from flask import Flask, request, render_template, jsonify
import os
from werkzeug.utils import secure_filename
import siec_2  # Importowanie sieci z pliku siec_2.py

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'Brak pliku w żądaniu'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Nie wybrano pliku'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Przetwarzanie pliku za pomocą siec_2.py
    result = siec_2.process_audio(filepath)

    return jsonify({'output': result})


if __name__ == '__main__':
    app.run(debug=True)

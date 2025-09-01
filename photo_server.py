#!/usr/bin/env python3
"""
Simple photo upload server for Tortoise Care Touch
Allows phones to upload tortoise photos via web interface
"""

import os
import threading
from flask import Flask, request, render_template_string, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from database.db_manager import DatabaseManager

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Photo storage directory
PHOTOS_DIR = os.path.join(os.path.dirname(__file__), 'photos')
os.makedirs(PHOTOS_DIR, exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# HTML template for upload interface
UPLOAD_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Tortoise Care - Photo Upload</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .header {
            text-align: center;
            color: #2E7D32;
            margin-bottom: 30px;
        }
        .tortoise-card {
            background: white;
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .tortoise-name {
            font-size: 18px;
            font-weight: bold;
            color: #2E7D32;
            margin-bottom: 5px;
        }
        .tortoise-info {
            font-size: 14px;
            color: #666;
            margin-bottom: 15px;
        }
        .upload-form {
            margin-top: 10px;
        }
        .file-input {
            width: 100%;
            padding: 10px;
            margin: 5px 0;
            border: 2px solid #ddd;
            border-radius: 5px;
            background: white;
        }
        .upload-btn {
            background-color: #4CAF50;
            color: white;
            padding: 12px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            width: 100%;
        }
        .upload-btn:hover {
            background-color: #45a049;
        }
        .current-photo {
            max-width: 150px;
            border-radius: 5px;
            margin: 10px 0;
        }
        .success {
            background-color: #d4edda;
            color: #155724;
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
        }
        .error {
            background-color: #f8d7da;
            color: #721c24;
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🐢 Tortoise Care Photo Upload</h1>
        <p>Select a tortoise to upload a photo</p>
    </div>
    
    {% if message %}
        <div class="{{ 'success' if success else 'error' }}">{{ message }}</div>
    {% endif %}
    
    {% for tortoise in tortoises %}
        <div class="tortoise-card">
            <div class="tortoise-name">{{ tortoise.name }}</div>
            <div class="tortoise-info">
                {{ tortoise.species }}
                {% if tortoise.subspecies and tortoise.subspecies != 'Unknown' %} - {{ tortoise.subspecies }}{% endif %}
                {% if tortoise.sex and tortoise.sex != 'Unknown' %} | {{ tortoise.sex }}{% endif %}
            </div>
            
            {% if tortoise.photo_path %}
                <img src="/photo/{{ tortoise.photo_path.split('/')[-1] }}" class="current-photo" alt="Current photo">
            {% endif %}
            
            <form method="post" enctype="multipart/form-data" class="upload-form">
                <input type="hidden" name="tortoise_id" value="{{ tortoise.id }}">
                <input type="file" name="photo" accept="image/*" capture="camera" class="file-input" required>
                <button type="submit" class="upload-btn">Upload Photo for {{ tortoise.name }}</button>
            </form>
        </div>
    {% endfor %}
    
    {% if not tortoises %}
        <div class="tortoise-card">
            <p>No tortoises found. Please add tortoises in the main application first.</p>
        </div>
    {% endif %}
</body>
</html>
"""

@app.route('/')
def upload_page():
    """Main upload page showing all tortoises"""
    db = DatabaseManager()
    try:
        tortoises = db.get_all_tortoises()
        message = request.args.get('message')
        success = request.args.get('success') == 'true'
        return render_template_string(UPLOAD_TEMPLATE, 
                                    tortoises=tortoises, 
                                    message=message, 
                                    success=success)
    finally:
        db.close()

@app.route('/', methods=['POST'])
def upload_photo():
    """Handle photo upload"""
    if 'photo' not in request.files:
        return redirect(url_for('upload_page', message='No file selected', success='false'))
    
    file = request.files['photo']
    tortoise_id = request.form.get('tortoise_id')
    
    if file.filename == '':
        return redirect(url_for('upload_page', message='No file selected', success='false'))
    
    if not tortoise_id:
        return redirect(url_for('upload_page', message='No tortoise selected', success='false'))
    
    if file and allowed_file(file.filename):
        # Create secure filename
        original_filename = secure_filename(file.filename)
        filename = f"tortoise_{tortoise_id}_{original_filename}"
        filepath = os.path.join(PHOTOS_DIR, filename)
        
        try:
            # Save the file
            file.save(filepath)
            
            # Update database with photo path
            db = DatabaseManager()
            try:
                db.update_tortoise_photo(int(tortoise_id), filepath)
                tortoise = db.get_tortoise_by_id(int(tortoise_id))
                tortoise_name = tortoise['name'] if tortoise else 'Unknown'
                return redirect(url_for('upload_page', 
                               message=f'Photo uploaded successfully for {tortoise_name}!', 
                               success='true'))
            finally:
                db.close()
                
        except Exception as e:
            return redirect(url_for('upload_page', 
                           message=f'Error uploading photo: {str(e)}', 
                           success='false'))
    else:
        return redirect(url_for('upload_page', 
                       message='Invalid file type. Please upload PNG, JPG, JPEG, GIF, or WebP files.', 
                       success='false'))

@app.route('/photo/<filename>')
def serve_photo(filename):
    """Serve uploaded photos"""
    from flask import send_from_directory
    return send_from_directory(PHOTOS_DIR, filename)

@app.route('/api/tortoises')
def api_tortoises():
    """API endpoint to get tortoise list"""
    db = DatabaseManager()
    try:
        tortoises = db.get_all_tortoises()
        return jsonify([{
            'id': t['id'],
            'name': t['name'],
            'species': t['species'],
            'has_photo': bool(t.get('photo_path'))
        } for t in tortoises])
    finally:
        db.close()

def start_photo_server():
    """Start the photo upload server in background"""
    try:
        # Get local IP address
        import socket
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        
        print(f"Photo upload server starting...")
        print(f"Access from phone: http://{local_ip}:5555")
        print(f"Local access: http://localhost:5555")
        
        app.run(host='0.0.0.0', port=5555, debug=False, threaded=True)
    except Exception as e:
        print(f"Error starting photo server: {e}")

def run_photo_server_background():
    """Run photo server in a background thread"""
    server_thread = threading.Thread(target=start_photo_server, daemon=True)
    server_thread.start()
    return server_thread

if __name__ == '__main__':
    start_photo_server()
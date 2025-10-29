from flask import Blueprint, request, jsonify, render_template
import os
import shutil
from azure_blob_service import upload_to_blob, download_from_blob

# Define blueprint
routes = Blueprint('routes', __name__)

# Folders for uploads and downloads
UPLOAD_FOLDER = "uploads"
DOWNLOAD_FOLDER = "downloads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Home page serving the upload form
@routes.route('/')
def home():
    return render_template('upload.html')

# Upload file to Azure Blob Storage AND save locally in downloads/
@routes.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file found"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    # Save locally first in uploads/
    local_upload_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(local_upload_path)

    # Upload to Azure Blob Storage
    upload_to_blob(local_upload_path, file.filename)

    # Also save a copy in downloads/ so it's available locally
    local_download_path = os.path.join(DOWNLOAD_FOLDER, file.filename)
    shutil.copy(local_upload_path, local_download_path)

    return jsonify({
        "message": f"File {file.filename} uploaded to Azure and saved locally in {DOWNLOAD_FOLDER}"
    }), 200

# Download file from Azure Blob Storage to downloads/
@routes.route('/fetch/<filename>', methods=['GET'])
def fetch_file(filename):
    local_path = os.path.join(DOWNLOAD_FOLDER, filename)
    download_from_blob(filename, local_path)
    return jsonify({
        "message": f"File {filename} downloaded from Azure to {local_path}"
    }), 200

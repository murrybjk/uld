from flask import Flask, render_template, request, send_from_directory, url_for
import os
import qrcode
import base64
import zipfile
from io import BytesIO
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
ZIP_FOLDER = "zips"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["ZIP_FOLDER"] = ZIP_FOLDER

# Ensure directories exist
for folder in [UPLOAD_FOLDER, ZIP_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

def rename_existing_file(file_path):
    """Renames existing files by appending a timestamp before saving a new one."""
    if os.path.exists(file_path):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name, ext = os.path.splitext(file_path)
        new_name = f"{name}_{timestamp}{ext}"
        os.rename(file_path, new_name)

def get_safe_filename(filename, orig_ext):
    """Ensures filename has the correct extension if missing."""
    if not filename.endswith(orig_ext):
        filename += orig_ext
    return filename

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        uploaded_files = request.files.getlist("files")
        filename_input = request.form.get("filename", "").strip()
        file_links = []

        if len(uploaded_files) == 1:  # Single file case
            file = uploaded_files[0]
            if file.filename:
                orig_name, orig_ext = os.path.splitext(file.filename)  # Get original extension

                # Ensure correct filename (preserve extension)
                if filename_input:
                    filename = get_safe_filename(filename_input, orig_ext)
                else:
                    filename = file.filename  # Use original name if blank

                file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

                # Rename existing file if it already exists
                rename_existing_file(file_path)

                file.save(file_path)
                file_url = url_for("uploaded_file", filename=filename, _external=True)
                qr_base64 = generate_qr_code(file_url)

                return render_template("success.html", files=[(file_url, qr_base64)])

        elif len(uploaded_files) > 1:  # Multiple files → Create ZIP
            # If user specified a filename, use it. Otherwise, create default name.
            zip_filename = f"{filename_input if filename_input else 'uploaded_files'}.zip"
            zip_path = os.path.join(app.config["ZIP_FOLDER"], zip_filename)

            # Rename existing ZIP file if it already exists
            rename_existing_file(zip_path)

            with zipfile.ZipFile(zip_path, "w") as zipf:
                for file in uploaded_files:
                    if file.filename:
                        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
                        rename_existing_file(file_path)  # Rename old file if exists
                        file.save(file_path)
                        zipf.write(file_path, file.filename)  # Add to ZIP

            zip_url = url_for("download_zip", filename=zip_filename, _external=True)
            qr_base64 = generate_qr_code(zip_url)

            return render_template("success.html", files=[(zip_url, qr_base64)])

    return render_template("index.html")

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/zips/<filename>")
def download_zip(filename):
    return send_from_directory(app.config["ZIP_FOLDER"], filename)

def generate_qr_code(url):
    """Generates a QR code for a given URL and returns the base64-encoded image."""
    qr = qrcode.make(url)
    buffered = BytesIO()
    qr.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8113, debug=True)


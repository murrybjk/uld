from flask import Flask, render_template, request, send_from_directory, url_for
import os
import qrcode
import base64
import zipfile
from io import BytesIO
from datetime import datetime

# Configuration
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
    """Rename existing file by appending timestamp to prevent overwriting."""
    if os.path.exists(file_path):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name, ext = os.path.splitext(file_path)
        new_name = f"{name}_{timestamp}{ext}"
        os.rename(file_path, new_name)


def get_safe_filename(filename, orig_ext):
    """Ensure filename has correct extension."""
    if not filename.endswith(orig_ext):
        filename += orig_ext
    return filename


def generate_qr_code(url):
    """Generate base64-encoded QR code for a URL."""
    qr = qrcode.make(url)
    buffered = BytesIO()
    qr.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        uploaded_files = request.files.getlist("file")
        filename_input = request.form.get("filename", "").strip()

        # Skip empty files
        uploaded_files = [f for f in uploaded_files if f and f.filename]

        if not uploaded_files:
            return render_template("index.html", error="Please select at least one file.")

        if len(uploaded_files) == 1:
            # Single file upload
            file = uploaded_files[0]
            orig_name, orig_ext = os.path.splitext(file.filename)
            filename = get_safe_filename(filename_input or file.filename, orig_ext)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

            rename_existing_file(file_path)
            file.save(file_path)

            file_url = url_for("uploaded_file", filename=filename, _external=True)
            qr_base64 = generate_qr_code(file_url)
            return render_template("success.html", files=[(file_url, qr_base64)])

        else:
            # Multiple files → ZIP archive
            zip_filename = f"{filename_input or 'uploaded_files'}.zip"
            zip_path = os.path.join(app.config["ZIP_FOLDER"], zip_filename)

            rename_existing_file(zip_path)

            with zipfile.ZipFile(zip_path, "w") as zipf:
                for file in uploaded_files:
                    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
                    rename_existing_file(file_path)
                    file.save(file_path)
                    zipf.write(file_path, file.filename)

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8113, debug=True)


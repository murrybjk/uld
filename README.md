# ULD - Upload with Link & Download

A Flask-based web application that provides easy file upload functionality with automatic QR code generation for mobile-friendly downloads.

## Features

- 📤 **Single & Multi-file Upload** - Support for uploading one or multiple files at once
- 🎯 **Drag-and-Drop Interface** - Modern, intuitive UI with drag-and-drop support
- 📱 **QR Code Generation** - Automatic QR codes for easy mobile access to download links
- 🗜️ **ZIP Archive Creation** - Automatically creates ZIP files when uploading multiple files
- 📝 **Smart File Versioning** - Existing files are renamed with timestamps to prevent data loss
- 🌐 **Network-Accessible** - Accessible from any device on your network
- 📄 **Custom Filenames** - Optional custom filename support for uploads

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **QR Codes**: qrcode library with Pillow
- **Templates**: Jinja2

## Installation

### Prerequisites

- Python 3.7+
- pip (Python package manager)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd uld
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

```bash
python app.py
```

The application will start on `http://localhost:8113`

### Accessing from Network

To access from other devices on your network, use:
```
http://<your-machine-ip>:8113
```

### Upload Files

1. **Single File Upload**:
   - Select one file and optionally provide a custom filename
   - Click upload and receive a download link with QR code

2. **Multiple File Upload**:
   - Select multiple files (the app will create a ZIP archive)
   - Optionally provide a custom ZIP filename
   - Download the ZIP with QR code for mobile access

### File Versioning

If you upload a file with the same name as an existing file, the old file will be renamed with a timestamp suffix (format: `YYYYMMDD_HHMMSS`) to prevent data loss.

## Project Structure

```
uld/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
├── CLAUDE.md             # Internal documentation
├── README.md             # This file
├── templates/
│   ├── index.html        # Upload form with drag-and-drop UI
│   └── success.html      # Success page with QR codes
├── uploads/              # Uploaded files directory (gitignored)
└── zips/                 # Generated ZIP files directory (gitignored)
```

## Configuration

The application uses the following default configuration:

```python
UPLOAD_FOLDER = 'uploads'      # Directory for single file uploads
ZIP_FOLDER = 'zips'            # Directory for ZIP archives
SERVER_HOST = '0.0.0.0'        # Listen on all interfaces
SERVER_PORT = 8113             # Application port
DEBUG = True                   # Debug mode (disable in production)
```

To modify these settings, edit `app.py` lines 9-18.

## API Reference

### Endpoints

#### Upload Files
- **URL**: `/`
- **Method**: `POST`
- **Form Data**:
  - `file` (required): File(s) to upload
  - `filename` (optional): Custom filename for the uploaded file(s)
- **Response**: HTML page with download link(s) and QR code(s)

#### Get Upload Form
- **URL**: `/`
- **Method**: `GET`
- **Response**: HTML upload form

#### Download Uploaded File
- **URL**: `/uploads/<filename>`
- **Method**: `GET`
- **Response**: File download

#### Download ZIP Archive
- **URL**: `/zips/<filename>`
- **Method**: `GET`
- **Response**: ZIP file download

## Development

### Running in Development Mode

The application runs with `DEBUG=True` by default. This provides:
- Automatic code reloading on file changes
- Detailed error pages
- Interactive debugger

### File Organization

- **Helper Functions** (app.py lines 20-32):
  - `rename_existing_file()`: Implements file versioning
  - `get_safe_filename()`: Ensures proper file extensions

- **Route Handlers** (app.py lines 34-92):
  - Upload handler with single/multi-file support
  - File serving endpoints

- **Utilities** (app.py lines 94-99):
  - QR code generation

## Production Deployment

Before deploying to production, consider:

1. **Disable Debug Mode**
   ```python
   app.run(debug=False)
   ```

2. **Use Production WSGI Server**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8113 app:app
   ```

3. **Add Security Features**
   - Implement file type validation
   - Set file size limits
   - Add CSRF protection
   - Enable HTTPS with SSL/TLS

4. **Configure Environment Variables**
   - Use `.env` file (see .gitignore)
   - Load configuration from environment

5. **Set Up Logging**
   - Replace print statements with proper logging
   - Log all uploads and downloads

6. **Add Rate Limiting**
   - Prevent upload abuse
   - Implement IP-based rate limiting

7. **Implement Cleanup**
   - Remove old files periodically
   - Monitor disk space

## Security Considerations

### Current Implementation (Development Only)

⚠️ **WARNING**: This application is designed for development/local use. For production:

- ❌ No file type validation (add whitelist of allowed extensions)
- ❌ No file size limits (set MAX_CONTENT_LENGTH)
- ❌ No authentication/authorization
- ❌ No CSRF protection
- ❌ No rate limiting
- ❌ Debug mode enabled

### Recommended Security Enhancements

```python
# Add file type validation
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip', 'docx'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Set file size limit (16MB)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Enable CSRF protection
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)
```

## Troubleshooting

### Port Already in Use

If port 8113 is already in use, modify the port in `app.py`:
```python
app.run(host="0.0.0.0", port=8114, debug=True)
```

### Permission Denied Errors

Ensure the `uploads/` and `zips/` directories have write permissions:
```bash
chmod 755 uploads/ zips/
```

### QR Code Not Generating

Ensure Pillow is properly installed:
```bash
pip install --upgrade Pillow
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check the `CLAUDE.md` file for internal development documentation

## Changelog

### Version 1.0.0
- Initial release
- Single and multi-file upload support
- QR code generation
- Drag-and-drop interface
- File versioning system

---

**Note**: For detailed information about the codebase structure and AI assistant guidelines, see `CLAUDE.md`.

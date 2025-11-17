# CLAUDE.md - AI Assistant Guide for ULD (Upload with Link & Download)

## Project Overview

**ULD** is a Flask-based web application that provides file upload functionality with automatic QR code generation for easy mobile downloads. The application supports both single and multiple file uploads, automatically creating ZIP archives for batch uploads.

### Key Features
- Single and multi-file upload with drag-and-drop interface
- Automatic QR code generation for download links
- Smart file versioning (existing files are renamed with timestamps)
- ZIP archive creation for multiple file uploads
- Mobile-friendly design with QR codes for quick access

---

## Codebase Structure

```
/home/user/uld/
├── app.py                 # Main Flask application
├── templates/             # Jinja2 HTML templates
│   ├── index.html        # Upload form with drag-and-drop UI
│   └── success.html      # Success page with QR codes
├── uploads/              # Directory for uploaded files (gitignored in practice)
└── zips/                 # Directory for generated ZIP files (gitignored in practice)
```

### File Responsibilities

#### `app.py` (Main Application - 104 lines)
The core Flask application with the following components:

**Configuration** (Lines 9-18):
- Flask app initialization
- Upload and ZIP folder configuration
- Automatic directory creation

**Helper Functions**:
- `rename_existing_file(file_path)` (Lines 20-26): Handles file versioning by appending timestamps
- `get_safe_filename(filename, orig_ext)` (Lines 28-32): Ensures proper file extensions
- `generate_qr_code(url)` (Lines 94-99): Creates base64-encoded QR codes using the qrcode library

**Routes**:
- `GET/POST /` (Lines 34-84): Main upload handler
  - Single file: Saves with optional custom filename
  - Multiple files: Creates ZIP archive with all files
- `GET /uploads/<filename>` (Lines 86-88): Serves uploaded files
- `GET /zips/<filename>` (Lines 90-92): Serves generated ZIP files

**Server Configuration** (Lines 101-102):
- Host: `0.0.0.0` (accessible from network)
- Port: `8113`
- Debug mode: `True`

#### `templates/index.html` (75 lines)
Upload form with modern drag-and-drop interface:
- Drag-and-drop zone with visual feedback
- File list preview
- Dynamic filename placeholder (changes based on single/multi-file selection)
- Client-side JavaScript for UX enhancements

#### `templates/success.html` (24 lines)
Success page displaying:
- Download links for uploaded files/ZIP
- QR codes for mobile access
- Link to upload more files

---

## Dependencies

### Required Python Packages
The application requires the following Python packages:

```python
Flask          # Web framework
qrcode         # QR code generation
Pillow         # Image processing (required by qrcode)
```

### Installation
```bash
pip install Flask qrcode[pil]
```

**Note**: A `requirements.txt` file should be created for dependency management.

---

## Development Workflow

### Running the Application

**Start the Flask server**:
```bash
python app.py
```

The application will be accessible at:
- Local: `http://localhost:8113`
- Network: `http://<your-ip>:8113`

### Git Workflow

**Current Branch**: `claude/claude-md-mi2n8uirjjc2yw32-01UoGEGE3ACiFTbhWVmhuiM8`

**Recent History**:
```
c98e1a1 Delete zips directory
42fcf06 Create temp.txt
8aab96f Create success.html
a441223 Create index.html
45cbae6 Create temp.txt
08cd878 Create app.py
```

**Branch Naming Convention**: Claude AI branches follow the pattern `claude/claude-md-<session-id>`

---

## Key Conventions and Patterns

### File Handling
1. **Versioning**: Files are never overwritten. Existing files are renamed with a timestamp suffix (format: `YYYYMMDD_HHMMSS`)
2. **Extension Preservation**: User-provided filenames automatically inherit the original file extension if missing
3. **ZIP Naming**: Multi-file uploads create ZIPs named either by user input or default to `uploaded_files.zip`

### Code Style
- **Indentation**: 4 spaces
- **String Quotes**: Double quotes for strings
- **Naming Convention**: Snake_case for functions and variables
- **Comments**: Docstrings for functions explaining purpose

### Security Considerations
**Current Implementation** (Development Mode):
- Debug mode is enabled (should be disabled in production)
- No file type validation (potential security risk)
- No file size limits (potential DoS vector)
- No authentication/authorization
- No CSRF protection
- Direct file serving without sanitization

### Template Patterns
- Uses Jinja2 templating syntax (`{% %}` for logic, `{{ }}` for variables)
- Base64-encoded images embedded directly in HTML
- Responsive meta viewport tag for mobile compatibility

---

## AI Assistant Guidelines

### When Making Changes

1. **Preserve File Versioning Logic**: The `rename_existing_file()` function is critical for preventing data loss. Never remove or modify this without explicit instruction.

2. **Maintain Extension Handling**: The `get_safe_filename()` function ensures files retain their original extensions. This prevents broken downloads.

3. **Test Both Upload Paths**:
   - Single file upload (uses custom filename if provided)
   - Multi-file upload (creates ZIP archive)

4. **Consider Security**: Before adding features, consider:
   - File type validation (whitelist approach recommended)
   - File size limits
   - Path traversal prevention
   - Authentication if needed

5. **Update Templates Consistently**: When modifying routes, ensure corresponding template changes are made.

### Common Tasks

#### Adding File Type Validation
Add to the upload handler (around line 43-50):
```python
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
```

#### Adding File Size Limits
Add to Flask config (around line 12):
```python
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit
```

#### Creating requirements.txt
```txt
Flask==3.0.0
qrcode==7.4.2
Pillow==10.1.0
```

#### Adding .gitignore
Essential entries:
```
uploads/
zips/
*.pyc
__pycache__/
.env
venv/
*.log
```

### Testing Checklist

When making changes, verify:
- [ ] Single file upload works with custom filename
- [ ] Single file upload works without custom filename
- [ ] Multi-file upload creates ZIP correctly
- [ ] QR codes generate and display properly
- [ ] File versioning prevents overwrites
- [ ] Extensions are preserved correctly
- [ ] Download links work from success page
- [ ] Drag-and-drop interface functions properly

---

## Architecture Notes

### Request Flow

1. **Upload Request** (`POST /`)
   - Client submits form with files and optional filename
   - Server checks if single or multiple files
   - **Single**: Save directly to `uploads/` folder
   - **Multiple**: Save all to `uploads/`, create ZIP in `zips/` folder
   - Generate QR code for download URL
   - Render success page with URL and QR code

2. **Download Request** (`GET /uploads/<file>` or `GET /zips/<file>`)
   - Serve file from respective directory using Flask's `send_from_directory`

### URL Generation
- Uses `url_for()` with `_external=True` for absolute URLs
- Critical for QR codes that need to work across networks

### QR Code Implementation
- Generated server-side using `qrcode` library
- Converted to PNG in memory (BytesIO)
- Base64-encoded for direct HTML embedding
- No temporary files created

---

## Production Deployment Considerations

Before deploying to production:

1. **Disable Debug Mode**: Change `debug=True` to `debug=False` in `app.run()`
2. **Use Production WSGI Server**: Replace Flask's built-in server with Gunicorn or uWSGI
3. **Add Security Headers**: Implement CSRF protection, CSP, etc.
4. **Implement File Validation**: Whitelist allowed file types
5. **Add Rate Limiting**: Prevent abuse of upload endpoint
6. **Set File Size Limits**: Prevent large uploads from consuming resources
7. **Configure Proper Logging**: Replace print statements with proper logging
8. **Use Environment Variables**: For configuration (port, debug mode, folders, etc.)
9. **Implement Cleanup**: Add cron job or background task to clean old files
10. **Add HTTPS**: Use reverse proxy (nginx) with SSL certificate

---

## Current State Summary

**Strengths**:
- Clean, readable code structure
- Good file versioning to prevent data loss
- User-friendly drag-and-drop interface
- QR code integration for mobile access
- Handles both single and multi-file uploads elegantly

**Areas for Improvement**:
- Missing `requirements.txt` for dependency management
- Missing `.gitignore` for uploads/zips directories
- No security measures (file validation, size limits, auth)
- Debug mode enabled (not production-ready)
- No error handling for disk space, permissions, etc.
- No logging implementation
- No automated tests

---

## Quick Reference

### Important File Paths
- **Main app**: `/home/user/uld/app.py:102`
- **Upload handler**: `/home/user/uld/app.py:34`
- **QR generation**: `/home/user/uld/app.py:94`
- **File versioning**: `/home/user/uld/app.py:20`
- **Upload template**: `/home/user/uld/templates/index.html`
- **Success template**: `/home/user/uld/templates/success.html`

### Default Configuration
- **Upload folder**: `uploads/`
- **ZIP folder**: `zips/`
- **Server port**: `8113`
- **Host**: `0.0.0.0` (all interfaces)

---

*This document was generated on 2025-11-17 for AI assistants working with the ULD codebase.*

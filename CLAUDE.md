# CLAUDE.md - Developer Guide

## Overview

**ULD** is a 101-line Flask app for file sharing with QR codes. Users upload files, get shareable links with QR codes for mobile access. Single files upload directly, multiple files auto-ZIP.

## Architecture

### app.py (101 lines)
- **Config** (Lines 9-19): Folders, Flask setup
- **Functions** (Lines 22-43):
  - `rename_existing_file()`: Append timestamp to existing files
  - `get_safe_filename()`: Preserve file extensions
  - `generate_qr_code()`: Create base64-encoded QR images
- **Routes** (Lines 45-101):
  - `POST /`: Handle uploads (single or multi)
  - `GET /uploads/<filename>`: Serve files
  - `GET /zips/<filename>`: Serve ZIPs

### templates/

- **index.html**: Upload form with modern gradient design, drag-drop, file list
- **success.html**: Download link + QR code display, copy-to-clipboard

### Core Logic

```
User uploads files
    ↓
Check if 1 or multiple files
    ↓
Single: Save to uploads/
Multiple: Save to uploads/ + ZIP to zips/
    ↓
Generate QR for download URL
    ↓
Show success page with link + QR
```

## Key Features

1. **File Versioning**: Existing files renamed with `YYYYMMDD_HHMMSS` suffix
2. **Extension Preservation**: Custom names keep original extension
3. **Smart ZIP**: Multiple files auto-archived
4. **No DB**: All file-based, simple storage

## Common Tasks

### Make filename optional (DONE)
- Removed `required` from input
- Default to original filename if not provided

### Add file validation
```python
ALLOWED = {'txt', 'pdf', 'png', 'jpg', 'docx', 'zip'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED
```

### Set file size limit
```python
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
```

### Add error handling
Error handling already implemented:
- Empty file check
- Returns error message on failure

## Code Patterns

- **Snake_case** for functions/variables
- **Double quotes** for strings
- **Docstrings** for all functions
- **4-space** indentation

## Testing

Before changes, verify:
- [ ] Single file upload
- [ ] Multi-file ZIP creation
- [ ] Custom filenames work
- [ ] File versioning (timestamp)
- [ ] QR codes display
- [ ] Downloads work
- [ ] Drag-drop works
- [ ] Mobile responsive

## Important Notes

⚠️ **Don't modify without reason:**
- `rename_existing_file()` - Critical for data safety
- `get_safe_filename()` - Prevents broken downloads
- Form field name `name="file"` - Matches app.py line 48

## Deployment Checklist

- [ ] Set `debug=False`
- [ ] Use Gunicorn/uWSGI
- [ ] Add file type validation
- [ ] Set MAX_CONTENT_LENGTH
- [ ] Enable HTTPS
- [ ] Add rate limiting
- [ ] Monitor disk space
- [ ] Regular file cleanup

## Quick Refs

| What | Where |
|------|-------|
| Main app | app.py:45 |
| Upload handler | app.py:46 |
| File versioning | app.py:22 |
| QR generation | app.py:38 |
| Upload form | templates/index.html |
| Success page | templates/success.html |

## Configuration

```python
UPLOAD_FOLDER = "uploads"   # Single files
ZIP_FOLDER = "zips"         # Archives
PORT = 8113                 # Server port
HOST = "0.0.0.0"           # All interfaces
DEBUG = True               # Dev mode
```

---

Keep it simple. ULD is meant to be lightweight and easy to understand.

# ULD - Upload with Link & Download

A lightweight Flask app for sharing files with automatic QR code generation. Upload files, get instant download links and QR codes for mobile access.

## Features

- 📤 **Single & Multi-file Upload** - Upload one or many files at once
- 🎯 **Drag & Drop Interface** - Modern, responsive design
- 📱 **QR Code Generation** - Instant QR codes for mobile downloads
- 🗜️ **ZIP Archives** - Automatically ZIP multiple files
- 📝 **File Versioning** - Existing files renamed with timestamps (no overwrites)
- 🌐 **Network Accessible** - Share across devices on your network
- ⚡ **No Dependencies** - Just Flask and two libraries

## Quick Start

```bash
# Clone and setup
git clone https://github.com/murrybjk/uld.git
cd uld

# Install dependencies
pip install -r requirements.txt

# Run
python app.py
```

Access at: **http://localhost:8113**

For network access: **http://<your-ip>:8113**

## How It Works

1. **Upload files** - Drag & drop or click to select
2. **Get link** - Instant download link generated
3. **Scan QR** - Mobile users scan QR code to download
4. **Done** - Files stay on your server, accessible via link

### Single File
- Upload one file with optional custom name
- Gets renamed if it already exists (timestamp added)

### Multiple Files
- Automatically creates ZIP archive
- Optional custom ZIP name
- All files extracted on download

## Project Structure

```
uld/
├── app.py                 # Flask application (101 lines)
├── requirements.txt       # Dependencies
├── README.md             # This file
├── CLAUDE.md             # Developer guide
├── .gitignore            # Git ignore rules
├── templates/
│   ├── index.html        # Upload form (modern UI)
│   └── success.html      # Success page with QR
├── uploads/              # Uploaded files (gitignored)
└── zips/                 # ZIP files (gitignored)
```

## Configuration

Edit `app.py` to customize:

```python
UPLOAD_FOLDER = "uploads"      # Where files are stored
ZIP_FOLDER = "zips"            # Where ZIPs are stored
PORT = 8113                    # Server port
DEBUG = True                   # Development mode
```

## Development

### Running locally
```bash
python app.py
```

Auto-reloads on code changes (debug mode enabled).

### Testing checklist
- [ ] Single file upload works
- [ ] Multiple file upload creates ZIP
- [ ] Custom filenames apply correctly
- [ ] File versioning (timestamp) works
- [ ] QR codes generate and scan
- [ ] Drag & drop works
- [ ] Mobile responsive

## Deployment

For production, consider:

1. **Disable debug mode** → `debug=False`
2. **Use production server** → Gunicorn or uWSGI
3. **Add file validation** → Whitelist file types
4. **Set size limits** → `app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024`
5. **Enable HTTPS** → Use reverse proxy (nginx) with SSL
6. **Add authentication** → If needed for your use case
7. **Monitor storage** → Clean up old files periodically

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8113 app:app
```

## API Reference

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Show upload form |
| `/` | POST | Upload files |
| `/uploads/<file>` | GET | Download uploaded file |
| `/zips/<file>` | GET | Download ZIP archive |

## Security Notes

⚠️ **Development mode only** - This app is designed for local/trusted networks.

For production, add:
- File type validation (whitelist)
- File size limits
- CSRF protection
- Rate limiting
- HTTPS/SSL
- Authentication if needed

## Troubleshooting

**Port already in use?**
```bash
python app.py  # Then change port in app.py
```

**Permission denied on uploads/?**
```bash
chmod 755 uploads/ zips/
```

**QR code not generating?**
```bash
pip install --upgrade Pillow
```

## License

MIT License - see LICENSE file

## Support

- Issues: Open GitHub issue
- Questions: Check CLAUDE.md for developer docs

---

**Made with ❤️ for simple file sharing**

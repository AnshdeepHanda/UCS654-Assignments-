# YouTube Mashup Creator - Roll Number: 102303124

A complete system for creating audio mashups from YouTube videos with both command-line and web interfaces.

## Project Structure

```
.
├── 102303124.py              # Command-line program (Program 1)
├── app.py                    # Flask web application (Program 2)
├── templates/
│   └── index.html           # Web interface
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## System Requirements

- Python 3.7 or higher
- ffmpeg (for audio conversion)
- pip (Python package manager)

### Install ffmpeg

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Download from https://ffmpeg.org/download.html and add to PATH

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `yt-dlp` - YouTube video downloader
- `pydub` - Audio processing
- `Flask` - Web framework

### 2. Verify ffmpeg Installation

```bash
ffmpeg -version
```

Should display ffmpeg version info.

---

## Program 1: Command-Line Interface

### Description
Downloads N videos of a singer from YouTube, converts them to audio, cuts the first Y seconds from each, and merges them into a single audio file.

### Usage

```bash
python 102303124.py <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>
```

### Parameters

| Parameter | Type | Description | Constraints |
|-----------|------|-------------|-------------|
| SingerName | String | Name of the singer | Required, min 2 chars |
| NumberOfVideos | Integer | How many videos to download | > 10 |
| AudioDuration | Integer | Seconds to cut from each video | > 20 |
| OutputFileName | String | Output file name | Must end with .mp3, .wav, or .m4a |

### Examples

```bash
# Example 1: Sharry Maan
python 102303124.py "Sharry Maan" 20 30 102303124-output.mp3

# Example 2: Arijit Singh
python 102303124.py "Arijit Singh" 15 25 arijit-mashup.mp3

# Example 3: Badshah
python 102303124.py "Badshah" 12 30 badshah-mix.mp3
```

### Output

The program will:
1. Download N videos from YouTube
2. Convert them to MP3 audio
3. Cut the first Y seconds from each
4. Merge all segments into a single file
5. Display progress with checkmarks (✓)

**Example Output:**
```
============================================================
YouTube Mashup Creator - Roll: 102303124
============================================================

[1/4] Downloading 20 videos of 'Sharry Maan'...
✓ Successfully downloaded 20 videos

[2/4] Converting videos to audio...
✓ Successfully converted 20 videos to audio

[3/4] Cutting first 30 seconds from each audio...
✓ Successfully cut 20 audio segments

[4/4] Merging all audio segments...
✓ Successfully merged all segments into 'mashup-output.mp3'
  Total duration: 10.0 minutes

✓ Temporary files cleaned up

============================================================
✓ Mashup creation successful!
Output file: 102303124-output.mp3
============================================================
```

### Error Handling

The program handles:
- Invalid parameter count
- Parameters outside constraints
- Missing ffmpeg
- Network errors during download
- Audio conversion failures
- Invalid file formats

---

## Program 2: Web Application

### Description
A Flask web application that provides a user-friendly interface to create mashups. Users submit a form and receive the result via email as a zip file.

### Setup

#### 1. Configure Email

Open `app.py` and update the email credentials:

```python
sender_email = "your_email@gmail.com"  # Your Gmail address
sender_password = "your_app_password"  # Gmail App Password
```

**Important:** Use a Gmail App Password, not your regular password.

**How to get Gmail App Password:**
1. Go to https://myaccount.google.com/
2. Select "Security" in the left menu
3. Enable "2-Step Verification" if not already enabled
4. Go back to Security → App passwords
5. Select "Mail" and "Windows Computer" (or your device)
6. Copy the generated 16-character password
7. Paste it in the code as `sender_password`

#### 2. Run the Application

```bash
python app.py
```

The application will start at `http://localhost:5000`

### Features

- **Input Validation:** All form fields are validated on the client and server
- **Email Validation:** Ensures valid email format before processing
- **Async Processing:** Mashup creation happens in background threads
- **Error Handling:** Detailed error messages sent via email if something fails
- **Progress Updates:** User receives email notification when mashup is ready

### Form Fields

1. **Singer Name** (Required)
   - Text input
   - Example: "Sharry Maan"

2. **Number of Videos** (Required)
   - Integer input
   - Constraint: > 10

3. **Duration** (Required)
   - Integer input (seconds)
   - Constraint: > 20

4. **Email Address** (Required)
   - Email input
   - Must be valid format

### Workflow

1. User fills the form
2. Client-side validation occurs
3. User clicks "Create Mashup"
4. Request sent to server
5. Server starts async processing
6. User receives confirmation message
7. Program 1 is executed in background
8. Results are zipped
9. Email sent to user with attachment
10. Temporary files cleaned up

### Email Template

Users receive an email like:

```
Subject: Your Mashup is Ready - Sharry Maan (20 videos)

Your audio mashup has been successfully created!

Singer: Sharry Maan
Videos: 20
Duration per segment: 30 seconds

Please find your mashup file attached as a zip archive.

Note: This is an automated email. Please do not reply to this address.

Regards,
Mashup Creator (Roll: 102303124)
```

---

## Troubleshooting

### Issue: "ffmpeg is not installed"
**Solution:** Install ffmpeg using the commands above

### Issue: YouTube videos not downloading
**Solution:** 
- Check internet connection
- YouTube may be blocking rapid downloads
- Try with a different singer name
- Update yt-dlp: `pip install --upgrade yt-dlp`

### Issue: Email not received
**Solution:**
- Verify email credentials in app.py
- Check spam/junk folder
- Ensure you're using Gmail App Password, not regular password
- Check email in firewall whitelist

### Issue: "Permission denied" on Linux/Mac
**Solution:**
```bash
chmod +x 102303124.py
```

### Issue: Audio quality issues
**Solution:**
- Ensure ffmpeg is properly installed: `ffmpeg -version`
- Try with fewer videos initially

---

## API Endpoints (Program 2)

### POST `/api/create-mashup`

**Request:**
```json
{
  "singerName": "Sharry Maan",
  "numVideos": 20,
  "duration": 30,
  "email": "user@example.com"
}
```

**Response (Success - 202):**
```json
{
  "success": true,
  "message": "Mashup creation started. You will receive an email at user@example.com when ready.",
  "jobId": "1234567890"
}
```

**Response (Error - 400):**
```json
{
  "success": false,
  "errors": [
    "Number of videos must be greater than 10.",
    "Duration must be greater than 20 seconds."
  ]
}
```

---

## Performance Notes

- **Download Time:** ~2-5 minutes for 20 videos (depends on internet)
- **Conversion Time:** ~5-10 minutes for 20 videos
- **Total Time:** 10-20 minutes for typical mashup

### Optimization Tips

- Use fewer videos for faster results (minimum 11)
- Use shorter durations (minimum 21 seconds)
- Ensure stable internet connection
- Run on a machine with SSD for faster file I/O

---

## Security Considerations

- Email validation prevents spam submissions
- CORS headers can be added for production
- Rate limiting recommended for production deployment
- File size limits in place (500MB)
- Input sanitization implemented

---

## Future Enhancements

Possible improvements:
- Job queue system for handling multiple requests
- Email notifications for job status
- Support for different audio formats
- Playlist support
- UI progress indicator with real-time updates
- Download option instead of email
- Custom audio effects
- Batch processing

---

## Important Notes

1. **Late Submission Penalty:** Only 50% marks if submitted after due date
2. **Plagiarism:** Zero marks for plagiarized code
3. **Testing:** Test both programs thoroughly before submission
4. **Documentation:** Include clear usage instructions
5. **Dependencies:** Ensure all required packages are in requirements.txt

---

## Submission Checklist

- [ ] Program 1 file: `102303124.py`
- [ ] Program 2 web app running and tested
- [ ] All dependencies in `requirements.txt`
- [ ] Email configuration set correctly
- [ ] Tested with multiple singers
- [ ] Error handling verified
- [ ] README with usage instructions
- [ ] Submitted before due date

---

## Author

Roll Number: 102303124
Institution: Thapar Institute of Engineering and Technology (TIET)

---

## License

Academic project - Thapar University Assignment

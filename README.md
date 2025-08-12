# Google-Meet-Bot
This project is a Python bot that automates the process of logging into Gmail, joining a Google Meet, recording the audio of the meeting, and then generating a summary, key points, action items, and sentiment analysis of the meeting. 


## Recording video/audio/transcripts from video conferencing calls
If you’re looking to use this repo to retrieve video/audio streams or transcripts from meeting platforms like Zoom, Google Meet, Microsoft Teams, consider checking out [Recall.ai](https://www.recall.ai), an API for meeting recording.
![Alt Text](https://github.com/dhruvldrp9/Google-Meet-Bot/blob/main/GoogleMeetBot.jpeg)

## Prerequisites

- Python 3.8 or higher
- Chrome browser
- OpenAI API Key
- A Gmail account
- A Google Meet link
- ffmpeg/ffprobe installed and available on PATH (for audio trimming if needed)

## Installation

### Option 1: Install from PyPI (Recommended)

```bash
pip install google-meet-bot
```

### Option 2: Install from source

1. Clone the repository:
   ```bash
   git clone https://github.com/dhruvldrp9/Google-Meet-Bot.git
   cd Google-Meet-Bot
   ```

2. Create Python environment:
   ```bash
   python3 -m venv env
   ```

3. Activate environment:
   - For Unix/Linux/macOS:
     ```bash
     source env/bin/activate
     ```
   - For Windows:
     ```bash
     env\Scripts\activate
     ```

4. Install package (local):
   ```bash
   pip install -U build
   pip install .
   ```

## Usage

### Command Line Interface

After installation, you can use the CLI:

```bash
# Basic usage
google-meet-bot --meet-link "https://meet.google.com/xxx-xxxx-xxx" --duration 60

# Skip analysis phase
google-meet-bot --meet-link "https://meet.google.com/xxx-xxxx-xxx" --duration 60 --no-analysis

# Run as Python module
python -m google_meet_bot --meet-link "https://meet.google.com/xxx-xxxx-xxx" --duration 60
```

### Programmatic Usage

```python
from google_meet_bot import JoinGoogleMeet, SpeechToText, AudioRecorder

# Initialize the bot
bot = JoinGoogleMeet()
bot.Glogin()
bot.turnOffMicCam("https://meet.google.com/xxx-xxxx-xxx")
bot.AskToJoin("output.wav", 60)

# Analyze the recording
speech_analyzer = SpeechToText()
speech_analyzer.transcribe("output.wav")
```

## Configuration

5. Configure environment variables:
   - Create a `.env` file in the project root with the following content:
     ```
     # Google Meet Credentials
     EMAIL_ID=your_email@gmail.com
     EMAIL_PASSWORD=your_password

     # Meeting Configuration
     MEET_LINK=https://meet.google.com/xxx-xxxx-xxx
     RECORDING_DURATION=60

     # Audio Configuration
     SAMPLE_RATE=44100
     MAX_AUDIO_SIZE_BYTES=20971520

     # OpenAI Configuration
     OPENAI_API_KEY=your_openai_api_key
     GPT_MODEL=gpt-4
     WHISPER_MODEL=whisper-1
     ```



## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| EMAIL_ID | Your Gmail address | - |
| EMAIL_PASSWORD | Your Gmail password | - |
| MEET_LINK | Google Meet URL to join | - |
| RECORDING_DURATION | Duration to record in seconds | 60 |
| SAMPLE_RATE | Audio recording sample rate | 44100 |
| MAX_AUDIO_SIZE_BYTES | Maximum audio file size in bytes | 20971520 (20MB) |
| OPENAI_API_KEY | Your OpenAI API key | - |
| GPT_MODEL | GPT model to use for analysis | gpt-4 |
| WHISPER_MODEL | Whisper model for transcription | whisper-1 |

## Features

- Automated Google Meet login and joining
- Audio recording of meetings
- Transcription using OpenAI's Whisper
- Meeting analysis including:
  - Abstract summary
  - Key points extraction
  - Action items identification
  - Sentiment analysis
- Automatic audio compression if size exceeds limit
- JSON output of meeting analysis

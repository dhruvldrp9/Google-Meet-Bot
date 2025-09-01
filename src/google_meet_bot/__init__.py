"""Google Meet Bot package.

Automate joining Google Meet, record audio, transcribe with Whisper, and summarize using GPT.
"""

from .record_audio import AudioRecorder
from .speech_to_text import SpeechToText
from .join_google_meet import JoinGoogleMeet

__all__ = [
    "AudioRecorder",
    "SpeechToText",
    "JoinGoogleMeet",
]



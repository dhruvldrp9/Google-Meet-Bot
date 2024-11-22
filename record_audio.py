import sounddevice as sd
from scipy.io.wavfile import write
import os
from dotenv import load_dotenv

load_dotenv()

class AudioRecorder:
    def __init__(self):
        self.sample_rate = int(os.getenv('SAMPLE_RATE', 44100))

    def get_audio(self, filename, duration):
        print("Recording...")
        recording = sd.rec(int(duration * self.sample_rate), samplerate=self.sample_rate, channels=2, dtype='int16')
        sd.wait()  # Wait until the recording is finished
        write(filename, self.sample_rate, recording)
        print(f"Recording finished. Saved as {filename}.")

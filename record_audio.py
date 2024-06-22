import sounddevice as sd
from scipy.io.wavfile import write


class AudioRecorder:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate

    def get_audio(self, filename, duration):
        print("Recording...")
        recording = sd.rec(int(duration * self.sample_rate), samplerate=self.sample_rate, channels=2, dtype='int16')
        sd.wait()  # Wait until the recording is finished
        write(filename, self.sample_rate, recording)
        print(f"Recording finished. Saved as {filename}.")
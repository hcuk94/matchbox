import pyaudio
import wave
from array import array
import config
import time

class Recording:
    def __init__(self):
        self.silence_threshold = config.recorder_silence_threshold
        self.chunk = config.recorder_chunk
        self.pyaudio_format = pyaudio.paInt16
        self.channels = config.recorder_channels
        self.rate = config.recorder_rate
        self.record_seconds = config.recorder_record_seconds
        self.wave_filename = 'recording' + str(time.time()) + '.wav'
        self.driver = pyaudio.PyAudio()
        self.frames = []
        self.stream = self.driver.open(
            format=self.pyaudio_format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk
        )

    def do_recording(self):
        for i in range(0, int(self.rate / self.chunk * self.record_seconds)):
            data = self.stream.read(self.chunk)
            self.frames.append(data)
        self.stream.stop_stream()
        self.stream.close()
        self.driver.terminate()

    def check_if_silent(self):
        data = array('h', self.stream.read(self.chunk))
        return max(data) < self.silence_threshold

    def save_file(self):
        wavfile = wave.open(self.wave_filename, 'wb')
        wavfile.setnchannels(self.channels)
        wavfile.setsampwidth(self.driver.get_sample_size(format))
        wavfile.setframerate(self.rate)
        wavfile.writeframes(b''.join(self.frames))
        wavfile.close()






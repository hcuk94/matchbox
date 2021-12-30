import io

import pyaudio
import wave
from array import array
import config
import time
import os


class Recording:
    def __init__(self):
        self.silence_threshold = config.recorder_silence_threshold
        self.chunk = config.recorder_chunk
        self.pyaudio_format = pyaudio.paInt16
        self.channels = config.recorder_channels
        self.rate = config.recorder_rate
        self.record_seconds = config.recorder_record_seconds
        self.wave_filename = 'recording' + str(time.time()) + '.wav'
        self.wave_file = io.BytesIO()
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
            data = self.stream.read(self.chunk, exception_on_overflow=False)
            self.frames.append(data)

    def check_if_silent(self):
        data = array('h', self.stream.read(self.chunk, exception_on_overflow=False))
        return max(data) < self.silence_threshold

    def close_stream(self):
        self.stream.stop_stream()
        self.stream.close()
        self.driver.terminate()

    def save_file(self):
        wavfile = wave.open(self.wave_filename, 'wb')
        wavfile.setnchannels(self.channels)
        wavfile.setsampwidth(self.driver.get_sample_size(self.pyaudio_format))
        wavfile.setframerate(self.rate)
        wavfile.writeframes(b''.join(self.frames))
        wavfile.close()

    def save_mem(self):
        wavfile = wave.open(self.wave_file, 'wb')
        wavfile.setnchannels(self.channels)
        wavfile.setsampwidth(self.driver.get_sample_size(self.pyaudio_format))
        wavfile.setframerate(self.rate)
        wavfile.writeframes(b''.join(self.frames))
        wavfile.close()

    def del_file(self):
        os.remove(self.wave_filename)


if __name__ == '__main__':
    test = Recording()
    print("Recording...")
    test.do_recording()
    print("Finished Recording")
    print("Silent: " + str(test.check_if_silent()))
    test.close_stream()
    test.save_mem()
    print("File saved...")




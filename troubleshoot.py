import pyaudio

pa = pyaudio.PyAudio()

print(pa.get_default_input_device_info)
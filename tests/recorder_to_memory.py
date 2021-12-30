import recorder

test = recorder.Recording()
print("Recording...")
test.do_recording()
print("Finished Recording")
print("Silent: " + str(test.check_if_silent()))
test.close_stream()
test.save_mem()
print("Saved to memory:")
print(test.wave_file)
print(test.wave_file.getbuffer())

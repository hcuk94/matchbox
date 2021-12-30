import recorder

test = recorder.Recording()
print("Recording...")
test.do_recording()
print("Finished Recording")
print("Silent: " + str(test.check_if_silent()))
test.close_stream()
test.save_file()
print("File saved...")
print(test.wave_filename)

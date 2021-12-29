import audd

# This one should match - Music by Joystock - https://www.joystock.org
file = 'sample-audio/joystock-popsicle.wav'
# This one should not
# file = 'sample-audio/walkthedog.wav'

test = audd.ApiReq(file)
output = test.match_file()

raw_output = test.result.text
processed_output = output

print("Raw output:")
print(raw_output)
print("Processed output:")
print(processed_output)

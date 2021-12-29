import acrcloud

mrt_api = 'acrcloud'
file = '../recording1640722157.6191108.wav'

test = acrcloud.ApiReq(file)
output = test.match_file()

raw_output = test.result.text
processed_output = output

print("Raw output:")
print(raw_output)
print("Processed output:")
print(processed_output)

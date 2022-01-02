import config
import io
import wave
from providers_match.audd import Audd

# This one should match
# file = 'sample-audio/joystock-popsicle.wav'
# This is not supposed to match, but may match to something else
# file = 'sample-audio/the_depressed_elephant_pt1.wav'
# This is just some noise and should not match
file = 'sample-audio/generic-noise.wav'

provider = Audd(config.providers_match['Audd']['config'])

wav_data = io.BytesIO()
with wave.open(wav_data, 'wb') as w:
    with wave.open(file, 'rb') as r:
        w.setparams(r.getparams())
        w.writeframes(r.readframes(r.getnframes()))
    lookup = provider.lookup_sample(wav_data.getbuffer())

print("Status: " + str(lookup.response))
print("Processed output: " + str(lookup))

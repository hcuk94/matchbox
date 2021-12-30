import config
from providers.acoustid import AcoustID

# This one should match - Music by Joystock - https://www.joystock.org
file = 'sample-audio/joystock-popsicle.wav'
# This one should not
# file = 'sample-audio/walkthedog.wav'


acoustid = AcoustID(config.audd_config)
output = acoustid.lookup_sample(file)

print("Processed output:" + str(output))

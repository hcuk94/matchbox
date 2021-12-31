import config
from providers_match.acrcloud import ACRCloud

# This one should match - Music by Joystock - https://www.joystock.org
# file = 'sample-audio/joystock-popsicle.wav'
# This one should not
file = 'sample-audio/the_depressed_elephant_pt1.wav'


audd = ACRCloud(config.acrcloud_config)
output = audd.lookup_sample(file)

print("Processed output:" + str(output))

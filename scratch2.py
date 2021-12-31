import io
from inspect import isclass
from pkgutil import iter_modules
from pathlib import Path
import config
import wave
from importlib import import_module
from providers_match import LookupProviderInterface

# iterate through the modules in the current package
package_dir = 'providers_match'
for (_, module_name, _) in iter_modules([package_dir]):

    # import the module and iterate through its attributes
    module = import_module(f"providers_match.{module_name}")
    for attribute_name in dir(module):
        attribute = getattr(module, attribute_name)

        if isclass(attribute):
            # Add the class to this package's variables
            globals()[attribute_name] = attribute

# classes = LookupProviderInterface.__subclasses__()
# print(classes)
# for provider in classes:
#     provider_config_name = str(provider.__name__).lower()
#     print(provider_config_name)

    # lookup_provider = provider(config.providers_match[provider_config_name]['config'])

providers_match = sorted(config.providers_match, key=lambda x: config.providers_match[x]['priority'])
print(providers_match)
for provider_config in providers_match:
    if config.providers_match[provider_config]['enabled'] is True:
        print(provider_config)
        provider_class = globals()[provider_config]
        lookup_provider = provider_class(config.providers_match[provider_config]['config'])

    #    file = 'tests/sample-audio/the_depressed_elephant_pt2.wav'
    #    file = 'tests/sample-audio/walkthedog.wav'
        file = 'tests/sample-audio/joystock-popsicle.wav'
        wav_data = io.BytesIO()
        with wave.open(wav_data, 'wb') as w:
            with wave.open(file, 'rb') as r:
                w.setparams(r.getparams())
                w.writeframes(r.readframes(r.getnframes()))
            lookup = lookup_provider.lookup_sample(wav_data.getbuffer())
            print(lookup.response)

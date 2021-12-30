from inspect import isclass
from pkgutil import iter_modules
from pathlib import Path
from importlib import import_module

# iterate through the modules in the current package
package_dir = 'providers'
for (_, module_name, _) in iter_modules([package_dir]):

    # import the module and iterate through its attributes
    module = import_module(f"providers.{module_name}")
    for attribute_name in dir(module):
        attribute = getattr(module, attribute_name)

        if isclass(attribute):
            # Add the class to this package's variables
            globals()[attribute_name] = attribute

from providers import LookupProviderInterface

classes = LookupProviderInterface.__subclasses__()

for provider in classes:
    print(provider.__name__)
    lookup_provider = provider
    lookup_provider.lookup_sample()
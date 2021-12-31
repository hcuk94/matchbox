import config
import lastfm
import providers
import recorder
import logging
from time import sleep
from inspect import isclass
from pkgutil import iter_modules
from importlib import import_module

# Import Match Providers
package_dir = 'providers'
for (_, module_name, _) in iter_modules([package_dir]):
    module = import_module(f"providers.{module_name}")
    for attribute_name in dir(module):
        attribute = getattr(module, attribute_name)
        if isclass(attribute):
            globals()[attribute_name] = attribute


def do_match(sample):
    providers_match = sorted(config.providers_match, key=lambda x: config.providers_match[x]['priority'])
    result = {
        'status': providers.LookupResponseCode.NO_RESULT
    }
    for provider_config in providers_match:
        if config.providers_match[provider_config]['enabled'] is True:
            logging.debug("Using match provider %s", provider_config)
            provider_class = globals()[provider_config]
            lookup_provider = provider_class(config.providers_match[provider_config]['config'])
            lookup = lookup_provider.lookup_sample(sample)
            if lookup.response == providers.LookupResponseCode.SUCCESS:
                logging.debug("Successful match.")
                result['lookup'] = lookup
                result['status'] = lookup.response
                return result
            else:
                logging.debug("Error returned from match interface: %s", lookup.response)
    return result


if __name__ == '__main__':
    logging.basicConfig(level=config.log_level, filename=config.log_filename,
                        filemode="a+", format="%(asctime)-15s %(levelname)-8s %(message)s")
    last_notify = {}
    logging.info("Application Started.")

    while True:
        logging.debug("Initialising Recorder")
        recording = recorder.Recording()
        logging.debug("Recording {} seconds of audio...".format(config.recorder_record_seconds))
        recording.do_recording()
        logging.debug("Checking if recording is silent...")
        is_silent = recording.check_if_silent()

        if is_silent is False:
            logging.debug("Recording is not silent.")
            logging.debug("Saving to memory...")
            recording.save_mem()
            file = recording.wave_file.getbuffer()
            logging.debug("Passing to match function...")
            track_match = do_match(file)

            if track_match['status'] != providers.LookupResponseCode.SUCCESS:
                logging.warning("Track could not be identified by any configured matching provider")
            else:
                this_notify = {
                    'title': track_match['lookup'].title,
                    'artist': track_match['lookup'].artist
                }
                if this_notify != last_notify:
                    logging.debug("Music data does not match previous notify, so we should notify.")
                    logging.debug("Initialising notify agent...")
                    notify = lastfm.LastFM(track_match['lookup'])
                    logging.debug("Updating 'now playing'...")
                    notify.now_playing()
                    logging.debug("Notifying track...")
                    notify.notify()
                    logging.info("Successfully notified {} by {} from album {}"
                                 .format(track_match['lookup'].title, track_match['lookup'].artist, track_match['lookup'].album))
                    last_notify = this_notify
                else:
                    logging.debug("Music data is same as previous notify, so we will not notify.")
            recording.close_stream()
        else:
            logging.info("Recording was deemed as silent, no action will be taken.")
            recording.close_stream()
        logging.debug("Sleeping... next run in {} seconds".format(config.retrigger_time))
        sleep(config.retrigger_time)

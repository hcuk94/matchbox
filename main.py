import config
import lastfm
import providers
import recorder
import logging
from time import sleep

from providers.acrcloud import ACRCloud
from providers.audd import Audd

if __name__ == '__main__':
    logging.basicConfig(level=config.log_level, filename=config.log_filename
                        , filemode="a+", format="%(asctime)-15s %(levelname)-8s %(message)s")
    last_scrobble = {}
    logging.info("Application Started")

    acrcloud = ACRCloud(config.acrcloud_config)
    audd = Audd(config.audd_config)

    while True:
        logging.debug("Initialising Recorder")
        recording = recorder.Recording()
        logging.debug("Recording {} seconds of audio...".format(config.recorder_record_seconds))
        recording.do_recording()
        logging.debug("Recording complete.")
        logging.debug("Checking if recording is silent...")
        is_silent = recording.check_if_silent()
        if is_silent is False:
            logging.debug("Recording is not silent.")
            # logging.debug("Saving temporary file...")
            # recording.save_file()
            # file = recording.wave_filename
            # logging.debug("File saved: {}".format(file))
            recording.save_mem()
            file = recording.wave_file.read()
            logging.debug("Checking MRT API option...")
            if config.mrt_api == 'acrcloud':
                logging.debug("Matching track using API {}".format(config.mrt_api))
                track_match = acrcloud.lookup_sample(file)
            else:
                logging.debug("Matching track using API {}".format(config.mrt_api))
                track_match = audd.lookup_sample(file)
            logging.debug("MRT API Output: {}".format(track_match))
            if track_match.response != providers.LookupResponseCode.SUCCESS:
                logging.error("MRT API {} encountered error: {}".format(config.mrt_api, track_match.response))
            else:
                this_scrobble = {
                    'title': track_match.title,
                    'artist': track_match.artist
                }
                if this_scrobble != last_scrobble:
                    logging.debug("Music data does not match previous scrobble, so we should scrobble.")
                    logging.debug("Initialising scrobbler...")
                    scrobble = lastfm.Scrobbler(track_match)
                    logging.debug("Updating 'now playing'...")
                    scrobble.now_playing()
                    logging.debug("Scrobbling track...")
                    scrobble.scrobble()
                    logging.info("Successfully scrobbled {} by {} from album {}"
                                 .format(track_match.title, track_match.artist, track_match.album))
                    last_scrobble = this_scrobble
                else:
                    logging.debug("Music data is same as previous scrobble, so we will not scrobble.")
            recording.close_stream()
            logging.debug("Deleting temporary file {}...".format(file))
            recording.del_file()
        else:
            logging.info("Recording was deemed as silent, no action will be taken.")
            recording.close_stream()
        logging.debug("Sleeping... next run in {} seconds".format(config.retrigger_time))
        sleep(config.retrigger_time)

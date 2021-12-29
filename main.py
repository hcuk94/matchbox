import config
import lastfm
import audd
import acrcloud
import recorder
import logging
from time import sleep

if __name__ == '__main__':
    logging.basicConfig(level=config.log_level, filename=config.log_filename
                        , filemode="a+", format="%(asctime)-15s %(levelname)-8s %(message)s")
    last_scrobble = {}
    logging.info("Application Started")
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
            logging.debug("Saving temporary file...")
            recording.save_file()
            file = recording.wave_filename
            logging.debug("File saved: {}".format(file))
            logging.debug("Checking MRT API option...")
            if config.mrt_api == 'acrcloud':
                logging.debug("Matching track using API {}".format(config.mrt_api))
                track_match = acrcloud.ApiReq(file)
            else:
                logging.debug("Matching track using API {}".format(config.mrt_api))
                track_match = audd.ApiReq(file)
            match_result = track_match.match_file()
            logging.debug("MRT API Output: {}".format(match_result))
            if match_result['status'] != 0:
                logging.error("MRT API {} encountered error: {}".format(config.mrt_api, match_result['status']))
            else:
                if match_result != last_scrobble:
                    logging.debug("Music data does not match previous scrobble, so we should scrobble.")
                    logging.debug("Initialising scrobbler...")
                    scrobble = lastfm.Scrobbler(match_result)
                    logging.debug("Updating 'now playing'...")
                    scrobble.now_playing()
                    logging.debug("Scrobbling track...")
                    scrobble.scrobble()
                    logging.info("Successfully scrobbled {} by {} from album {}"
                                 .format(match_result['title'], match_result['artist'], match_result['album']))
                    last_scrobble = match_result
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

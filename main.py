import lastfm
import audd
import recorder

if __name__ == '__main__':
    recording = recorder.Recording()
    recording.do_recording()
    recording.check_if_silent()
    if recording.check_if_silent() is False:
        recording.save_file()
        file = recording.wave_filename
        track_match = audd.ApiReq(file)
        match_result = track_match.match_file()
        scrobble = lastfm.Scrobbler(match_result)
        scrobble.now_playing()
        scrobble.scrobble()
        print("Successfully scrobbled {} by {} from album {}".format(match_result['title'],
                                                                     match_result['artist'], match_result['album']))
        recording.close_stream()
        recording.del_file()
    else:
        print("Recording has been deemed silent, so we will do nothing.")
        recording.close_stream()


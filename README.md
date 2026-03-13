# MatchBox

MatchBox listens to an audio source of your choice, tries to identify the currently playing song, and forwards the result to one or more downstream services such as Last.fm, Libre.fm, ListenBrainz, or Telegram. It is designed for people who play music physically or outside a streaming app but still want "now playing" updates or scrobbles.

Originally designed as a means to 'scrobble' my vinyl records to last.fm, it now adopts a modular design, allowing numerous services to be notified upon a successful match of a track.

# What it does

-   Records a short audio sample from the default input device.
-   Checks whether the captured audio appears silent.
-   Sends the sample to a configured music-identification provider.
-   If a song is identified, sends:
    -   a full notification/scrobble when the track changes
    -   a keepalive / "now playing" update while the same track is still
        detected
-   Sleeps for a configured interval, then repeats forever.

# Supported providers

## Match providers

-   ACRCloud
-   AudD

## Notify providers

-   LastFM
-   LibreFM
-   ListenBrainz
-   Telegram

# Wiki
For information on installation, and setup of providers, please refer to the Wiki documentation below.

- [Getting Started](https://github.com/hcuk94/matchbox/wiki/Getting-Started)
- [High-Level Design](https://github.com/hcuk94/matchbox/wiki/High%E2%80%90level-Design)
- [Match Providers](https://github.com/hcuk94/matchbox/wiki/Match-Providers)
- [Notify Providers](https://github.com/hcuk94/matchbox/wiki/Notify-Providers)
- [Troubleshooting](https://github.com/hcuk94/matchbox/wiki/Troubleshooting)
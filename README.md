# MatchBox

MatchBox listens to audio from your machine, tries to identify the currently playing song, and forwards the result to one or more downstream services such as Last.fm, Libre.fm, ListenBrainz, or Telegram. It is designed for people who play music physically or outside a streaming app but still want "now playing" updates or scrobbles.

Originally designed as a means to 'scrobble' my vinyl records to last.fm, it now adopts a modular design, allowing numerous services to be notified upon a successful match of a track.

------------------------------------------------------------------------

# What it does

-   Records a short audio sample from the default input device.
-   Checks whether the captured audio appears silent.
-   Sends the sample to a configured music-identification provider.
-   If a song is identified, sends:
    -   a full notification/scrobble when the track changes
    -   a keepalive / "now playing" update while the same track is still
        detected
-   Sleeps for a configured interval, then repeats forever.

------------------------------------------------------------------------

# Supported providers

## Match providers

-   ACRCloud
-   AudD

ACRCloud has a free tier which allows 100 match requests per day.

## Notify providers

-   LastFM
-   LibreFM
-   ListenBrainz
-   Telegram

------------------------------------------------------------------------

# High‑level design

At startup, MatchBox imports provider classes dynamically from
configured package directories:
- A 'match' provider is a service which receives recorded audio and attempts to match it to a known musical work.
- A 'notify' provider will receive notification of each matched work.

Each cycle performs:

1.  Record audio sample
2.  Detect silence
3.  Attempt track match using match providers (priority order, until match is found or all providers exhausted)
4.  If successful, notify downstream services (all which are enabled in config)
5.  Sleep for configured interval
6.  Repeat

Pipeline:

    Audio Input → Recorder → Silence Detection → Match Provider → Track Result → Notify Providers

------------------------------------------------------------------------

# Requirements

As a python application, Matchbox is pretty flexible in terms of where you want to run it. My personal setup uses a Raspberry Pi Model 3B with a USB audio card for the input.

High-level requirements are:
-   Python 3
-   Working microphone or audio input device
-   Internet access for provider APIs

Python dependencies:

-   requests
-   pyaudio
-   pylast
-   pylistenbrainz

------------------------------------------------------------------------

# Installation

Clone the repository and install dependencies:

``` bash
git clone https://github.com/hcuk94/matchbox.git
cd matchbox

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

NB: On Mac devices a manual install of PortAudio is required, this can be done via Homebew with
``brew install portaudio``

Copy the sample config:

``` bash
cp config_sample.py config.py
```

Edit `config.py` with your provider credentials.

Start MatchBox with:

``` bash
python main.py
```
Consider running as a service to avoid the need to manually start/monitor the application.

------------------------------------------------------------------------

# Usage

1.  Configure at least one **match provider**
2.  Configure at least one **notify provider**
3.  Start the application
4.  Play music that your microphone/input can hear

Logs will indicate:

-   recording start
-   silence detection
-   provider lookup
-   track match
-   notification activity

------------------------------------------------------------------------

# Troubleshooting

## config module not found

Ensure:

    config_sample.py → config.py

## PyAudio installation issues

PyAudio depends on **PortAudio** and may require system audio libraries
to be installed, especially on Mac devices.

## No tracks detected

Check:

-   microphone input
-   silence threshold
-   provider credentials
-   provider priority configuration

## Notifications not appearing

Verify:

-   provider enabled
-   credentials correct
-   API tokens valid

------------------------------------------------------------------------
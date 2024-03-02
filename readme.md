# tune-sniffer

A Python project that utilizes both Discogs' and Spotify's API to get some new music reccomendations for people who already know what they're looking for

## Features (partially implemented)

- provide a style as argument when running the script to generate 10 random tracks from 10 random albums that fit the specified style (f.e. `python discogs.py prog+rock`)
- those 10 tracks will be looked up on Spotify and inserted into a newly generated playlist
- on playlist start, the tracks will be automatically skipped every 30sec. while checking whether they have been favorite'd (if so, the timer will be suspended for the duration of the song)

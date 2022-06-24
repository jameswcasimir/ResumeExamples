# Hey! Here is some code I wrote
You're thinking about hiring me, and you came here hoping to see some examples of code I have written. 

I have spent a lot of time creating automated services that make my life easier

# Why do these scripts exist?
A big project of mine, is an automated media system

I have a very large video media library, viewable through a service called Plex

I created a project to automate tasks involved with maintaining such a system
These are scripts that fill in the gaps left by other services

* Finds media to obtain (from youtube and such)
* Downloads Media
* Decides when to upgrade media quality (if available)
* Sorts Media into a consistent file structure
* Transcodes media into consistent video format
* Downloads subtitles for media
* Tags media based on a number of criteria

This is a selection of some functionality of that system

# Example Scripts
* YakScripts.sh
  * This is a launcher for this project
  * Most of these scripts are called from cron, this makes that simple
  * It also sets variables like the pythonpath, implements logging
  * I left this more or less unaltered, so that you can see everything it does
* PauseDownloader_WithPlexActivity
  * There are 2 processes on my server which consume a lot of cpu usage
  * Plex, and my Newsgroup downloader
  * I wrote this script, to pause the downloader when plex is active
* FixVideoTitleMetadata.py
  * This script exists because sometimes the title of a video I was watching was wrong on my plex server. 
  * This occurs most of the time because the file has some weird value encoded in the title metadata field
  * So what all this means is that this script:
    * Identifies when a video has a title mismatch
    * Determines correct title for video
    * Re-encodes the video file with the correct title
* SearchForUpcomingMovies.py
  * This script was created to keep a concise list of all upcoming movies
  * This is tracked in a system called "Radarr"
  * It gets upcoming movies from the TmDB API
  * So what this script does:
    * Queries TmDB for upcoming movies
    * Sorts through paginated results, adds movie to Radarr
      * If a movie already exists in Radarr, nbd.
    * Sends the user a fancy notification that a list of movies were added to the system

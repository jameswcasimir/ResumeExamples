# ResumeExamples
This repository is meant to showcase some scripts that I have created.


# Example Scripts:
* YakScripts.sh
  * This is a launcher for this project
  * Most of these scripts are called from cron, this makes that simple
  * It also sets variables like the pythonpath, implements logging
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

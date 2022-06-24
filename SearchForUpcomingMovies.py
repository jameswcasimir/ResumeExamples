import datetime
import json
from datetime import date
import requests

import project_secrets
import globalData

from Notifications.Pushover import pushover
import Agora.Radarr.radarr as radarr

addedMovies = []


# generates api request string for Radarr
def getRadarrApiRequestString(endpoint):
    radarr_ip = globalData.addresses["local_ip"] + ":" + globalData.ports["radarr"]
    api_key = project_secrets.api_keys["radarr"]

    return "http://" + radarr_ip + "/api/v3/" + endpoint + "?apikey=" + api_key


# generates api request string for TmDB
def getTheMovieDBRequestString(inputPage):
    themoviedb_ip = "https://api.themoviedb.org/3/movie/now_playing"
    api_key = project_secrets.api_keys["themoviedb"]

    result = themoviedb_ip + "?api_key=" + api_key + "&language=en-US&page=" + str(inputPage)
    return result


# adds the movie to radarrs list
def addMovieToRadarr(movie):
    title = movie["title"]
    tmdb_id = movie["id"]

    body = json.dumps({
        "title": title,
        "qualityProfileId": 1,
        "tmdbid": tmdb_id,
        "monitored": "true",
        "rootFolderPath": "/movies/"
    })

    radarr_request = getRadarrApiRequestString("movie")
    response = requests.post(radarr_request, data=body)
    return response


# creates a fancy notification to send to users
def createAddedMoviesNotificationsString(addedMovies):
    result = ""
    for movie in addedMovies:
        result += movie + "\n"
    return result


try:
    # this loads all recently released movies
    # we are going to check their release dates against the loop below
    tmdb_response = json.loads(requests.get(getTheMovieDBRequestString(1)).text)

    j = 60
    while j < 200:
        today = date.today() + datetime.timedelta(days=-1 * j)
        formattedDate = today.strftime("%Y-%m-%d")
        print(formattedDate)

        pages = tmdb_response["total_pages"]  # tmdb returns ~50 pages of 7 or 8 results each

        i = 1  # pages start at 1 not 0 *sigh*
        # loops through all pages, this happens very quickly
        while i <= pages:
            tmbd_page_response = json.loads(requests.get(getTheMovieDBRequestString(i)).text)
            page_results = tmbd_page_response["results"]
            page = tmbd_page_response["page"]

            # loops through all movies, checks if movie release date is equal to the check date
            for movie in page_results:  # filters out non-english movies (sorry)
                if movie["release_date"] == formattedDate and movie["original_language"] == "en":
                    response = radarr.add_movie(movie["id"])
                    print("Adding movie: " + movie["title"])

                    addedMovies.append(movie["title"])

            i += 1

        #we found some new movies! send the user a fancy notification
        notificationsString = createAddedMoviesNotificationsString(addedMovies)
        if len(addedMovies) > 0:
            pushover.sendMessage("Found " + str(len(addedMovies)) + " Upcoming Movies", notificationsString)
        else:
            print("No Movies to add... Exiting...")

        j += 1

except Exception as e:
    pushover.sendMessage("Unable to add Upcoming Movies", e)

import json
import os
import re
import xml.etree.ElementTree as ET
import requests

import globalData as globalData
import project_secrets



movies_dir = "/mnt/pack/Media/Movies/"


#gets all movies from plex database
def getPlexMovies():
    plexUrl="http://" + globalData.addresses["local_ip"] + ":" + globalData.ports["plex"]
    plexUrl+="/library/sections/1/all?X-Plex-Token=" + project_secrets.api_keys["plex"]

    response = requests.get(plexUrl)._content

    movies_object = ET.fromstring(response)
    return movies_object

#this takes a movie id (key) and gets details about the movie
#these details include the path, file info, runtime, format
def getPlexMovieInfo(key):
    plexUrl="http://" + globalData.addresses["local_ip"] + ":" + globalData.ports["plex"]
    plexUrl+= str(key) + "?X-Plex-Token=" + project_secrets.api_keys["plex"]

    response = requests.get(plexUrl)

    movies_object = ET.fromstring(response._content)
    return movies_object

#fetches the title as tmd reports it
def getTmdbTitle(id):
    tmdbIdUrl="https://api.themoviedb.org/3/movie/" + str(id)
    tmdbIdUrl += "?api_key=" + project_secrets.api_keys["themoviedb"]

    response = json.loads(requests.get(tmdbIdUrl).text)
    return response["title"]

#this gets the title as the file reports it
def getTitleFromFile(details):
    fileWithYear = getTitleWithYearFromFile(details)
    title = re.search(r"(.*)(\(\d{4}\))", fileWithYear).group(1) #gets just the title
    return title.strip()

def getTitleWithYearFromFile(details):
    filepath = getFilePath(details)
    fileWithYear = filepath.split("/")[2]  #its the 3rd element with '/'s
    return fileWithYear

#extracts filepath from file details
def getFilePath(details):
    filepath = details[0][0][0].attrib["file"] #filepath from plex metadata
    return filepath

#plex returns path from docker image
#this trims that path, and replaces it with movies dir
def getAbsoluteFilePath(details):
    filepath = getFilePath(details)
    filepath = filepath.replace("/movies/", "")
    return movies_dir + filepath

#sometimes plex tags movies with other dbs
#this checks if this has happened
def idIsTmdbID(id):
    tag = re.search(r"^\w*", id).group()
    return tag == "tmdb"

#gets the Tmdb id of the movie
#this is used commonly to tag movies
def getTmdbID(details):
    success = False
    for child in details[0]:
        if(child.tag == "Guid"):
            if(idIsTmdbID(child.attrib["id"])):
                id = re.search(r"\w*$", child.attrib["id"]).group()
                return id
    if( not success ): return 0


def processTitle(title):
    title = title.strip()
    title = title.replace(":", "")
    title = title.replace("(", "")
    title = title.replace(")", "")
    title = title.replace("\\", "")
    title = title.replace("{", "")
    title = title.replace("}", "")
    title = title.replace("[", "")
    title = title.replace("]", "")
    title = title.replace("/", "")
    title = title.replace(".", "")
    title = title.replace(",", "")
    title = title.replace("-", "")
    title = title.replace("?", "")
    title = title.replace("!", "")
    title = title.replace("#", "")
    title = title.replace("$", "")
    title = title.replace(" ", "")
    title = title.lower()
    return title

def titleIsSimiliar(plexTitle, compareTitle):
    plexTitle = processTitle(plexTitle)
    compareTitle = processTitle(compareTitle)

    return (plexTitle == compareTitle)



def fixTitleMetadata(filepath, title):
    print("Adding metadata to file " + filepath)

    fileWithoutExtension = filepath.split(").")[0] + ")"
    fileExtension = filepath.split(").")[1]



    os.system("ffmpeg -i \"" + filepath + "\" -vcodec copy -acodec copy -metadata title=\"" + title + "\" \"" + fileWithoutExtension + "_new." + fileExtension + "\"")
    print("Removing Original File")
    os.system("rm -v \"" + filepath + "\"")
    print("Replacing Original File")
    os.system("mv -v \"" + fileWithoutExtension + "_new." + fileExtension + "\" \"" + filepath + "\"")

    print()
    print("DONE")
    print()
    print()
    print()


#Checks that all movies exist with the correct title on Plex
def processMovies(movies):
    for movie in movies:
        key = movie.attrib["key"]
        #gets the title as plex reports it
        plexTitle = movie.attrib["title"]

        #plex stores details about the file (path, size, type, etc)
        plex_details = getPlexMovieInfo(key)


        tmdbid=getTmdbID(plex_details)
        if(tmdbid == 0):
            fileTitle = getTitleFromFile(plex_details)
            if( not titleIsSimiliar(plexTitle, fileTitle)):
                print()
                print("Found a title mismatch")
                print("Plex: " + plexTitle)
                print("File: " + fileTitle)
                print()
                print()

                filepath=getAbsoluteFilePath(plex_details)
                newTitleMetadata = getTitleFromFile(plex_details)
                fixTitleMetadata(filepath, newTitleMetadata)
        else:
            tmdbTitle = getTmdbTitle(tmdbid)
            if( not titleIsSimiliar(plexTitle, tmdbTitle)):
                print()
                print("Found a title mismatch")
                print("Plex: " + plexTitle)
                print("File: " + tmdbTitle)
                print()
                print()

                filepath=getAbsoluteFilePath(plex_details)
                fixTitleMetadata(filepath, tmdbTitle)





movies = getPlexMovies()
processMovies(movies)
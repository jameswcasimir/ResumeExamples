
import requests


import Agora.NzbGet.nzbget as nzbGet

import globalData
import project_secrets


try:
    #queries tautulli (plex management software) for activity stats
    tautulli_ip = globalData.yakshak_sites["tautulli"]
    api_key = project_secrets.api_keys["tautulli"]
    response = requests.get(tautulli_ip + "/api/v2?apikey=" + api_key + "&cmd=get_activity").json()

    streamCount = response["response"]["data"]["stream_count"]

    if (int(streamCount) > 0):
        print("Active stream found... Pausing NzbGet")
        nzbGet.pause()
    else:
        print("No active stream found... Resuming NzbGet")
        nzbGet.resume()
except Exception as e:
    print(e)


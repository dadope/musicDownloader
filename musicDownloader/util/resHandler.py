import glob
import json
from urllib.parse import urlparse, parse_qs

from ..constants import RESOURCES_DIR, logger
from ..models import playlist

def getPlaylists() -> list:
    """
    Loads all playlists

    :return: a list of all playlists
    """
    lst = [playlist.Playlist.fromJson(json.load(open(file, "r"))) for file in glob.glob(str(RESOURCES_DIR/ "playlists"/ "*.json"))]

    if len(lst) == 0:
        print("No playlists could be found, fatal!")
        logger.critical("No playlists could be found, fatal!")
        exit(1)

    return lst

def getVideoId(url:str):
    if "https://" not in url:
        url = "https://" + url

    query = urlparse(url)
    videoId = None

    if query.hostname == 'youtu.be':
        videoId = query.path[1:]
    elif query.hostname in ('www.youtube.com', 'youtube.com', 'music.youtube.com'):
        if query.path == '/watch': videoId = parse_qs(query.query)['v'][0]
        if query.path[:7] == '/embed/': videoId = query.path.split('/')[2]
        if query.path[:3] == '/v/': videoId = query.path.split('/')[2]
    else:
        logger.critical(f"Could not extract videoId from the provided url: {url}")
        print(f"Could not extract videoId from the provided url: {url}")
        return url

    return videoId
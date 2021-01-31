import glob
import json
import logging
from os.path import basename
from pathlib import Path

playlist_dir = Path()

def makePlaylistsInMusicFolder(music_dir):
    for playlist in glob.glob(str(music_dir / "*")):
        name = basename(playlist)
        genres = [name]
        directories = [playlist]

        createPlaylist(name, genres, directories)

def createPlaylist(name:str, genres:list, directories:list, ):
    jsonString = \
    {
        "name": name,
        "genres": genres,
        "directories": directories
    }

    file = open(str(playlist_dir / (name + ".json")), "w")
    json.dump(jsonString, file)

def initialSetup(_user_dir:Path, RESOURCES_DIR:Path, USER_DATA_DIR:Path):
    global playlist_dir

    playlist_dir = RESOURCES_DIR / "playlists"
    playlist_dir.mkdir(parents=True)

    RESOURCES_DIR.mkdir(parents=True, exist_ok=True)
    USER_DATA_DIR.mkdir(parents=True, exist_ok=True)

    music_dir = _user_dir / "Music"
    makePlaylistsInMusicFolder(music_dir)

def setup_logger(name, log_file, formatter_text):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)
    handler.setFormatter(logging.Formatter(formatter_text))

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    return logger
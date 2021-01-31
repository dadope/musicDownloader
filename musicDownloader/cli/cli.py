import questionary

from pathlib import Path

from ..util import resHandler

def selectPlaylist():
    playlists = resHandler.getPlaylists()
    playlistNames = [x.name for x in playlists]

    if len(playlists) == 1:
        return playlists[0]

    index = questionary.select(
        "Select a playlist:",
        choices=playlistNames,
    ).ask()
    print()

    return playlists[playlistNames.index(index)]

def selectGenre(genres: list):
    if len(genres) == 1:
        return genres[0]

    return questionary.select(
        "Select a genre:",
        choices=genres
    ).ask()

def selectDirectory(directories:list) -> Path:
    if len(directories) == 1:
        return Path(directories[0])

    return Path(questionary.select(
        "Select a a directory:",
        choices = directories
    ).ask())

def confirmArtist(artist:str):
    if artist:
        choice = questionary.confirm(
            str(f"Is this the artist of the song? {artist}")
        ).ask()

        if choice:
            return artist
    else:
        print("Could not find any indication towards the artist!")

    return input("Please input the name of the artist:\n")


def confirmTitle(title:str):
    if title:
        choice = questionary.confirm(
            str(f"Is this the title of the song? {title}")
        ).ask()

        if choice:
            return title
    else:
        print("Could not find any indication towards the title!")

    return input("Please input the title of the song:\n")


def confirmAlbum(album:str):
    if album:
        choice = questionary.confirm(
            str(f"Is this the album of the song? {album}")
        ).ask()

        if choice:
            return album
    else:
        print("Could not find any indication towards the album!")

    return input("Please input the album of the song:\n")

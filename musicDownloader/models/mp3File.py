import eyed3
import youtube_dl

from pathlib import Path
from os import remove, rename

from os.path import basename
from urllib.request import urlretrieve

from .playlist import Playlist as pl
from ..constants import logger, url_logger, TMP_DIR

from ..cli.cli import \
    confirmArtist, confirmTitle, confirmAlbum, selectPlaylist, selectGenre, selectDirectory
from ..util.resHandler import getVideoId, getPlaylists


class mp3File:
    def __init__(self, url: str, playlist: (pl, str), endFilename:str):

        self.url = self._cleanup_url(url)

        if not playlist:
            self.playlist = selectPlaylist()

        elif type(playlist) == str:
            try:
                self.playlist = [x for x in getPlaylists() if x.name == playlist][0]
            except IndexError:
                selectPlaylist()
        else:
            self.playlist = playlist

        self.genre = selectGenre(self.playlist.genres)
        self.endDir = selectDirectory(self.playlist.directories)

        self.title = None
        self.album = None
        self.artist = None
        self.guessTitle = None
        self.guessArtist = None
        self.guessAlbum = self.genre

        self.audiofile = None

        self.file = None
        self.currDir = TMP_DIR
        self.currFilename = None
        self.endFilename = endFilename

        url_logger.info((self.url, self.endFilename))

    def _mp3_check(self, name:str) -> str:
        if name[-4:] != ".mp3":
            name = name + ".mp3"

        return name

    # TODO: make video playlist downloads possible (the metadata stripping also deletes any playlist references)
    def _cleanup_url(self, url:str) -> str:
        """
        Eliminates metadata that could interfere with the download,
        also strips playlists information...

        :param url: url to cleanup
        :return: cleaned up url
        """
        videoId = getVideoId(url)

        return "https://www.youtube.com/watch?v=" + videoId

    def _download_and_convert(self):
        """
        Downloads the video to TMP_DIR and converts it to mp3,
        also guesses from youtube-metadata the artist, title and album
        """

        logger.info("Downloading " + self.url)
        print("Downloading", self.url + "\n")

        _ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
            "outtmpl": str(TMP_DIR / "%(title)s.%(ext)s")
        }

        with youtube_dl.YoutubeDL(_ydl_opts) as ydl:
            info_dict = ydl.extract_info(self.url, download=True)
            self.guessArtist = info_dict["artist"]
            self.guessTitle = info_dict["alt_title"]
            self.guessAlbum = info_dict["album"] if None else self.genre

            # removes filetype returned by youtube-dl as it does not correspond to the actual filetype of the file,
            # but rather the downloaded audio codec (eg. m4a) before ffmpeg converts it
            self.file = ydl.prepare_filename(info_dict).rsplit('.', 1)[0] + ".mp3"
            self.currFilename = basename(self.file)

            logger.info("Downloaded " + self.file)
            print("Downloaded " + self.file + "\n\n")

        self.audiofile = eyed3.load(self.file)

    def _download_and_add_cover(self):
        """
        Downloads the video icon from youtube, stores it in TMP_DIR/thumb.jpg,
        adds the image to the file-metadata and then deletes the original image
        """

        if not self.audiofile:
            print("File could not be found!, exiting")
            logger.critical("Audiofile doesnt exist!")
            exit(1)

        if self.audiofile.tag is None: self.audiofile.initTag()

        videoId = getVideoId(self.url)
        thumbUrl = "http://img.youtube.com/vi/%s/0.jpg" % videoId
        imgFile = str(TMP_DIR / "thumb.jpg")
        urlretrieve(thumbUrl, imgFile)

        logger.info("Adding cover to " + self.file)

        self.audiofile.tag.images.set(3, open(imgFile, 'rb').read(), 'image/jpeg')
        self.audiofile.tag.images.set(2 , open(imgFile, 'rb').read(), 'image/jpeg')

        self.audiofile.tag.save()

        remove(imgFile)

    def download(self) -> str:
        """
        public download function:
        downloads the provided url and adds metadata,
        then moves the file to the selected directory

        :return: file-path
        """
        self._download_and_convert()
        self._download_and_add_cover()
        self._addMetadata()
        self.move(self.endDir)
        self.rename(self.endFilename)

        url_logger.info((self.url, self.file))
        self.printMetadata()

        return self.file

    def _addMetadata(self):
        """
        Gets user confirmation on file metadata and then adds it,
        also sets enfFilename to "<artist> - <title>.mp3" if not set in beforehand
        """

        if self.audiofile.tag is None:
            self.audiofile.initTag()

        self.artist = confirmArtist(self.guessArtist).strip()
        self.title = confirmTitle(self.guessTitle).strip()
        self.album = confirmAlbum(self.guessAlbum).strip()

        self.audiofile.tag.title = self.title
        self.audiofile.tag.genre = self.genre
        self.audiofile.tag.album = self.album
        self.audiofile.tag.artist = self.artist

        self.audiofile.tag.save()

        if self.endFilename is None:
            self.endFilename = f"{self.artist} - {self.title}.mp3"

    def move(self, directory:Path) -> str:
        """
        Moves the current file to a given directory

        :param directory: directory to move the file to
        :return: moved file-path
        """

        self.currDir = directory
        file = str(directory / basename(self.file))

        rename(self.file, file)

        self.file = file
        return self.file

    def rename(self, filename:str) -> str:
        """
        Renames the current file to a given filename

        :param filename: filename to rename to
        :return: renamed file-path
        """
        self.currFilename = filename
        file = str(self.currDir / filename)

        rename(self.file, file)

        self.file = file
        return self.file

    def printMetadata(self):
        if self.audiofile.tag is None:
            self.audiofile.initTag()

        metadataText = f"""
file: {self.file}

    url: {self.url}
    playlist:{self.playlist.name}
    
    artist:{self.artist}
    title:{self.title}
    
    genre:{self.genre}
    album:{self.album}"""

        print(metadataText)
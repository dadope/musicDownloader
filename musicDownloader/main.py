import argparse

from .models import mp3File
from .constants import logger

parser = argparse.ArgumentParser(prog="musicDownloader", description="A video downloader, with integrated mp3 conversion and metadata addition")

parser.add_argument("url", action="store", type=str, help="Specify the url to be downloaded")

parser.add_argument("-p", "--playlist", action="store", type=str, help="Specify the playlist")
parser.add_argument("-n", "--filename", action="store", type=str, help="Specify the filename")

args = parser.parse_args()


def main():
    logger.info("##### Initialising #####")
    file = mp3File.mp3File(args.url, args.playlist, args.filename)
    file.download()


if __name__ == "__main__":
    main()

import json
from typing import io

class Playlist:
    def __init__(self, name:str, genres:list, directories:list):
        self.name = name
        self.genres = genres
        self.directories = directories

    @classmethod
    def fromJson(cls, jsonSnippet:dict):
        return cls(
            jsonSnippet["name"],
            jsonSnippet["genres"],
            jsonSnippet["directories"]
        )

    @classmethod
    def fromFile(cls, file:io.TextIO):
        cls.fromJson(json.load(file))
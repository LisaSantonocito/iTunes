from dataclasses import dataclass


@dataclass
class Album:
    AlbumId : int
    Title : str
    ArtistId: int
    durata : int

    def __hash__(self):
        return hash(self.AlbumId)

    def __str__(self):
        return f"{self.Title} -- {self.toMinutes(self.durata)}"

    def toMinutes(self,d):
        return d/1000/60

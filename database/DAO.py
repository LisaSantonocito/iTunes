from database.DB_connect import DBConnect
from model.album import Album


class DAO():
    @staticmethod
    def getAllAlbum(durata):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select tb.AlbumId,tb.Title,tb.ArtistId, tb.durata 
                   from (select a.AlbumId, a.title,a.artistId,  sum(t.Milliseconds) as durata from album a , track t where a.AlbumId =t.AlbumId group by a.AlbumId,a.title,a.artistId) as tb
                   where tb.durata>%s"""
        cursor.execute(query, (durata, ))

        for row in cursor:
            result.append(Album(**row))  # seinomidelladataclasssonoquellidellatabella**rowsenzamettereprivati
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdges(idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinctrow t1.AlbumId as a1, t2.AlbumId as a2
                   from track t1, playlisttrack p1,track t2, playlisttrack p2 
                   where p1.PlaylistId = p2.PlaylistId 
                   and p2.TrackId =t2.TrackId 
                   and p1.TrackId =t1.TrackId 
                   and t1.AlbumId < t2.AlbumId"""
        cursor.execute(query, ())

        for row in cursor:
            if row["a1"] in idMap and row["a2"] in idMap:
                result.append((idMap[row["a1"]],idMap[row["a2"]]))  # seinomidelladataclasssonoquellidellatabella**rowsenzamettereprivati
        cursor.close()
        conn.close()
        return result
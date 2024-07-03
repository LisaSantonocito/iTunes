import copy

import networkx as nx

from database.DAO import DAO

class Model:
    def __init__(self):
        self._allAlbum = None
        self._idMapAlbum = {}
        self._grafo = nx.Graph()
        self._bestSet = None
        self._durataTot = 0

    def getAllAlbum(self, durata):
        d = tomillisecond(durata)
        self._allAlbum = DAO.getAllAlbum(d)
        return self._allAlbum

    def buildGraph(self,durata):
        self._grafo.clear()
        nodes = self.getAllAlbum(durata)
        if len(self._allAlbum)==0:
            print("Lista album vuota")
            return
        self._grafo.add_nodes_from(nodes)
        self._idMapAlbum = {a.AlbumId : a for a in list(self._grafo.nodes)}
        edges = DAO.getEdges(self._idMapAlbum)
        self._grafo.add_edges_from(edges)

    def getComponenteConnessa(self, v0):
        conn = nx.node_connected_component(self._grafo, v0)
        durataTOT = 0
        for album in conn:
            durataTOT += tominutes(album.durata)

        return len(conn), durataTOT
    def durataComplessivaA(self,listOfNodes ):
        dtot = 0
        for n in listOfNodes:
            dtot += n.durata
        return tominutes(dtot)

    def cercaPercorso(self, v0, soglia):
        self._bestSet = None
        self._Tot = 0 #maggiornumalbum
        connessa = nx.node_connected_component(self._grafo, v0)
        parziale = set([v0])
        connessa.remove(v0)
        self._ricorsione(parziale, connessa, soglia)

        return self._bestSet, self.durataComplessivaA(self._bestSet)

    def _ricorsione(self, parziale, connessa, soglia):
        if self.durataComplessivaA(parziale)>soglia:
            return
        if len(parziale)>self._Tot:
            self._bestSet = copy.deepcopy(parziale)
            self._Tot = len(parziale)

        for c in connessa:
            if c not in parziale:
                parziale.add(c)
                # rimanenti = copy.deepcopy(connessa)
                # rimanenti.remove(c)
                self._ricorsione(parziale, connessa, dTOT)
                parziale.remove(c)

    def printGraphDetails(self):
        print(f"Grafo creato con {len(self._grafo.nodes)} nodi e {len(self._grafo.edges)} archi.")

    def getNodes(self):
        return list(self._grafo.nodes)
    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

def tomillisecond(durata):
    return durata*60*1000

def tominutes(durata):
    return durata/1000/60

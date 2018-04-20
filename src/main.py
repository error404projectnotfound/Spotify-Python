# -*- coding: utf-8 -*-

import time
import logging

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pymongo import MongoClient

logging.basicConfig(filename='../datos/logs/logs_D.log', filemode='w', level=logging.INFO)
logging.info('Fecha y hora de INICIO: ' + time.strftime('%c'))

fichero_entrada = open('../datos/artistas/Billboard_authors_D.txt', 'r')
artistas_fichero = fichero_entrada.readline()
fichero_entrada.close()

lista_artistas = artistas_fichero.split('|')
artistas_fichero = None # free memory
lista_unica_artistas = list(set(lista_artistas))
lista_unica_artistas.sort()

numero_artistas_validos = 0
numero_artistas_spotify = 0

client_credentials_manager = SpotifyClientCredentials(client_id='9d4ce57a9fd74454800518b361d5d849',
                                                      client_secret='254f846eba8a4388840c99a11032ca14')
spotipy_instance = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

client = MongoClient()
db = client.Test  # Nombre de la bbdd es Test

for artista in lista_unica_artistas:
    #    artista = 'DJ Aligator' # Para hacer testeos
    if len(artista) > 0: # Puede haber nombres de artistas con una sola letra. Ejemplo: D
        numero_artistas_validos += 1
        artista_instancia = spotipy_instance.search(artista, type='artist')

        if artista_instancia['artists']['total'] > 0:
            logging.info('- Artista: ' + artista)
            numero_artistas_spotify += 1
            artista_id = artista_instancia['artists']['items'][0]['id']  # id de cada artista
            albums = spotipy_instance.artist_albums(artista_id, album_type='Album', limit=50)  # albums de cada artista

            for iteratorAlbum in range(len(albums['items'])):
                album_id = albums['items'][iteratorAlbum]['id']
                logging.info('-- Album: ' + album_id)
                # album = sp.album(albumId)   #info del album para sacar el genero
                tracks = spotipy_instance.album_tracks(album_id, limit=50)  # tracks de cada album
                try:
                    for iteratorTrack in range(len(tracks['items'])):
                        track_id = tracks['items'][iteratorTrack]['id']
                        features = spotipy_instance.audio_features(track_id)  # features de cada track
                        # audio = sp.audio_analysis(trackId)   #audio analisis de cada track

                        if features:
                            try:
                                tracks['items'][iteratorTrack]['features'] = dict(features[0])
                                # tracks['items'][iteratorTrack]['audio_analisis'] = audio
                                tracks['items'][iteratorTrack]['release_date'] = albums['items'][iteratorAlbum][
                                    'release_date']
                                # tracks['items'][iteratorTrack]['genre'] = album['genres']
                                result = db.LetraD.insert_one(
                                    tracks['items'][iteratorTrack])  # Features es el nombre de la coleccion
                            except :
                                logging.error('-- Artista -> %s, album -> %s y cancion -> %s' %(artista, album_id, track_id))
                except:
                    logging.error('-- Artista -> %s y album -> %s' % (artista, album_id))
        else:
            logging.warning('- Artista no encontrado: ' + str(artista))

logging.info('Fecha y hora FIN: ' + time.strftime('%c'))
logging.info('Numero de artistas validos: ' + str(numero_artistas_validos))
logging.info('Numero de artistas insertados: ' + str(numero_artistas_spotify))

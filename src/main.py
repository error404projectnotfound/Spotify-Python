# -*- coding: utf-8 -*-

import time
import logging
import os
from os import path

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pymongo import MongoClient
from google.cloud.bigquery.client import Client

logging.basicConfig(filename='../datos/logs/logs_D.log', filemode='w', level=logging.INFO)
logging.info('Fecha y hora de INICIO: ' + time.strftime('%c'))

fichero_entrada = open('../datos/artistas/Billboard_authors_D.txt', 'r', encoding='utf-8')
artistas_fichero = fichero_entrada.readline()
fichero_entrada.close()

lista_artistas = artistas_fichero.split('|')
artistas_fichero = None # Libera memoria
lista_unica_artistas = list(set(lista_artistas))
lista_unica_artistas.sort()

numero_artistas_validos = 0 # Numero de artistas que por longitud, sus nombres pueden ser validos
numero_artistas_spotify = 0 # Numero de artistas que se han solicitado a Spotify de forma satisfactoria

client_credentials_manager = SpotifyClientCredentials(client_id='9d4ce57a9fd74454800518b361d5d849',
                                                      client_secret='254f846eba8a4388840c99a11032ca14')
spotipy_instance = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

client = MongoClient()
db = client.Test  # Nombre de la BBDD es Test

for artista in lista_unica_artistas:
    if len(artista) > 0: # Puede haber nombres de artistas con una sola letra. Ejemplo: D
        numero_artistas_validos += 1
        artista_instancia = spotipy_instance.search(artista, type='artist')

        if artista_instancia['artists']['total'] > 0: # Comprueba que ela longitud del nombre del artista es valido
            logging.info('- Artista: ' + artista)
            numero_artistas_spotify += 1
            artista_id = artista_instancia['artists']['items'][0]['id']  # Id de cada artista
            albums = spotipy_instance.artist_albums(artista_id, album_type='Album', limit=50)  # Albumes de cada artista
            logging.info('-- Numero de albumes: ' + str(len(albums['items'])))

            for iteratorAlbum in range(len(albums['items'])): # Itera los albumes del artista
                album_id = albums['items'][iteratorAlbum]['id']
                logging.info('-- Album: ' + album_id)
                tracks = spotipy_instance.album_tracks(album_id, limit=50)  # tracks de cada album
                logging.info('Numero de canciones: ' + str(len(tracks['items'])))

                try:
                    for iteratorTrack in range(len(tracks['items'])): # Itera las canciones que contiene el album
                        track_id = tracks['items'][iteratorTrack]['id']

                        try:
                            track = spotipy_instance.track(track_id)
                            popularity = track['popularity']
                            name = track['name']
                            features = spotipy_instance.audio_features(track_id)  # features de cada track
                            danceability = features[0]['danceability']
                            energy = features[0]['energy']
                            clave_key = features[0]['key']
                            loudness = features[0]['loudness']
                            mode = features[0]['mode']
                            speechiness = features[0]['speechiness']
                            acousticness = features[0]['acousticness']
                            instrumentalness = features[0]['instrumentalness']
                            liveness = features[0]['liveness']
                            valence = features[0]['valence']
                            tempo = features[0]['tempo']
                            tipo_type = features[0]['type']
                            id_ = features[0]['id']
                            uri = features[0]['uri']
                            track_href = features[0]['track_href']
                            analysis_url = features[0]['analysis_url']
                            duration_ms = features[0]['duration_ms']
                            time_signature = features[0]['time_signature']
                            # Fila a insertar en la tabla
                            rows_to_insert = [(popularity, danceability, energy, clave_key, loudness, mode,
                                               speechiness, acousticness, instrumentalness, liveness, valence,
                                               tempo, tipo_type, id_, uri, track_href, analysis_url, duration_ms,
                                               time_signature, name)]
                            # Autenticación
                            os.environ[
                                'GOOGLE_APPLICATION_CREDENTIALS'] = path + 'MusicProjectTest-98a6983937ab.json'
                            # Conexion con la API de Big Query
                            big_query_client = Client()
                            # Se establece la BBDD
                            dataset_ref = big_query_client.dataset('Test_2')
                            # establecemos la tabla
                            table_ref = dataset_ref.table('track_features')
                            table = big_query_client.get_table(table_ref)
                            # Insertar datos en Big Query
                            errors = big_query_client.insert_rows(table, rows_to_insert)  # API request
                            for error in errors:
                                logging.error('Big Query: ' + errors)
                        except :
                            logging.error('-- Artista -> %s, album -> %s y cancion -> %s' %(artista, album_id, track_id))
                except:
                    logging.error('-- Artista -> %s y album -> %s' % (artista, album_id))
        else:
            logging.warning('- Artista no encontrado: ' + str(artista))

logging.info('Fecha y hora FIN: ' + time.strftime('%c'))
logging.info('Numero de artistas validos: ' + str(numero_artistas_validos))
logging.info('Numero de artistas obtenidos de Spotify: ' + str(numero_artistas_spotify))

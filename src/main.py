# -*- coding: utf-8 -*-

import time
import logging
import os

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from google.cloud.bigquery.client import Client

#fecha = time.strftime("%Y%m%d_%H%M")
logging.basicConfig(filename='../datos/logs/logs_a.log', filemode='a', level=logging.INFO)
logging.info('Fecha y hora de INICIO: ' + time.strftime('%c'))

fichero_entrada = open('../datos/artistas/Billboard_authors_A.txt', 'r', encoding='utf-8')
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

#client = MongoClient()
#db = client.Test  # Nombre de la BBDD es Test

for artista in lista_unica_artistas:
    if len(artista) > 0: # Puede haber nombres de artistas con una sola letra. Ejemplo: D
        numero_artistas_validos += 1
        artista_instancia = spotipy_instance.search(artista, type='artist')

        if artista_instancia['artists']['total'] > 0: # Comprueba que ela longitud del nombre del artista es valido
            logging.info('- Artista: ' + artista)
            numero_artistas_spotify += 1
            #sacamos las caracteristicas de los artistas
            artist=artista_instancia['artists']['items'][0]
            artist_id = artist['id']  # Id de cada artista
            artist_followers=artist['followers']['total']
            artist_genres=artist['genres']
            artist_popularity=artist['popularity']
            #artist_name=artista
            #obtenemos los albunes
            albums = spotipy_instance.artist_albums(artist_id, album_type='Album', limit=50)  # Albumes de cada artista
            #albums=results['items']
            #albums.extend(results['items'])
            logging.info('-- Numero de albumes: ' + str(len(albums)))
            for iteratorAlbum in range(len(albums['items'])): # Itera los albumes del artista
            #for album in albums:
                album=albums['items'][iteratorAlbum]
                album_id =album['id']
                album_type=album['album_type']
                #album_genres=album['genres']
                album_genres=""
                #album_label=album['label']
                album_label=""
                album_name=album['name']
                #album_popularity=album['popularity']
                album_popularity=""
                album_release_date=album['release_date']
                album_realease_date_precision=album['release_date_precision']
                logging.info('---Album['+str(iteratorAlbum)+']: ' + album_name+"("+album_id+")")
                #obtenemos las tracks del album
                tracks = spotipy_instance.album_tracks(album_id, limit=50)  # tracks de cada album
                logging.info('----Numero de canciones: ' + str(len(tracks['items'])))
                try:
                    for iteratorTrack in range(len(tracks['items'])): # Itera las canciones que contiene el album
                        track_id = tracks['items'][iteratorTrack]['id']
                        try:
                            track = spotipy_instance.track(track_id)
                            #obtenemos los campos del objeto track
                            track_avalible_markets=track['available_markets']
                            track_explicit=track['explicit']
                            track_name=track['name']
                            track_popularidad=track['popularity']
                            track_number=track['track_number']
                            #obtenemos los campos del objeto features
                            features = spotipy_instance.audio_features(track_id)  # features de cada track
                            features_acousticness = features[0]['acousticness']
                            features_analysis_url=features[0]['analysis_url']
                            features_danceability= features[0]['danceability']
                            features_duration_ms = features[0]['duration_ms']
                            features_energy = features[0]['energy']
                            features_instrumentalness = features[0]['instrumentalness']
                            features_key = features[0]['key']
                            features_liveness= features[0]['liveness']
                            features_loudness = features[0]['loudness']
                            features_mode = features[0]['mode']
                            features_speechiness= features[0]['speechiness']
                            features_tempo= features[0]['tempo']
                            features_time_signature = features[0]['time_signature']
                            features_valence = features[0]['valence']
                            # Fila a insertar en la tabla
                            rows_to_insert = [(artista,artist_followers,str(artist_genres),artist_id,artist_popularity,
                                               album_type,album_genres,album_id,album_label,album_name,album_popularity,
                                               album_release_date,album_realease_date_precision,track_name,str(track_avalible_markets),
                                               str(track_explicit),track_id,track_popularidad,track_number,features_acousticness,features_analysis_url,
                                               features_danceability,features_duration_ms,features_energy,features_instrumentalness,features_key,features_liveness,
                                               features_loudness,features_mode,features_speechiness,features_tempo,features_time_signature,features_valence)]
                            # Autenticación
                            os.environ[
                                'GOOGLE_APPLICATION_CREDENTIALS'] = '../datos/MusicProjectTest-98a6983937ab.json'
                            # Conexion con la API de Big Query
                            big_query_client = Client()
                            # Se establece la BBDD
                            dataset_ref = big_query_client.dataset('musicDataset')
                            # establecemos la tabla
                            table_ref = dataset_ref.table('datos_spotify_A')
                            table = big_query_client.get_table(table_ref)
                            # Insertar datos en Big Query
                            errors = big_query_client.insert_rows(table, rows_to_insert)  # API request
                            for error in errors:
                                logging.error('Big Query: ' + error)
                        except :
                            logging.error('-- Artista -> %s, album -> %s y cancion -> %s' %(artista, album_id, track_id))
                except:
                    logging.error('-- Artista -> %s y album -> %s' % (artista, album_id))
        else:
            logging.warning('- Artista no encontrado: ' + str(artista))

logging.info('Fecha y hora FIN: ' + time.strftime('%c'))
logging.info('Numero de artistas validos: ' + str(numero_artistas_validos))
logging.info('Numero de artistas obtenidos de Spotify: ' + str(numero_artistas_spotify))

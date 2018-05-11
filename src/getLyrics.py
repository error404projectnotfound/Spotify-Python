# -*- coding: utf-8 -*-
"""
Created on Mon May  7 15:24:33 2018

@author: xmcollantes
"""

import os
import requests
from google.cloud.bigquery.client import Client

os.environ[
'GOOGLE_APPLICATION_CREDENTIALS'] = '../datos/MusicProjectTest-98a6983937ab.json'

#cabecera de las peticiones a music match
headers={
         "X-Mashape-Key": "n1pAMoMxzvmshxHnxIl0x2tZALugp1IRgr3jsnd4E0dGin208W",
         "Accept": "application/json"
            }

#llamadas al cliente de big query
big_query_client = Client()
#query para obtener el nombre del artista y nombre de cancion
query_job = big_query_client.query('SELECT artista, track_name FROM `musicDataset.datos_spotify_test`')
results = query_job.result()
#variables para el almacenamiento y log
lyrics_language=""
lyrics_body=""
for row in results:
    artist=row.artista
    print("artista: "+artist)
    track=row.track_name
    print("track_name: "+track)
    #cancion se le tiene que pasar el nombre del artista y la canción
    r = requests.get('https://musixmatchcom-musixmatch.p.mashape.com/wsr/1.1/matcher.track.get?f_has_lyrics=1&q_artist='+artist+'&q_track='+track, headers = headers)
    status_artist= r.status_code
    print("Estado: "+str(status_artist))
    if status_artist == 200:
        status= r.status_code
        body = r.json()
        #print(body)
        id_track=body["track_id"]
        #obtenemos la letra
        r = requests.get('https://musixmatchcom-musixmatch.p.mashape.com/wsr/1.1/track.lyrics.get?track_id='+str(id_track), headers = headers)
        #Verificamos que haya respuesta
        status_lyrics=r.status_code
        print("Estado: "+str(status_lyrics))
        if status_lyrics == 200:
            json_body = r.json()
            #obtenemos tanto la letra como el leguaje de la letra
            lyrics_body=json_body["lyrics_body"]
            init_trash=lyrics_body.find("...")
            lyrics_clean=lyrics_body[0:init_trash]
            lyrics_language=json_body["lyrics_language"]
            print("Idioma: "+lyrics_language)
            print("Letra: "+lyrics_clean)
        else:
            print(track+": Sin letra")
        rows_to_insert = [(artist,track,lyrics_language,lyrics_clean,status_artist,status_lyrics)]
        dataset_ref = big_query_client.dataset('musicDataset')
        table_ref = dataset_ref.table('lyricsMusixMatch_A')
        table = big_query_client.get_table(table_ref)
        errors = big_query_client.insert_rows(table, rows_to_insert)  # API request
        for error in errors:
            print('Big Query: ' + error)
    
#Prueba de Github
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pymongo import MongoClient
import time

Log = open ('C:\\Temp\\Resultado_D.txt', 'w', encoding='utf8')
Log.write ('Fecha y hora INICIO ' + time.strftime('%c')) #Hora de inicio

ficheroEntrada = open ('C:\\Temp\\Billboard_authors_D.txt', 'r', encoding='utf8')
autores_fichero= ficheroEntrada.readline()

lista_autores = autores_fichero.split('|')
lista_unica_autores = list(set(lista_autores))
lista_unica_autores.sort()

numeroAutores=0

client_credentials_manager = SpotifyClientCredentials(client_id='9d4ce57a9fd74454800518b361d5d849', 
                                                      client_secret='254f846eba8a4388840c99a11032ca14')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

client = MongoClient()
db = client.Test #Test nombre de la bbdd

for autor in lista_unica_autores:
#    autor = 'DJ Aligator' # Para hacer testeos
    if autor != "" and len(autor) != 1 and len(autor) != 0:
        
        artists = sp.search(autor, type='artist')

        if artists['artists']['total'] != 0 :
            Log.write('Autor: ' + autor)
            numeroAutores = numeroAutores + 1            
            artistId = artists['artists']['items'][0]['id']  #id de cada autor   
            albums = sp.artist_albums(artistId, album_type ='Album', limit = 50) #albums de cada autor

            for iteratorAlbum in range (len(albums['items'])):
                albumId = albums['items'][iteratorAlbum]['id']
                #album = sp.album(albumId)   #info del album para sacar el género
                tracks = sp.album_tracks(albumId, limit=50)   #tracks de cada album
                try: 
                    for iteratorTrack in range (len(tracks['items'])):
                        trackId = tracks['items'][iteratorTrack]['id']
                        features = sp.audio_features(trackId)   #features de cada track
                        #audio = sp.audio_analysis(trackId)   #audio analisis de cada track
                 
                        if features:
                            try:
                                tracks['items'][iteratorTrack]['features'] = dict(features[0])
                                #tracks['items'][iteratorTrack]['audio_analisis'] = audio
                                tracks['items'][iteratorTrack]['release_date'] = albums['items'][iteratorAlbum]['release_date']
                                #tracks['items'][iteratorTrack]['genre'] = album['genres']
                                result = db.LetraD.insert_one(tracks['items'][iteratorTrack]) #Features es el nombre de la colección
                            except:
                                None
                except:
                    ficheroEntrada.close()                    
ficheroEntrada.close()
Log.write('Numero de autores insertados: ' + numeroAutores)
Log.write ('Fecha y hora FIN ' + time.strftime('%c'))

Log.close()
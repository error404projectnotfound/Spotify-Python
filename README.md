# Spotify-Python
Este proyecto consiste en el proceso ETL (Extraction, Transformation an Load) de Spotify a nuestra base de datos MongoDB, usando la librería de Python "spotipy".
## Getting Started
Estas instrucciones te permitirán obtener una copia del proyecto en funcionamiento en tu máquina local.
### Prerrequisitos
1. Tener instalado **Python** en el sistema operativo. 
2. Disponer de **pip** para poder instalar todos los complementos necesarios. Para ello, abre un terminal y ejecuta:
```
python get-pip.py
```
3. Instalar **virtualenv*. La cual es una herramienta de desarrollo usada para crear entornos aislados para Python, en los que es posible instalar paquetes sin interferir en el resto de paquetes instalados en el sistema o en otros entornos virtuales.
Para ello escribe en el terminal:
```
pip install virtualenv
```
4. **Falta MongoDB**
### Instalación
1. Ve a la ruta en la que quieras crear tu entorno virtual. Dónde lo crees es irrelevante, pero aconsejamos que todos entornos virtuales se creen en el mismo directorio y fuera de los proyectos en los que vayan a ser usados.
2. Crea tu virtualenv.
```
virtualenv nombre_de_tu_entorno_virtual
```
3 Activa tu virtualenv. Ejecuta:
```
source nombre_de_tu_entorno_virtual/bin/activate
```
Si todo ha ido bien, verás a la izquierda del path del terminal, el nombre de tu entorno virtual.
4. Ve al directorio donde quieras clonar este repositorio.
5. Ejecuta:
```
git clone https://github.com/error404projectnotfound/Spotify-Python.git
```
6. Accede al repositorio ya descargado en tu local:
```
cd Spotify-Python
```
7. Instala todos los paquetes necesarios para ejecutar el proyecto. **Recuerda que tienes tu entorno virtual activado y solo se instalarán en él**
```
pip install requirements.txt
```
8. **Falta MongoDB**
## Ejecuta el proyecto!
```
cd src
python main.py
```
No funcionará, **falta MongoDB**

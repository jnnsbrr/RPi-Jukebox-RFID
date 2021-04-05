from gtts import gTTS
from time import sleep
import os
import configparser
from mpd import MPDClient
import random
import sys 
# get config
conf_file = "./python-phoniebox/phoniebox.conf"

# function to intialize client
def mpd_init_connection(conf_file):
    config = configparser.ConfigParser()
    config.read(conf_file)
    """ connect to mpd """
    client = MPDClient()
    client.connect(config["mpd"]["host"],
                   int(config["mpd"]["port"]))
    client.timeout = float(config["mpd"]["timeout"])
    return client

# init mpd client to control Mopidy
client = mpd_init_connection(conf_file)

# get all playlist info
playlist = client.playlistinfo()
# select all albums with their first tracks pos

albums = [(album['album'], int(album['pos'])) for album in playlist if int(album['track']) == 1]

if sys.argv[1] == "random":
    # get random albums first track
    nextalbum = random.choice(albums)
else:
    current_album = client.currentsong()["album"]
    nextalbum = albums[next(i+1 for i,album in enumerate(albums) if album[0] == current_album)]

# read album title
tts = gTTS(text=nextalbum[0], lang='de')
# workaround via temporary file
filename = './temp.mp3'
tts.save(filename)

if client.status()["state"] == "play":
    client.pause()

volume = 32768*int(os.environ["VOLPERCENT"])/100
os.system("mpg123 -f -{} temp.mp3".format(volume))
#remove temperory file
os.remove(filename)

# play track
client.play(nextalbum[1])
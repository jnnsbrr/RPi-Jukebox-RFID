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

# get current albumnnn                      
playalbum = client.currentsong()


# read album title
tts = gTTS(text=playalbum["album"], lang='de')
# workaround via temporary file
filename = './temp.mp3'
tts.save(filename)

if client.status()["state"] == "play":
    client.pause()

volume = 32768*int(os.environ["VOLPERCENT"])/100
os.system("mpg123 -a hw:1,0 -f -{} temp.mp3".format(volume))
#remove temperory file
os.remove(filename)

# play track
client.play()
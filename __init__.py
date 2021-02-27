from mycroft import MycroftSkill, intent_handler
from mycroft.api import DeviceApi
import time
# used to communicate with the Sonos Node JS Server
import requests

import soco



class SpeechOverSonos(MycroftSkill):

    # important values for the skill to function
    # can be edited in the normal Mycroft Skill settings on home.mycroft.ai
    sonos_server_ip = ""
    room = ""
    url = ""

    has_been_playing = False
    has_been_playing_uri = ""
    is_playing = False
    played_uri = ""

    # values for the soco package
    all_speakers = []
    speaker = None

    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self):
        SpeechOverSonos.sonos_server_ip = self.settings.get("sonos_server_ip")
        SpeechOverSonos.room = str(DeviceApi().get()["description"])
        # putting the values in str() is necessary
        SpeechOverSonos.url = "http://" + str(SpeechOverSonos.sonos_server_ip) + ":5005/" + str(SpeechOverSonos.room) + "/"

        # initializes soco
        SpeechOverSonos.initialize_soco()

        # connects with the mycroft-playback-control messagebus
        self.add_event("recognizer_loop:wakeword", self.activation_confirmation_noise_on_sonos)
        self.add_event("speak", self.output_speech_on_sonos)


    def initialize_soco():
        SpeechOverSonos.all_speakers = soco.discover()
        for current_speaker in SpeechOverSonos.all_speakers:
            if current_speaker.player_name == SpeechOverSonos.room:
                SpeechOverSonos.speaker = current_speaker


    # general function to call the sonos api
    def sonos_api(action = ""):
        return requests.get(SpeechOverSonos.url + str(action))

    # function to make the activation noise on the Sonos speaker
    # requires the fil start_listening.wav in the folder node-sonos-http-api/static/clips on the machine where the node js server runs
    # the start_listening.wav file can be found in mycroft-core/mycroft/res/snd/start_listening.wav
    def activation_confirmation_noise_on_sonos(self, message):
        # gets the current playback state of the Sonos speaker and stores it
        current_transport_state = SpeechOverSonos.speaker.get_current_transport_info().get("current_transport_state")
        if (current_transport_state == "PLAYING") or (current_transport_state == "TRANSITIONING"):
            SpeechOverSonos.has_been_playing = True
            SpeechOverSonos.has_been_playing_uri = SpeechOverSonos.speaker.get_current_track_info().get("uri")
        else:
            SpeechOverSonos.has_been_playing = False

        SpeechOverSonos.sonos_api(action = "clip/start_listening.wav/45")
        # if SpeechOverSonos.is_playing == True:
            # this lets the music continu
            # SpeechOverSonos.speaker.next()

    # function to output speech over the Sonos speaker using the TTS feature of the node js sonos server
    def output_speech_on_sonos(self, message):
        # gets the current playback state of the Sonos speaker and stores it
        current_transport_state = SpeechOverSonos.speaker.get_current_transport_info().get("current_transport_state")
        if (current_transport_state == "PLAYING") or (current_transport_state == "TRANSITIONING"):
            SpeechOverSonos.is_playing = True
            SpeechOverSonos.played_uri = SpeechOverSonos.speaker.get_current_track_info().get("uri") 

        else:
            SpeechOverSonos.is_playing = False

        response = SpeechOverSonos.sonos_api(action = "say/" + str(message.data.get("utterance")) + "/de-de")
        self.log.info("now finished with speech output")
        
        if SpeechOverSonos.is_playing == True:
            # SpeechOverSonos.speaker.next()
            SpeechOverSonos.speaker.play_uri(SpeechOverSonos.played_uri)

        if SpeechOverSonos.has_been_playing == True:
            SpeechOverSonos.speaker.play_uri(SpeechOverSonos.has_been_playing_uri)
        #while finished == False:
        #    time.sleep(0.2)
        #    next_transport_state = SpeechOverSonos.speaker.get_current_transport_info().get("current_transport_state")
        #    if (next_transport_state == "STOPPED"):
        #SpeechOverSonos.speaker.remove_from_queue(0)
        #        finished = True

    @intent_handler("speech.in.room.intent")
    def speech_in_room(self, message):
        message = message.data.get("message") 
        room = message.data.get("room")
        if room == None:
            room = SpeechOverSonos.room

        url = "http://" + str(SonosMusicController.sonos_server_ip) + ":5005/" + str(room) + "/say/" + str(message) + "/de-de"
        requests.get(url)



def create_skill():
    return SpeechOverSonos()


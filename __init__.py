from mycroft import MycroftSkill, intent_file_handler
# used to communicate with the Sonos Node JS Server
import requests
from mycroft.api import DeviceApi


class SpeechOverSonos(MycroftSkill):

    # important values for the skill to function
    # can be edited in the normal Mycroft Skill settings on home.mycroft.ai
    sonos_server_ip = ""
    room = ""
    url = ""

    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self):
        SpeechOverSonos.sonos_server_ip = self.settings.get("sonos_server_ip")
        SpeechOverSonos.room = str(DeviceApi().get()["description"])
        # putting the values in str() is necessary
        SpeechOverSonos.url = "http://" + str(SpeechOverSonos.sonos_server_ip) + ":5005/" + str(SpeechOverSonos.room) + "/"

        # connects with the mycroft-playback-control messagebus
        self.add_event("recognizer_loop:wakeword", self.activation_confirmation_noise_on_sonos)
        self.add_event("speak", self.output_speech_on_sonos)


    # general function to call the sonos api
    def sonos_api(action = ""):
        requests.get(SpeechOverSonos.url + str(action))

    # function to make the activation noise on the Sonos speaker
    # requires the file start_listening.wav in the folder node-sonos-http-api/static/clips on the machine where the node js server runs
    # the start_listening.wav file can be found in mycroft-core/mycroft/res/snd/start_listening.wav
    def activation_confirmation_noise_on_sonos(self, message):
        SpeechOverSonos.sonos_api(action = "clip/start_listening.wav/45")

    # function to output speech over the Sonos speaker using the TTS feature of the node js sonos server
    def output_speech_on_sonos(self, message):
        SpeechOverSonos.sonos_api(action = "say/" + str(message.data.get("utterance")) + "/de-de")


def create_skill():
    return SpeechOverSonos()


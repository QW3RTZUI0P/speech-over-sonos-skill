from mycroft import MycroftSkill, intent_file_handler
# used to communicate with the Sonos Node JS Server
import requests


class SpeechOverSonos(MycroftSkill):

    # important values for the skill to function
    # can be edited in the normal Mycroft Skill settings on home.mycroft.ai
    sonos_server_ip = ""
    room = ""
    url = ""

    is_playing = False

    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self):
        SpeechOverSonos.sonos_server_ip = self.settings.get("sonos_server_ip")
        SpeechOverSonos.room = self.settings.get("room")
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
        # gets the current playback state of the Sonos speaker and stores it
        # state = requests.get(SpeechOverSonos.url + "state")
        # state_json = state.json()
        # if state_json["playbackState"] == "PLAYING":
        #     SpeechOverSonos.is_playing = True
        # else:
        #     SpeechOverSonos.is_playing = False

        SpeechOverSonos.sonos_api(action = "clip/start_listening.wav/45")
        # if SpeechOverSonos.is_playing == True:
        #     sonos_api(action = "play")

    # function to output speech over the Sonos speaker using the TTS feature of the node js sonos server
    def output_speech_on_sonos(self, message):
        # gets the current playback state of the Sonos speaker and stores it
        state = requests.get(SpeechOverSonos.url + "state")
        state_json = state.json()
        self.log.info("message: " + str(message))
        if state_json["playbackState"] == "PLAYING" or state_json["playbackState"] == "TRANSITIONING":
            self.log.info("PLAYING")
            SpeechOverSonos.is_playing = True
        else:
            self.log.info("content: " + state_json["playbackState"])
            SpeechOverSonos.is_playing = False

        SpeechOverSonos.sonos_api(action = "say/" + str(message.data.get("utterance")) + "/de-de")
        if SpeechOverSonos.is_playing == True:
            SpeechOverSonos.sonos_api(action = "play")


def create_skill():
    return SpeechOverSonos()


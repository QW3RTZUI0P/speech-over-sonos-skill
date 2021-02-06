from mycroft import MycroftSkill, intent_file_handler


class SpeechOverSonos(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('sonos.over.speech.intent')
    def handle_sonos_over_speech(self, message):
        self.speak_dialog('sonos.over.speech')


def create_skill():
    return SpeechOverSonos()


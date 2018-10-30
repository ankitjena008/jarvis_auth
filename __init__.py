# TODO: Add an appropriate license to your skill before publishing.  See
# the LICENSE file for more information.

# Below is the list of outside modules you'll be using in your skill.
# They might be built-in to Python, from mycroft-core or from external
# libraries.  If you use an external library, be sure to include it
# in the requirements.txt file so the library is installed properly
# when the skill gets installed later by a user.

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler, intent_file_handler
import pyaudio, wave, sys
import requests
import hashlib
import time

CHUNK = 8192
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = 'Audio_.wav'


# Each skill is contained within its own class, which inherits base methods
# from the MycroftSkill class.  You extend this class as shown below.

# TODO: Change "Template" to a unique name for your skill
class AuthenticateSkill(MycroftSkill):

    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(AuthenticateSkill, self).__init__(name="AuthenticateSkill")

        # Initialize working variables used within the skill.
        self.count = 0

    # The "handle_xxxx_intent" function is triggered by Mycroft when the
    # skill's intent is matched.  The intent is defined by the IntentBuilder()
    # pieces, and is triggered when the user's utterance matches the pattern
    # defined by the keywords.  In this case, the match occurs when one word
    # is found from each of the files:
    #    vocab/en-us/Hello.voc
    #    vocab/en-us/World.voc
    # In this example that means it would match on utterances like:
    #   'identify me'
    #   'Authenticate me'
    @intent_handler(IntentBuilder("").require("Hello").require("World"))
    def handle_authenticate_me_intent(self, message):
        p = pyaudio.PyAudio()
        for i in range(p.get_device_count()):
            print('Index : ', i, "\n", p.get_device_info_by_index(i))
        self.speak_dialog("auth.me")
        time.sleep(5)
        record_audio()
        play_audio('Audio_.wav')
        check_voice_it()

def check_voice_it():
    password = "Password1234@"
    pwd = hashlib.sha256(password.encode("ascii")).hexdigest()
    print(pwd)
    userId = "bharathwaj"
    developerID = "a3f54f38702e4477ad2d5befe6282725"
    with open('/home/brad/Desktop/mycroft-core/Audio_.wav', 'rb') as file:
            wavData = file.read()

    headers = {'PlatformID': '2', 'Content-Type': 'audio/wav', "UserId": userId, "VsitPassword": pwd, "VsitDeveloperId": developerID, "ContentLanguage":"en-US"}
    response = requests.post(
                "https://siv.voiceprintportal.com/sivservice/api/authentications", headers=headers, data=wavData)
    
    
    print(response.text)
     
def record_audio():

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels = 1,
                    rate = RATE,
                    input = True,
                    input_device_index = 1,
                    frames_per_buffer = CHUNK)

    print("* Now Recording")

    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* Done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


def play_audio(file):
    f = wave.open(file, "rb")
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                    channels=f.getnchannels(),
                    rate=f.getframerate(),
                    output=True)
    data = f.readframes(CHUNK)
    while data:
        stream.write(data)
        data = f.readframes(CHUNK)
    stream.stop_stream()
    stream.close()
    p.terminate()


# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return AuthenticateSkill()

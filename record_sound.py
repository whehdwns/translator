import sounddevice as sd
from scipy.io.wavfile import write
import os
from pydub import AudioSegment
from ibm_watson import SpeechToTextV1 
import json
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from pandas.io.json import json_normalize
import sys
from ibm_watson import LanguageTranslatorV3
from pandas.io.json import json_normalize

#Record the sound and save in to wav file
fs = 44100  # this is the frequency sampling; also: 4999, 64000
seconds = 3  # Duration of recording
myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
print("Starting: Speak now!")
sd.wait()  # Wait until recording is finished
print("finished Recording")
write('output.wav', fs, myrecording)  # Save as WAV file

#Change from wav file to mp3 file
sound = AudioSegment.from_wav('output.wav')
sound.export('myfile.mp3', format='mp3')

#sys.stdout = open('speech_to_text.txt','w')

#Using Speech to Text-tz From IBM Cloud
#https://cloud.ibm.com/apidocs/speech-to-text/speech-to-text?code=python
url_s2t = "URL" #URL
iam_apikey_s2t = "API_KEY" #API Key
authenticator = IAMAuthenticator(iam_apikey_s2t)
s2t = SpeechToTextV1(authenticator=authenticator)
s2t.set_service_url(url_s2t)
s2t
filename='myfile.mp3'
with open(filename, mode="rb")  as wav:
    response = s2t.recognize(audio=wav, content_type='audio/mp3')
response.result
recognized_text=response.result['results'][0]["alternatives"][0]["transcript"]
print(recognized_text) #print recorded word or sentence

#Using Language Translator-wv From IBM Cloud
#https://cloud.ibm.com/docs/language-translator?topic=language-translator-gettingstarted
url_lt='URL'#URL
apikey_lt='API_KEY'#API Key
version_lt='2020-02-06'
authenticator1 = IAMAuthenticator(apikey_lt)
language_translator = LanguageTranslatorV3(version=version_lt,authenticator=authenticator1)
language_translator.set_service_url(url_lt)
language_translator
json_normalize(language_translator.list_identifiable_languages().get_result(), "languages")

translation_response = language_translator.translate(\
    text=recognized_text, model_id='en-ko') #English to Korean
translation=translation_response.get_result()

language_translation =translation['translations'][0]['translation']
print(language_translation)

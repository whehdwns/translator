from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
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
import time
import xlrd
import csv

def clearAll():
	input_field.delete(0, END)
	output_field.delete(0,END)


def checkError() : 
  
    # if any of the entry field is empty 
    # then show an error message and clear  
    # all the entries 
    if (input_field.get() == "") : 
  
        # show the error message 
        messagebox.showerror("Input Error") 
  
        # clearAll function calling 
        clearAll() 
          
        return -1


def new_lang_input():
        print(root.input_language_box.get())

def translate_voice():
	#Record the sound and save in to wav file
	fs = 44100  # this is the frequency sampling; also: 4999, 64000
	seconds = 3  # Duration of recording
	myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
	#print("Starting: Speak now!")
	sd.wait()  # Wait until recording is finished
	print("finished Recording")
	write('output.wav', fs, myrecording)  # Save as WAV file

	#Change from wav file to mp3 file
	sound = AudioSegment.from_wav('output.wav')
	sound.export('myfile.mp3', format='mp3')

	#sys.stdout = open('speech_to_text.txt','w')

	#Using Speech to Text-tz From IBM Cloud
	#https://cloud.ibm.com/apidocs/speech-to-text/speech-to-text?code=python
	url_s2t = #URL
	iam_apikey_s2t = #API Key
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
	#t=2 
   # time.sleep(2)
	translate_text()


def translate_text(inputs_lang, outputs):
	
	value = checkError()

	if value == -1:
		return
	else:
	
		url_lt=#URL
		apikey_lt=#API KEY
		version_lt='2018-05-01'
		authenticator = IAMAuthenticator(apikey_lt)
		language_translator = LanguageTranslatorV3(version=version_lt,authenticator=authenticator)
		language_translator.set_service_url(url_lt)
		language_translator
		json_normalize(language_translator.list_identifiable_languages().get_result(), "languages")
		
		recognized_text = str(input_field.get())
		#recognized_text = input("Translate (lowercase): ")
		#"Hello"
		#https://cloud.ibm.com/docs/language-translator?topic=language-translator-identifiable-languages
		
		translation_response = language_translator.translate(
		    text=recognized_text, model_id='{0}-{1}'.format(inputs_lang, outputs))
		#print(translation_response)

		translation=translation_response.get_result()
		#print(translation)

		language_translation =translation['translations'][0]['translation']
		#print(language_translation)

		output_field.insert(10,str(language_translation))

def centreWindow():
    w = 500
    h = 300
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = (sw - w)/2
    y = (sh - h)/2
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

def onExit():
        root.quit()

def callback_input (event):
	global inp
	print(input_language_chosen.get())
	inp= input_language_chosen.get()

def callback_output (event):
	global outp
	print(output_language_chosen.get())
	outp= output_language_chosen.get()
	#print(output_language_chosen.get())




def language_func():
	#global inp, outp
	translate_text(inp, outp)



if __name__ == '__main__':


	#Creating the GUI window
	root = Tk()   

	#Title of the app       
	root.title('Translate')

	#Setting the background color
	root.config(background='white')
	root.style=Style()
	root.style.theme_use("default")


	centreWindow()
  	#Background on GUI
	#root.geometry('600x550')
	root.resizable(width=FALSE, height=FALSE)

	#---------label/ box---------
    # Language selection(from ___ to ____)
    # Text box on both side (left/ right) or (top/bottom)
    # select voice button for voice translation
    # Translate button,
	loc = ('C:\\Users\\dongj\\Desktop\\Python\\Watson\\voice_translate\\Language_list.csv')
	# Read values from filename
	"""
	creatures = []
	with open('Language_selection.txt') as inFile:
	    creatures = [line for line in inFile]
	"""
	creatures = []
	with open(loc, newline='') as inFile:
	    reader = csv.DictReader(inFile)
	    for i in reader:
	    	creatures = [i['Name'] for i in reader]
	#input field
	Label(root, text="Input").grid(row=2, column=0, sticky=W+E)

	#Combo Box
	# Creature Drop Down
	input_language_box = StringVar()
	input_language_box.set("select language below")
	input_language_chosen = Combobox(root, width=30, state='readonly')
	input_language_chosen['values'] = tuple(creatures)

	
	input_language_chosen.bind("<<ComboboxSelected>>", callback_input)
	input_language_chosen.grid(row=2, column=1, padx=5, pady=5, ipady=2, sticky=W)

	#Create a Text entry for translation
	input_field=Entry(root, width=30)
		#, padx=5, pady=5, width=20, height=6)
	input_field.grid(row=3, column=1, padx=5, pady=5, sticky=W)

	#output Field
	#Label(root, text="Output").grid(column=13, row=0,sticky='N')
	Label(root, text="Output").grid(row=2, column=2, sticky=W+E)
	#Combo Box
	# Creature Drop Down
	output_language_box = StringVar()
	output_language_box.set("select language below")
	output_language_chosen = Combobox(root, width=30, state='readonly')
	output_language_chosen['values'] = tuple(creatures)
	
	output_language_chosen.bind("<<ComboboxSelected>>", callback_output)
	output_language_chosen.grid(row=2, column=3, padx=5, pady=5, ipady=2, sticky=W)


	#Create a Text entry for translation
	output_field=Entry(root,width=30)
		#,padx=5, pady=5, width=20, height=6)
	output_field.grid(row=3, column=3, padx=5, pady=5, sticky=W)
       
    
	btn_translate = Button(
	    master=root,
	    text="\N{RIGHTWARDS BLACK ARROW}(translate)",
	    command= language_func
	    #lambda inp, outp :
	)
	btn_translate.grid(row=5, column=1)
	"""
	btn_voice= Button(
		master=root,
		text=" \N{TELEPHONE LOCATION SIGN} (Voice) ",
		command=translate_voice
	)

	btn_voice.grid(row=5, column=2)
	"""
	btn_clear = Button(
		master=root,
		text="\N{LATIN CAPITAL LETTER X} (Clear)",
		command=clearAll
	)
	btn_clear.grid(row= 10, column=1)
	
	closeBtn=Button(
		master = root,
		text="Close", 
		command=onExit
	)
	closeBtn.grid(row=10, column=2)

	# Start GUI
	root.mainloop()

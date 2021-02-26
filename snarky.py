from gtts import gTTS
import speech_recognition as sr
import os
import re
import webbrowser
import smtplib
import time
import requests
import mpg123
import winsound
import win32com.client as wincl
import playsound
import pyttsx3
import subprocess
from weather import Weather
import sys , bs4
from urllib.parse import urlparse
import urllib.request
import urllib3
#Asistentul Snarky
   #by Zaharie Andrei
#==========================================================
vocea=0
def speak(audio):
    "speaks audio passed as argument"
    global vocea
 
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[vocea].id)
    
    print(audio)
    engine.say(audio)
    engine.runAndWait()
   

    #tts = gTTS(text = audio, lang = 'ro-RO')
    #tts.save('audio.mp3')
    #voce="audio.mp3"
    #print(audio)
    #for line in audio.splitlines():
      # playsound.playsound(voce)
   



#CAUTARE AVANSATA ===================
def cautare_avansata(audio):
    
    res=requests.get('https://google.com/search?q='+ ''.join(audio))
    soup=bs4.BeautifulSoup(res.text,"html.parser")
    linkElements = soup.select(' a')
    linkOpen=min(9, len(linkElements))
    for i in range(linkOpen):
       if i !=0 and i!=1 and i!=6:
         webbrowser.open('https://www.google.com'+linkElements[i].get('href'))
    
    
    speak('That is everithing I found for'+ audio)


   
      #MAKE A NOTE ===========================================
def note(audio):
    date = 'note'
    file_name = str(date).replace(":", "-") + "-note.txt"
    with open(file_name, "w") as f:
        f.write(audio)

    subprocess.Popen(["notepad.exe", file_name])

     
   #Comanda vocala pentru asistent===============================


def comandaA():
    "listens for commands"
    
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
        
    try:
 
        comanda = r.recognize_google(audio).lower()
        print('You said: ' + comanda + '\n')

    #loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print('Your last command couldn\'t be heard')
        comanda = comandaA();

    return comanda


#comenzile ce le interpreteaza ========================================
iesire =0
NOTE = ["make a note", "write this down", "remember this", "type this"]
def assistant(comanda):
    "if statements for executing commands"
    
    if 'change your voice' in comanda:
           global vocea
           if vocea==1:
            vocea=0
            speak('I have changed my voice back, sir!')
           else:
            vocea=1
            speak('I have changed my voice for you')
           
    elif 'close' in comanda:
        global iesire
        iesire = 1
    elif 'make a note' in comanda:
          speak("What would you like me to write down? ")
          scrie = comandaA()
          note(scrie)
          speak("I've made a note of that.")
        
    elif 'open ' in comanda:
        reg_ex = re.search('open (.+)', comanda)

        if reg_ex:
         
            domain =reg_ex.group(1)
            url = 'https://www.'+domain +'.com'
            webbrowser.open(url)
            print('Done!')
        else:
            pass

    elif 'how are you' in comanda:
        speak("I am good how are you?")
    elif 'joke' in comanda:
        res = requests.get(
                'https://icanhazdadjoke.com/',
                headers={"Accept":"application/json"}
                )
        if res.status_code == requests.codes.ok:
            speak(str(res.json()['joke']))
        else:
            speak('Hmmm Sorry sir I think I ran out of jokes.')

    elif 'search' in comanda:
         com = re.search('search (.+)', comanda)
         cautare= com.group(1)
         cautare_avansata(cautare)

speak('Good evening Andrei! My name is Snarky and i will be your bot assistant.')
#loop to continue executing multiple commands

while iesire==0:
    assistant(comandaA())
if iesire ==1:
    speak('I will close myself. Goodbye sir!')
    print('Program closed...')


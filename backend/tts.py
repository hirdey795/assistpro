# !pip install pyttsx3

import pyttsx3

# class speaker():
    
#     def __init__(self):
#         self.engine = pyttsx3.init('nsss')  # If windows, change param values

#     def speak(self, text):
#         engine = self.engine
#         engine.say(text)
#         print("🤖: ",text)
#         engine.runAndWait()

engine = pyttsx3.init()  # If windows, change param values

def speak(text):
        engine.say(text)
        print("🤖: ",text)
        engine.runAndWait()

from gtts import gTTS
import os
import time

tts = gTTS(text='쯉쯉쯉쯉쯉', lang='ko')
tts.save("hello.mp3")

while True:
	os.system("mpg321 hello.mp3")
	time.sleep(5)

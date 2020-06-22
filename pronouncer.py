import os
from gtts import gTTS
from pygame import mixer

def make_speech(text, lang='en', slow=False, filename='current_word.mp3'):
    filename = 'current_word.mp3'
    print('The dirs are', os.listdir(os.getcwd()))
    if filename in os.listdir(os.getcwd()):
        filename = '_' + filename
    speech = gTTS(text=text, lang=lang, slow=slow)
    speech.save(filename)
    return filename


def play_sound(filepath):
    if not mixer.get_init():
        mixer.init()
    mixer.music.load(filepath)
    mixer.music.play()
    while mixer.music.get_busy():
        continue

def say(text, lang='ru', slow=False):
    speech_file = make_speech(text, lang, slow)
    play_sound(speech_file)
    if speech_file.startswith('_'):
        os.remove(speech_file[1:])
    # os.remove()

def main():
    play_speech_of_text('Masio is a piece of stupid bad shit.')

if __name__ == '__main__':
    main()
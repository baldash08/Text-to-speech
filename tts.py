from gtts import gTTS
def text_to_speech(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    tts.save('output.mp3')
    # Дальнейший код для воспроизведения или сохранения файла
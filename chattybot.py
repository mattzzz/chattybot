"""
2023 - speech interface chat program to ChatGPT

Install:
    brew install portaudio flac
    pip install -r requirements.txt


don't forget to set env var for OpenAI key: 
    export OPENAI_API_KEY=""
    
"""
import logging
import io
# import pyaudio  # For capturing microphone input
import speech_recognition as sr  # For speech-to-text
import pyttsx3  # For text-to-speech
from openai import OpenAI
from mpg123 import Mpg123, Out123
from gtts import gTTS

logging.basicConfig(format='%(asctime)s %(message)s', level = logging.INFO)
logger = logging.getLogger(__name__)


# Initialize modules
recognizer = sr.Recognizer()
microphone = sr.Microphone()
with microphone as source:
    recognizer.adjust_for_ambient_noise(source)
tts_engine = pyttsx3.init()#"nsss")
# rate = tts_engine.getProperty('rate')
# tts_engine.setProperty('rate', rate-80)
client = OpenAI()

chats = [
            {"role": "system", "content": "you are a helpful personal assistant"}
        ]


def listen_with_mic():
    with microphone as source:
        # audio = recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    logger.debug('audio captured.')
    return audio


def transcribe_audio(audio):
    try:
        logger.debug('transcribing...')
        transcript = recognizer.recognize_google(audio)  
        # transcript = recognizer.recognize_whisper(audio)
    except sr.exceptions.UnknownValueError:
        logger.debug('no input speech heard.')
        transcript = None
    
    return transcript


def query_chatgpt(text):
    # This function needs to send a request to ChatGPT API and get the response
    chats.append({"role": "user", "content": text})

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=chats,
        stream = True
    )

    complete_response = ""
    part = ''
    for chunk in completion:
        word = chunk.choices[0].delta.content
        if not word: continue
        part += word
        if word in ',.?!':
            yield part
            complete_response += part
            part = ''

    chats.append({"role": "assistant", "content": complete_response})
    

def speak_text(text):
    # uses offline pyttsx3 engine
    tts_engine.say(text)
    tts_engine.runAndWait()


def speak_text_gtts(text):
    # uses google online cloud tts service
    tts = gTTS(text=text, lang='en')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)

    mp3 = Mpg123()
    mp3.feed(fp.read())

    out = Out123()

    for frame in mp3.iter_frames(out.start):
        out.play(frame)


def main():
    try:
        while True:
            logger.info("Listening...")
            audio = listen_with_mic()

            if not audio: continue
            
            text = transcribe_audio(audio)
            if not text: continue

            print(f"Transcribed: {text}")

            if text:
                print('ChatGPT: ', end = ' ')
                for response in query_chatgpt(text):
                    if response:
                        print(response, end = ' ', flush = True)

                        # speak_text(response)
                        speak_text_gtts(response)
                print()
    except KeyboardInterrupt:
        print("Program terminated by user.")


if __name__ == "__main__":
    main()

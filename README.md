# chattybot


chattybot is a python program that allows you to talk and listen to an LLM such as ChatGPT using voice via microphone.

## It is composed of following stages:

audio capture - using speech recognition\
speech to text - using OpenAI's Whisper or Google Cloud\
LLM - using ChatGPT, streaming to reduce latency\
text to speech - using pyttsx (offline) or google tts (online)

## Issues or improvements

* audio capture can be a bit flaky depending on changes in background noise


## Installation on MacOS
brew install portaudio flac mpg123 \
pip install -r requirements.txt

Don't forget to set env var for OpenAI key: \
    export OPENAI_API_KEY=""


    

# Using Humelo API

If you want to use Humelo's TTS service, you can get the token by executing ```python login.py```

After getting the token you have to define that ```token = "Access Token Address"``` (We will write this code later.)

Let's go back to the ```ChatGPT-OpenAI-Smart-Speaker/``` and rewrite some code to use Humelo's TTS.

Inside our ```smart_speaker.py```, we will make some changes.

## ```convert_to_mp3()```
Since ```VoiceSynthesizer.py``` generates ````.wav```` file, we have to covert it into ```.mp3``` format to play the sound using ```play_audio_file```.

Add the code below in ```smart_speaker.py```
```
def convert_to_mp3(input_file, output_file, bitrate='192k'):
    # Load the WAV file
    audio = AudioSegment.from_wav(input_file)

    # Export the audio in MP3 format
    audio.export(output_file, format="mp3", bitrate=bitrate)
```

## ```main()```
Our initial code:
```
def main():
    # run the program
    while True:
        if recognize_speech():
            prompt = speech()
            print(f"This is the prompt being sent to OpenAI: {prompt}")
            responses = chatgpt_response(prompt)
            message = responses.choices[0].text
            print(message)
            generate_audio_file(message)
            play_audio_file()
            pixels.off()
        else:
            print("Speech was not recognised")
            pixels.off()
```
Changed code:
```
from VoiceSynthesizer import VoiceSynthesizer

def main():

    token = "Access Token Address"
    text = "Hello, this voice is a speech synthesis test.     Hello, this voice is a speech synthesis test.     Hello, this voice is a speech synthesis test.     Hello, this voice is a speech synthesis test.   "
    voice_name = "vos-kt25"

    synthesizer = VoiceSynthesizer(token)

    # run the program
    while True:
        if recognize_speech():
            prompt = speech()
            print(f"This is the prompt being sent to OpenAI: {prompt}")
            responses = chatgpt_response(prompt)
            message = responses.choices[0].text
            print(message)

            text = message
            synthesizer.text_gen(voice_name, text)
            convert_to_mp3("tts.wav", "response.mp3")
            
            play_audio_file()
            pixels.off()
        else:
            print("Speech was not recognised")
            pixels.off()
```
```token = "Access Token Address"``` update Access Token Address as you received before.

### Now Humelo's STT should work!



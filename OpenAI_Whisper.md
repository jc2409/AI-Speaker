# Using Whisper 

We were using Google's Speech Recognition for our STT.

From now on, I will introduce how we can use Whisper in our code.

First, we will install Whisper Packages:
```pip install whisper```

Then, we should now update ```recognize_speech()``` and ```speech()``` functions.

## ```recognize_speech()```

Updated code:
```
import whisper
model = whisper.load_model("base")

def recognize_speech():
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Waiting for wake word...")
        while True:
            try:
                r.adjust_for_ambient_noise(source)
                audio_stream = r.listen(source)
                with open(_tempfile, "w+b") as f:
                    f.write(audio_stream.get_wav_data())
                    f.close()
                with open(_tempfile, 'rb') as audio_file:
                    try:
                        # convert the audio to text
                        result = openai.Audio.transcribe('whisper-1',audio_file,language="en")
                        print(f"Whisper thinks you said {result['text']}")
                        speech = result['text']
                        if ("Lily" not in speech) and ("Lily" not in speech):
                            # the wake word was not detected in the speech
                            print("Wake word not detected in the speech")
                            # Close the current microphone object  
                            return False
                        else:
                            # the wake word was detected in the speech
                            print("Found wake word!")
                            # wake up the display
                            pixels.wakeup()
                            return True
                    except sr.UnknownValueError:
                        print("Whisper could not understand audio")
                        print("Waiting for wake word...")
                        return False
                    except sr.RequestError as e:
                        print("Could not request results from Whisper; {0}".format(e))
                        print("Waiting for wake word...")
                        return False
                    finally:
                        f.close()
            except KeyboardInterrupt:
                print("Interrupted by User Keyboard")
                break

```
In this updated code, we have generated the temporary file where we will store our audio file. 

After that, we transcribe the audio using ```openai.Audio.transcribe('whisper-1',audio_file,language="en")```.

We can call the transcribed result by ```speech = result['text']```

## ```speech()```

Now, we will follow the same step for ```speech()``` function to implement whisper.

Updated code:
```
def speech():
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # play_audio_file("recognition_voice1.mp3") # play sound before it listens to a speaker
        print("Waiting for user to speak...")
        while True:
            try:
                r.adjust_for_ambient_noise(source)
                audio_stream = r.listen(source)
                # recognize speech using Google Speech Recognition
                with open(_tempfile, "w+b") as f:
                    f.write(audio_stream.get_wav_data())
                    f.close()
                with open(_tempfile, 'rb') as audio_file:
                    try:
                        # convert the audio to text
                        result = openai.Audio.transcribe('whisper-1',audio_file,language="ko")
                        print("Whisper thinks you said " + result['text'])
                        speech = result['text']
                        return speech
                    except sr.UnknownValueError:
                        play_audio_file("recognition_voice2.mp3")
                        print("Whisper could not understand audio")
                        print("Waiting for user to speak...")
                        continue
                    except sr.RequestError as e:
                        print("Could not request results from Whisper; {0}".format(e))
                        print("Waiting for user to speak...")
                        continue
                    finally:
                        audio_file.close()
            except KeyboardInterrupt:
                print("Interrupted by User Keyboard")
                break
```
I changed the language to Korean so that we can send the prompt to ChatGPT in Korean.

## (Optional) Using ```"gpt-3.5-turbo"``` model
Change the model engine to ```model_engine = "gpt_3.5-turbo"```

Change ```chatgpt_response()``` as below:
```
def chatgpt_response(prompt):
    # send the converted audio text to chatgpt
    response = openai.ChatCompletion.create(
        model=model_engine,
        messages=[
            {"role":"user", "content": f'{prompt}'}
        ],
        # prompt=prompt,
        max_tokens=1024,
        # n=1,
        temperature=0.7,
    )
    print(f'gpt res: {response}')
    return response
```

Change ```main()``` as below:
```
def main():

    token = "Humelo Accesss Token"
    text = "Hello, this voice is a speech synthesis test.     Hello, this voice is a speech synthesis test.     Hello, this voice is a speech synthesis test.     Hello, this voice is a speech synthesis test.   "
    voice_name = "vos-kt25"

    synthesizer = VoiceSynthesizer(token)

    # run the program
    while True:
        if recognize_speech():
            prompt = speech()
            print(f"This is the prompt being sent to OpenAI: {prompt}")
            responses = chatgpt_response(prompt+' 50자내로 답변해줘') # Add "50자내로 답변해줘" to receive short answer
            # message = responses.choices[0].text
            message = responses["choices"][0]["message"]["content"]
            print(message)

            text = message
            # generate_audio_file(message)
            synthesizer.text_gen(voice_name, text)
            convert_to_mp3("tts.wav", "response.mp3")
            
            play_audio_file("response.mp3")
            pixels.off()
        else:
            print("Speech was not recognised")
            pixels.off()
```
I added "50자내로 답변해줘" to receive short answer.

## That's it! Now you can use OpenAI's Whisper as your STT.

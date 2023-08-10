# AI-Speaker
## AI Speaker using ChatGPT for Connected Car Project

In this project, we will use Raspberry Pi 4B, ReSpeaker 4-mic Array for Raspberry Pi (You can use other microphones but you will need other codes to test them), and USB Speaker to design our AI Speaker.

### Prepare Your Hardware
First, you have to install Raspberry Pi os (Raspberry Pi 64-bit recommended).
- Prepare your Micro SD card and follow the tutorial on YouTube https://www.youtube.com/watch?v=ntaXWS8Lk34Download
- Either work directly on Raspberry Pi or use SSH (Secure Shell) to program it
- If you want to use SSH, you have to enable SSH and configure your wireless LAN before installing the os (If you have not, you need to reinstall the operating system)

### Connect with SSH
Once you are ready, you can now access your Raspberry Pi
1. Open the terminal and write the code below:
  ```
  ssh <USER_NAME>@<IP_ADDRESS>
  ```
  Replace `<USER_NAME>` and `<IP_ADDRESS>` with your user name and IP address that you specified in the settings

2. Enter the password
3. Congrats! Now you are remotely connected to your Raspberry Pi

(You can also use text editors if Remote-SSH extension is installed)

### Install the driver for ReSpeaker
If you are connected to your Raspberry Pi, you are now ready to install the driver for our ReSpeaker
1.  First, we will get the Seeed voice card source code:
```
sudo apt-get update
git clone https://github.com/HinTak/seeed-voicecard.git
cd seeed-voicecard
sudo ./install.sh
sudo reboot
```
2. Select audio output on Raspberry Pi:
```
sudo raspi-config
# Select 1 System options
# Select S2 Audio
# Select your preferred Audio output device (USB if you are connecting speaker with usb cable)
# Select Finish
```
3. Check that the sound card name looks like this:
```
pi@raspberrypi:~ $ arecord -L
null
    Discard all samples (playback) or generate zero samples (capture)
jack
    JACK Audio Connection Kit
pulse
    PulseAudio Sound Server
default
playback
ac108
sysdefault:CARD=seeed4micvoicec
    seeed-4mic-voicecard,
    Default Audio Device
dmix:CARD=seeed4micvoicec,DEV=0
    seeed-4mic-voicecard,
    Direct sample mixing device
dsnoop:CARD=seeed4micvoicec,DEV=0
    seeed-4mic-voicecard,
    Direct sample snooping device
hw:CARD=seeed4micvoicec,DEV=0
    seeed-4mic-voicecard,
    Direct hardware device without any conversions
plughw:CARD=seeed4micvoicec,DEV=0
    seeed-4mic-voicecard,
    Hardware device with all software conversions
usbstream:CARD=seeed4micvoicec
    seeed-4mic-voicecard
    USB Stream Output
usbstream:CARD=ALSA
    bcm2835 ALSA
    USB Stream Output
```
If your results are the same as mine, you are ready for the next step!

### Record sound with Python
We will check if our microphone and speaker are working
1. Clone https://github.com/respeaker/4mics_hat.git repository to your Raspberry Pi:
```
git clone https://github.com/respeaker/4mics_hat.git
```
2. Install the necessary dependencies from mic_hat repository folder
```
sudo apt-get install portaudio19-dev libatlas-base-dev
cd 4mics_hat/ # Do not forget to change to the correct directory
pip3 install -r requirements.txt
```
3. We use PyAudio python library to record sound with Python
```
python3 recording_examples/get_device_index.py
```
4. You will see the device ID as below.
```
Input Device id  2  -  seeed-4mic-voicecard: - (hw:1,0)
```
5. To record the sound, open recording_examples/record.py file with nano or other text editor and change RESPEAKER_INDEX = 2 to index number of ReSpeaker on your system. Then run python script record.py to make a recording:
```
python3 recording_examples/record.py
```
6. To play the recorded samples you can use aplay:
```
aplay output.wav # Recorded voice will be saved in the output.wav file
```

If the sound does not play, check if both microphone and speaker are connected properly and the right audio output is selected 
(You can check using ```raspi-config```)


## ChatGPT Smart Speaker (speech recognition and text-to-speech using OpenAI and gTTS)
We will use Olney1's Repository to set-up our AI Speaker
1. Clone the repository
```
https://github.com/Olney1/ChatGPT-OpenAI-Smart-Speaker.git
```
2. Install and update essential packages
```
pip install openai gTTS pyaudio SpeechRecognition playsound python-dotenv pyobject
sudo apt update
sudo apt install python3-gpiozero
```
3. Get your API key from OpenAPI (You will probably need to add your payment method if you are not new to OpenAI)
4. Set up the environment variable for your Open API Key. To do this create a ```.env file``` in the same directory and add your API Key to the file like this:
``` OPENAI_API_KEY = "API KEY GOES HERE" ```
5. There is an initial code inside ```smart_speaker.py``` that does not work well, therefore we have to replace it with our new code:
- First, install the required package using: ```pip install pydub```
- Initial code looks like this:
```
def play_audio_file():
    # play the audio file and wake speaking LEDs
    pixels.speak()
    # os.system("mpg321 response.mp3")
    playsound("response.mp3", block=False) # There’s an optional second argument, block, which is set to True by default. Setting it to False makes the function run asynchronously.
```
- Replace the initial code above with our new code below:

```
from pydub import AudioSegment
from pydub.playback import play

def play_audio_file():
    song = AudioSegment.from_mp3("response.mp3")
    play(song)
```
6. You are now ready to use AI Speaker. Simply move to ```ChatGPT-OpenAI-Smart-Speaker``` directory and execute ```smart_speaker.py```
7. Say the wake word ```Lily``` and ask the question when it is ready. (You can exit the code using ```ctr + Z```)
8. If you cannot hear well, you may need to adjust the volume using the code below:
```
alsamixer
```
9. Exit the interface after the adjustment


### That is it! You can now play with the AI Speaker!

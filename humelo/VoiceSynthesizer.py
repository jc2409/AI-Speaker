import http.client
import json

class VoiceSynthesizer:
    def __init__(self, token):
        self.token = token
        self.conn = http.client.HTTPSConnection("aivoicestudio.ai")
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Service-Code": "001API999",
            "Content-Type": "application/json"
        }
        self.params = "?bgm=false&preview=true"
    
    def text_gen(self, voice_name, input_text):
        payload = {
            "voiceName": voice_name,
            "text": input_text,
            "emotion": "neutral",
            "language": "",
            "gender": "",
            "pitch": 1.0,
            "speed": 1.0,
            "fileFormat": "WAV",
            "sampleRate": 24000,
            "volume": 50,
            "isTestEnvironment": True
        }
        payload_json = json.dumps(payload)

        self.conn.request("POST", "/api/v1/voice-synthesis" + self.params, body=payload_json, headers=self.headers)
        response = self.conn.getresponse()

        if response.status == 301:
            redirect_location = response.getheader("Location")
            print("Redirecting to:", redirect_location)

            redirected_conn = http.client.HTTPSConnection("aivoicestudio.ai")
            redirected_conn.request("POST", redirect_location, body=payload_json, headers=self.headers)
            redirected_response = redirected_conn.getresponse()

            print("Response Status:", redirected_response.status)
            print("Response Headers:")
            for header, value in redirected_response.getheaders():
                print(header + ":", value)

            if redirected_response.getheader("Content-Type") == "application/octet-stream":
                with open("tts.wav", "wb") as file:
                    file.write(redirected_response.read())
                print("File saved as tts.wav")
            else:
                print("Response Body:")
                print(redirected_response.read().decode())

            redirected_conn.close()
        else:
            print("Response Status:", response.status)
            print("Response Headers:")
            for header, value in response.getheaders():
                print(header + ":", value)

            if response.getheader("Content-Type") == "application/octet-stream":
                with open("tts.wav", "wb") as file:
                    file.write(response.read())
                print("File saved as tts.wav")
            else:
                print("Response Body:")
                print(response.read().decode())

    def close_connection(self):
        self.conn.close()



token = "eyJhbGciOiJSUzI1NiJ9.eyJyb2xlIjoiUmp5ZWZuWWVHWl9idEZ2cUlqNDRNZyIsInNlcnZpY2VDb2RlIjoiUG5pWVZkSUN3Z3M5cWxlelM5VUkzUSIsImVtYWlsIjoiVlFnUW9ndGpOdHd1ODM0T2dwSGlrQSIsIm1lbWJlcklkIjoiVG5EY29EZ0RDSE9SV1lscGdvXzZHUSIsImlhdCI6MTY4OTgyNzMyMSwiZXhwIjoxNjkwNDMyMTIxfQ.Qgqh7xWljBl_RzoZq67-7Jl7a3qRc0DN4QXnbfnUI1Oy70kumk7wzjJXxblS0unwCn_cpQGr3aGFHjn8pi2dwQ1ccXm2NDnKjwTWgqoZu9olZsGZS7Gm-NBVrjqib0M8R9CvSW-GWgdiFoZ9EMFdrGI6Z3bpJQMvjcjCuZON1sX5riKC5nm2CQMaW4VpqxUxOHlUtnWfvbl4agCcdW2qNLhRZQlEIBfcizBm_u3XBwF1hxNXZQbV2IVS8gVtHdusCVjxJYVrqgkrLInN04Dg8oicIaBTZGS1e2I1VUL-q0PI69FZSq-g85Vn86svPAJHmEXKWQCbIXnA2W25QKbfMw"
text = "Hello, this voice is a speech synthesis test.     Hello, this voice is a speech synthesis test.     Hello, this voice is a speech synthesis test.     Hello, this voice is a speech synthesis test.   "
voice_name = "vos-kt25"


synthesizer = VoiceSynthesizer(token)
synthesizer.text_gen(voice_name, text)
synthesizer.close_connection()

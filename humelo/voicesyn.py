import http.client
import json

# Create a connection to the server
conn = http.client.HTTPConnection("aivoicestudio.ai")

# Set the request headers
headers = {
    "Service-Code": "001API999",
    "Content-Type": "application/json"
}

# Set the request parameters
params = "?bgm=false&preview=true"

# Set the request body
payload = {
    "voiceName": "COMMON-VOICE",
    "text": "안녕하세요 음성 합성 인수 테스트 입니다.",
    "emotion": "neutral",
    "language": "",
    "gender": "",
    "pitch": 1.0,
    "speed": 1.0,
    "fileFormat": "WAV",
    "sampleRate": 24000,
    "volume": 50,
    "isTestEnvironment": true
}
payload_json = json.dumps(payload)

# Send a POST request to the server
conn.request("POST", "/api/v1/voice-syn" + params, body=payload_json, headers=headers)

# Get the response from the server
response = conn.getresponse()

# Print the response status code
print("Response Status:", response.status)

# Print the response headers
print("Response Headers:")
for header, value in response.getheaders():
    print(header + ":", value)

# Check if the response is binary data
if response.getheader("Content-Type") == "application/octet-stream":
    # Save the binary data as a WAV file
    with open("tts.wav", "wb") as file:
        file.write(response.read())
    print("File saved as tts.wav")
else:
    # Print the response body
    print("Response Body:")
    print(response.read().decode())

# Close the connection
conn.close()



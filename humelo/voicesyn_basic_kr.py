import http.client
import json

# Create a connection to the server
conn = http.client.HTTPSConnection("aivoicestudio.ai")

# Set the request headers
headers = {
    "Authorization": "Bearer e7Jl7a3qgdiFoZ9EJYVMw",
    "Service-Code": "001API999",
    "Content-Type": "application/json"
}

# Set the request parameters
params = "?bgm=false&preview=true"

# Set the request body
payload = {
    "voiceName": "vos-kt25",
    "text": "Hello, Thankyou.",
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

# Send a POST request to the server
conn.request("POST", "/api/v1/voice-synthesis" + params, body=payload_json, headers=headers)

# Get the response from the server
response = conn.getresponse()

# Check if it's a redirect
if response.status == 301:
    redirect_location = response.getheader("Location")
    print("Redirecting to:", redirect_location)

    # Create a connection to the redirected location
    redirected_conn = http.client.HTTPSConnection("aivoicestudio.ai")
    redirected_conn.request("POST", redirect_location, body=payload_json, headers=headers)
    redirected_response = redirected_conn.getresponse()

    # Print the response status code
    print("Response Status:", redirected_response.status)

    # Print the response headers
    print("Response Headers:")
    for header, value in redirected_response.getheaders():
        print(header + ":", value)

    # Check if the response is binary data
    if redirected_response.getheader("Content-Type") == "application/octet-stream":
        # Save the binary data as a WAV file
        with open("tts.wav", "wb") as file:
            file.write(redirected_response.read())
        print("File saved as tts.wav")
    else:
        # Print the response body
        print("Response Body:")
        print(redirected_response.read().decode())

    # Close the redirected connection
    redirected_conn.close()
else:
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

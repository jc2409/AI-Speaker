import http.client
import json

# Create a connection to the server
conn = http.client.HTTPSConnection("aivoicestudio.ai")

# Set the request headers
headers = {
    "Service-Code": "001API999",
    "Content-Type": "application/json; charset=UTF-8"
}

# Set the request body
payload = {
    "email": "test001",
    "password": "password1!",
    "recaptchaResponse": "true"
}
payload_json = json.dumps(payload)

print("Where am I")
# Send a POST request to the server
conn.request("POST", "/api/v1/token/authenticate", body=payload_json, headers=headers)
print("Where am I")

# Get the response from the server
response = conn.getresponse()
print("Where am I")

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

    # Print the response body
    print("Response Body:")
    print(response.read().decode())

# Close the connection
conn.close()


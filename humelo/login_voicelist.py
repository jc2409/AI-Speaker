import http.client
import json
import time

def get_substring(string):
    start_index = string.find("access_token\":") + len("access_token\":")
    end_index = string.find(",\"refresh_token")
    if start_index < end_index:
        return string[start_index:end_index]
    else:
        return ""

# Create a connection to the server
conn = http.client.HTTPSConnection("aivoicestudio.ai")

# Set the request headers
login_headers = {
    "Service-Code": "001API999",
    "Content-Type": "application/json; charset=UTF-8"
}

voicelist_headers = {
    "Authorization": "{access-token}",
    "Service-Code": "001API999",
    "Content-Type": "application/json"
}

# Set the request body
payload = {
    "email": "test001",
    "password": "password1!",
    "recaptchaResponse": "true"
}
payload_json = json.dumps(payload)

# Send a POST request to the server
conn.request("POST", "/api/v1/token/authenticate", body=payload_json, headers=login_headers)

# Get the response from the server
response = conn.getresponse()

# Check if it's a redirect
if response.status == 301:
    redirect_location = response.getheader("Location")
    print("Redirecting to:", redirect_location)

    # Create a connection to the redirected location
    redirected_conn = http.client.HTTPSConnection("aivoicestudio.ai")
    redirected_conn.request("POST", redirect_location, body=payload_json, headers=login_headers)
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
    input_string = redirected_response.read().decode()
    substring = get_substring(input_string)
    
    voicelist_headers["Authorization"] = substring
    
    print("Substring")
    print(substring)
    
    time.sleep(1)
    
    redirected_conn.request("GET", redirect_location, headers=voicelist_headers)
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

    time.sleep(1)
    
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


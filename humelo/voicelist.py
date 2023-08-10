import http.client
import json

# Create a connection to the server
conn = http.client.HTTPSConnection("aivoicestudio.ai")

# Set the request headers
headers = {
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiJ9.eyJyb2xlIjoiUmp5ZWZuWWVHWl9idEZ2cUlqNDRNZyIsInNlcnZpY2VDb2RlIjoiUG5pWVZkSUN3Z3M5cWxlelM5VUkzUSIsImVtYWlsIjoiVlFnUW9ndGpOdHd1ODM0T2dwSGlrQSIsIm1lbWJlcklkIjoiVG5EY29EZ0RDSE9SV1lscGdvXzZHUSIsImlhdCI6MTY4OTgyNzMyMSwiZXhwIjoxNjkwNDMyMTIxfQ.Qgqh7xWljBl_RzoZq67-7Jl7a3qRc0DN4QXnbfnUI1Oy70kumk7wzjJXxblS0unwCn_cpQGr3aGFHjn8pi2dwQ1ccXm2NDnKjwTWgqoZu9olZsGZS7Gm-NBVrjqib0M8R9CvSW-GWgdiFoZ9EMFdrGI6Z3bpJQMvjcjCuZON1sX5riKC5nm2CQMaW4VpqxUxOHlUtnWfvbl4agCcdW2qNLhRZQlEIBfcizBm_u3XBwF1hxNXZQbV2IVS8gVtHdusCVjxJYVrqgkrLInN04Dg8oicIaBTZGS1e2I1VUL-q0PI69FZSq-g85Vn86svPAJHmEXKWQCbIXnA2W25QKbfMw",
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

# Send a GET request to the server
conn.request("GET", "/api/v1/voice", body=payload_json, headers=headers)

# Get the response from the server
response = conn.getresponse()

# Check if it's a redirect
if response.status == 301:
    redirect_location = response.getheader("Location")
    print("Redirecting to:", redirect_location)

    # Create a connection to the redirected location
    redirected_conn = http.client.HTTPSConnection("aivoicestudio.ai")
    redirected_conn.request("GET", redirect_location, body=payload_json, headers=headers)
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

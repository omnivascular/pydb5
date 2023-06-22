import requests


# https://barcode.orcascan.com/?data=Hello&text=World

url = "https://barcode.orcascan.com/?data=ZeeIsCool&text=Scan Me&format=png"

# Send a GET request to the API endpoint
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Get the filename from the response headers or use a default filename
    # filename = response.headers.get('content-disposition', 'image.jpg').split('filename=')[1]
    filename = "testimage2.png"

    # Save the image content to a file
    with open(filename, "wb") as file:
        file.write(response.content)
    print("Image saved successfully.")
else:
    print("Failed to retrieve the image.")

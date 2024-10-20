# Automating SSRF Exploitation with Python

This Python script automates HTTP POST requests for **Server-Side Request Forgery (SSRF)** exploitation by replacing parameters from a wordlist into a request file template. It processes responses to extract relevant data and performs follow-up requests. This tool is ideal for penetration testers and security professionals working on web application security.


# Installation

**Clone the repository**:
   ```bash
   git clone https://github.com/4l4chh46/request_auto_resend.git
   cd request_auto_resend
```

# Usage

```
python request_auto_resend.py -r <request_file> -w <wordlist_file> -u <base_url>

```
usage: request_auto_resend.py [-h] -r REQUEST_FILE -w WORDLIST_FILE -u BASE_URL

Automated script to send HTTP requests using a request file and wordlist, and
perform SSRF exploitation.

optional arguments:
  -h, --help            show this help message and exit
  -r REQUEST_FILE, --request_file REQUEST_FILE
                        Path to the request file (e.g., ssrf.request)
  -w WORDLIST_FILE, --wordlist_file WORDLIST_FILE
                        Path to the wordlist file (e.g., wordlist.txt)
  -u BASE_URL, --base_url BASE_URL
                        Base URL for the second request (e.g.,
                        http://editorial.htb/)

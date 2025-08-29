"""
Web app to test:
    http://10.0.0.217/DVWA/
"""

import requests

wordlist = open('common_web_dirs.txt', 'r')

# target_url = input("Enter host to scan: ")

for word in wordlist:
    print(word)

# request = requests.get(target_url)

# print(request.status_code)

"""
have user input url

initialize wordlist

def dir_search(url)
    for each word in the wordlist
        new url = input_url + word appended

        if request_of_new_url.status = ok
            print directory found (word)
            
            dir_search(new_url)

"""

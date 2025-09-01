"""
TODO:

    add user input rather than using hackthissite everytime
    add threading so it can go faster (it's very slow now)
    add arguements so users can add whatever wordlist they like
"""

import requests
import time

# dirlist = open('common_web_dirs.txt',)

with open('common_web_dirs.txt', 'r') as f:
    dirlist = [line.strip() for line in f.readlines() if line.strip()]

# target_url = input("Enter host to scan: ")




def dir_search(url, max_depth=2, current_depth=0):

    # Had an issue with infinite recursion so here's to prevent that
    if current_depth > max_depth:
        return

    found_dirs = []

    print(f"Searching {url}")

    for directory in dirlist:
        if url.endswith('/'):
            test_url = url + directory
        else:
            test_url = url + '/' + directory


        try:
            new_request = requests.get(test_url, timeout=5, allow_redirects=True)

            if new_request.history:
                print(f"  Redirect chain: {[r.status_code for r in new_request.history]} -> {new_request.status_code}")
                print(f"  Final URL: {new_request.url}")

            if new_request.status_code == 200:
                print(f"Directory found! {test_url}, HTTP: {new_request.status_code}")
                found_dirs.append(test_url)

            elif new_request.status_code == 301:
                print(f"Redirect on: {test_url}, HTTP: {new_request.status_code}")
                found_dirs.append(test_url)
            
            elif new_request.status_code == 302:
                print(f"Directory found! {test_url}, HTTP: {new_request.status_code}")
                found_dirs.append(test_url)
            
            elif new_request.status_code == 403:
                print(f'Forbidden: {test_url}, HTTP: {new_request.status_code}')
            
            elif new_request.status_code == 404:
                pass

            time.sleep(0.1)
        
        except requests.exceptions.RequestException as e:
            print(f'Error accessing {test_url}')

    # Handle our super duper special recursion process 
    if current_depth < max_depth - 1:
        for found_dir in found_dirs:
            dir_search(found_dir, max_depth, current_depth + 1)


dir_search('https://hackthissite.org')

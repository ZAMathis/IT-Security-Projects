"""
TODO:

    add user input rather than using hackthissite everytime
    add threading so it can go faster (it's very slow now) <--- IN PROGRESS
    add arguements so users can add whatever wordlist they like
"""

import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

# Open up default wordlist for now
with open("common_web_dirs.txt", "r") as f:
    dirlist = [line.strip() for line in f.readlines() if line.strip()]


def test_single_url(url):
    # Returns a url, the status code of it, and whether or not it's worth scanning

    try:
        response = requests.get(url, timeout=5, allow_redirects=True)

        interesting = response.status_code in [200, 301, 302, 403]

        return (url, response.status_code, interesting)
    except requests.exceptions.RequestException:
        return (url, None, False)


# New dir_search function, but for threading:
def dir_search_threaded(base_url, max_threads=10):
    urls_to_test = []

    for directory in dirlist:
        if base_url.endswith('/'):
            test_url = base_url + directory
        else:
            test_url = base_url + '/' + directory
        urls_to_test.append(test_url)

    # Now let's add the threading
    found_dirs = []

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        future_to_url = {
            executor.submit(test_single_url, url): url for url in urls_to_test
        }

        for future in as_completed(future_to_url):
            url, status_code,is_interesting = future.result()

            # if/elif logic goes here

            if is_interesting:
                # print result, append to found_dirs
            pass

    return found_dirs

def dir_search(url, max_depth=2, current_depth=0):

    # Had an issue with infinite recursion so here's to prevent that
    if current_depth > max_depth:
        return

    found_dirs = []

    print(f"Searching {url}")

    for directory in dirlist:
        if url.endswith("/"):
            test_url = url + directory
        else:
            test_url = url + "/" + directory

        try:
            new_request = requests.get(test_url, timeout=5, allow_redirects=True)

            # For debugging:
            """
            if new_request.history:
                print(
                    f"  Redirect chain: {[r.status_code for r in new_request.history]} -> {new_request.status_code}"
                )
                print(f"  Final URL: {new_request.url}")
            """

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
                print(f"Forbidden: {test_url}, HTTP: {new_request.status_code}")

            elif new_request.status_code == 404:
                pass

            time.sleep(0.1)

        except requests.exceptions.RequestException:
            print(f"Error accessing {test_url}")

    # Handle our super duper special recursion process
    if current_depth < max_depth - 1:
        for found_dir in found_dirs:
            dir_search(found_dir, max_depth, current_depth + 1)


if __name__ == "__main__":
    dir_search("https://hackthissite.org")

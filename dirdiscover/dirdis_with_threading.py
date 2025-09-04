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

        is_interesting = response.status_code in [200, 302]

        return (url, response.status_code, is_interesting)
    except requests.exceptions.RequestException:
        return (url, None, False)


# New dir_search function, but for threading:
def dir_search_threaded(base_url, max_threads=10, max_depth=2, current_depth=0):

    # preventing infinite recursion
    if current_depth > max_depth:
        return

    urls_to_test = []

    for directory in dirlist:
        if base_url.endswith("/"):
            test_url = base_url + directory
        else:
            test_url = base_url + "/" + directory
        urls_to_test.append(test_url)

    # Now let's add the threading
    found_dirs = []

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        future_to_url = {
            executor.submit(test_single_url, url): url for url in urls_to_test
        }

        for future in as_completed(future_to_url):
            url, status_code, is_interesting = future.result()

            # if/elif logic goes here
            match status_code:
                case 200:
                    print(f"Possible directory found: {url}, HTTP: {status_code}")
                    found_dirs.append(url)
                case 301:
                    print(f"Redirect on: {url}, HTTP: {status_code}")
                case 302:
                    print(f"Directory found/moved: {url}, HTTP: {status_code}")
                    found_dirs.append(url)
                case 403:
                    print(f"Forbidden directory: {url}, HTTP: {status_code}")

    if current_depth < max_depth - 1:
        for directory in found_dirs:
            dir_search_threaded(directory, max_threads, max_depth, current_depth + 1)

    return found_dirs


if __name__ == "__main__":
    # dir_search("https://hackthissite.org")
    print("Beginning search")
    dir_search_threaded("https://hackthissite.org")

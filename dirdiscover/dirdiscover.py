import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests


# function to help filter out false positives
def get_baseline_response(base_url):
    fake_url = base_url + "/xyzdefinitely-fake-12345-notreal"

    try:
        response = requests.get(fake_url, timeout=5, allow_redirects=True)
        return len(response.content), response.status_code, response.text
    except:
        return 0, 404, ""


def test_single_url(url, baseline_length=None, baseline_content=None):
    try:
        response = requests.get(url, timeout=5, allow_redirects=True)

        # ensure we're not getting any false positives
        if baseline_length and len(response.content) == baseline_length:
            is_interesting = False
        else:
            is_interesting = response.status_code in [200, 302]

        return (url, response.status_code, is_interesting, len(response.content))
    except requests.exceptions.RequestException:
        return (url, None, False, 0)


def dir_search_threaded(base_url, max_threads=10, max_depth=2, current_depth=0):

    # preventing infinite recursion
    if current_depth > max_depth:
        return []

    # get baseline response for comparison
    baseline_length, baseline_status, baseline_content = get_baseline_response(base_url)
    print(f"Baseline for {base_url}: {baseline_status} with {baseline_length} bytes")

    urls_to_test = []

    for directory in dirlist:
        if base_url.endswith("/"):
            test_url = base_url + directory
        else:
            test_url = base_url + "/" + directory
        urls_to_test.append(test_url)

    found_dirs = []

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        future_to_url = {
            executor.submit(test_single_url, url, baseline_length): url
            for url in urls_to_test
        }

        for future in as_completed(future_to_url):
            url, status_code, is_interesting, content_length = future.result()

            if is_interesting and content_length > len(baseline_content):
                print(
                    f"Possible directory found: {url}, HTTP: {status_code}, {content_length} bytes"
                )
                found_dirs.append(url)

    if current_depth < max_depth - 1:
        for directory in found_dirs:
            dir_search_threaded(directory, max_threads, max_depth, current_depth + 1)

    return found_dirs


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Threaded python web directory scanner"
    )

    parser.add_argument(
        "-u",
        "--url",
        help="Target hostname to scan (example: http|https://YOURTARGET.com)",
    )

    parser.add_argument(
        "-w",
        "--wordlist",
        default="common_web_dirs.txt",
        help="Wordlist to use if desired, default is common_web_dirs.txt",
    )

    args = parser.parse_args()

    try:
        with open(args.wordlist, "r") as wl:
            dirlist = [line.strip() for line in wl.readlines() if line.strip()]
            print(f"Loaded {len(dirlist)} words from {args.wordlist}")
    except FileNotFoundError:
        print(
            f"Error: could not find {args.wordlist}. Try moving to program directory. Exiting..."
        )
        exit(1)

    print(f"Beginning search on {args.url}")
    dir_search_threaded(args.url)

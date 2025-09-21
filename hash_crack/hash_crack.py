import hashlib

"""
TODO:
add argparse
    add arguements for hashtype, for multiple hashes in a file, and custom wordlists
add more encryption types
"""

TEST_HASH = hashlib.sha1("LuckyCharm".encode()).hexdigest()


def compare_md5(user_hash, word):
    hashed_word = hashlib.md5(word.encode()).hexdigest()

    if user_hash == hashed_word:
        return True


def compare_sha1(user_hash, word):
    hashed_word = hashlib.sha1(word.encode()).hexdigest()

    if user_hash == hashed_word:
        return True


def check_hash(user_hash, wordlist, hash_type):
    is_found = False

    for word in wordlist:
        match (hash_type):
            case "md5":
                if compare_md5(user_hash, word):
                    print(f"Password found! {word}, {hash_type}")
                    is_found = True
                    break

            case "sha1":
                if compare_sha1(user_hash, word):
                    print(f"Password found! {word}, {hash_type}")
                    is_found = True
                    break

    if not is_found:
        print("Nope")


if __name__ == "__main__":

    with open("passwords.txt", "r") as wl:
        pass_list = [line.strip() for line in wl.readlines() if line.strip()]
        print(f"loaded {len(pass_list)} words from passwords.txt")

    check_hash(TEST_HASH, pass_list, "sha1")

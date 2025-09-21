import hashlib

"""
TODO:
add argparse
    add arguements for hashtype, for multiple hashes in a file, and custom wordlists
add more encryption types
"""

TEST_HASH = hashlib.sha1("LuckyCharm".encode()).hexdigest()


# Combining compare functions
def compare_hash(user_hash, word, hash_type):
    match (hash_type):
        case "md5":
            return (
                True if hashlib.md5(word.encode()).hexdigest() == user_hash else False
            )
        case "sha1":
            return (
                True if hashlib.sha1(word.encode()).hexdigest() == user_hash else False
            )


def check_hash(user_hash, wordlist, hash_type):
    is_found = False

    for word in wordlist:
        match (hash_type):
            case "md5":
                if compare_hash(user_hash, word, hash_type):
                    print(f"Password found! {word}, {hash_type}")
                    is_found = True
                    break

            case "sha1":
                if compare_hash(user_hash, word, hash_type):
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

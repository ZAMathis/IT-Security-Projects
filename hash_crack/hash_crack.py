import argparse
import hashlib

"""
TODO:
add argparse <-- DONE
    add arguments for hashtype <-- DONE 
    for multiple hashes in a file 
    custom wordlists <-- DONE
add more encryption types <-- IN PROGRESS
add ability to use a list of hashes
"""


# compare function
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
        case "sha224":
            return (
                True
                if hashlib.sha224(word.encode()).hexdigest() == user_hash
                else False
            )
        case "sha256":
            return (
                True
                if hashlib.sha256(word.encode()).hexdigest() == user_hash
                else False
            )
        case "sha384":
            return (
                True
                if hashlib.sha384(word.encode()).hexdigest() == user_hash
                else False
            )
        case "sha512":
            return (
                True
                if hashlib.sha512(word.encode()).hexdigest() == user_hash
                else False
            )

        case _:
            print(
                "Invalid encryption type. Could not be added to program, but check your spelling"
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
    parser = argparse.ArgumentParser(
        description="Command line tool written in python to crack hashes"
    )

    parser.add_argument("-t", "--target", help="Target hash to crack")

    parser.add_argument(
        "-w",
        "--wordlist",
        help="Dictionary/wordlist to use to crack the hash",
        default="passwords.txt",
    )

    parser.add_argument(
        "--hashtype",
        help="Type of hash that you're trying to crack. I.e md5, sha1, etc",
    )

    args = parser.parse_args()

    try:
        with open(args.wordlist, "r") as wl:
            wordlist = [line.strip() for line in wl.readlines() if line.strip()]
            print(f"Loaded {len(wordlist)} lines from {args.wordlist}")
    except FileNotFoundError:
        print("Could not find provided wordlist, exiting...")
        exit()

    check_hash(args.target, wordlist, args.hashtype)

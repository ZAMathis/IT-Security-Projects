import argparse
import hashlib

"""
TODO:
add option to save output of results to a file <-- IN PROGRESS
add ability to actually FIND OUT what type of hash is inputted, if possible

BUGS:
there is a bug that if the user is decrypting a list, it will print out "Nope" at the top
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
        if compare_hash(user_hash, word, hash_type):
            is_found = True
            return f"{user_hash} = {word}: {hash_type}"

    if not is_found:
        return "Password not found with current hashtype/wordlist!"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Command line tool written in python to crack hashes"
    )

    parser.add_argument("-t", "--target", help="Target hash to crack")

    parser.add_argument(
        "-wl",
        "--wordlist",
        help="Dictionary/wordlist to use to crack the hash",
        default="passwords.txt",
    )

    parser.add_argument(
        "-ht",
        "--hashtype",
        help="Type of hash that you're trying to crack. I.e md5, sha1, etc",
    )

    parser.add_argument(
        "-f", "--file", help="Target file with a list of hashes to crack"
    )

    parser.add_argument("-o", "--output", help="Output results to a file")

    args = parser.parse_args()

    try:
        with open(args.wordlist, "r") as wl:
            wordlist = [line.strip() for line in wl.readlines() if line.strip()]
            print(f"Loaded {len(wordlist)} lines from {args.wordlist}")
    except FileNotFoundError:
        print("Could not find provided wordlist, exiting...")
        exit()

    if args.target:
        result = check_hash(args.target, wordlist, args.hashtype)
        # lets check and see if user wants to output results first
        if args.output:
            with open(f"{args.output}", "w") as output_file:
                output_file.write(result)
                print(f"Results printed to {args.output}")
        print(result)

    elif args.file:
        try:
            with open(args.file, "r") as target_file:
                target_list = [
                    line.strip() for line in target_file.readlines() if line.strip()
                ]

                if args.output:
                    with open(f"{args.output}", "w") as output_file:
                        for line in target_list:
                            result = check_hash(line, wordlist, args.hashtype)
                            if result:
                                output_file.write(f"{result}\n")
                    print(f"Results outputted to {args.output}")
                else:
                    for line in target_list:
                        print(check_hash(line, wordlist, args.hashtype))
        except FileNotFoundError:
            print("Target file not found, check your spelling. Exiting...")
            exit()

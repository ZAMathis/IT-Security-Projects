import argparse
import hashlib

"""
TODO: refine the checktype flag and code a bit more if necessary

BUGS:
there is a bug that if the user is decrypting a list, it will print out "Nope" at the top
as a matter of fact, there's a good amount of bugs and formatting that could be 
done in regards to the text output
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
            print(f"Password found! {user_hash} = {word}: {hash_type}")
            is_found = True

    if not is_found:
        print("Password not found with current hashtype/wordlist!")
        return None


def identify_type(user_hash):
    try:
        if int(user_hash, 16):
            # placeholder variable
            possible_type: str = ""

            match len(user_hash):
                case 32:
                    possible_type = "MD5"
                case 40:
                    possible_type = "SHA1"
                case 56:
                    possible_type = "SHA224"
                case 64:
                    possible_type = "SHA256"
                case 96:
                    possible_type = "SHA384"
                case 128:
                    possible_type = "SHA512"

            if possible_type != "":
                return f"Possible hash type {possible_type}"
    except ValueError:
        return "Provided input is not a hexadecimal string"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Command line tool written in python to crack hashes"
    )

    parser.add_argument("-t", "--target", help="Target hash to crack")

    parser.add_argument(
        "-wl",
        "--wordlist",
        help="Dictionary/wordlist to use to crack the hash",
        # wordlist from repo, uncomment if unwanted
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

    parser.add_argument(
        "--checktype",
        help="Check what possible hash type is being provided. Currently only functional with a single hash",
    )

    args = parser.parse_args()

    if args.checktype:
        print(identify_type(args.checktype))
        exit()

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
        if args.output and result:
            with open(f"{args.hashtype}-decrypted.md5", "w") as output_file:
                output_file.write(result)
        else:
            print(result)

    elif args.file:
        try:
            with open(args.file, "r") as target_file:
                target_list = [
                    line.strip() for line in target_file.readlines() if line.strip()
                ]
                for line in target_list:
                    check_hash(line, wordlist, args.hashtype)
        except FileNotFoundError:
            print("Target file not found, check your spelling. Exiting...")
            exit()

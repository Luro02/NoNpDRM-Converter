import hashlib
import sys
import os


def setup():
    if os.path.exists("config") == False:
        key = []
        print("There are multiple Links in the Readme 2.0 of the Databse:")
        key.append(input("Please enter the Games Link: ") + "\n")  # 0
        key.append(input("Please enter the DLC Link: ") + "\n")  # 1
        key.append(input("Please enter the PSM Link: ") + "\n")  # 2
        key.append(input("Please enter the PSX Link: ") + "\n")  # 3
        key.append(
            input("We also need the Pastebin Link (it's under the Vita Section): ") + "\n")  # 4
        key.append(input(
            "There is a Hmac Key needed to download updates:(found on Vita Dev Wiki and it ends with 114) ") + "\n")  # 5
        key.append(input("Please enter the PSP Link: ") + "\n")  # 6
        # Hashcheck (I think that stuff isn't needed lol)
        hash_5 = hashlib.sha256((key[5].encode("utf-8")))
        hash_5 = hash_5.hexdigest()

        if hash_5 != "e2dc9e79cf7fc0ffaa3713ba14487ce90b68c8f94daff7d13c1b76d3a8bf925f":
            print("The Hash: " + hash_5)
            sys.exit("The Hmac Key is wrong")

        else:
            with open("config", "w", encoding='utf-8') as w:
                w.writelines(key)
                w.close()
            return key

    else:
        with open("config", "r", encoding='utf-8') as r:
            key = r.readlines()
            r.close()
        # Hashchecks ---------------------------------------------------------------------

        hash_5 = hashlib.sha256((key[5].encode("utf-8")))
        hash_5 = hash_5.hexdigest()

        if hash_5 != "e2dc9e79cf7fc0ffaa3713ba14487ce90b68c8f94daff7d13c1b76d3a8bf925f":
            print("The Hash: " + hash_5)
            sys.exit("The Hmac Key is wrong (config file)")

        else:
            return key

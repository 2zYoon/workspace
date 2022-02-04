import sys
import json

from pprint import pprint
from constant import *


def main():
    howtouse = "use: python dump.py [users]"
    args = sys.argv
    if len(args) >= 2:
        if args[1] == "users":
            with open(PATH_DATA + "users") as f:
                pprint(json.load(f))

        else:
            print(howtouse)   

    else:
        print(howtouse)   

if __name__ == "__main__":
    main()
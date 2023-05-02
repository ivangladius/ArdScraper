import argparse
import subprocess

import requests as requests
import sys

# my libs
from items import *
from scraper import *

json_path = "json"
test_path = "test_dir"


def usage():
    print("""
     Usage: ./main.py [--option]
            ./main.py --fetch -> fetch all json files
            ./main.py --init  -> initialize database with content
            """)


def fetch_json_pages():
    # get number of pages to fetch
    url = 'https://storage.googleapis.com/fra-uas-mobappex-ss23-amin/ard-feed-0.json'
    req = requests.get(url)
    content = json.loads(req.text)
    pages = content['totalPageCount']

    url_to_fetch = 'https://storage.googleapis.com/fra-uas-mobappex-ss23-amin/ard-feed-{}.json'
    # for p in range(int(pages)):
    #     fetch_url = url_to_fetch.format(p)
    #     print(f"fetching: {fetch_url}")
    #     req = requests.get(fetch_url)
    #     with open(f"json/json_file{p}.json", "w") as fd:
    #         fd.write(req.text)

    # improve performance instead of writing to 153 files write to one big one
    # so no need for 153 open / close calls io are slow

    with open("data.json", "a") as fd:
        for p in range(int(pages)):
            fetch_url = url_to_fetch.format(p)
            req = requests.get(fetch_url)
            fd.write(req.text)


class OptionMenu:
    def __init__(self):
        self.items = Scraper()

    def show(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--fetch', action='store_true')
        parser.add_argument('--init', action='store_true')
        args = parser.parse_args(sys.argv[1:])

        if args.fetch:
            json_path_exist = os.path.exists(json_path)
            test_path_exist = os.path.exists(test_path)
            if not json_path_exist:
                os.makedirs(json_path)
                print("created directory json")
            if not test_path_exist:
                os.makedirs(test_path)
                print("created directory test")

            fetch_json_pages()

        elif args.init:
            self.items.initialize().print()
        else:
            usage()
            sys.exit(1)


if __name__ == '__main__':
    OptionMenu().show()
# items = Items("feed.json").initialize()
# items.print()

# print(items.fetched_count)
# usage()

import argparse
import getopt
import requests as requests
from bs4 import BeautifulSoup as soup
import json
import sys

# my libs
from Scraper import Scraper
from items import Item


def usage():
    print("""
     Usage: ./main.py [--option]
            ./main.py --fetch -> fetch all json files
            ./main.py --init  -> initialize database with content
            """)
def fetch_json_pages(self):
    # get number of pages to fetch
    url = 'https://storage.googleapis.com/fra-uas-mobappex-ss23-amin/ard-feed-0.json'
    req = requests.get(url)
    content = json.loads(req.text)
    pages = content['totalPageCount']

    url_to_fetch = 'https://storage.googleapis.com/fra-uas-mobappex-ss23-amin/ard-feed-{}.json'
    for p in range(int(pages)):
        req = requests.get(url_to_fetch.format(p))
        with open(f"json/json_file{p}.json", "w") as fd:
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
            self.fetch_json_pages()
        elif args.init:
            self.items.initialize().print()
        else:
            usage()
            sys.exit(1)



    def read_json_pages(self):
        pass


if __name__ == '__main__':
    OptionMenu().show()
# items = Items("feed.json").initialize()
# items.print()

# print(items.fetched_count)
# usage()

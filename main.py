import argparse
import shutil
import subprocess

import requests as requests
import sys

# my libs
from items import *
from scraper import *

import filecmp

main_path = "json"
fetch_path = "json_fetch"


def usage():
    print("""
     Usage: ./main.py [--option]
            ./main.py --fetch -> fetch all json files
            ./main.py --init  -> initialize database with content
            """)


def update_json(dest, src):
    with open(src, "rb") as fa:
        with open(dest, "wb") as fb:
            fb.write(fa.read())


def compare_files(file):
    main_file = f"{main_path}/{file}"
    fetch_file = f"{fetch_path}/{file}"
    if os.path.exists(fetch_file):
        if os.path.exists(main_file):
            if not filecmp.cmp(main_file, fetch_file):
                print("updating database...")
                update(main_file)
                print("updating database done!")
                update_json(dest=main_file, src=fetch_file)
        else:
            update_json(dest=main_file, src=fetch_file)


#           update_json(dest=main_path, src=fetch_path)

def update_files(file_template):
    files_count = next(os.walk(fetch_path))[2]  # directory is your directory path as string
    for fc in range(len(files_count)):
        compare_files(file_template.format(fc))


def fetch_json_pages():
    # get number of pages to fetch
    url = 'https://storage.googleapis.com/fra-uas-mobappex-ss23-amin/ard-feed-0.json'
    req = requests.get(url)
    content = json.loads(req.text)
    pages = content['totalPageCount']

    # if json folder is empty store the next fetch there
    # if not then create new folder json_fetch and store it there
    # later compare if there is a diff between the two folder, if yes replace with new fetched file

    if not os.path.exists(main_path):
        os.makedirs(main_path)
        store_path = main_path
    else:
        if os.path.exists(fetch_path):
            shutil.rmtree(fetch_path)
        os.makedirs(fetch_path)
        store_path = fetch_path

    url_to_fetch = 'https://storage.googleapis.com/fra-uas-mobappex-ss23-amin/ard-feed-{}.json'
    for p in range(int(1)):
        fetch_url = url_to_fetch.format(p)
        print(f"fetching: {fetch_url}")
        req = requests.get(fetch_url)
        with open(f"{store_path}/json_file{p}.json", "w") as fd:
            fd.write(req.text)

    update_files("json_file{}.json")


def show_menu():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fetch', action='store_true')
    parser.add_argument('--init', action='store_true')
    args = parser.parse_args(sys.argv[1:])

    if args.fetch:
        fetch_json_pages()

    elif args.init:
        write_items()
    else:
        usage()
        sys.exit(1)


if __name__ == '__main__':
    show_menu()

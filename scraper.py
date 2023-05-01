import os
import sys
from datetime import datetime

import requests as requests
from bs4 import BeautifulSoup as soup

import json

from ArdDatabase.database import Database
from items import Item

sys.path.append(os.path.join(os.path.dirname(__file__),
                             '~/', 'p'))


def is_video_still_watchable(time_stamp):
    host_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

    # if video is watchable, true else false
    return host_time < time_stamp


def fetch_raw_mp4(count, url):
    req = requests.get(url, stream=True)
    content_len = int(req.headers.get("Content-length"))
    print(f"{count} Downloading Mp4 {(content_len / 1024):.2f} KB...\n")
    page_soup = soup(req.text, 'lxml')
    data = page_soup.select("[id='fetchedContextValue']")[0]
    if data is not None:
        json_result = json.loads(data.text)
        try:
            if json_result is not None:
                result = \
                    json_result[0][1]['data']['widgets'][0]['mediaCollection']['embedded']['streams'][0]['media'][0][
                        'url']
                return result, content_len
        except (IndexError, TypeError):
            return "", 0

    return "", 0


class Scraper:

    def __init__(self):
        self.fetched_count = 0
        self.data_items = []

    # parse one whole json page
    def initialize(self):
        db = Database().instance()
        db.create_video_table()

        files = next(os.walk("json"))[2]  # directory is your directory path as string
        file_read_path = 'json_file{}.json'
        file_write_path = 'test_file{}.txt'

        for f in range(len(files)):
            with open(f"json/{file_read_path.format(f)}", "r") as fr:
                with open(f"test_dir/{file_write_path.format(f)}", "a") as fw:
                    data = json.load(fr)
                    for x in range(int(data['pageItemCount'])):
                        url = data['items'][x]['links']['web']  # url
                        video_url, video_size = fetch_raw_mp4(x, url)
                        if is_video_still_watchable(data['items'][x]['availableTo']):
                            # self.dataItems.append(DataItem(
                            item = Item(
                                url,
                                video_url,
                                video_size,
                                data['items'][x]['images'][0]['url'],  # thumb_nail
                                data['items'][x]['created'],  # creation date
                                data['items'][x]['publisher']['institution']['title'],  # institution
                                data['items'][x]['publisher']['institution']['imageURL'],  # institution_logo
                                data['items'][x]['publisher']['title'],  # publisher
                                data['items'][x]['show']['title'],  # video title
                                data['items'][x]['keywords'],  # keywords
                                data['items'][x]['durationSeconds'],  # duration
                                data['items'][x]['genreCategory']['title'],  # Category
                                data['items'][x]['availableFrom'],  # available_from
                                data['items'][x]['availableTo'],  # available_to
                                data['items'][x]['isChildContent']  # is_child_content
                            )
                            fw.write(str(item))

                        self.fetched_count += 1

        return self

    def print(self):
        for item in self.data_items:
            print(str(item))

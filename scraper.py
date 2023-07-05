import os
import sys
from datetime import datetime

import requests
from bs4 import BeautifulSoup as soup

import json

from ScrapeArdDatabase.database import Database
from items import Item


def is_video_still_watchable(time_stamp):
    host_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    # if video is watchable, true else false
    return host_time < time_stamp


def parse_mp4(count, url):
    req = None
    try:
        req = requests.get(url, stream=True)
    except requests.ConnectionError:
        pass
    if req is not None:
        content_len = int(req.headers.get("Content-length"))
        print(f"{count} Downloading Mp4 {(content_len / 1024):.2f} KB...\n")
        page_soup = soup(req.text, 'lxml')
        data = page_soup.select("[id='fetchedContextValue']")[0]
        if data is not None:
            json_result = json.loads(data.text)
            try:
                if json_result is not None:
                    result = \
                        json_result[0][1]['data']['widgets'][0]['mediaCollection']['embedded']['streams'][0]['media'][
                            0][
                            'url']
                    return result, content_len
            except (IndexError, TypeError):
                return None, None
    return None, None


def write_items():
    db = Database().instance()

    if os.path.exists("json"):
        files = next(os.walk("json"))[2]  # directory is your directory path as string
        file_read_path = 'json_file{}.json'

        for f in range(len(files)):
            with open(f"json/{file_read_path.format(f)}", "r") as fr:
                data = json.load(fr)
                for x in range(int(data['pageItemCount'])):
                    item = parse_item(data, x)
                    if item is not None:
#                        db.get_random_videos(20)
#                        print(item.item_to_list(), "\n")
                        db.insert_video(item)
    else:
        return


def parse_item(data, index):
    url = data['items'][index]['links']['web']  # url
    if is_video_still_watchable(data['items'][index]['availableTo']):
        video_url, video_size = parse_mp4(index, url)
        if video_url is not None:
            item = Item(
                url,
                video_url,  # FIXME
                video_size,
                data['items'][index]['images'][0]['url'],  # thumb_nail
                data['items'][index]['created'],  # creation date
                data['items'][index]['publisher']['institution']['title'],  # institution
                data['items'][index]['publisher']['institution']['imageURL'],  # institution_logo
                data['items'][index]['publisher']['title'],  # publisher
                data['items'][index]['show']['title'],  # video title
                data['items'][index]['keywords'],  # keywords
                data['items'][index]['durationSeconds'],  # duration
                data['items'][index]['genreCategory']['title'],  # Category
                data['items'][index]['availableFrom'],  # available_from
                data['items'][index]['availableTo'],  # available_to
                data['items'][index]['isChildContent']  # is_child_content
            )
            return item
    return None
        


# updates database after fetch
def update(file):
    db = Database().instance()
    items = []
    with open(file, "r") as fd:
        data = json.load(fd)
        items_count = data['pageItemCount']
        for index in range(int(items_count)):
            item = parse_item(data, index)
            if item is not None:
                items.append(item)
    db.update_database(items)

    # def initialize(self):
    #
    #     db = Database().instance()
    #     db.create_video_table()  # if not exist
    #
    #     with open("data.json", "r") as fr:
    #
    #         data = json.load(fr)
    #         for x in range(int(data['pageItemCount'])):
    #
    #             url = data['items'][x]['links']['web']  # url
    #             video_url, video_size = fetch_raw_mp4(x, url)
    #             if is_video_still_watchable(data['items'][x]['availableTo']):
    #                 # self.dataItems.append(DataItem(
    #                 item = Item(
    #                     url,
    #                     video_url,
    #                     video_size,
    #                     data['items'][x]['images'][0]['url'],  # thumb_nail
    #                     data['items'][x]['created'],  # creation date
    #                     data['items'][x]['publisher']['institution']['title'],  # institution
    #                     data['items'][x]['publisher']['institution']['imageURL'],  # institution_logo
    #                     data['items'][x]['publisher']['title'],  # publisher
    #                     data['items'][x]['show']['title'],  # video title
    #                     data['items'][x]['keywords'],  # keywords
    #                     data['items'][x]['durationSeconds'],  # duration
    #                     data['items'][x]['genreCategory']['title'],  # Category
    #                     data['items'][x]['availableFrom'],  # available_from
    #                     data['items'][x]['availableTo'],  # available_to
    #                     data['items'][x]['isChildContent']  # is_child_content
    #                 )
    #                 db.insert_video(item)

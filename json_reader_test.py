import sys

import ijson


def read_chunks():
    with open("data.json", "rb") as fd:
        for record in ijson.items(fd, "items.item"):
            print(record)


if __name__ == '__main__':
    read_chunks()

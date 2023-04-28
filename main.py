

from Items import Items, DataItem

if __name__ == '__main__':
    items = Items("feed.json").initialize()
    items.print()




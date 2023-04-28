import json


class Items():

    def __init__(self, fileName):
        self.fileName = fileName
        self.dataItems = []

    def initialize(self):
        with open(self.fileName, "r") as fd:
            data = json.load(fd)

            for x in range(10):
                self.dataItems.append(DataItem(
                    data['items'][x]['links']['android'],  # url
                    data['items'][x]['show']['title'],  # video title
                    data['items'][x]['created']
                ))  # creation date

        return self

    def print(self):
        for item in self.dataItems:
            print(str(item))


class DataItem():
    def __init__(self,
                 siteUrl,
                 title,
                 created):
        self.siteUrl = siteUrl
        self.videoUrl = None

        self.created = created

        self.publisher = None
        self.publisher_title = None

        self.title = title
        self.keywords = []
        self.duration = None
        self.category = None

        self.availableFrom = None
        self.availableTo = None

        self.isChildContent = False

    def __str__(self):
        return "###################\n" \
               f"{self.siteUrl}\n" \
               f"{self.title}\n" \
               f"{self.created}\n" \
               "###################\n"

import json
from datetime import datetime


class Items:

    def __init__(self, file_name):
        self.file_name = file_name
        self.dataItems = []

    # parse one whole json page
    def initialize(self):
        with open(self.file_name, "r") as fd:
            data = json.load(fd)

            for x in range(200):
                if self.is_video_still_watchable(data['items'][x]['availableTo']):
                    self.dataItems.append(DataItem(
                        data['items'][x]['links']['android'],                     # url
                        data['items'][x]['images'][0]['url'],                     # thumb_nail
                        data['items'][x]['created'],                              # creation date
                        data['items'][x]['publisher']['institution']['title'],    # institution
                        data['items'][x]['publisher']['institution']['imageURL'], # institution_logo
                        data['items'][x]['publisher']['title'],                   # publisher
                        data['items'][x]['show']['title'],                        # video title
                        data['items'][x]['keywords'],                             # keywords
                        data['items'][x]['durationSeconds'],                      # duration
                        data['items'][x]['genreCategory']['title'],               # Category
                        data['items'][x]['availableFrom'],                        # available_from
                        data['items'][x]['availableTo'],                          # available_to
                        data['items'][x]['isChildContent']                        # is_child_content
                    ))
        return self

    def is_video_still_watchable(self, time_stamp):

        host_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

        # if video is watchable, true else false
        return host_time < time_stamp

    def print(self):
        for item in self.dataItems:
            print(str(item))


class DataItem:
    def __init__(self,
                 site_url,
                 thumb_nail,
                 created,
                 institution,
                 institution_logo,
                 publisher,
                 title,
                 keywords,
                 duration,
                 category,
                 available_from,
                 available_to,
                 is_child_content
                 ):
        self.site_url = site_url
        self.thumb_nail = thumb_nail
        self.videoUrl = None # FIXME

        self.created = created

        self.institution = institution
        self.institution_logo = institution_logo
        self.publisher = publisher

        self.title = title
        self.keywords = keywords
        self.duration = duration
        self.category = category

        self.available_from = available_from
        self.available_to = available_to

        self.isChildContent = is_child_content

    def __str__(self):
        return "###################\n" \
               f"site_url: {self.site_url}\n" \
               f"thumb_nail: {self.thumb_nail}\n" \
               f"created: {self.created}\n" \
               f"institution: {self.institution}\n" \
               f"institution_logo: {self.institution_logo}\n" \
               f"publisher: {self.publisher}\n" \
               f"title: {self.title}\n" \
               f"keywords: {self.keywords}\n" \
               f"duration: {self.duration}\n" \
               f"category {self.category}\n" \
               f"available_from: {self.available_from}\n" \
               f"available_to: {self.available_to}\n" \
               f"is_child_content: {self.isChildContent}\n" \
               "###################\n"

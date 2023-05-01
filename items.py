import json

import ciso8601


class Item:
    def __init__(self,
                 site_url,
                 video_url,
                 video_size,
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
                 is_child_friendly
                 ):
        self.site_url = site_url
        self.video_url = video_url
        self.video_size = video_size
        self.thumb_nail = thumb_nail

        # convert to MariaDB TIMESTAMP
        self.created = ciso8601.parse_datetime_as_naive(created)

        self.institution = institution
        self.institution_logo = institution_logo
        self.publisher = publisher

        self.title = title
        self.keywords = keywords
        self.duration = duration
        self.category = category

        # convert to MariaDB TIMESTAMP
        self.available_from = ciso8601.parse_datetime_as_naive(available_from)
        self.available_to = ciso8601.parse_datetime_as_naive(available_to)

        # convert to Bool for mariaDB
        # convert to Bool (integer 1 or 0)
        self.is_child_friendly = int(is_child_friendly) # json.loads(is_child_content.lower())

    def __str__(self):
        return "###################\n" \
               f"site_url: {self.site_url}\n" \
               f"video_url: {self.video_url}\n" \
               f"vide_size: {self.video_size}\n" \
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
               f"is_child_content: {self.is_child_friendly}\n" \
               "###################\n"

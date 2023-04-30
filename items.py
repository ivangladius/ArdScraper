

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
                 is_child_content
                 ):
        self.site_url = site_url
        self.video_url = video_url
        self.video_size = video_size
        self.thumb_nail = thumb_nail

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
               f"is_child_content: {self.isChildContent}\n" \
               "###################\n"

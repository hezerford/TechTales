from bson import ObjectId
from datetime import datetime

class Article:
    def __init__(self, title, content, views=0, likes=0, comments=None, publication_date=None, description=None):
        self.id = ObjectId()
        self.title = title
        self.content = content
        self.views = views
        self.likes = likes
        self.comments = comments or []
        self.publication_date = datetime.now().date()
        self.description = description

class Comment:
    def __init__(self, username, content=None, timestamp = None):
        self.username = username
        self.content = content
        self.timestamp = datetime.now()
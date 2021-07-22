from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.ext.declarative import declarative_base


base = declarative_base()

class Article(base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

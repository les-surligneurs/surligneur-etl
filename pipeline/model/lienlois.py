from sqlalchemy import Column, String
from model import base


class lienlois(base):
    __tablename__ = 'lienlois'

    url = Column(String, primary_key=True)

    def __init__(self, url: str):
        self.url = url

from app import db
import requests
from app.models.zipcode import ZipCode

import logging

##def find_all() -> [ZipCode]:
def find_all() -> str:
    return ZipCode.find_all()

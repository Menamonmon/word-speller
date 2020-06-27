from dictionary import get_definition, get_property, make_dict_request
from dotenv import load_dotenv
from os import getenv

load_dotenv()

DICT_API_KEY = getenv('MWEBSTER_DICT_API_KEY')
REQ_URL = getenv('DICT_REQ_URL')

class Word:

    def __init__(self, name: str, definition: str):
        self.name = name
        self._definition = definition
        self.json = None

    def __str__(self):
        return f'{self.name}: {self.definition}'

    @property
    def definition(self):
        if self._definition:
            return self._definition
            
        self.json = make_dict_request(self.name, DICT_API_KEY, REQ_URL)
        self._definition = get_definition(self.json)
        return self._definition

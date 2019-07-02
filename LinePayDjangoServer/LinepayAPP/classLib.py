import json
from types import SimpleNamespace as Namespace
class decodeJson:
    def __init__(self,json):
        self.json = json
    def parse(self):
        try:
            x = json.loads(self.json, object_hook=lambda d: Namespace(**d))
            return x
        except:
            pass
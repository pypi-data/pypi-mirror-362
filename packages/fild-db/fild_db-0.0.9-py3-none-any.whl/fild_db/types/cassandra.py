import json

from fild_db.types.common import DBBaseJson


class DBJsonDict(DBBaseJson):
    def to_db(self):
        return json.dumps(self.value).encode('utf-8')

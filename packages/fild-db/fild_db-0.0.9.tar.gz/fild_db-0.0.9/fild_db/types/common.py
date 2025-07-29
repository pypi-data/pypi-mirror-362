import json

from pytz import timezone

from fild.sdk import Field, Dictionary, dates


class DbTimestamp(Field):
    def generate_value(self):
        return dates.generate_time()

    def to_db(self):
        return self.value

    def to_format(self, fmt=dates.Pattern.DATE):
        return self.value.strftime(fmt)

    def to_timezone(self, tz):
        return self.value.astimezone(tz=timezone(tz))


class DBBaseJson(Dictionary):
    def with_values(self, values):
        if isinstance(values, str):
            values = json.loads(values)

        if values is not None:
            return super().with_values(values)

        return self

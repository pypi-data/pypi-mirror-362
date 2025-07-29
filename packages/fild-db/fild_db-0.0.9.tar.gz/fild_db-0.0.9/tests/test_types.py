import uuid
from datetime import datetime

from fild_compare import compare
from pytz import timezone

from fild_db.types.common import DbTimestamp
from fild_db.types.mysql import DbBool, DbJsonArray
from fild_db.types.postgres import DbUuid
from tests.data import SampleDict

DATE_VALUE = datetime.now().replace(
    year=2022, month=5, day=13, hour=12, minute=0, second=10, microsecond=0
)
TZ = datetime.now().replace(
    year=2022, month=5, day=13, hour=12, minute=0, second=10, microsecond=0
).astimezone(tz=timezone('CET'))
DATE = DbTimestamp().with_values(DATE_VALUE)
Uuid = DbUuid()


def test_to_db():
    assert DATE.to_db() == DATE_VALUE


def test_to_timezone():
    assert DATE.to_timezone('CET') == TZ


def test_to_text():
    assert DATE.to_format() == '2022-05-13'


def test_mysql_bool_with_values():
    assert DbBool().with_values(1).value is True


def test_mysql_bool_to_db():
    assert DbBool().with_values(0).to_db() == 0


def test_uuid():
    assert isinstance(DbUuid().with_values(uuid.uuid4()).value, str)


def test_json_dict_with_values():
    compare(
        actual=SampleDict().with_values('{"id":234,"name":"val"}').value,
        expected={
            SampleDict.Id.name: 234,
            SampleDict.Name.name: 'val'
        }
    )


def test_json_dict_to_db():
    assert SampleDict().with_values({
        SampleDict.Id.name: 1,
        SampleDict.Name.name: 'test'
    }).with_values(None).to_db() == '{"id":1,"name":"test"}'


def test_json_array_to_db():
    assert DbJsonArray(SampleDict).with_values([{
        SampleDict.Id.name: 1,
        SampleDict.Name.name: 'test'
    }]).with_values(None).to_db() == '[{"id":1,"name":"test"}]'


def test_json_array_with_values():
    compare(
        actual=DbJsonArray(SampleDict).with_values(
            '[{"id":234,"name":"val"}]'
        ).value,
        expected=[{
            SampleDict.Id.name: 234,
            SampleDict.Name.name: 'val'
        }]
    )

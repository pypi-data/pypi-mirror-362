from fild_compare import compare
from fild_compare.rules import has_some_value

from tests.data import Model, Table


def test_model():
    assert Model.get_table_name() == 'table_name'


def test_regular_data():
    compare(
        actual=Model().to_db(),
        expected={
            'id': 1, 'is_global': True, 'metadata_column': 'm', 'name': 'name'
        },
        rules={
            'id': has_some_value,
            'is_global': has_some_value,
            'metadata_column': has_some_value,
            'name': has_some_value
        }
    )


def test_custom_data():
    compare(
        actual=Model(is_custom=True).to_db(),
        expected={'id': 1, 'name': 'name'},
        rules={
            'id': has_some_value,
            'name': has_some_value
        }
    )


def test_full_data():
    compare(
        actual=Model(is_full=True).to_db(),
        expected={
            'id': 1,
            'is_global': True,
            'metadata_column': 'm',
            'name': 'name',
            'comment': 's',
            'created_at': 'test'
        },
        rules={
            'id': has_some_value,
            'is_global': has_some_value,
            'metadata_column': has_some_value,
            'name': has_some_value,
            'comment': has_some_value,
            'created_at': has_some_value
        }
    )


def test_to_table_record():
    assert isinstance(Model().to_table_record(), Table)

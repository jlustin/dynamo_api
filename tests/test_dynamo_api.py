import pytest

from botocore.exceptions import ClientError
from dynamo_api import __version__
from dynamo_api.dynamo_api import create_resource, put, get, update, delete


def test_version():
    assert __version__ == '0.1.4'


config = {
    'host': "localhost",
    'port': "8000",
    'region_name': "us-west-2",
    'aws_access_key_id': "dummy_access_key",
    'aws_secret_access_key': "dummy_secret_key",
    'verify': False
}


def setup_function():
    print('setting up')

    create_resource(config).create_table(
        TableName="Test",
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'N'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )


def test_create_resource():
    conn = create_resource(config)
    assert conn is not None


def test_put():
    conn = create_resource(config)
    test_object = {
        'id': 1
    }
    response = put("Test", test_object, conn)
    assert response['ResponseMetadata']['HTTPStatusCode'] == 200


def test_get():
    conn = create_resource(config)
    test_object = {
        'id': 1,
        'name': 'test'
    }
    put("Test", test_object, conn)
    response = get("Test", {'id': 1}, conn)
    assert response == test_object


def test_get_error():
    conn = create_resource(config)
    test_object = {
        'id': 1,
        'name': 'test'
    }
    put("Test", test_object, conn)
    with pytest.raises(ClientError):
        get("Test", {'name': 'test1'}, conn)


def test_update():
    conn = create_resource(config)
    test_object = {
        'id': 1,
        'test_name': 'test'
    }
    put("Test", test_object, conn)
    update_expr = "set test_name=:n"
    expr_values = {
        ':n': 'passed'
    }
    response = update("Test", {'id': 1}, update_expr, expr_values, conn)
    assert response['test_name'] == 'passed'


def test_delete():
    conn = create_resource(config)
    test_object = {
        'id': 1,
        'test_name': 'test'
    }
    put("Test", test_object, conn)
    response = delete("Test", {'id': 1}, conn)
    assert response['ResponseMetadata']['HTTPStatusCode'] == 200


def test_delete_error():
    conn = create_resource(config)
    with pytest.raises(ClientError):
        delete("Test", {'name': 1}, conn)


def teardown_function():
    print('tearing down')
    table = create_resource(config).Table('Test')
    table.delete()

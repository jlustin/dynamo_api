from dynamo_api import __version__
from dynamo_api.dynamo_api import create_resource, put


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


def test_version():
    assert __version__ == '0.1.2'


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


def teardown_function():
    print('tearing down')
    table = create_resource(config).Table('Test')
    table.delete()

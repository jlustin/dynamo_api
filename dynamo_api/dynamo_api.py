import boto3


def create_resource(config):
    return boto3.resource(
        'dynamodb',
        endpoint_url='http://' + config['host'] + ':' + config['port'],
        region_name=config['region_name'],
        aws_access_key_id=config['aws_access_key_id'],
        aws_secret_access_key=config['aws_secret_access_key'],
        verify=config['verify']
    )


def put(table_name, item, dynamodb):
    table = dynamodb.Table(table_name)
    response = table.put_item(Item=item)
    return response

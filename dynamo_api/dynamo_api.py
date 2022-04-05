import boto3
from botocore.exceptions import ClientError


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


def get(table_name, key, dynamodb):
    table = dynamodb.Table(table_name)
    try:
        response = table.get_item(Key=key)
    except ClientError as e:
        print(e.response)
        raise
    else:
        try:
            return response['Item']
        except KeyError:
            print("No items found")
            raise


def update(table_name, key, update_expr, expr_values, dynamodb):
    table = dynamodb.Table(table_name)
    response = table.update_item(
        Key=key,
        UpdateExpression=update_expr,
        ExpressionAttributeValues=expr_values,
        ReturnValues='UPDATED_NEW'
    )
    return response['Attributes']


def delete(table_name, key, dynamodb):
    table = dynamodb.Table(table_name)
    try:
        response = table.delete_item(Key=key)
    except ClientError as e:
        print(e.response)
        raise
    else:
        return response


def conditional_update(table_name, key, update_expr,
                       condition_expr, expr_values, dynamodb):
    table = dynamodb.Table(table_name)
    try:
        response = table.update_item(
            Key=key,
            UpdateExpression=update_expr,
            ConditionExpression=condition_expr,
            ExpressionAttributeValues=expr_values,
            ReturnValues="UPDATED_NEW"
        )
    except ClientError as e:
        print(e.response)
        raise
    else:
        return response


def conditional_delete(table_name, key, condition_expr, expr_values, dynamodb):
    table = dynamodb.Table(table_name)
    try:
        response = table.delete_item(
            Key=key,
            ConditionExpression=condition_expr,
            ExpressionAttributeValues=expr_values
        )
    except ClientError as e:
        print(e.response)
        raise
    else:
        return response

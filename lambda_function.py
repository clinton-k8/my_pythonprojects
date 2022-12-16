import boto3
import json
from custom_encoder import CustomEncoder
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodbTableName = "product-inventory"
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(dynamodbTableName)

getMethod = "GET"
postMethod = "POST"
patchMethod = "PATCH"
deleteMethod = "DELETE"
healthPath = "/health"
productPath = "/product"
productsPath = "/products"


def lambda_handler(event, context):
    logger.info(event)
    httpMethod = event["httpMethod"]
    path = event['path']
    if httpMethod == getMethod and path == healthPath:
        response = buildResponse(200)
    elif httpMethod == getMethod and path == productPath:
        response = getProduct(event['queryStringParameters']['Productid'])
    elif httpMethod == getMethod and path == productsPath:
        response = getProducts()
    elif httpMethod == postMethod and path == productPath:
        response = saveProduct(json.loads(event['body']))
    elif httpMethod == patchMethod and path == productPath:
        requestBody = json.loads(event['body'])
        response = modifyProduct(requestBody['productid'], requestBody['updateKey'], requestBody['updateValue'])
    elif httpMethod == deleteMethod and path == productPath:
        requestBody = json.loads(event['body'])
        response = deleteProduct(requestBody['productid'])
    else:
        response = buildResponse(404, "Not Found")
    return response


def getProduct(productid):
    try:
        response = table.get_item(
            key={
                'productid': productid
            }
        )
        if 'Item' in response:
            return buildResponse(200, response['Item'])
        else:
            return buildResponse(404, {'Message': 'productid: %s not found' % productid})
    except:
        logger.exception('Do your custom error handling here. I am just gonna log it out here!')


def getProducts():
    try:
        response = table.scan()
        result = response['Item']

        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            result.extend(response['item'])

            body = {
                'products': response
            }
            return buildResponse(200, body)
    except:
        logger.exception('Do your custom error handling here. I am just gonna log it out here!')


def saveProduct(requestBody):
    try:
        table.put_item(Item=requestBody)
        body = {
            'Operation': 'SAVE',
            'Message': 'SUCCESS',
            'Item': 'requestBody'

        }
        return buildResponse(200, body)
    except:
        logger.exception('Do your custom error handling here. I am just gonna log it out here!')


def modifyProduct(productid, updateKey, updateValue):
    try:
        response = table.update_item(
            Key={
                'productid': productid
            },
            UpdateExpression='set %s = :value' % updateKey,
            ExpressionAttributeValues={
                ':value': updateValue
            },
            ReturnValues='UPDATED_NEW'

        )
        body = {
            'Operation': 'UPDATE',
            'Message': 'SUCCESS',
            'UpdatedAttributes': response
        }
        return buildResponse(200, body)
    except:
        logger.exception('Do your custom error handling here. I am just gonna log it out here!')


def deleteProduct(productid):
    try:
        response = table.delete_item(
            key={
                'productid': productid
            },
            ReturnValues='ALL_OLD'
        )
        body = {
            'Operation': 'DELETE',
            'Message': 'SUCCESS',
            'deleteItems': response
        }
        return buildResponse(200, body)
    except:
        logger.exception('Do your custom error handling here. I am just gonna log it out here!')


def buildResponse(statusCode, body=None):
    response = {
        'statusCode': statusCode,
        'headers': {
            'content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
    if body is not None:
        response['body'] = json.dumps(body, cls=CustomEncoder)
    return response


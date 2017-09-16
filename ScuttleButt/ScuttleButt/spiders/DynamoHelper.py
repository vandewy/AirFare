from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


class DynamoHelper():

    def add_to_dynamo(self, airport_id, airfare, last_update):
        client = boto3.client(
            'dynamodb',
            aws_access_key_id='AKIAJMHPSQ6T6EVAJJBA',
            aws_secret_access_key='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',
            region_name='us-west-2'
            # aws_session_token=SESSION_TOKEN,
        )

        dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")

        table = dynamodb.Table('GPT_Table')
        table.put_item(
           Item={
                'airport_id': airport_id,
                'airfare': airfare,
                'last_update': last_update
            }
        )
        print("PutItem succeeded:")
        # print(json.dumps(response, indent=4, cls=DecimalEncoder))

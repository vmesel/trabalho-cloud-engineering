import boto3

def get_dynamo_table():
    dynamodb = boto3.resource("dynamodb")
    return dynamodb.Table("eventos-pizzaria")

def create(event, context):
    body = event["body"]
    table = get_dynamo_table()
    table.put_item(
        Item={
            "pedido": body["detail"]["pedido"],
            "status": body["detail"]["status"],
            "cliente": body["detail"]["cliente"],
            "time": body["time"],
        }
    )

    return {
        "status": 200,
        "body": "OK",
    }

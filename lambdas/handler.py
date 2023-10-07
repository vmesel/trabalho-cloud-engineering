import json
import boto3

from sqsHandler import SqsHandler


def get_dynamo_table():
    dynamodb = boto3.resource("dynamodb")
    return dynamodb.Table("eventos-pizzaria")

def create(body, context):
    """
    Função que cria o registro dentro do Dynamo
    """
    print(body)
    detail = body.get("detail")
    table = get_dynamo_table()
    table.put_item(
        Item={
            "pedido": str(detail["pedido"]),
            "status": detail["status"],
            "cliente": detail["cliente"],
            "time": body["time"],
        }
    )

    return {
        "status": 200,
        "body": "OK",
    }


queue = SqsHandler("https://sqs.us-east-1.amazonaws.com/452836010939/espera-entrega")


def detail(event, context):
    """
    Função que encaminha mensagem ao SQS caso as regras do EventBridge
    sejam válidas para o Payload que ela envia.
    """
    print(f"Received: {event}")
    queue.send(json.dumps(event))


def delivered(event, context):
    """
    Última função chamada no ciclo de chamada da aplicação, ela é a função
    que finaliza a cadeia de chamadas mostrando qual Pizza está pronta
    """
    print(event)
    for message in event["Records"]:
        
        print(f"Received: {message}")
        message_body = json.loads(message["body"])
        message_body = message_body["detail"]
        n_pedido, nome_pedido = message_body["pedido"], message_body["cliente"]
        print(f"Pedido {n_pedido} de {nome_pedido} foi entregue.")
    
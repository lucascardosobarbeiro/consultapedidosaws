import boto3

# Conectar ao DynamoDB
dynamodb = boto3.resource("dynamodb")
tabela_pedidos = dynamodb.Table("Pedidos")  # Substitua pelo nome real da tabela

def lambda_handler(event, context):
    try:
        # Obtendo o pedidoID da entrada do Lex
        slots = event.get("sessionState", {}).get("intent", {}).get("slots", {})
        pedidoID_str = slots.get("pedidoID", {}).get("value", {}).get("interpretedValue")

        # Verificando se pedidoID foi fornecido
        if not pedidoID_str:
            return {
                "messages": [
                    {"content": "Por favor, forneça um número de pedido válido.", "contentType": "PlainText"}
                ],
                "sessionState": {
                    "dialogAction": {"type": "ElicitSlot", "slotToElicit": "pedidoID"},
                    "intent": event["sessionState"]["intent"]
                }
            }

        # Convertendo pedidoID para inteiro (pois no DynamoDB é do tipo Number)
        try:
            pedidoID = int(pedidoID_str)
        except ValueError:
            return {
                "messages": [
                    {"content": "O número do pedido deve ser um valor numérico.", "contentType": "PlainText"}
                ],
                "sessionState": {
                    "dialogAction": {"type": "ElicitSlot", "slotToElicit": "pedidoID"},
                    "intent": event["sessionState"]["intent"]
                }
            }

        # Buscando o pedido no DynamoDB
        response = tabela_pedidos.get_item(Key={"pedidoID": pedidoID})

        # Verificando se o pedido existe
        if "Item" not in response:
            return {
                "messages": [
                    {"content": f"O pedido {pedidoID} não foi encontrado. Verifique e tente novamente.", "contentType": "PlainText"}
                ],
                "sessionState": {
                    "dialogAction": {"type": "ElicitSlot", "slotToElicit": "pedidoID"},
                    "intent": {
                        "name": "ConsultaStatusPedido",
                        "slots": slots,
                        "state": "InProgress",  # Definir estado como "InProgress" para continuar coletando dados
                        "confirmationState": "None"
                    }
                }
            }

        # Pegando o status do pedido no DynamoDB
        status_pedido = response["Item"].get("status", "Status desconhecido")

        # Respondendo com o status do pedido
        return {
            "messages": [
                {"content": f"Pedido {pedidoID} está {status_pedido} e chegará em breve!", "contentType": "PlainText"}
            ],
            "sessionState": {
                "dialogAction": {"type": "Close"},
                "intent": {
                    "name": "ConsultaStatusPedido",
                    "state": "Fulfilled"
                }
            }
        }

    except Exception as e:
        print(f"Erro: {str(e)}")
        return {
            "messages": [
                {"content": "Ocorreu um erro ao processar sua solicitação. Tente novamente mais tarde.", "contentType": "PlainText"}
            ],
            "sessionState": {
                "dialogAction": {"type": "Close"},
                "intent": {
                    "name": "ConsultaStatusPedido",
                    "state": "Failed"
                }
            }
        }
# Documentação do Chatbot de Consulta de Pedidos

## Visão Geral
Este projeto é um chatbot baseado no Amazon Lex para consulta de status de pedidos armazenados no Amazon DynamoDB. Ele recebe um número de pedido informado pelo usuário, busca o status correspondente na base de dados e retorna a informação de forma interativa.

## Tecnologias Utilizadas
- **AWS Lambda** (Execução do backend do chatbot)
- **Amazon Lex** (Processamento de linguagem natural)
- **Amazon DynamoDB** (Armazenamento dos pedidos)
- **Boto3** (SDK para interação com AWS via Python)

## Configuração do Ambiente
1. Criar uma tabela no **Amazon DynamoDB** com:
   - **Nome**: `Pedidos`
   - **Chave Primária**: `pedidoID` (Number)
   - **Atributo**: `status` (String)
2. Criar uma **função Lambda** com:
   - Tempo de execução: **Python 3.8+**
   - Permissões: Acesso ao DynamoDB
   - Dependências: `boto3`
3. Criar um **bot no Amazon Lex**:
   - **Intent**: `ConsultaStatusPedido`
   - **Slot**: `pedidoID` (Number)
   - **Integração**: Lambda

## Fluxo de Execução
1. O chatbot recebe a mensagem do usuário.
2. Se for a primeira interação, exibe uma mensagem de boas-vindas.
3. Solicita o **número do pedido** se ainda não foi informado.
4. Busca o pedido no **DynamoDB**.
5. Se encontrar o pedido, retorna o status.
6. Pergunta ao usuário se deseja realizar outra consulta.
7. Se o usuário disser **não**, a conversa é encerrada.

## Estrutura do Código Lambda
O código utiliza **Boto3** para acessar o DynamoDB e responde ao Lex com mensagens estruturadas.

### Trechos Importantes do Código
```python
# Conectar ao DynamoDB
dynamodb = boto3.resource("dynamodb")
tabela_pedidos = dynamodb.Table("Pedidos")
```

**Gerenciamento de Sessão:**
```python
session_attributes = event.get("sessionState", {}).get("sessionAttributes", {})
if "saudacao_enviada" not in session_attributes:
    session_attributes["saudacao_enviada"] = "true"
```

**Consulta ao DynamoDB:**
```python
response = tabela_pedidos.get_item(Key={"pedidoID": pedidoID})
if "Item" not in response:
    return {"messages": [{"content": "Pedido não encontrado."}]}
```

**Resposta ao Lex:**
```python
return {
    "messages": [{"content": f"Seu pedido {pedidoID} está {status_pedido}."}],
    "sessionState": {"dialogAction": {"type": "Close"}}
}
```

## Possíveis Melhorias
- Adicionar logs para monitoramento no **Amazon CloudWatch**.
- Implementar um banco de dados relacional caso a estrutura cresça.
- Criar um frontend simples para interação com o chatbot.![2025-03-10 15-39-25](https://github.com/user-attachments/assets/88f71646-331d-494a-b5f9-a25fb06ce299)


- 

## Conclusão
Este chatbot melhora a experiência do usuário ao fornecer informações rápidas sobre pedidos. Ele pode ser integrado a outras plataformas como **WhatsApp, Telegram e sites empresariais** para facilitar consultas automatizadas.


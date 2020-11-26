'''
PMR3412 - Redes Industriais (2020)
Diego Jun Sato Kurashima - 10274231

Segunda Entrega - Exercício 2
Server
'''

import asyncio
import websockets

#=== DEFINIÇÕES DO SERVER ===

HOST = "localhost"
PORT = 8080

#=== DEFINIÇÕES DO CLIENT ===

# Dicionario para conversão websocket e nome
client_dic = {}

# Enviar mensagem com alvo selecionável
async def client_message_handler(text, sender):
    '''
    Processa as mensagens de determinado client e faz o envio
    :param text: mesagem a ser enviada, obtida pelo método .recv()
    :param sender: identificar o sender de origem sender.send()
    '''

    # Verificar se tem um destino especificado
    if text[:2] == ">>":

        target_end = text.find(">>", 2)
        if target_end  != -1:
            target = text[2:text.find(">>", 2)]
            text = text[text.find(">>", 2)+2:]

        else:
            await sender.send("Para mensagem privada use a notação '>>[nome do usuário]>>' ")
            target = None

        if target not in client_dic.values():
            await sender.send("Esse usuário não está na  sala :(")
            target = None

    else: target = "all"

    # Mensagem para todos os usuários
    if target ==  'all':

        message = str(client_dic[sender]) + " : " + text
        #await sender.send(message)
        for key in client_dic.keys():
            #if client_dic[key] != sender:
            client = key
            await client.send(message)

    # Mensagem para um target em específico
    elif target in client_dic.values():

        message = str(client_dic[sender]) + " >> " + str(target) + " : " + text
        await sender.send(message)
        for key in client_dic.keys():
             if client_dic[key] == target:
                client = key
                await client.send(message)

# Mensagens do servidor, com escolha de excessões
async def server_message_handler(text, exception_websocket = []):
    '''
    Processa mensagens do servidor
    :param text: mensagem a ser enviada
    :param exception_websocket: lista com os nomes dos clients a não receberem a mensagem
    '''
    message = text

    for key in client_dic.keys():
        if  client_dic[key] not in exception_websocket:
            client = key
            await client.send(message)

async def register(websocket, name):
    '''
    Registra um novo client no dicionário de clientes
    :param websocket: websocket
    :param name: nome do client
    '''
    client_dic[websocket] = name
    message = str(name) +  " se juntou à sala :)"
    await server_message_handler(message, [name])

async def unregister(websocket):
    '''
    Retira da lista um websocket desconectado
    :param websocket: websocket
    '''
    message = str(client_dic[websocket]) + " saiu da sala :("
    client_dic.pop(websocket)
    await server_message_handler(message)


#=== CLIENT HANDLER ===

async def client_handler(websocket, path):
    '''
    Processa as interações entre client e servidor
    :param websocket: websocket do client
    '''

    # Novo Client Conectado !!!
    await websocket.send("Bem-vindo à Sala de Bate Papo com WebSockets !!!")
    await websocket.send("Sua primeira mensagem será o seu nome que será configurado.")

    # Registrar
    name = await websocket.recv()
    while(name in client_dic.values()):
        await websocket.send("Esse nome já está sendo utilizado, por favor digite outra opção ...")
        name = await websocket.recv()

    await register(websocket, name)
    await websocket.send("Prontinho " + str(name) + " !!! Envie mensagens para conversar na sala !")
    await websocket.send("Para enviar mensagens no privado inicie a mensagem com '>>[nome do usuário]>>' ")

    # Loop do Handler
    while True:
        try:
            message = await websocket.recv()
            await client_message_handler(message, websocket)

        except:
            await unregister(websocket)
            break


if __name__ == "__main__":
    start_server = websockets.serve(client_handler, HOST, PORT)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
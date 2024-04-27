import roomdata
from websocket_server import WebsocketServer
import json
import datetime
from loguru import logger
import sys

logger.configure(handlers=[
    {
        "sink": 'gifts.log',
        "format": "{time:YYYY-MM-DD HH:mm:ss.SSS}   {message}",
        "colorize": False
    },
])


def consoleLog(message):
    current_time = datetime.datetime.now()
    print(f"{current_time}: {message}")


def getusername(message):
    name = ''
    if message['user_badgelevel'] > 0:
        name += '[Lv:' + str(message['user_badgelevel']) + ']'
    if message['user_fansLevel'] > 0:
        name += '[' + message['user_fansLightName'] + ':' + str(message['user_fansLevel']) + ']'
    name += message['user_nickName']
    return name


#   礼物
def parseGift(message):
    roomdata.newgift(message['user_id'], message['user_nickName'], message['user_gender'], message['user_isAdmin'],
                     message['user_badgelevel'], message['user_fansLevel'], message['gift_id'], message['gift_name'],
                     message['gift_comboCount'], message['gift_diamondCount'])
    refresh_show(server)
    loguser = message['user_id'] + '   ' + message['user_nickName'] + '    ' + message['user_gender'] + '  ' + str(message['user_badgelevel']) + '    ' + message['user_fansLightName'] + '    ' + str(message['user_fansLevel']) + '   ' + message['user_avatar']
    loggift = message['gift_id'] + '   ' + message['gift_name'] + '   ' + str(message['gift_comboCount']) + '   ' + str(message['gift_repeatCount']) + '   ' + message['gift_image'] + '   ' + str(message['gift_diamondCount']) + '   ' + message['gift_describe']
    logger.info(loguser + '  ' + loggift)
    log = getusername(message) + ':送出 [' + str(message['gift_comboCount']) + '] 个 ' + message['gift_name'] + 'Diamond:[' + str(message['gift_diamondCount']) + ']'
    consoleLog(log)

#   聊天
def parseChat(message):
    log = getusername(message) + ':' + message['msg_content']
    consoleLog(log)


#   来了
def parseMember(message):
    log = getusername(message) + ':' + message['msg_content']
    consoleLog(log)


#   点赞
def parseLike(message):
    log = getusername(message) + ':' + message['msg_content']
    consoleLog(log)


#   分享
def parseRoom(message):
    log = message['user_nickName'] + ':' + message['msg_content']
    consoleLog(log)


#   加入粉丝团
def parseFansclub(message):
    log = getusername(message) + ':' + message['msg_content']
    consoleLog(log)


#   未知命令
def parseUndefined(message):
    log = 'Undefind' + ':' + message['msg_content']
    consoleLog(log)


message_parsers = {
    'WebcastGiftMessage': parseGift,
    'WebcastChatMessage': parseChat,
    'WebcastMemberMessage': parseMember,
    'WebcastLikeMessage': parseLike,
    'WebcastRoomMessage': parseRoom,
    'WebcastFansclubMessage': parseFansclub,
}


def parseMsg(message):
    msg_type = message['method']
    parser = message_parsers.get(msg_type)  # Use parseUndefined for unknown methods
    if parser:
        parser(message)
    else:
        parseUndefined(message)


##############################################################
#	websocket调用
##############################################################
# Called for every client connecting (after handshake)
def new_client(client, server):
    print("New client connected and was given id %d" % client['id'])
    #server.send_message_to_all("Hey all, a new client has joined us")
    server.send_message(client, "Wellcom " + str(client['id']))


#数据显示客户端
client_show = []


# Called for every client disconnecting
def client_left(client, server):
    log = ""
    for item in client_show:
        if item == client:
            client_show.remove(item)
            log = str("ClientShow(%d) disconnected" % client['id'])
            return
    log = str("Client(%d) disconnected" % client['id'])
    print(log)


def refresh_show(svr):
    msg = roomdata.refreshwindow()
    for client in client_show:
        svr.send_message(client, msg)


# Called when a client sends a message
def message_received(client, server, message):
    #if len(message) > 200:
    #    message = message[:200] + '..'
    #print("Client(%d) said: %s" % (client['id'], message))
    if message == "show":
        for item in client_show:
            if item == client:
                return

        client_show.append(client)
    else:
        obj_json = json.loads(message)
        parseMsg(obj_json)


##############################################################
#				服务端启动
##############################################################
PORT = 9527
server = WebsocketServer(port=PORT)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()

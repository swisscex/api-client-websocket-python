import websocket, json, logging

logging.basicConfig(level=logging.DEBUG)

def on_message(ws, message):
    logging.debug(message)

def on_error(ws, error):
    logging.debug(error)

def on_close(ws):
    logging.info('### closed ####')

def on_open(ws):
    # This is optional but if you want to get 'private' messages then you have to send an 'auth' message
    send_message(ws, 'auth', {'apiKey': "<YOUR_API_KEY_HERE>"})

def send_message(ws, key, message):
    encoded_message = encode_for_socketio(key, message)
    logging.debug("Encoded message [%s]", encoded_message)
    ws.send(encoded_message)

def encode_for_socketio(key, message):
    if isinstance(message, basestring):
        encoded_msg = message
    elif isinstance(message, (object, dict)):
        encoded_msg = json.dumps(message)
    else:
        raise ValueError("Can't encode message.")

    return '42["' + key + '",' + encoded_msg + ']'

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp('wss://stream.swisscex.com:444/socket.io/?EIO=2&transport=websocket',
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
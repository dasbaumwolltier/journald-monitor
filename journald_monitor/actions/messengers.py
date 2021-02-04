import logging as log

def send_telegram_message(config_dict: dict, line: str, message: str, config: str) -> str:
    import requests

    applied_config = config_dict['telegram']['configs'][config]
    token = applied_config.token
    chat_id = applied_config.chat_id

    log.debug('Sending message "%s" to room "%s"'%(message, chat_id))

    url = 'https://api.telegram.org/bot' + token + '/sendMessage?chat_id=' + chat_id + '&parseMode=Markdown&text=' + message
    response = requests.get(url)
    return response.json()

# This method requires the matrix_client package
def send_matrix_message(config_dict: dict, line: str, message: str, config: str) -> str:
    from matrix_client.client import MatrixClient, Room, MatrixRequestError

    used_config = config_dict['matrix']['configs'][config]
    client = MatrixClient(used_config.url, token=used_config.token, user_id=used_config.user_id)

    log.debug('Sending message "%s" to room "%s" on server "%s"', message, used_config.room_id, used_config.url)

    try:
        room: Room = client.get_rooms()[used_config.room_id]
        return room.send_html(message)
    except MatrixRequestError:
        return None

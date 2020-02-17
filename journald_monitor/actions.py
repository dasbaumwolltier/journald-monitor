import logging as log

from pyhocon import ConfigTree

def send_telegram_message(config: ConfigTree, line: str, message: str, config_number: int) -> str:
    import requests

    applied_config = config.get('telegram.configs')[config_number]
    token = applied_config.token
    chat_id = applied_config.chat_id

    url = 'https://api.telegram.org/bot' + token + '/sendMessage?chat_id=' + chat_id + '&parseMode=Markdown&text=' + message
    response = requests.get(url)
    return response.json()

def send_matrix_message(config: ConfigTree, line: str, message: str, config_number: int) -> str:
    from matrix_client.client import MatrixClient, Room, MatrixRequestError

    used_config = config.get('matrix.configs')[config_number]
    client = MatrixClient(used_config.url, token=used_config.token, user_id=used_config.user_id)

    log.debug('Sending message "%s" to room "%s" on server "%s"', message, used_config.room_id, used_config.url)

    try:
        room: Room = client.get_rooms()[used_config.room_id]
        return room.send_html(message)
    except MatrixRequestError:
        return None
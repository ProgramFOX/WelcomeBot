#!/usr/bin/env python
import getpass
import logging
import logging.handlers
import os
import random
import sys

import ChatExchange.chatexchange.client
import ChatExchange.chatexchange.events


logger = logging.getLogger(__name__)

def main():
    setup_logging()
    # Run `. setp.sh` to set the below testing environment variables

    host_id = 'stackexchange.com'
    room_id = '14219'  # Charcoal Chatbot Sandbox

    if 'ChatExchangeU' in os.environ:
        email = os.environ['ChatExchangeU']
    else:
        email = raw_input("Email: ")
    if 'ChatExchangeP' in os.environ:
        password = os.environ['ChatExchangeP']
    else:
        password = getpass.getpass("Password: ")

    client = ChatExchange.chatexchange.client.Client(host_id)
    client.login(email, password)

    global room
    room = client.get_room(room_id)
    room.join()
    room.watch(on_message)

    print "(You are now in room #%s on %s.)" % (room_id, host_id)
    while True:
        message = raw_input("<< ")
        room.send_message(message)

    client.logout()


def on_message(message, client):
    if isinstance(message, ChatExchange.chatexchange.events.UserEntered):
        room.send_message("@kitty you have entered the domain of the Zombie Pony Queen!")


def setup_logging():
    logging.basicConfig(level=logging.INFO)
    logger.setLevel(logging.DEBUG)

    # In addition to the basic stderr logging configured globally
    # above, we'll use a log file for chatexchange.client.
    wrapper_logger = logging.getLogger('ChatExchange.chatexchange.client')
    wrapper_handler = logging.handlers.TimedRotatingFileHandler(
        filename='client.log',
        when='midnight', delay=True, utc=True, backupCount=7,
    )
    wrapper_handler.setFormatter(logging.Formatter(
        "%(asctime)s: %(levelname)s: %(threadName)s: %(message)s"
    ))
    wrapper_logger.addHandler(wrapper_handler)


if __name__ == '__main__':
    main(*sys.argv[1:])
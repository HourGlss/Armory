from telnetlib import Telnet, DO, WILL, IAC
import time
from utils.Player import Player

player = Player()


def option_handler_callback(socket, command, option):
    if command == DO:
        if option == b'\x18':
            socket.send(IAC + WILL + b'\x18')
        if option == b'\x5b':
            socket.send(IAC + WILL + b'\x5b')



with Telnet('exilemud.com', 4000) as tn:
    tn.set_debuglevel(0)
    player.tn = tn
    tn.set_option_negotiation_callback(option_handler_callback)
    while True:
        # YO WE NEED TO LOGIN
        if not player.logged_in:
            player.login()
        else:
            item_names = player.get_inv()
            print(len(item_names),item_names)
            player.id_all(item_names)
            player.logout()
            break

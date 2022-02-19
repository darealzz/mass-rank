import colorama
from colorama import Fore, Back, Style

colorama.init()

class Colors:
    def __init__(self, *args):
        self.fore = args[0]
        self.back = args[1]
        self.style = args[2]
        self.symb = f'[{args[3]}]'

    @classmethod
    def information(cls):
        return cls(Fore.CYAN, Back.RESET, Style.BRIGHT, '+')

    @classmethod
    def take(cls):
        return cls(Fore.RED, Back.RESET, Style.BRIGHT, '?')

    @classmethod
    def take_info(cls):
        return cls(Fore.RED, Back.RESET, Style.BRIGHT, '-')


class Keys:
    user_id = 'USER_ID'
    cookie = 'COOKIE'

import sys
import os
from .types import Style

class Textual:
    @staticmethod       
    def del_lines(number):
        for _ in range(number):
            sys.stdout.write("\x1b[1A")
            sys.stdout.write("\x1b[2K")

    @staticmethod
    def log(*args, **kwargs):
        content = args[0]
        _type = kwargs['type']

        print(f'{_type.fore} {_type.back} {_type.style} {_type.symb} {content}{Style.RESET_ALL}')

    @staticmethod
    def take_inptut(*args, **kwargs):
        content = args[0]
        _type = kwargs['type']
        _cls = kwargs['cls']

        if _cls:
            os.system('cls')
        inp = input(f'{_type.fore} {_type.back} {_type.style} {_type.symb} {content}{Style.RESET_ALL} ')
        return inp.strip()

        

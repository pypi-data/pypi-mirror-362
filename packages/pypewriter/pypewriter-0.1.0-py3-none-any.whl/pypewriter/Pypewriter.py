from time import sleep
import random, sys

pypewriter_colors: dict = {
    'end_color': '\033[0m',

    'red': '\x1b[1;31m',
    'green': '\x1b[1;32m',
    'yellow': '\x1b[1;33m',
    'blue': '\x1b[1;34m',
    'magenta': '\x1b[1;35m',
    'cyan': '\x1b[1;36m',

    'red_bg': '\x1b[1;37;41m',
    'green_bg': '\x1b[1;37;42m',
    'yellow_bg': '\x1b[1;37;43m',
    'blue_bg': '\x1b[1;37;44m',
    'magenta_bg': '\x1b[1;37;45m',
    'cyan_bg': '\x1b[1;37;46m'        
}

def get_random_color() -> str: return random.choice(list(pypewriter_colors.values()))

def pypewrite(string: str = 'Hello, World!', speed: float = 7, pause: float = 0.5, color: str = None, new_line: bool = True):

    ''' 
        Prints characters of a given string one at a time \n
        Speed is passed as milliseconds while pause as seconds
    '''
    
    if color is not None: string = f'{color}{string}{pypewriter_colors['end_color']}'
        
    for char in string:
        print(char, end = '', flush = True)
        sleep(speed / 1000)
        sys.stdout.flush() # Clear buffer

    sleep(pause)
    if new_line: print()
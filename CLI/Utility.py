from subprocess import call
from os import name

def ClearTerminal():
    call('cls' if name=='nt' else 'clear', shell=True)

def Clamp(number, min, max):
    number = number if number > min else min
    number = number if number < max else max

    return number
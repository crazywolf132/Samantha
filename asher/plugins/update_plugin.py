from asher.conversation import Statement
from time import sleep
from os import system, execv
import random
import os
import re
from asher.required.required import *

application = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))+'/application.py'

class Plugin:
    def __init__(self):
        """
        Please leave this here or it will cause errors.
        """
        self.the_command = ['update']

    def action(self, command, statement, ash):
        ash_print(ash, 'Please dont think that this file is going to work.')
        system('clear')
        ash_print(ash, '\003[1;32mGoing to run an update now.\033[0m')
        sleep(0.2)
        system('cd ~/')
        system('curl -L "https://raw.githubusercontent.com/crazywolf132/Ai-Setup/master/Update.sh" > update.sh')
        system('bash update.sh')
        exit()

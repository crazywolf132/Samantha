from asher.conversation import Statement
from time import sleep
from os import system
import random
import re
from asher.required.required import *


class Plugin:
    def __init__(self):
        """
        Please leave this here or it will cause errors.
        """

        self.who = ['who are you', '?']
        self.help = ['help']
        self.exit = ['exit please', "quit"]
        self.bye = ['fuck off']

        self.the_command = self.who + self.help + self.exit + self.bye

    def action(self, command, statement, ash):

        if command in self.who:
            ash_print(ash, 'My name is Andrew. I am here to help and serve you.')
            sleep(1)
            ash_print(ash, 'Feel free to ask me anything. If i do not know it, I will learn it.')
        elif command in self.help:
            ash_print(ash, 'what with?')
        elif command in self.exit:
            ash_print(ash, 'Good bye sir.')
            exit()
        elif command in self.bye:
            ash_print(ash, 'Good bye sir.')
            exit()

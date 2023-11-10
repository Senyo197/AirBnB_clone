#!/usr/bin/python3

import cmd
import sys

class HBNBCommand(cmd.Cmd):
    prompt = '(hbnb) '

    def do_quit(self, arg):
        return True

    def help_quit(self):
        print("Quit command to exit the program")

    def do_EOF(self, arg):
        return True

    def help_EOF(self):
        print("EOF command to exit the program")

    def emptyline(self):
        pass

if __name__ == '__main__':
    if sys.stdin.isatty():
        HBNBCommand().cmdloop()
    else:
        commands = sys.stdin.read().splitlines()
        for command in commands:
            print('(hbnb)')
            HBNBCommand().onecmd(command)
        print('(hbnb)')

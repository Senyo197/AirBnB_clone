#!/usr/bin/python3

import cmd
import sys
from models.base_model import BaseModel
from models import storage


class HBNBCommand(cmd.Cmd):
    prompt = '(hbnb) '

    def do_create(self, arg):
        if not arg:
            print("** class name missing **")
            return
        class_name = split()[0]
        try:
            new_instance = eval(class_name)()
            new_instance.save()
            print(new_instance.id)
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, arg):
        args = arg.split()
        if not args:
            print("** class name missing **")
            return

        class_name = args[0]

        instances = storage.all()

        if class_name not in instances.items():
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        instance_id = args[1]
        key = "{}.{}".format(class_name, instance_id)

        if key not in instances:
            print("** no instance found **")
            return
        else:
            obj = instances[key]
            print(obj)
            return

    def do_destroy(self, arg):
        args = arg.split()
        if not args:
            print("** class name missing **")
        try:
            class_name = args[0]
            if class_name not in storage.all():
                print("** class doesn't exist **")
                return
            if len(args) < 2:
                print("** instance id missing **")
                return
            instance_id = args[1]
            key = "{}.{}".format(class_name, instance_id)
            instances = storage.all()
            if key not in instances:
                print("** no instance found **")
                return
            else:
                del instances[key]
                storage.save()
        except Exception:
            print("** class doesn't exist **")

    def do_all(self, arg):
        args = arg.split()
        instances = storage.all()
        if not args:
            result = []
            for key in instances:
                result.append(str(instances[key]))
            print(result)
        else:
            class_name = arg[0]
            if class_name not in storage.all():
                print("** class doesn't exist **")
            result = []
            for key in instances:
                if key.startswith(class_name):
                    result.append(str(instances[key]))
                print(result)

    def do_update(self, arg):
        args = arg.split()
        if not args:
            print("** class name missing **")
        try:
            class_name = args[0]
            if class_name not in storage.all():
                print("** class doesn't exist **")
                return
            if len(args) < 2:
                print("** instance id missing **")
                return
            instance_id = args[1]
            key = "{}.{}".format(class_name, instance_id)
            instances = storage.all()
            if key not in instances:
                print("** no instance found **")
                return
            if len(args) < 3:
                print("** attribute name missing **")
                return
            attribute_name = args[2]
            if len(args) < 4:
                print("** value missing **")
                return
            attribute_value = args[3]
            instance = instances[key]
            setattr(instance, attribute_name, attribute_value)
            instances.save()
        except Exception:
            print("** class doesn't exist **")

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

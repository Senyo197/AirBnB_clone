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
        try:
            new_instance = eval(arg)()
            new_instance.save()
            print(new_instance.id)
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, arg):
        args = arg.split()
        if not args:
            print("** class name missing **")
            return

        try:
            class_name = args[0]

            if class_name not in globals():
                print("** class doesn't exist **")
                return

            if len(args) < 2:
                print("** instance id missing **")
                return

            instance_id = args[1]
            key = f"{class_name}, {instance_id}"
            instances = storage.all()

            if key not in instances:
                print("** no instance found **")
                return

            instance = instances[key]
            print(instance)

        except IndexError:
            print("** instance id missing **")
        except NameError:
            print("** class doesn't exist **")

    def do_destroy(self, arg):

        args = arg.split()

        if not args:
            print("** class name missing **")
            return

        try:
            class_name = args[0]

            if class_name not in globals():
                print("** class doesn't exist **")
                return

            if len(args) < 2:
                print("** instance id missing **")
                return

            instance_id = args[1]
            key = f"{class_name}, {instance_id}"
            instances = storage.all()

            if key not in instances:
                print("** no instance found **")
                return

            instance = instances[key]
            del instance
            storage.save()

        except IndexError:
            print("** instance id missing **")
        except NameError:
            print("** class doesn't exist **")

    def do_all(self, arg):

        args = arg.split()
        instances = storage.all()

        if args:
            class_name = args[0]
            if class_name not in globals():
                print("** class doesn't exist **")
                return

            filtered_instances = {}
            for key, value in instances.items():
                if class_name == key.split('.')[0]:
                    filtered_instances[key] = value
        result = []
        for key in instances.values():
            result.append(str(key))
        print(result)

    def do_update(self, arg):

        args = arg.split()

        if not args:
            print("** class name missing **")
            return

        try:
            class_name = args[0]

            if class_name not in globals():
                print("** class doesn't exist **")
                return

            if len(args) < 2:
                print("** instance id missing **")
                return

            instance_id = args[1]
            key = f"{class_name}.{instance_id}"
            instances = storage.all()

            if key not in instances:
                print("** no instance found **")
                return

            instance = instances[key]

            if len(args) < 3:
                print("** attribute name missing **")
                return

            attribute_name = args[2]

            if len(args) < 4:
                print("** value missing **")
                return

            value_str = args[3]

            if value_str.startswith('"') and value_str.endswith('"'):
                value_str = value_str[1:-1]

            try:
                value = int(value_str)
            except ValueError:
                try:
                    value = float(value_str)
                except ValueError:
                    value = value_str

            if isinstance(value, (str, int, float)):
                setattr(instance, attribute_name, value)
                instance.save()

        except IndexError:
            print("** instance id missing **")
        except NameError:
            print("** class doesn't exist **")

    def do_show_state(self, arg):
        self.do_show(f"state {arg}")

    def do_create_state(self, arg):
        self.do_create(f"state {arg}")

    def do_destroy_state(self, arg):
        self.do_destroy(f"state {arg}")

    def do_all_state(self, arg):
        self.do_all(f"state")

    def do_update_state(self, arg):
        self.do_update(f"state {arg}")

    def do_city_state(self, arg):
        self.do_city(f"state {arg}")

    def do_amenity_state(self, arg):
        self.do_amenity(f"state {arg}")

   def do_place_state(self, arg):
        self.do_place(f"state {arg}")

   def do_review_state(self, arg):
        self.do_review(f"state {arg}")

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

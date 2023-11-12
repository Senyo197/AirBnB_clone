#!/usr/bin/python3

import cmd
import sys
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.state import State
from models.place import Place
from models.amenity import Amenity
from models.city import City
from models.review import Review

""" A class that represents a console """


class HBNBCommand(cmd.Cmd):
    """HBNBCommand - Custom command-line interface for data management

    Attributes:
        prompt (str): The prompt string for the command-line interface
    """
    prompt = '(hbnb) '

    def do_create(self, arg):
        """Create a new instance of a specified class and save it"""
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
        """Prints the string representation of an instance
         based on the class name and id"""
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
        """Deletes an instance based on the class name and id"""

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
        """Prints all string representations of all instances
         based on the class name"""
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
        """Updates an instance based on the class name and id by adding or
         updating attribute"""
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
        """Prints the string representation of a User instance
         based on the id"""
        self.do_show(f"state {arg}")

    def do_create_state(self, arg):
        """Creates a new instance of User, saves it, and prints the id"""
        self.do_create(f"state {arg}")

    def do_destroy_state(self, arg):
        """Deletes a User instance based on the id"""
        self.do_destroy(f"state {arg}")

    def do_all_state(self, arg):
        """Prints all string representations of User instances"""
        self.do_all(f"state")

    def do_update_state(self, arg):
        """Updates a User instance based on the id by adding or
         updating attribute"""
        self.do_update(f"state {arg}")

    def do_city_state(self, arg):
        """Execute the 'do_city' method with the specified state argument"""
        self.do_city(f"state {arg}")

    def do_amenity_state(self, arg):
        """Execute the 'do_amenity' method with the specified state argument"""
        self.do_amenity(f"state {arg}")

    def do_place_state(self, arg):
        """Execute the 'do_place' method with the specified state argument"""
        self.do_place(f"state {arg}")

    def do_review_state(self, arg):
        """Execute the 'do_review' method with the specified state argument"""
        self.do_review(f"state {arg}")

    def do_quit(self, arg):
        """Exit the console using 'quit' """
        return True

    def help_quit(self):
        """Print information about the 'quit' command"""
        print("Quit command to exit the program")

    def do_EOF(self, arg):
        """Exit the console using 'EOF' """
        return True

    def help_EOF(self):
        """Print information about the 'EOF' command"""
        print("EOF command to exit the program")

    def emptyline(self):
        """Do nothing on an empty line"""
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

1ff1d1d1-15b1-4d49-957c-9cd2132f99821ff1d1d1-15b1-4d49-957c-9cd2132f99821ff1d1d1-15b1-4d49-957c-9cd2132f99821ff1d1d1-15b1-4d49-957c-9cd2132f99821ff1d1d1-15b1-4d49-957c-9cd2132f99821ff1d1d1-15b1-4d49-957c-9cd2132f99821ff1d1d1-15b1-4d49-957c-9cd2132f99821ff1d1d1-15b1-4d49-957c-9cd2132f99821ff1d1d1-15b1-4d49-957c-9cd2132f99821ff1d1d1-15b1-4d49-957c-9cd2132f9982#!/usr/bin/python3
"""
Module: console.py
This module defines the HBNBCommand class,
a command-line interpreter for managing AirBnB objects.
"""
import cmd
import json
import re
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models import storage


class HBNBCommand(cmd.Cmd):
    """
    HBNBCommand class: Command-line interpreter for managing AirBnB objects.

    Attributes:
        prompt (str): The command prompt displayed to the user.
        all_classes (dict):
            A dictionary mapping class names to their corresponding classes.

    Methods:
        do_create(self, line):
            Creates a new model instance of the class passed as an argument.
        do_destroy(self, line):
            Deletes a model instance based on class name and ID.
        do_EOF(self, line): Handles End-of-File (EOF) input.
        do_quit(self, line):
            Quits the command interpreter and exits the program.
        emptyline(self): Handles an empty line input.
        do_show(self, line):
            Displays the string representation of an instance
            based on class name and ID.
        do_all(self, line):
            Prints all string representations of instances based on class name.

    Usage:
        Execute this script to launch the AirBnB command-line interpreter.
    """
    prompt = "(hbnb) "
    all_classes = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review
    }

    def do_create(self, line):
        """Creates a new model instance of the class passed as arg

            Usage:
                `create <ModelName>`
        """
        args = line.split()
        if not args or not args[0]:
            print("** class name missing **")
            return
        try:
            new_instance = HBNBCommand.all_classes[args[0]]()
            new_instance.save()
            print(new_instance.id)
        except KeyError:
            print("** class doesn't exist **")

    def do_destroy(self, line):
        """do_destroy deletes a model instance based on class name and ID.

        Usage: `destroy <ModelName> <ModelId>`
        Args:
            line (str): model name and model ID.
        """
        args = line.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        model_name = args[0]
        if model_name not in HBNBCommand.all_classes:
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        model_id = args[1]
        key = model_name + "." + model_id
        all_objs = storage.all()
        if key not in all_objs:
            print("** no instance found **")
            return
        del all_objs[key]
        storage.save()

    def do_update(self, line):
        """update updates a model instance

            Usage: update <ModelName> <ModelId> <attribute_name>
            <attribute_value>
        Args:
            line (str): model name, model id, attribute name, attribute value
        """
        args = line.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        model_name = args[0]
        if model_name not in HBNBCommand.all_classes:
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        model_id = args[1]
        key = model_name + "." + model_id
        all_objs = storage.all()
        if key not in all_objs:
            print("** no instance found **")
            return
        if len(args) == 2:
            print("** attribute name missing **")
            return
        if len(args) == 3:
            print("** value missing **")
            return
        model_name = args[0]
        model_id = args[1]
        attr_name = args[2]
        attr_value = args[3]
        if attr_name in ['id', 'created_at', 'updated_at']:
            return
        key = model_name + "." + model_id
        model_obj = all_objs[key]
        try:
            setattr(model_obj, attr_name, json.loads(
                '"' + attr_value + '"'))
            model_obj.save()
        except json.JSONDecodeError:
            return

    def do_EOF(self, line):
        """Handle End-of-File (EOF) input"""
        return True

    def do_quit(self, line):
        """Quit command to exit the program"""
        return True

    def emptyline(self):
        """An empty line + `ENTER` shouldn’t execute anything"""

    def do_show(self, line):
        """Show instance based on class name and id

            Usage: show <ClassName> <InstanceID>
        """
        args = line.split()
        if not args or not args[0]:
            print('** class name missing **')
            return

        class_name = args[0]
        if class_name not in HBNBCommand.all_classes:
                print("** class doesn't exist **")
                return

        if len(args) < 2:
            print("** instance id missing **")
            return

        id = args[1]
        key = f"{class_name}.{id}"

        if key not in storage.all():
            print('** no instance found **')
        else:
            print(storage.all()[key])

    def do_all(self, line):
        """Prints all string rep. of instances based on class name.

        Usage:
            `all <ClassName>` or `all`
        """
        args = line.split()

        if args:
            class_name = args[0]
            if class_name not in HBNBCommand.all_classes:
                print("** class doesn't exist **")
                return

            instances = [
                str(obj) for obj in storage.all().values()
                if isinstance(obj, HBNBCommand.all_classes[class_name])]
            print(instances)
        else:
            instances = [str(obj) for obj in storage.all().values()]
            print(instances)

    def do_update(self, line):
        """update updates a model instance

            Usage: update <ModelName> <ModelId> <attribute_name>
            <attribute_value>
        Args:
            line (str): model name, model id, attribute name, attribute value
        """
        errors = {
            0: "** class name missing **",
            1: "** instance id missing **",
            2: "** attribute name missing **",
            3: "** value missing **"
        }
        args = line.split()
        if len(args) == 0:
            print(errors[0])
            return
        model_name = args[0]
        if model_name not in HBNBCommand.all_classes:
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print(errors[1])
            return
        model_id = args[1]
        key = model_name + "." + model_id
        all_objs = storage.all()
        if key not in all_objs:
            print("** no instance found **")
            return
        if len(args) < 4:
            print(errors[len(args)])
            return
        model_name = args[0]
        model_id = args[1]
        attr_name = args[2]
        attr_value = args[3]
        if attr_name in ['id', 'created_at', 'updated_at']:
            pass
        else:
            key = model_name + "." + model_id
            model_obj = all_objs[key]
            try:
                setattr(model_obj, attr_name, json.loads(
                    '"' + attr_value + '"'))
                model_obj.save()
            except json.JSONDecodeError:
                return
        return


if __name__ == '__main__':
    HBNBCommand().cmdloop()

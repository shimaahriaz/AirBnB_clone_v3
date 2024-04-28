#!/usr/bin/python3
""" Console """

import cmd
import shlex
from models.base_model import BaseModel
from models import storage

classes = {"BaseModel": BaseModel}


class HBNBCommand(cmd.Cmd):
    """ HBNB console """
    prompt = '(hbnb) '

    def do_EOF(self, arg):
        """Exits console"""
        return True

    def emptyline(self):
        """ overwriting the emptyline method """
        pass

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def _key_value_parser(self, args):
        """creates a dictionary from a list of strings"""
        new_dict = {}
        for arg in args:
            if "=" in arg:
                key, value = arg.split('=', 1)
                if value[0] == value[-1] == '"':
                    value = shlex.split(value)[0].replace('_', ' ')
                else:
                    try:
                        value = int(value)
                    except ValueError:
                        try:
                            value = float(value)
                        except ValueError:
                            continue
                new_dict[key] = value
        return new_dict

    def do_create(self, arg):
        """Creates a new instance of a class"""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return False
        class_name = args[0]
        if class_name in classes:
            new_dict = self._key_value_parser(args[1:])
            instance = classes[class_name](**new_dict)
        else:
            print("** class doesn't exist **")
            return False
        print(instance.id)
        instance.save()

    def do_show(self, arg):
        """Prints an instance as a string based on the class and id"""
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
            return False
        if args[0] in classes:
            if len(args) > 1:
                key = "{}.{}".format(args[0], args[1])
                print(storage.all().get(key, "** no instance found **"))
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_destroy(self, arg):
        """Deletes an instance based on the class and id"""
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
        elif args[0] in classes:
            if len(args) > 1:
                key = "{}.{}".format(args[0], args[1])
                objs = storage.all()
                if key in objs:
                    objs.pop(key)
                    storage.save()
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_all(self, arg):
        """Prints string representations of instances"""
        args = shlex.split(arg)
        obj_list = []
        objs = storage.all()
        if not args:
            obj_dict = objs
        elif args[0] in classes:
            obj_dict = {k: v for k, v in objs.items() if isinstance(v, classes[args[0]])}
        else:
            print("** class doesn't exist **")
            return False
        for obj in obj_dict.values():
            obj_list.append(str(obj))
        print("[{}]".format(", ".join(obj_list)))

    def do_update(self, arg):
        """Update an instance based on the class name, id, attribute & value"""
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
            return
        if args[0] not in classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = "{}.{}".format(args[0], args[1])
        objs = storage.all()
        if key not in objs:
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
        obj = objs[key]
        attr = args[2]
        value = args[3]
        if attr in ["number_rooms", "number_bathrooms", "max_guest", "price_by_night"]:
            value = int(value)
        elif attr in ["latitude", "longitude"]:
            value = float(value)
        setattr(obj, attr, value)
        storage.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()


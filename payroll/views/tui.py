import getpass

from tabulate import tabulate


class TUI:

    @classmethod
    def user_name(cls):
        return input("Username:\n")

    @classmethod
    def password(cls):
        return getpass.getpass("Password:\n")

    @classmethod
    def print_message(cls, message):
        print(message)

    @classmethod
    def get_input(cls, message):
        return input(message)

    @classmethod
    def pretty_print(cls, data, columns):
        print(tabulate(data, headers=columns))

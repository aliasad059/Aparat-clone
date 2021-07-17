import getpass

from mysql.connector import connect, Error
from prettytable import PrettyTable
import logging

import functions


def config_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(f'{__name__}.log')

    console_handler.setLevel(logging.INFO)
    file_handler.setLevel(logging.WARNING)

    console_format = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s] : %(message)s',
                                       datefmt='%d-%b-%y %H:%M:%S')
    file_fomrat = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s] : %(message)s',
                                    datefmt='%d-%b-%y %H:%M:%S')

    console_handler.setFormatter(console_format)
    file_handler.setFormatter(file_fomrat)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


config = {
    'user': 'root',
    'password': 'secret',
    'host': '127.0.0.1',
    'database': 'Aparat',
    'buffered': True
}

if __name__ == '__main__':
    logger = config_logger()
    logger.info("Aparat started.")

    try:
        logger.info('Try to connect to the database.')
        with connect(**config) as connection:
            try:
                with connection.cursor() as cursor:
                    logger.info('Connected successfully.')
                    print("Welcome to Aparat.")

                    in_main_panel = True
                    while in_main_panel:
                        command = input('>')
                        com, *args = command.split()
                        if com.lower() in ('q', 'quit'):
                            logger.info('Shutting down program.')
                            print('Have a Good day, dude. :)\nRemember us.\nAparat')
                            in_main_panel = False
                            continue
                        elif com.lower() in ('h', 'help'):
                            print('help command')
                        elif com.lower() == 'signin':
                            if len(args) != 3:
                                args = list()
                                args.append('-u')
                                args.append(input('Username> '))
                                args.append(input('Password> '))
                            if functions.signIn(logger, cursor, *args):
                                username = args[2]
                                password = args[3]
                                isAdmin = False
                                if args[1] in ('-a', '--admin'):
                                    isAdmin = True

                                print('Greeting ' + username + '!')
                                print('Here is your Apart panel.')
                                if isAdmin:
                                    print('admin')
                                else:
                                    in_user_panel = True
                                    while in_user_panel:
                                        command = input('>>')
                                        com, *args = command.split()

                        elif com.lower() == 'signup':
                            if len(args) != 7:
                                args = list()
                                args.append(input('Username> '))
                                args.append(input('Password> '))
                                args.append(input('FirstName> '))
                                args.append(input('LastName> '))
                                args.append(input('Email> '))
                                args.append(input('PhoneNumber> '))
                                args.append(input('MelliCode> '))

                            print(args)
                            if functions.signUp(logger, cursor, *args):
                                print('tss')
                        else:
                            print('Invalid Command.\nNeed help? Enter \'help\' command')

            except Error as e:
                print(e)
    except Error as e:
        logger.error('Error occurred while connecting to database.')
        print(e)

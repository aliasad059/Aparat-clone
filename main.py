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

    console_handler.setLevel(logging.ERROR)
    file_handler.setLevel(logging.INFO)

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
    'buffered': True,
    'autocommit': True
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
                        try:
                            com, *args = command.split()
                        except ValueError:
                            continue
                        if com.lower() in ('q', 'quit'):
                            logger.info('Shutting down program.')
                            print('Have a Good day, dude. :)\nRemember us.\nAparat')
                            in_main_panel = False
                            continue
                        elif com.lower() in ('h', 'help'):
                            print('help command in main panel')
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

                            functions.signUp(logger, cursor, *args)
                        elif com.lower() == 'signin':
                            if len(args) != 3:
                                args = list()
                                args.append('-u')
                                args.append(input('Username> '))
                                args.append(input('Password> '))
                            if functions.signIn(logger, cursor, *args):
                                username = args[1]
                                password = args[2]
                                isAdmin = False
                                if args[1] in ('-a', '--admin'):
                                    isAdmin = True
                                functions.printHeader('Greeting ' + username + '!\nHere is your Apart panel.')

                                if isAdmin:
                                    in_admin_panel = True
                                    while in_admin_panel:
                                        command = input('>>')
                                        try:
                                            com, *args = command.split()
                                        except ValueError:
                                            continue
                                        if com.lower() in ('q', 'quit'):
                                            in_admin_panel = False
                                            continue
                                        elif com.lower() in ('h', 'help'):
                                            print('help command in user panel')

                                        elif com.lower() == 'add':  #
                                            print('')
                                        elif com.lower() == 'remove':  #
                                            print('')
                                        elif com.lower() == 'edit':  #
                                            print('')
                                        elif com.lower() == 'update':  #
                                            print('')
                                        elif com.lower() == 'category':  #
                                            print('')
                                        elif com.lower() == 'tag':  #
                                            print('')
                                else:
                                    while True:
                                        command = input('>>')
                                        try:
                                            com, *args = command.split()
                                        except ValueError:
                                            continue
                                        if com.lower() in ('q', 'quit'):
                                            break
                                        elif com.lower() in ('h', 'help'):
                                            print('help command in user panel')

                                        elif com.lower() == 'info':
                                            functions.getInfo(logger, cursor, username)

                                        elif com.lower() == 'edit':  # edit personal info
                                            functions.printHeader('In edit information panel ')
                                            while True:
                                                command = input('>>>')
                                                try:
                                                    com, *args = command.split()
                                                except ValueError:
                                                    continue
                                                if com.lower() in ('q', 'quit'):
                                                    break
                                                elif com.lower() in ('h', 'help'):
                                                    print('edit info help')
                                                elif com.lower() == 'info':
                                                    functions.getInfo(logger, cursor, username)
                                                elif com.lower() == 'password':
                                                    new_info = input('New Password>>>')
                                                    functions.changePassword(logger, cursor, username, new_info)
                                                elif com.lower() in ('last', 'last_name', 'lastname'):
                                                    new_info = input('New LastName >>>')
                                                    functions.changeLastName(logger, cursor, username, new_info)
                                                elif com.lower() in ('first', 'first_name', 'firstname'):
                                                    new_info = input('New FirstName>>>')
                                                    functions.changeFirstName(logger, cursor, username, new_info)
                                                elif com.lower() in ('email'):
                                                    new_info = input('New Email>>>')
                                                    functions.changeEmail(logger, cursor, username, new_info)
                                                elif com.lower() in ('phone_number', 'phonenumber', 'phone'):
                                                    new_info = input('New PhoneNumber>>>')
                                                    functions.changePhoneNumber(logger, cursor, username, new_info)
                                                elif com.lower() in ('melli', 'melli_code', 'mellicode'):
                                                    new_info = input('New MelliCode>>>')
                                                    functions.changeMelliCode(logger, cursor, username, new_info)

                                        elif com.lower() == 'wallet':  # increase balance
                                            functions.printHeader('In your wallet:')
                                            args = list()
                                            args.append(username)
                                            functions.walletBalance(logger, cursor, *args)
                                            while True:
                                                command = input('>>>')
                                                try:
                                                    com, *args = command.split()
                                                except ValueError:
                                                    continue
                                                if com.lower() in ('q', 'quit'):
                                                    break
                                                elif com.lower() in ('h', 'help'):
                                                    print('wallet help')
                                                elif com.lower() == 'increase':
                                                    functions.increaseBalance(logger, cursor, username, args[0])

                                        elif com.lower() == 'invite':  # invite friend
                                            inviter_username = input('Inviter Username>>')
                                            functions.inviteFriend(logger, cursor, inviter_username, username)

                                        elif com.lower() == 'upgrade':  # upgrade (show vip membership status, upgrade from point or credit)
                                            print('')

                                        elif com.lower() in ('watch', 'show','film'):  # show films(search,sort,buy vp films)
                                            print('')
                                        elif com.lower() == 'playlist':  # create playlist, show myplaylist(add, remove film), show all playlist
                                            print('')

                        else:
                            print('Invalid Command.\nNeed help? Enter \'help\' command')

            except Error as e:
                print(e)
    except Error as e:
        logger.error('Error occurred while connecting to database.')
        print(e)

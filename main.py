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
                                                elif com.lower() in ('status', 'balance'):
                                                    functions.walletBalance(logger, cursor, username)
                                                elif com.lower() == 'increase':
                                                    if len(args) == 0:
                                                        args = list()
                                                        args.append(input('How Much? >>>'))
                                                    functions.increaseBalance(logger, cursor, username, args[0])

                                        elif com.lower() == 'invite':  # invite friend
                                            inviter_username = input('Inviter Username>>')
                                            functions.inviteFriend(logger, cursor, inviter_username, username)

                                        elif com.lower() in ('membership', 'upgrade'):
                                            while True:
                                                command = input('>>>')
                                                try:
                                                    com, *args = command.split()
                                                except ValueError:
                                                    continue
                                                if com.lower() in ('q', 'quit'):
                                                    break
                                                elif com.lower() in ('h', 'help'):
                                                    print('membership help')
                                                elif com.lower() == 'status':
                                                    functions.showVipMembershipStatus(logger, cursor, username)
                                                elif com.lower() in ('point', 'points'):
                                                    functions.upgradeVipMembership(logger, cursor, username, 100,
                                                                                   'points')
                                                elif com.lower() in ('credit', 'balance', 'money'):
                                                    functions.upgradeVipMembership(logger, cursor, username, 100,
                                                                                   'credit')

                                        elif com.lower() in ('playlist', 'list'):
                                            functions.printHeader('In playlist:')
                                            while True:
                                                command = input('>>>')
                                                try:
                                                    com, *args = command.split()
                                                except ValueError:
                                                    continue

                                                if com.lower() in ('q', 'quit'):
                                                    break

                                                elif com.lower() in ('h', 'help'):
                                                    print('playlist help')

                                                elif com.lower() in ('my', 'myplaylist', 'myplaylists', 'mylists', 'mylist'):
                                                    functions.showPlaylists(logger, cursor, username)
                                                    while True:
                                                        command = input('>>>>')
                                                        try:
                                                            com, *args = command.split()
                                                        except ValueError:
                                                            continue
                                                        if com.lower() in ('q', 'quit'):
                                                            break
                                                        elif com.lower() == 'show':
                                                            functions.showPlaylists(logger, cursor, username)
                                                        elif com.lower() == 'create':
                                                            playlist_name = input('Playlist Name>>>> ')
                                                            playlist_description = ''
                                                            while True:
                                                                inp = input(
                                                                    'Playlist Description(Type exit to stop)>>>> ')
                                                                if inp == 'exit':
                                                                    break
                                                                playlist_description = playlist_description + " " + inp
                                                            functions.createPlaylist(logger, cursor, username,
                                                                                     playlist_name,
                                                                                     playlist_description)
                                                        elif com.lower() in ('add', 'addto', 'add_to'):
                                                            if len(args) == 0:
                                                                args = list()
                                                                args.append(input('Playlist To Add Number>>>> '))
                                                            if len(args) == 1:
                                                                move_next = functions.showFilms(logger, cursor,0, 10)
                                                                while True:
                                                                    current_position = 0
                                                                    print('Enter the film\'s number.')
                                                                    print('Or enter next, prev to see other films')
                                                                    com = input('>>>>> ')
                                                                    if com.lower() == 'next':
                                                                        if move_next:
                                                                            current_position += 10
                                                                            move_next = functions.showFilms(logger,cursor,current_position,10)
                                                                        else:
                                                                            continue
                                                                    elif com.lower() == 'prev':
                                                                        if current_position - 10 >= 0:
                                                                            current_position -= 10
                                                                            functions.showFilms(logger,cursor,current_position,10)
                                                                            move_next = True
                                                                        else:
                                                                            continue
                                                                    else:
                                                                        args.append(com)
                                                                        break

                                                            functions.addFilmTo(logger, cursor, username, args[0],args[1])

                                                elif com.lower() in ('all', 'show'):
                                                    functions.showPlaylists(logger, cursor, None)

                                                elif com.lower() in ('watch', 'select', 'choose'):
                                                    if len(args) == 0:
                                                        args = list()
                                                        args.append(input('Playlist Number>>> '))
                                                    if len(args) == 1:
                                                        move_next = functions.showPlaylistFilms(logger, cursor, args[0],0, 10)
                                                        while True:
                                                            current_position = 0
                                                            print('Enter the film\'s number.')
                                                            print('Or enter next, prev to see other films')
                                                            com = input('>>>> ')
                                                            if com.lower() == 'next':
                                                                if move_next:
                                                                    current_position += 10
                                                                    move_next = functions.showPlaylistFilms(logger, cursor,args[0],current_position, 10)
                                                                else:
                                                                    continue
                                                            elif com.lower() == 'prev':
                                                                if current_position - 10 >= 0:
                                                                    current_position -= 10
                                                                    functions.showPlaylistFilms(logger, cursor,args[0], current_position,10)
                                                                    move_next = True
                                                                else:
                                                                    continue
                                                            else:
                                                                args.append(com)
                                                                break

                                                    is_vip = functions.filmDetail(logger, cursor, args[1])
                                                    if is_vip:
                                                        print('This film is VIP.')
                                                        print('If you haven\'t bought this before, Enter \'buy\' to purchase the film. else enter \'no\'.')
                                                        com = input('>>> ')
                                                        if com.lower() in ('yes', 'buy'):
                                                            functions.buyVipFilm(logger, cursor, username, args[0])

                                                    watch_res = functions.watchFilm(logger,cursor,username,args[1])
                                                    if watch_res:
                                                        while True:
                                                            print('Film '+args[1]+' is now playing.')
                                                            print('Enter \'finish\' to finish watching it.')
                                                            print('Enter \'later\' to watch it later.')
                                                            com = input('>>>> ')
                                                            if com == 'finish':
                                                                functions.finishWatching(logger,cursor,username,args[1])
                                                                break
                                                            elif com == 'later':
                                                                break

                                        elif com.lower() in ('watch', 'show', 'film'):
                                            move_next = functions.showFilms(logger, cursor, 0, 10)
                                            while True:
                                                current_position = 0
                                                print('Enter the film\'s number.')
                                                print('Or enter next, prev to see other films')
                                                com = input('>>> ')
                                                if com.lower() == 'next':
                                                    if move_next:
                                                        current_position += 10
                                                        move_next = functions.showFilms(logger, cursor,current_position, 10)
                                                    else:
                                                        continue
                                                elif com.lower() == 'prev':
                                                    if current_position - 10 >= 0:
                                                        current_position -= 10
                                                        functions.showFilms(logger, cursor, current_position, 10)
                                                        move_next = True
                                                    else:
                                                        continue
                                                else:
                                                    args.append(com)
                                                    break
                                            is_vip = functions.filmDetail(logger,cursor,args[0])
                                            if not is_vip:
                                                print('This film is VIP.')
                                                print('If you haven\'t bought this before, Enter \'buy\' to purchase the film. else enter \'no\'.')
                                                com = input('>>> ')
                                                if com.lower() in ('yes','buy'):
                                                    functions.buyVipFilm(logger,cursor,username,args[0])

                                            watch_res = functions.watchFilm(logger, cursor, username, args[0])
                                            if watch_res:
                                                while True:
                                                    print('Film '+args[0]+' is now playing.')
                                                    print('Enter \'finish\' to finish watching it.')
                                                    print('Enter \'later\' to watch it later.')
                                                    com = input('>>>> ')
                                                    if com == 'finish':
                                                        functions.finishWatching(logger,cursor,username,args[0])
                                                        break
                                                    elif com == 'later':
                                                        break
                        else:
                            print('Invalid Command.\nNeed help? Enter \'help\' command')

            except Error as e:
                print(e)
    except Error as e:
        logger.error('Error occurred while connecting to database.')
        print(e)

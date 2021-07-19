# functions that are needed to interact with database
from mysql.connector import Error
from prettytable import *


def printHeader(str):
    header = PrettyTable(['...Aparat...'])
    header.add_row([str])
    print(header)


def signIn(logger, cursor, option, username: str, password: str):
    if option in ('-a', '--admin'):
        try:

            cursor.callproc('Admin_SignIn', args=(username, password))
            logger.info(f'[SignIn] Admin <{username}> successfully signed in.')
            return True

        except Error as e:
            logger.error(f'[SignIn] {e.msg}')
            return False
    elif option in ('-u', '--user'):
        try:

            cursor.callproc('User_SignIn', args=(username, password))
            logger.info(f'[SignIn] User <{username}> successfully signed in.')
            return True

        except Error as e:
            logger.error(f'[SignIn] {e.msg}')
            return False


def signUp(logger, cursor, username: str, password: str,
           first_name: str, last_name: str, email: str,
           phone_number: str, melli_code: str):
    try:
        res = cursor.callproc('SignUp',
                              args=(username, password, first_name, last_name, email, phone_number, melli_code, ''))
        res_str = res[7]
        if res_str == '':
            logger.info(f'[SignUp] User <{username}> successfully signed up.')
            return True
        logger.error(f'[SignUp] ' + res_str)
        return False


    except Error as e:
        logger.error(f'[SignUp] {e.msg}')
        return False


def walletBalance(logger, cursor, username: str):
    try:
        cursor.callproc('GetBalance', args=(username,))
        for res in cursor.stored_results():
            data = res.fetchone()
            print('Your wallet has ' + str(data[0]) + ' credits')

    except Error as e:
        logger.error(f'[GetBalance] {e.msg}')
        return


def increaseBalance(logger, cursor, username, amount):
    try:
        cursor.callproc('IncreaseBalance', args=(username, amount))

    except Error as e:
        logger.error(f'[IncreaseBalance] {e.msg}')
        return


def getInfo(logger, cursor, username):
    try:
        operation = "SELECT * FROM user WHERE user.username = %(username_param)s"
        cursor.execute(operation, {'username_param': username})
        info = from_db_cursor(cursor)
        print(info)
    except Error as e:
        logger.error(f'[GetInfo] {e.msg}')
        return


def changePassword(logger, cursor, username: str, new_password: str):
    try:
        cursor.callproc('ChangePassword', args=(username, new_password,))
    except Error as e:
        logger.error(f'[ChangePassword] {e.msg}')


def changeFirstName(logger, cursor, username: str, new_firstname: str):
    try:
        cursor.callproc('ChangeFirstName', args=(username, new_firstname,))
    except Error as e:
        logger.error(f'[ChangeFirstName] {e.msg}')


def changeLastName(logger, cursor, username: str, new_lastname: str):
    try:
        cursor.callproc('ChangeLastName', args=(username, new_lastname,))
    except Error as e:
        logger.error(f'[ChangeLastName] {e.msg}')


def changePhoneNumber(logger, cursor, username: str, new_phone_number: str):
    try:
        cursor.callproc('ChangePhoneNumber', args=(username, new_phone_number,))
    except Error as e:
        logger.error(f'[ChangePhoneNumber] {e.msg}')


def changeEmail(logger, cursor, username: str, new_email: str):
    try:
        cursor.callproc('ChangeEmail', args=(username, new_email,))
    except Error as e:
        logger.error(f'[ChangeEmail] {e.msg}')


def changeMelliCode(logger, cursor, username: str, new_melli_code: str):
    try:
        cursor.callproc('ChangeMelliCode', args=(username, new_melli_code,))
    except Error as e:
        logger.error(f'[ChangeMelliCode] {e.msg}')


def inviteFriend(logger, cursor, inviter: str, invited: str):
    try:
        cursor.callproc('Invite', args=(inviter, invited,))
    except Error as e:
        logger.error(f'[Invite] {e.msg}')


def showVipMembershipStatus(logger, cursor, username_param):
    try:
        cursor.callproc('Update_Membership_Status', args=(username_param,))
        operation = "SELECT user.balance,user.point, user.vip_membership_expiration_date FROM user WHERE user.username = %(username_param)s"
        cursor.execute(operation, {'username_param': username_param})
        status = from_db_cursor(cursor)
        print(status)

    except Error as e:
        logger.error(f'[Status] {e.msg}')


def upgradeVipMembership(logger, cursor, username_param: str, price: int, p_type: str):
    try:
        cursor.callproc('BuyVipMembership', args=(username_param, price, p_type,))
    except Error as e:
        logger.error(f'[Invite] {e.msg}')


def showPlaylists(logger, cursor, creator_username: str):
    try:
        cursor.callproc('ShowPlaylists', args=(creator_username,))
        table = PrettyTable(['id', 'name', 'description', 'creator'])
        for res in cursor.stored_results():
            data = res.fetchall()
            for i in data:
                table.add_row(i)
        print(table)
    except Error as e:
        logger.error(f'[ShowPlaylists] {e.msg}')


def showPlaylistFilms(logger, cursor, playlist_id_param, start_bound, number_of_films):
    try:
        cursor.callproc('ShowPlaylistFilms', args=(playlist_id_param, start_bound, number_of_films))
        table = PrettyTable(['id', 'name', 'release_date',
                             'price', 'details', 'viewers',
                             'average rate', 'all rates'])
        rowcount = 0
        for res in cursor.stored_results():
            data = res.fetchall()
            rowcount = len(data)
            for i in data:
                table.add_row(i)
        print(table)
        if rowcount < number_of_films:
            return False
        return True
    except Error as e:
        logger.error(f'[ShowPlaylistFilm] {e.msg}')


def createPlaylist(logger, cursor, creator_username_param: str, playlist_name_param: str, playlist_description: str):
    try:
        cursor.callproc('CreatePlaylist', args=(creator_username_param, playlist_name_param, playlist_description,))
    except Error as e:
        logger.error(f'[CreatePlaylist] {e.msg}')


def addFilmTo(logger, cursor, creator_username_param, playlist_id_param, film_id_parm):
    try:
        cursor.callproc('AddNewFilmToPlaylist',
                        args=(creator_username_param, playlist_id_param, film_id_parm,))
    except Error as e:
        logger.error(f'[AddNewFilmToPlaylist] {e.msg}')


def showFilms(logger, cursor, start_bound, number_of_films):
    try:
        cursor.callproc('ShowFilms', args=(start_bound, number_of_films,))
        table = PrettyTable(['id', 'name', 'release_date',
                             'price', 'details', 'viewers',
                             'average rate', 'all rates'])
        rowcount = 0
        for res in cursor.stored_results():
            data = res.fetchall()
            rowcount = len(data)
            for i in data:
                table.add_row(i)
        print(table)
        if rowcount < number_of_films:
            return False
        return True
    except Error as e:
        logger.error(f'[ShowFilms] {e.msg}')


def searchForFilm(logger, cursor, search_term, sort_term, start_bound, number_of_films):
    try:
        cursor.callproc('SearchForFilm', args=(search_term, sort_term, start_bound, number_of_films,))
        table = PrettyTable(['id', 'name', 'release_date',
                             'price', 'details', 'viewers',
                             'average rate', 'all rates'])
        rowcount = 0
        for res in cursor.stored_results():
            data = res.fetchall()
            rowcount = len(data)
            for i in data:
                table.add_row(i)
        print(table)
        if rowcount < number_of_films:
            return False
        return True
    except Error as e:
        logger.error(f'[SearchForFilm] {e.msg}')


def watchFilm(logger, cursor, viewer_username, film_id):
    try:
        cursor.callproc('WatchFilm', args=(viewer_username, film_id,))
        return True
    except Error as e:
        logger.error(f'[WatchFilm] {e.msg}')
        return False


def finishWatching(logger, cursor, viewer_username, film_id):
    try:
        cursor.callproc('FinishWatching', args=(viewer_username, film_id,))
    except Error as e:
        logger.error(f'[FinishWatching] {e.msg}')


def buyVipFilm(logger, cursor, buyer_username, film_id):
    print('Enter purchase type(points or credit)')
    purchase_type = input('>>>')
    try:
        cursor.callproc('BuyVipFilm', args=(buyer_username, film_id, purchase_type))
    except Error as e:
        logger.error(f'[BuyVipFilm] {e.msg}')


def checkIfBought(logger, cursor, buyer_username, film_id):
    try:
        cursor.callproc('CheckIfBought', args=(buyer_username, film_id,))
        return True
    except Error as e:
        logger.error(f'[CheckIfBought] {e.msg}')
        return False


def addNewComment(logger, cursor, username, film_id, comment, rate):
    try:
        cursor.callproc('AddNewComments', args=(username, film_id, comment, rate,))
    except Error as e:
        logger.error(f'[AddNewComments] {e.msg}')


def showComments(logger, cursor, film_id, start_bound, number_of_comments):
    try:
        cursor.callproc('ShowComments', args=(film_id, start_bound, number_of_comments,))
        table = PrettyTable(['Viewer', 'Comment', 'Rate'])
        rowcount = 0
        for res in cursor.stored_results():
            data = res.fetchall()
            rowcount = len(data)
            for i in data:
                table.add_row(i)
        print(table)
        if rowcount < number_of_comments:
            return False
        return True
    except Error as e:
        logger.error(f'[ShowComments] {e.msg}')


def isVip(logger, cursor, film_id):
    try:
        cursor.callproc('IsVIP', args=(film_id,))
        return True
    except Error:
        return False


def filmInfo(logger, cursor, film_id_param):
    try:
        print('Film Info:')
        operation = "SELECT * FROM film WHERE film.id = %(film_id_param)s"
        cursor.execute(operation, {'film_id_param': film_id_param})
        table = from_db_cursor(cursor)
        print(table)

    except Error as e:
        logger.error(f'[FilmInfo] {e.msg}')


def filmTags(logger, cursor, film_id_param):
    try:
        print('Tags:')
        operation = "SELECT film_tag.tag_name FROM film_tag WHERE film_tag.film_id = %(film_id_param)s"
        cursor.execute(operation, {'film_id_param': film_id_param})
        table = from_db_cursor(cursor)
        print(table)

    except Error as e:
        logger.error(f'[FilmTags] {e.msg}')


def filmCreators(logger, cursor, film_id_param):
    try:
        print('Creators:')
        operation = "SELECT * FROM film_creator WHERE film_creator.film_id = %(film_id_param)s"
        cursor.execute(operation, {'film_id_param': film_id_param})
        table = from_db_cursor(cursor)
        print(table)

    except Error as e:
        logger.error(f'[FilmCreators] {e.msg}')


def filmPanel(logger, cursor, username, film_id):
    is_vip = isVip(logger, cursor, film_id)
    print('The following film is selected:')
    filmInfo(logger, cursor, film_id)
    print('You are now in Film panel')
    while True:
        com = input('>>>>')
        if com.lower() in ('q', 'quit'):
            break
        elif com.lower() in ('h', 'help'):
            print('film panel help')
        elif com.lower() in ('info', 'about'):
            filmInfo(logger, cursor, film_id)
        elif com.lower() in ('creator', 'creators'):
            filmCreators(logger, cursor, film_id)
        elif com.lower() in ('tag', 'tags'):
            filmTags(logger, cursor, film_id)
        elif com.lower() in ('play', 'watch', 'start'):
            if is_vip:
                has_bought = checkIfBought(logger, cursor, username, film_id)
                if not has_bought:
                    print('Enter \'buy\' to purchase the film. else enter \'no\'.')
                    com = input('>>>>')
                    if com.lower() in ('yes', 'buy'):
                        buyVipFilm(logger, cursor, username, film_id)

            watch_res = watchFilm(logger, cursor, username, film_id)
            if watch_res:
                while True:
                    print('Film ' + film_id + ' is now playing.')
                    print('Enter \'finish\' to finish watching it.')
                    print('Enter \'later\' to watch it later.')
                    com = input('>>>>')
                    if com == 'finish':
                        finishWatching(logger, cursor, username, film_id)
                        break
                    elif com == 'later':
                        break

        elif com.lower() in ('comment', 'comments'):
            current_position = 0
            move_next = showComments(logger, cursor, film_id, current_position, 5)
            while True:
                command = input('>>>>>')
                if command.lower() in ('q', 'quit'):
                    break
                elif command.lower() in ('add', 'new', 'comment'):
                    comment_text = ''
                    while True:
                        inp = input('Your comment(Type exit to stop)>>>>>')
                        if inp == 'exit':
                            break
                        comment_text = comment_text + " " + inp
                    rate = input('Your rate(0 to 5)>>>>>')
                    addNewComment(logger, cursor, username, film_id, comment_text, rate)
                elif command.lower() == 'next':
                    if move_next:
                        current_position += 5
                        move_next = showComments(logger, cursor, film_id, current_position, 5)
                    else:
                        continue
                elif command.lower() == 'prev':
                    if current_position - 5 >= 0:
                        current_position -= 5
                        showComments(logger, cursor, film_id, current_position, 5)
                        move_next = True
                    else:
                        continue


def chooseFilm(logger, cursor):
    print('In choose Film Panel:')
    while True:
        command = input('>>>')
        if command.lower() in ('q', 'quit'):
            return -1
        elif command.lower() in ('h', 'help'):
            print('choose film panel help')
        elif command.lower() in ('filter', 'search'):
            search_term = input('Search Term>>>')
            sort_term = input('Sort Term(rate,viewers,film name)>>>')
            move_next = searchForFilm(logger, cursor, search_term, sort_term, 0, 10)
            current_position = 0
            while True:
                print('Enter the film\'s number.')
                print('Or enter next, prev to see other films.')
                com = input('>>>>')
                if com.lower() in ('q', 'quit'):
                    break
                elif com.lower() == 'next':
                    if move_next:
                        current_position += 10
                        move_next = searchForFilm(logger, cursor, search_term, sort_term, current_position, 10)
                    else:
                        continue
                elif com.lower() == 'prev':
                    if current_position - 10 >= 0:
                        current_position -= 10
                        searchForFilm(logger, cursor, search_term, sort_term, current_position, 10)
                        move_next = True
                    else:
                        continue
                else:
                    return com
        elif command.lower() == 'all':
            move_next = showFilms(logger, cursor, 0, 10)
            current_position = 0
            while True:
                print('Enter the film\'s number.')
                print('Or enter next, prev to see other films')
                com = input('>>>>')
                if com.lower() in ('q', 'quit'):
                    break
                elif com.lower() == 'next':
                    if move_next:
                        current_position += 10
                        move_next = showFilms(logger, cursor,
                                              current_position, 10)
                    else:
                        continue
                elif com.lower() == 'prev':
                    if current_position - 10 >= 0:
                        current_position -= 10
                        showFilms(logger, cursor, current_position, 10)
                        move_next = True
                    else:
                        continue
                else:
                    return com

# TODO: admin panel

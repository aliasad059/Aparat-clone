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


def upgrade_vip_membership(logger, cursor, username_param: str, price: int, p_type: str):
    try:
        cursor.callproc('BuyVipMembership', args=(username_param, price, p_type,))
    except Error as e:
        logger.error(f'[Invite] {e.msg}')


def showPlaylists(logger, cursor, creator_username: str):
    try:
        cursor.callproc('ShowPlaylists', args=(creator_username,))
    except Error as e:
        logger.error(f'[ShowPlaylists] {e.msg}')


def showPlaylistFilms(logger, cursor, playlist_id_param, start_bound, number_of_films):
    try:
        cursor.callproc('ShowPlaylistFilm', args=(playlist_id_param, start_bound, number_of_films))
        if cursor.rowcount < number_of_films:
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
        if cursor.rowcount < number_of_films:
            return False
        return True
    except Error as e:
        logger.error(f'[ShowFilms] {e.msg}')


def watchFilm(logger, cursor, viewer_username, film_id):
    try:
        cursor.callproc('WatchFilm', args=(viewer_username, film_id,))
    except Error as e:
        logger.error(f'[WatchFilm] {e.msg}')


def finishWatching(logger, cursor, viewer_username, film_id):
    try:
        cursor.callproc('FinishWatching', args=(viewer_username, film_id,))
    except Error as e:
        logger.error(f'[FinishWatching] {e.msg}')

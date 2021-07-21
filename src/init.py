from mysql.connector import Error

from tables import *
from triggers import *
from procedures import *


def createTables(logger, cursor):
    try:
        cursor.execute(create_table_admin)
        cursor.execute(create_table_user)
        cursor.execute(create_table_film)
        cursor.execute(create_table_category)
        cursor.execute(create_table_film_category)
        cursor.execute(create_table_film_tag)
        cursor.execute(create_table_film_creator)
        cursor.execute(create_table_watch_film)
        cursor.execute(create_table_invite_user)
        cursor.execute(create_table_film_comment)
        cursor.execute(create_table_playlist)
        cursor.execute(create_table_playlist_film)
        cursor.execute(create_table_buy_vip_film)
        cursor.execute(create_table_friend)
        cursor.execute(create_table_log)
        cursor.execute(create_table_mysqlErrors)
        return True
    except Error as e:
        logger.error(f'[CreateTables] {e.msg}')
        return False


def createProcedures(logger, cursor):
    try:
        cursor.execute(create_signUp_procedure)
        cursor.execute(create_user_signIn_procedure)
        cursor.execute(create_admin_signIn_procedure)
        cursor.execute(create_change_password_procedure)
        cursor.execute(create_change_firstname_procedure)
        cursor.execute(create_change_lastname_procedure)
        cursor.execute(create_change_email_procedure)
        cursor.execute(create_change_phonenumber_procedure)
        cursor.execute(create_change_mellicode_procedure)
        cursor.execute(create_getbalance_procedure)
        cursor.execute(create_increase_balance_procedure)
        cursor.execute(create_update_vip_membership_status_procedure)
        cursor.execute(create_buy_vip_membership_procedure)
        cursor.execute(create_buy_vip_film_procedure)
        cursor.execute(create_add_new_film_procedure)
        cursor.execute(create_edit_film_info_procedure)
        cursor.execute(create_category_procedures)
        cursor.execute(create_search_for_film_procedure)
        cursor.execute(create_is_vip_procedure)
        cursor.execute(create_check_if_bought_procedure)
        cursor.execute(create_watch_film_procedure)
        cursor.execute(create_finish_watching_procedure)
        cursor.execute(create_show_comment_procedure)
        cursor.execute(create_add_comment_procedure)
        cursor.execute(create_invite_procedure)
        cursor.execute(create_playlist_procedure)
        cursor.execute(create_show_playlist_procedure)
        cursor.execute(create_add_filmto_playlist_procedure)
        cursor.execute(create_show_films_procedure)
        cursor.execute(create_show_playlist_films_procedure)
        cursor.execute(creator_follow_procedure)
        cursor.execute(creator_unfollow_procedure)
        cursor.execute(creator_myfriend_playlist_procedure)

        return True
    except Error as e:
        logger.error(f'[CreateProcedures] {e.msg}')
        return False


def createTriggers(logger, cursor):
    try:
        cursor.execute(create_update_film_viewers_trigger)
        cursor.execute(create_update_film_rate_avg_trigger)
        cursor.execute(create_logger_triggers)
        return True
    except Error as e:
        logger.error(f'[CreateTriggers] {e.msg}')
        return False

#
# def initTables(logger, cursor):
#     fd = open('init_tables.sql', 'r')
#     sql_file = fd.read()
#     fd.close()
#     sql_commands = sql_file.split(';')
#     for command in sql_commands:
#         try:
#             cursor.execute(command)
#         except Error as e:
#             logger.error(f'[InitTable] {e.msg}')

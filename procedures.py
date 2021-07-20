# procedures and functions of database

create_signUp_procedure = """
CREATE PROCEDURE SignUp(
    username_param varchar(50),
    password_param varchar(50),
    last_name_param varchar(50),
    first_name_param varchar(50),
    email_param varchar(50),
    phone_number_param char(10),
    melli_code_param char(10),
    OUT result varchar(200)
)
BEGIN
    START TRANSACTION;
    set result = '';
    if username_param in (
        select user.username
        from user
    ) then
        set result = '\nThis username is already taken.';
    END if;

    if email_param is not null AND email_param in (
        select user.email
        from user
    ) then
        set result = concat(result, '\nA user with this email has signed up before.');
    END if;

    if phone_number_param is not null then
        if phone_number_param in (
            select user.phone_number
            from user
        ) then
            set result = concat(result, '\nA user with this phone number has signed up before.');
        END if;
        if char_length(phone_number_param) <> 10 then
            set result = concat(result, '\nPhone number must be exactly 10 characters.');
        END if;
    END if;

    if melli_code_param is not null then
        if melli_code_param in (
            select user.melli_code
            from user
        ) then
            set result = concat(result, '\nA user with this Melli code has signed up before.');
        END if;
        if char_length(melli_code_param) <> 10 then
            set result = concat(result, '\nMelli code must be exactly 10 characters');
        END if;
    END if;

    if not (password_param REGEXP '[0-9]' and
        password_param REGEXP BINARY '[A-Z]' and
        password_param REGEXP BINARY '[a-z]' and
        char_length(password_param) > 7) then
        set result = concat(result, '\nEntered password must contain at least a number, an uppercase letter, and 8 characters.');
    END if;


    if strcmp(result, '') <> 0 then
        rollback ;
    else
        insert into user (username, password, last_name, first_name, email, phone_number, melli_code)
        values (username_param, password_param, last_name_param, first_name_param, email_param, phone_number_param,
                melli_code_param);
        COMMIT;
    END if;

END;
"""

create_user_signIn_procedure = """
CREATE PROCEDURE User_SignIn(username_param varchar(50), password_param varchar(50))
BEGIN
    if username_param not in (
        select user.username
        from user
    ) then
        SIGNAL SQLSTATE '02000'
            SET MESSAGE_TEXT = 'User not found.', MYSQL_ERRNO = 9000;
    END if;

    if not exists(
            select *
            from user
            where (username, password) = (username_param, password_param)
        ) then
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Entered password does not match.', MYSQL_ERRNO = 9001;

    END if;
END;

"""

create_admin_signIn_procedure = """
CREATE PROCEDURE Admin_SignIn(username_param varchar(50), password_param varchar(50))
BEGIN
    if username_param not in (
        select admin.username
        from admin
    ) then
        SIGNAL SQLSTATE '02000'
            SET MESSAGE_TEXT = 'Admin not found.', MYSQL_ERRNO = 9011;
    END if;

    if not exists(
            select *
            from admin
            where (username, password) = (username_param, password_param)
        ) then
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Entered password does not match.', MYSQL_ERRNO = 9001;

    END if;
END;
"""

create_edit_personal_info_procedures = """
CREATE PROCEDURE ChangePassword(
    username_param varchar(50),
    new_password varchar(50)
)
BEGIN

    if not (new_password REGEXP '[0-9]' and
            new_password REGEXP BINARY '[A-Z]' and
            new_password REGEXP BINARY '[a-z]' and
            char_length(new_password) > 7) then
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT =
                    'Entered password must contain at least a number, an uppercase letter, and 8 characters.', MYSQL_ERRNO = 9002;
    END if;
    update user
    set user.password = new_password
    where user.username = username_param;
END;

CREATE PROCEDURE ChangeFirstName(
    username_param varchar(50),
    new_firstname varchar(50)
)
BEGIN
    update user
    set user.first_name = new_firstname
    where user.username = username_param;
END;

CREATE PROCEDURE ChangeLastName(
    username_param varchar(50),
    new_lastname varchar(50)
)
BEGIN
    update user
    set user.last_name = new_lastname
    where user.username = username_param;
END;

CREATE PROCEDURE ChangeEmail(
    username_param varchar(50),
    new_email varchar(50)
)
BEGIN
    if new_email in (
        select user.email
        from user
    ) then
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT =
                    'A user with this email has signed up before.', MYSQL_ERRNO = 9007;
    end if;

    update user
    set user.email = new_email
    where user.username = username_param;
END;

CREATE PROCEDURE ChangePhoneNumber(
    username_param varchar(50),
    new_phoneNumber varchar(50)
)
BEGIN
    if new_phoneNumber in (
        select user.phone_number
        from user
    ) then
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT =
                    'A user with this phone number has signed up before.', MYSQL_ERRNO = 9006;
    END if;
    if char_length(new_phoneNumber) <> 10 then
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT =
                    'Phone number must be exactly 10 characters.', MYSQL_ERRNO = 9005;
    END if;
    update user
    set user.phone_number = new_phoneNumber
    where user.username = username_param;
END;

CREATE PROCEDURE ChangeMelliCode(
    username_param varchar(50),
    new_melli_code varchar(50)
)
BEGIN
    if new_melli_code in (
        select user.melli_code
        from user
    ) then
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT =
                    'A user with this Melli code has signed up before.', MYSQL_ERRNO = 9004;
    END if;
    if char_length(new_melli_code) <> 10 then
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT =
                    'Melli code must be exactly 10 characters.', MYSQL_ERRNO = 9003;
    END if;
    update user
    set user.melli_code = new_melli_code
    where user.username = username_param;
END;
"""

create_increase_balance_procedure = """

CREATE PROCEDURE GetBalance(username_param varchar(50))
BEGIN
    select user.balance from user where user.username = username_param;
END;

CREATE PROCEDURE IncreaseBalance(
    username_param varchar(50),
    amount int
)
BEGIN
    if amount <= 0 then
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT =
                    'Amount value must be positive', MYSQL_ERRNO = 9009;
    end if;
    update user
    set user.balance = user.balance + amount
    where user.username = username_param;
END;
"""

create_vip_membership_procedures = """
CREATE PROCEDURE Update_Membership_Status(
    username_param varchar(50)
)
BEGIN
    update user
    set user.vip_membership_expiration_date = IF(user.vip_membership_expiration_date < CURRENT_DATE(), NULL,
                                                 user.vip_membership_expiration_date)
    where user.username = username_param;
END;

CREATE PROCEDURE BuyVipMembership(
    username_param varchar(50),
    vip_membership_price int,
    purchase_type varchar(20)
)
BEGIN
    if purchase_type = 'credit' then
        if vip_membership_price > (
            select user.balance
            from user
            where user.username = username_param
        )
        then
            SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT =
                        'Not enough money', MYSQL_ERRNO = 9010;
        end if;

        update user
        set user.balance                        = user.balance - vip_membership_price
          , user.vip_membership_expiration_date =
            IF((user.vip_membership_expiration_date is not NULL AND
                user.vip_membership_expiration_date > CURRENT_DATE())
                , ADDDATE(user.vip_membership_expiration_date, INTERVAL 1 MONTH)
                , ADDDATE(CURRENT_DATE(), INTERVAL 1 MONTH)
                )
        where user.username = username_param;
    end if;

    if purchase_type = 'points' then
        if 3 > (
            select user.point
            from user
            where user.username = username_param
        )
        then
            SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT =
                        'Not enough points', MYSQL_ERRNO = 9015;
        end if;

        update user
        set user.point                          = user.point - 3
          , user.vip_membership_expiration_date =
            IF((user.vip_membership_expiration_date is not NULL AND
                user.vip_membership_expiration_date > CURRENT_DATE())
                , ADDDATE(user.vip_membership_expiration_date, INTERVAL 1 MONTH)
                , ADDDATE(CURRENT_DATE(), INTERVAL 1 MONTH)
                )
        where user.username = username_param;
    end if;

END;

CREATE PROCEDURE BuyVipFilm(
    username_param varchar(50),
    film_id_param int,
    purchase_type varchar(20)
)
BEGIN
    CALL Update_Membership_Status(username_param);
    if username_param not in
       (
           select user.username
           from user
           where user.vip_membership_expiration_date is not NULL
       )
    then
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'You do not have any active vip-membership.', MYSQL_ERRNO = 9012;
    end if;

    if purchase_type = 'credit' then
        if (select film.price from film where film.id = film_id_param) >
           (select user.balance from user where user.username = username_param)
        then
            SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'Not enough money.', MYSQL_ERRNO = 9010;
        end if;

        insert into buy_vip_film(buyer_username, film_id) value (username_param, film_id_param);

        update user
        set user.balance = user.balance - (select film.price from film where film.id = film_id_param)
        where user.username = username_param;

    end if;

    if purchase_type = 'points' then
        if (select user.point from user where user.username = username_param) = 0
        then
            SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'Not enough points.', MYSQL_ERRNO = 9015;
        end if;

        insert into buy_vip_film(buyer_username, film_id) value (username_param, film_id_param);

        update user
        set user.point = user.point - 1
        where user.username = username_param;

    end if;

END;
"""

create_add_new_film_procedure = """
CREATE PROCEDURE AddNewFilm(
    name_param varchar(50),
    release_date_param date,
    price_param int,
    details_param varchar(200)
)
BEGIN
    insert into film (id, name, release_date, price, details)
    values (0,
            name_param,
            IF(release_date_param is not NULL, release_date_param, CURRENT_DATE()),
            IF(price_param is not NULL, price_param, 0),
            details_param);
END;
"""

create_edit_film_info_procedure = """
CREATE PROCEDURE EditFilmInfo(
    id_param int,
    name_param varchar(50),
    release_date_param date,
    price_param int,
    details_param varchar(200)
)
BEGIN
    update film
    set film.name         = IF(name_param is not NULL, name_param, film.name),
        film.release_date = IF(release_date_param is not NULL, release_date_param, film.release_date),
        film.price        = IF(price_param is not NULL, price_param, film.price),
        film.details      = IF(details_param is not NULL, details_param, film.details)
    where film.id = id_param;
END;
"""

create_category_procedures = """
CREATE PROCEDURE ShowCategoryFilms(
    category_id int,
    start_bound int,
    number_of_films int
)
BEGIN
    select *
    from film
    where film.id in
          (
              select film_category.film_id
              from film_category
              where film_category.category_id = category_id
          )
    limit start_bound,number_of_films;
END;


"""

create_search_for_film_procedure = """
CREATE PROCEDURE SearchForFilm(
    search_term varchar(200),
    sort_term varchar(50),
    start_bound int,
    numberOfFilms int
)
BEGIN
    SELECT *
    from (
             ( -- search over film details
                 SELECT id,
                        name,
                        release_date,
                        price,
                        details,
                        viewers,
                        rate_avg,
                        rates
                 FROM film
                 WHERE film.details regexp (search_term)
                    OR film.name regexp (search_term)
             )
             UNION
             ( -- search over creators
                 SELECT film.id,
                        film.name,
                        film.release_date,
                        film.price,
                        film.details,
                        film.viewers,
                        film.rate_avg,
                        film.rates
                 FROM film
                          INNER JOIN film_creator ON film.id = film_creator.film_id
                 WHERE film_creator.creator_firstname regexp (search_term)
                    OR film_creator.creator_lastname regexp (search_term)
             )
             order by case
                          when strcmp(sort_term, 'viewers') = 0 then viewers
                          when strcmp(sort_term, 'rate_avg') = 0 then rate_avg
                          when strcmp(sort_term, 'release_date') = 0 then release_date
                          else name
                          end DESC
         ) as res
    limit start_bound,numberOfFilms;
END;
"""

create_watch_film_procedures = """
CREATE PROCEDURE IsVIP(
film_id_param int
)
BEGIN
    if (SELECT film.price FROM film WHERE film.id = film_id_param) = 0 then
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'This film is free.', MYSQL_ERRNO = 9019;
    end if;
END;

CREATE PROCEDURE CheckIfBought(
    buyer_username_param varchar(50),
    film_id_param int)
BEGIN
    if (buyer_username_param, film_id_param) not in
       (
           select *
           from buy_vip_film
       ) then
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'You have not bought this film before.', MYSQL_ERRNO = 9013;
    end if;
END;

CREATE PROCEDURE WatchFilm(
    username_param varchar(50),
    film_id_param int
)
BEGIN
    CALL Update_Membership_Status(username_param);
    if film_id_param in (select film.id from film where film.price > 0)
    then
        if username_param in
           (select user.username from user where user.vip_membership_expiration_date is NULL)
        then
            SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'You do not have any active vip-membership.', MYSQL_ERRNO = 9012;
        end if;

        if username_param not in
           (select buy_vip_film.buyer_username from buy_vip_film where buy_vip_film.film_id = film_id_param)
        then
            SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'You have not bought this film before.', MYSQL_ERRNO = 9013;
        end if;
    end if;

    insert into watch_film (film_id, viewer_username)
    values (film_id_param, username_param);

END;

CREATE PROCEDURE FinishWatching(
    username_param varchar(50),
    film_id_param varchar(50)
)
BEGIN
    update watch_film
    set watch_film.has_finished = TRUE
    where watch_film.viewer_username = username_param
      AND watch_film.film_id = film_id_param;
END;
"""

create_comment_procedures = """
CREATE PROCEDURE ShowComments(
    film_id_param int,
    start_bound int,
    numberOfFilms int
)
BEGIN
    SELECT film_comment.viewer_username,film_comment.comment,film_comment.rate
    FROM film_comment
    WHERE film_comment.film_id = film_id_param
    LIMIT start_bound,numberOfFilms;
END;

CREATE PROCEDURE AddNewComments(
    viewer_username_param varchar(50),
    film_id_param int,
    comment_param varchar(200),
    rate_param int
)
BEGIN
    if viewer_username_param not in
       (
           select watch_film.viewer_username
           from watch_film
           where watch_film.film_id = film_id_param
             and watch_film.has_finished
       )
    then
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'You have not watched this film before.', MYSQL_ERRNO = 9014;
    end if;
    
    insert into film_comment (film_id, viewer_username, comment, rate)
    values (film_id_param, viewer_username_param, comment_param, rate_param);
    
END;
"""

create_invite_procedure = """
CREATE PROCEDURE Invite(
    inviter_param varchar(50),
    invited_param varchar(50)
)
BEGIN
    if invited_param in
       (
           select invite_user.invited_username
           from invite_user
       )
    then
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'You have been invited by another user before.', MYSQL_ERRNO = 9016;
    end if;

    if (invited_param, inviter_param) in
       (
           select invite_user.inviter_username, invite_user.invited_username
           from invite_user
       )
    then
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'You both have got your points before.', MYSQL_ERRNO = 9017;
    end if;

    insert into invite_user (inviter_username, invited_username)
    values (inviter_param, invited_param);

    update user
    set user.point = user.point + 1
    where user.username = inviter_param
       or user.username = invited_param;

END;
"""

create_playlist_procedures = """
CREATE PROCEDURE CreatePlaylist(
    creator_username_param varchar(50),
    playlist_name_param varchar(50),
    description_param varchar(200)
)
BEGIN
    CALL Update_Membership_Status(creator_username_param);

    if (select user.vip_membership_expiration_date from user where user.username = creator_username_param) is NULL
    then
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'You do not have any active vip-membership.', MYSQL_ERRNO = 9012;
    end if;

    insert into playlist(id, creator_username, name, description) value (0, creator_username_param, playlist_name_param, description_param);
END;

CREATE PROCEDURE ShowPlaylists(
    creator_username_param varchar(50)
)
BEGIN    
    if creator_username_param is NULL then
        select * from playlist;
    else
        select * from playlist where playlist.creator_username =creator_username_param;
    end if;
END;

CREATE PROCEDURE AddNewFilmToPlaylist(
    creator_username_param varchar(50),
    playlist_id_param int,
    film_id_param int
)
BEGIN
    CALL Update_Membership_Status(creator_username_param);
    if (select user.vip_membership_expiration_date from user where user.username = creator_username_param) is NULL
    then
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'You do not have any active vip-membership.', MYSQL_ERRNO = 9012;
    end if;
    if (creator_username_param,playlist_id_param) NOT in (select playlist.creator_username,playlist.id from playlist )
    then
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'You do not have access to add new films to this playlist.', MYSQL_ERRNO = 9018;
    end if;
    insert into playlist_film(playlist_id, film_id) value (playlist_id_param,film_id_param);
END;
"""

create_show_film_list_procedures = """
CREATE PROCEDURE ShowFilms(
    start_bound int,
    numberOfFilms int)
BEGIN
    SELECT *
    FROM film
    LIMIT start_bound,numberOfFilms;
END;

CREATE PROCEDURE ShowPlaylistFilms(
    playlist_id_param int,
    start_bound int,
    numberOfFilms int)
BEGIN
    SELECT *
    FROM film
    WHERE film.id in
          (
              select playlist_film.film_id from playlist_film where playlist_film.playlist_id = playlist_id_param
          )
    LIMIT start_bound,numberOfFilms;
END;
"""

creator_social_procedures = """
CREATE PROCEDURE Follow(
    username_param varchar(50),
    friend_username_param varchar(50)
)
BEGIN
    insert into friend (username, friend_username)
    values (username_param, friend_username_param);
END;

CREATE PROCEDURE Unfollow(
    username_param varchar(50),
    friend_username_param varchar(50)
)
BEGIN
    if (username_param, friend_username_param) not in (
        select *
        from friend
    ) then
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'You have not followed this user before.', MYSQL_ERRNO = 9020;
    end if;
    DELETE FROM friend WHERE friend.friend_username = friend_username_param and friend.username = username_param;
END;
CREATE PROCEDURE MyFriendPlaylist(
    username_param varchar(50)
)
BEGIN
    select *
    from playlist
    where playlist.creator_username in
          (
              select friend.friend_username
              from friend
              where friend.username = username_param
          );
END;
"""


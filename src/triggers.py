# triggers and transactions
create_update_film_viewers_trigger = """
CREATE TRIGGER UpdateViewers
    AFTER Update
    ON watch_film
    FOR EACH ROW
BEGIN
    if NEW.has_finished = true and OLD.has_finished = false
    then
        update film
        set film.viewers = film.viewers + 1
        where film.id = NEW.film_id;
    end if;
END;
"""
create_update_film_rate_avg_trigger = """
CREATE TRIGGER UpdateAvgRate
    AFTER INSERT
    ON film_comment
    FOR EACH ROW
BEGIN
    update film
    set film.rates = film.rates + 1
    where film.id = NEW.film_id;

    update film
    set film.rate_avg = (film.rate_avg * (film.rates - 1) + NEW.rate) / film.rates
    where film.id = NEW.film_id;
END;
"""
create_logger_triggers = """
CREATE TRIGGER NewAdminLog
    AFTER INSERT
    ON admin
    FOR EACH ROW
BEGIN
    INSERT INTO log (username, activity_type, activity_description)
    VALUES (NEW.username, 'NEW ADMIN', concat('New Admin ', NEW.username, ' added.'));
END;

CREATE TRIGGER BuyVipFilmLog
    AFTER INSERT
    ON buy_vip_film
    FOR EACH ROW
BEGIN
    INSERT INTO log (username, activity_type, activity_description)
    VALUES (NEW.buyer_username, 'BUY VIP FILM', concat(NEW.buyer_username, ' has bought film ', NEW.film_id));
END;

CREATE TRIGGER NewCategoryLog
    AFTER INSERT
    ON category
    FOR EACH ROW
BEGIN
    INSERT INTO log (activity_type, activity_description)
    VALUES ('NEW CATEGORY', concat('New category ', NEW.name, ' added'));
END;

CREATE TRIGGER NewFilmLog
    AFTER INSERT
    ON film
    FOR EACH ROW
BEGIN
    INSERT INTO log (activity_type, activity_description)
    VALUES ('NEW FILM', concat('New film ', NEW.name, ' added'));
END;

CREATE TRIGGER UpdateFilmLog
    AFTER Update
    ON film
    FOR EACH ROW
BEGIN
    INSERT INTO log (activity_type, activity_description)
    VALUES ('UPDATE FILM', concat('Film ', NEW.id, ' updated'));
END;

CREATE TRIGGER DeleteFilmLog
    AFTER DELETE
    ON film
    FOR EACH ROW
BEGIN
    INSERT INTO log (activity_type, activity_description)
    VALUES ('DELETE FILM', concat('Film ', OLD.id, ' deleted'));
END;

CREATE TRIGGER FilmCategoryLog
    AFTER INSERT
    ON film_category
    FOR EACH ROW
BEGIN
    INSERT INTO log (activity_type, activity_description)
    VALUES ('NEW FILM IN CATEGORY', concat('Film ', NEW.film_id, ' added to category ', NEW.category_id));
END;

CREATE TRIGGER NewCommentLog
    AFTER INSERT
    ON film_comment
    FOR EACH ROW
BEGIN
    INSERT INTO log (username, activity_type, activity_description)
    VALUES (NEW.viewer_username, 'NEW COMMENT', concat(NEW.viewer_username, ' commented on ', NEW.film_id));
END;

CREATE TRIGGER NewCreatorLog
    AFTER INSERT
    ON film_creator
    FOR EACH ROW
BEGIN
    INSERT INTO log (activity_type, activity_description)
    VALUES ('NEW FILM CREATOR',
            concat(NEW.creator_firstname, ' ', NEW.creator_lastname, ' added as ', NEW.role, ' of film ', NEW.film_id));
END;

CREATE TRIGGER NewTagLog
    AFTER INSERT
    ON film_tag
    FOR EACH ROW
BEGIN
    INSERT INTO log (activity_type, activity_description)
    VALUES ('NEW FILM TAG',
            concat(NEW.tag_name, ' added as a new tag for ', NEW.film_id));
END;

CREATE TRIGGER InviteLog
    AFTER INSERT
    ON invite_user
    FOR EACH ROW
BEGIN
    INSERT INTO log (username, activity_type, activity_description)
    VALUES (NEW.invited_username, 'NEW INVITE CODE',
            concat(NEW.invited_username, ' invited by ', NEW.inviter_username));
END;

CREATE TRIGGER NewPlaylistLog
    AFTER INSERT
    ON playlist
    FOR EACH ROW
BEGIN
    INSERT INTO log (username, activity_type, activity_description)
    VALUES (NEW.creator_username, 'NEW PLAYLIST', concat(NEW.name, ' created by ', NEW.creator_username));
END;

CREATE TRIGGER NewPlaylistFilmLog
    AFTER INSERT
    ON playlist_film
    FOR EACH ROW
BEGIN
    INSERT INTO log (activity_type, activity_description)
    VALUES ('ADD NEW FILM TO PLAYLIST', concat(NEW.film_id, ' added to ', NEW.playlist_id));
END;

CREATE TRIGGER NewUserLog
    AFTER INSERT
    ON user
    FOR EACH ROW
BEGIN
    INSERT INTO log (username, activity_type, activity_description)
    VALUES (NEW.username, 'NEW USER', concat(NEW.first_name, ' ', NEW.last_name, ' signed up as ', NEW.username));
END;

CREATE TRIGGER UpdateUserLog
    AFTER Update
    ON user
    FOR EACH ROW
BEGIN
    if NEW.point != OLD.point then
        INSERT INTO log (username, activity_type, activity_description)
        VALUES (NEW.username, 'UPDATE USER POINT',
                concat(NEW.username, 's points changed from ', OLD.point, ' to ', NEW.point));

    elseif NEW.balance != OLD.balance then
        INSERT INTO log (username, activity_type, activity_description)
        VALUES (NEW.username, 'UPDATE USER BALANCE',
                concat(NEW.username, 's balance changed from ', OLD.balance, ' to ', NEW.balance));

    elseif (OLD.vip_membership_expiration_date is NULL and NEW.vip_membership_expiration_date is not NULL) then
        INSERT INTO log (username, activity_type, activity_description)
        VALUES (NEW.username, 'UPDATE USER VIP MEMBERSHIP',
                concat(NEW.username, ' has bought new vip membership until ', NEW.vip_membership_expiration_date));
    elseif (OLD.vip_membership_expiration_date is Not NULL and NEW.vip_membership_expiration_date is NULL) then
        INSERT INTO log (username, activity_type, activity_description)
        VALUES (NEW.username, 'UPDATE USER VIP MEMBERSHIP', concat(NEW.username, 's vip-membership expired'));

    elseif (NEW.vip_membership_expiration_date != OLD.vip_membership_expiration_date) then
        INSERT INTO log (username, activity_type, activity_description)
        VALUES (NEW.username, 'UPDATE USER VIP MEMBERSHIP', concat(NEW.username, 's membership updated from ',
                                                                   OLD.vip_membership_expiration_date, ' to ',
                                                                   NEW.vip_membership_expiration_date));

    else
        INSERT INTO log (username, activity_type, activity_description)
        VALUES (NEW.username, 'UPDATE USER INFO', concat(NEW.username, 's personal info  updated'));
    end if;
END;

CREATE TRIGGER WatchFilmLog
    AFTER INSERT
    ON watch_film
    FOR EACH ROW
BEGIN
    INSERT INTO log (username, activity_type, activity_description)
    VALUES (NEW.viewer_username, 'WATCH FILM', concat(NEW.viewer_username, ' started watching film ', NEW.film_id));
END;

CREATE TRIGGER FinishedWatchingLog
    AFTER Update
    ON watch_film
    FOR EACH ROW
BEGIN
    INSERT INTO log (username, activity_type, activity_description)
    VALUES (NEW.viewer_username, 'FINISHED WATCHING FILM', concat(NEW.viewer_username, ' has finished watching film ', NEW.film_id));
END;

CREATE TRIGGER FollowLog
    AFTER INSERT
    ON friend
    FOR EACH ROW
BEGIN
    INSERT INTO log (username, activity_type, activity_description)
    VALUES (NEW.username, 'FOLLOWS', concat(NEW.username, ' started following ', NEW.friend_username));
END;

CREATE TRIGGER UnfollowLog
    AFTER DELETE
    ON friend
    FOR EACH ROW
BEGIN
    INSERT INTO log (username, activity_type, activity_description)
    VALUES (OLD.username, 'UNFOLLOWS', concat(OLD.username, ' unfollows ', OLD.friend_username));
END;

"""

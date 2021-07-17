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

# procedures and functions of database

create_signUp_procedure = """
CREATE PROCEDURE SignUp(
    username_param varchar(20),
    password_param varchar(128),
    last_name_param varchar(20),
    first_name_param varchar(20),
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
        set result = 'This username is already taken.\n';
    end if;

    if email_param is not null AND email_param in (
        select user.email
        from user
    ) then
        set result = concat(result, 'A user with this email has signed up before\n');
    end if;

    if phone_number_param is not null then
        if phone_number_param in (
            select user.phone_number
            from user
        ) then
            set result = concat(result, 'A user with this phone number has signed up before\n');
        end if;
        if char_length(phone_number_param) <> 10 then
            set result = concat(result, 'Phone number must be exactly 10 characters\n');
        end if;
    end if;

    if melli_code_param is not null then
        if melli_code_param in (
            select user.melli_code
            from user
        ) then
            set result = concat(result, 'A user with this Melli code has signed up before\n');
        end if;
        if char_length(melli_code_param) <> 10 then
            set result = concat(result, 'Melli code must be exactly 10 characters\n');
        end if;
    end if;

    if not (password_param REGEXP '[0-9]' and
        password_param REGEXP BINARY '[A-Z]' and
        password_param REGEXP BINARY '[a-z]' and
        char_length(password_param) > 7) then
        set result = concat(result, 'Entered password must contain at least a number, an uppercase letter, and 8 characters\n');
    end if;


    if strcmp(result, '') <> 0 then
        rollback ;
    else
        insert into user (username, password, last_name, first_name, email, phone_number, melli_code)
        values (username_param, password_param, last_name_param, first_name_param, email_param, phone_number_param,
                melli_code_param);
        set result = concat(username_param, ' signed up successfully\n');
        COMMIT;
    end if;

END
;"""

create_signUp_procedure = """
CREATE PROCEDURE SignIn(username_param varchar(50), password_param varchar(50))
BEGIN
    if username_param not in (
        select user.username
        from user
    ) then
        SIGNAL SQLSTATE '02000'
            SET MESSAGE_TEXT = 'User not found! Please sign up first.', MYSQL_ERRNO = 9990;
    end if;

    if not exists(
            select *
            from user
            where (username, password) = (username_param, password_param)
        ) then
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Your password is not correct. Please try again.', MYSQL_ERRNO = 9994;

    end if;
END;
;"""


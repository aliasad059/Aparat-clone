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
        set result = 'This username is already taken.\n';
    END if;

    if email_param is not null AND email_param in (
        select user.email
        from user
    ) then
        set result = concat(result, 'A user with this email has signed up before\n');
    END if;

    if phone_number_param is not null then
        if phone_number_param in (
            select user.phone_number
            from user
        ) then
            set result = concat(result, 'A user with this phone number has signed up before\n');
        END if;
        if char_length(phone_number_param) <> 10 then
            set result = concat(result, 'Phone number must be exactly 10 characters\n');
        END if;
    END if;

    if melli_code_param is not null then
        if melli_code_param in (
            select user.melli_code
            from user
        ) then
            set result = concat(result, 'A user with this Melli code has signed up before\n');
        END if;
        if char_length(melli_code_param) <> 10 then
            set result = concat(result, 'Melli code must be exactly 10 characters\n');
        END if;
    END if;

    if not (password_param REGEXP '[0-9]' and
        password_param REGEXP BINARY '[A-Z]' and
        password_param REGEXP BINARY '[a-z]' and
        char_length(password_param) > 7) then
        set result = concat(result, 'Entered password must contain at least a number, an uppercase letter, and 8 characters\n');
    END if;


    if strcmp(result, '') <> 0 then
        rollback ;
    else
        insert into user (username, password, last_name, first_name, email, phone_number, melli_code)
        values (username_param, password_param, last_name_param, first_name_param, email_param, phone_number_param,
                melli_code_param);
        set result = concat(username_param, ' signed up successfully\n');
        COMMIT;
    END if;

END;"""

create_signIn_procedure = """
CREATE PROCEDURE SignIn(username_param varchar(50), password_param varchar(50))
BEGIN
    if username_param not in (
        select user.username
        from user
    ) then
        SIGNAL SQLSTATE '02000'
            SET MESSAGE_TEXT = 'User not found! Please sign up first.', MYSQL_ERRNO = 9000;
    END if;

    if not exists(
            select *
            from user
            where (username, password) = (username_param, password_param)
        ) then
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Your password is not correct. Please try again.', MYSQL_ERRNO = 9001;

    END if;
END;"""

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
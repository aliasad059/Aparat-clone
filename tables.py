# tables of database

create_table_admin = """
create table admin
(
    username varchar(50) primary key,
    password varchar(50) not null
);
"""

create_table_user = """
create table user
(
    username                       varchar(50) primary key,
    password                       varchar(50) not null,
    last_name                      varchar(50),
    first_name                     varchar(50),
    email                          varchar(50),
    phone_number                   char(10),
    melli_code                     char(10),
    balance                        int  default 0,
    point                          int  default 0,
    has_vip_membership             bool default false,
    vip_membership_expiration_date date default null
);
"""

create_table_film = """
create table film
(
    id           int auto_increment primary key,
    name         varchar(50),
    release_date date,
    price        int default 0,
    details      varchar(200),
    viewers      int default 0
);
"""

create_table_category = """
create table category
(
    name varchar(50) primary key 
);
"""

create_table_tag = """
create table tag
(
    tag_value varchar(50) primary key 
);
"""

create_table_film_category = """
create table film_category
(
    film_id       int,
    category_name   varchar(50),
    primary key (film_id,category_name),
    foreign key (film_id) references film (id),
    foreign key (category_name) references category (name)
);
"""

create_table_film_tag = """
create table film_tag
(
    film_id       int,
    tag_name   varchar(50),
    primary key (film_id,tag_name),
    foreign key (film_id) references film (id),
    foreign key (tag_name) references tag (tag_value)
);
"""

create_table_film_creator = """
create table film_creator
(
    film_id           int primary key,
    creator_firstname varchar(50),
    creator_lastname  varchar(50),
    role              varchar(50),
    foreign key (film_id) references film (id)
);
"""

create_table_watch_film = """
create table watch_film
(
    film_id         int primary key,
    viewer_username varchar(50),
    has_finished    bool default false
);
"""

create_table_invite_user = """
create table invite_user
(
    inviter_username varchar(50),
    invited_username varchar(50),
    primary key (inviter_username, invited_username),
    foreign key (inviter_username) references user (username),
    foreign key (invited_username) references user (username)
);
"""

create_table_film_comment = """
create table film_comment
(
    film_id         int,
    viewer_username varchar(50),
    comment         varchar(200),
    rate            int,
    check ( rate >= 0 and rate <= 5),
    primary key (film_id, viewer_username),
    foreign key (film_id) references film (id),
    foreign key (viewer_username) references user (username)
);
"""

create_table_playlist = """
create table playlist
(
    id               int auto_increment primary key,
    name             varchar(50),
    description      varchar(200),
    creator_username varchar(50),
    foreign key (creator_username) references user (username)
);
"""

create_table_playlist_film = """
create table playlist_film
(
    playlist_id int,
    film_id     int,
    primary key (playlist_id, film_id),
    foreign key (playlist_id) references playlist (id),
    foreign key (film_id) references film (id)
);
"""

create_table_follow_user = """
create table follow_user
(
    follower_username  varchar(50),
    following_username varchar(50),
    primary key (follower_username, following_username),
    foreign key (follower_username) references user (username),
    foreign key (following_username) references user (username)
);
"""

create_table_log = """
create table log
(
    username             varchar(50),
    activity_type        varchar(50),
    occurred_at          timestamp default now(),
    activity_description varchar(200)
);
"""

create_table_mysqlErrors = """
create table my_errors(
    err_number int auto_increment,
    err_description varchar(200)
);
"""
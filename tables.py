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
    viewers      int default 0,
    rate_avg     int default 0,
    rates        int default 0
);
"""

create_table_category = """
create table category
(
    id int auto_increment primary key,
    name varchar(50)
);
"""

create_table_film_category = """
create table film_category
(
    film_id       int,
    category_id   int,
    primary key (film_id,category_id),
    foreign key (film_id) references film (id) on delete cascade ,
    foreign key (category_id) references category (id) on delete cascade 
);
"""

create_table_film_tag = """
create table film_tag
(
    film_id       int,
    tag_name   varchar(50),
    foreign key (film_id) references film (id) on delete cascade 
);
"""

create_table_film_creator = """
create table film_creator
(
    film_id           int ,
    creator_firstname varchar(50),
    creator_lastname  varchar(50),
    role              varchar(50),
    foreign key (film_id) references film (id) on delete cascade
);
"""

create_table_watch_film = """
create table watch_film
(
    film_id         int ,
    viewer_username varchar(50),
    has_finished    bool default false,
    foreign key (film_id) references film (id) on delete cascade
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
    comment         varchar(200) NULL,
    rate            int NOT NULL,
    check ( rate >= 0 and rate <= 5),
    foreign key (film_id) references film (id) on delete cascade ,
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
    foreign key (film_id) references film (id) on delete cascade 
);
"""

create_table_friend = """
create table friend
(
    username  varchar(50),
    friend_username varchar(50),
    primary key (username, friend_username),
    foreign key (username) references user (username),
    foreign key (friend_username) references user (username)
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
create_table_buy_vip_film = """
create table buy_vip_film
(
    buyer_username varchar(50),
    film_id        int,
    primary key (buyer_username, film_id),
    foreign key (buyer_username) references user (username),
    foreign key (film_id) references film (id) on delete cascade 
);
"""

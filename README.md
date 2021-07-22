# Aparat-Clone
This is my final project of Database Design course at AUT.

Aparat-Clone is a basic version of Iranian video-sharing service [Aparat](https://www.aparat.com/).

All the logic part of the project are written in mysql queries ( as it's my DB course :) )


# How To Use
You first need to create a new user in mysql as follows
```sql 
mysql> CREATE USER 'username-you-like'@'localhost' IDENTIFIED BY 'a-strong-password';
```
and then grant all permission to the new user
```sql
mysql> GRANT ALL PRIVILEGES ON * . * TO 'username-you-like'@'localhost';
mysql> FLUSH PRIVILEGES;
```
and finally create database
```sql
mysql> CREATE DATABASE IF NOT EXISTS Aparat
```
before you run the main programm, you need to set your configurations you did before.

you just need to set the config.json file as:

``` json 
{
  "user": "your-user-name",
  "password": "your-password",
  "host": "127.0.0.1",
  "database": "Aparat",
  "buffered": true,
  "autocommit": true
}
```

To test this program, install requirements of it by `pip`.
like this.
```
pip install -r requirements.txt
```
then you can start program by below command.
```
python3 main.py
```
# Features
- Create an Aparat account
- Sign-in as admin and CRUD the films, categories,and see log history of what users done 
- Sign-in as a user
- Watch movies, add new comment and rate 
- Create Playlist of Aparat films and share it to others
- Upgrade to VIP-Member to watch the VIP-films
- Follow and Unfollow a friend to see his/her Playlist
- ...

# Requirements
  - Mysql
  - mysql-connector-python
  - prettytable
# sms_pc project

This project is on working but for working on it do:

## How to run

1. Install python3, pip3, virtualenv, MySQL in your system.

2. Clone the project `https://github.com/mgmgst/sms_pc.git` && cd sms_serial_verification

3. in the app folder, rename the `config.py.sample` to `config.py` and do proper changes.

4. run this comand in MYSQL database : `CREATE DATABASE smsmysql;`

5. run this comand in MYSQL database : `CREATE USER 'smsmysql'@'localhost' IDENTIFIED BY 'test';`

6. run this comand in MYSQL database : `GRANT ALL PRIVILEGES ON smsmysql.* TO 'smsmysql'@'localhost';`

7. run this comand in MYSQL database : `DROP TABLE IF EXISTS messages;`

8. db configs are in config.py. Create the db and grant all access to the specified user with specified password, but you also need to add this table to the database manually: `CREATE TABLE messages (sender VARCHAR(100) , message VARCHAR(1024));`

9. Create a virtualenve named build using `virtualenv -p python3 venv`

10. Connect to virtualenv using `source venv/bin/activate`

11. From the project folder, install packages using `pip install -r ./app/requirements.txt`

12. Now environment is ready. Run it by `python app/main.py`

### Or you can use Dockerfile

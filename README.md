## hammer
hammer is an basic lightweight inventory management system developed in Python with a Tkinter GUI and a SQLite3 database.
hammer's abilities include:
- Creating and managing Records and Items
- Creating and managing users
- Checking Items out and returning them

## Development Note
hammer is still in very early development. Changes can and will happen, and your current databases and settings files may 
not work in later versions of hammer. As we get closer to a stable, functional state, we will begin implementing measures
to allow for the updating of databases and settings files to ensure compatibility.

hammer currently utilizes MySQL for its database. We have recently switched to MySQL from SQLite3, so there will likely be some
issues leftover from that conversion, as well as old SQLite3 code. If you run into any issues, please open an Issue. MySQL must
be configured separately from hammer.

## Configuring
In this current revision, for hammer to work as intended, a .env file in the src folder in hammer's directory *MUST* be
configured. In this file, you will find three variables that need to be filled out:
```env
db_host=<insert_host_address>
db_user=<insert_user_name>
db_password=<insert_desired_user_password>
```
Assuming your information is correct, opening hammer will create the required database, hammerDB, and the necessary
tables.

## Requirements
In order to run hammer yourself from source, you will be required to install:
- Python 3.11
  - This is the version that we are currently targeting, but it *should* work with any recent version of Python.
- bcrypt
  - This can be installed with ```pip install bcrypt```.
- Python MySQL
  - This can be installed with ```pip install mysql-python-connector```.
- python-dotenv
    - This can be installed with ```pip install python-dotenv```.
- tkcalendar
  - tkcalendar is used to handle date entry in the Create User and Manage User screens. It can be installed with ```pip install tkcalendar```.

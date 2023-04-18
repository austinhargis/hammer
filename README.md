## hammer
hammer is an basic lightweight inventory management system developed in Python with a Tkinter GUI and a SQLite3 database.
hammer's abilities include:
- Creating and managing Records and Items
- Creating and managing users
- Checking Items out and returning them
- Switching between databases

## Development Note
hammer is still in very early development. Changes can and will happen, and your current databases and settings files may 
not work in later versions of hammer. As we get closer to a stable, functional state, we will begin implementing measures
to allow for the updating of databases and settings files to ensure compatibility.

hammer currently utilizes SQLite3 for its databases. However, in the future hammer will likely switch to another SQL module
in order to allow for databases hosted off of the system in which hammer is deployed. Compatibility of databases between 
these modules is currently uncertain.

## Requirements
In order to run hammer yourself from source, you will be required to install:
- Python 3.11
  - This is the version that we are currently targeting, but it *should* work with any recent version of Python.
- tkcalendar
  - tkcalendar is used to handle date entry in the Create User and Manage User screens. It can be installed with ```pip install tkcalendar```.

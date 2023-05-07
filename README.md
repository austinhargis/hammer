## hammer
hammer is a basic lightweight inventory management system developed in Python with a Tkinter GUI and a MySQL database.
hammer's abilities include:
- Creating and managing Records and Items
- Creating and managing users
- Checking Items out and returning them

## Development Note
hammer is still in very early development. Changes can and will happen, and your current databases and settings files may 
not work in later versions of hammer. As we get closer to a stable, functional state, we will begin implementing measures
to allow for the updating of databases and settings files to ensure compatibility.

## Configuring
Upon launching hammer, you may be presented with a configuration screen, asking for a hostname, SQL user, and a SQL password.
This information is necessary in order to create hammer's database and tables. Once you enter the required information, 
you can press 'Save'. This will save your changes and close the popup window. Reopen hammer with its executable, and you 
will be brought to the login page. The default credentials are:
- ```Username: admin```
- ```Password: 12345```

The password for this account can be changed in the Manage User screen, however, this account cannot be disabled.

If after entering your MySQL database credentials, you continue to see the configuration window, please double-check that
you have correctly configured your database. If you are certain that you have configured your database correctly,
please open an issue on hammer's GitHub page. 

## Requirements
In order to run hammer yourself from source, you will be required to install a few modules. These can all be installed with
```pip install -r requirements.txt```. The following Python version is required:
- Python 3.11 (or greater)

The following modules are required:
- bcrypt
- MySQL Connector Python
- pyinstaller
- python-dotenv
- tkcalendar
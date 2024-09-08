version: Python 3.10.12

To start the app:

Make sure Python 3 is installed.

Start a virtual environment and then run the code: 

  pip3 install -r requirements.txt

Once you have everything installed cd into the folder with 'manage.py'
and run this line:

  python3 manage.py createsuperuser

This will prompt you to create an admin for the site.

*Note, if you're on PC, commands should start with python instead
of python3, on Mac/Linux commands start with pip3 and python3*

Once you're made an admin user run these lines:

  python3 manage.py makemigrations
  python3 manage.py migrate
  python3 manage.py runserver

This will transfer the models into an SQLite database and start the
site on your local host, then just enter your local host into your
browsers URL line or if you're using VS Code you can CTRL click
the address in the terminal.

You can then log in as your admin to see the website with all features,
register some buildings from the Users page, register a staff member as 
the admin and log in as them, then you can
register as a user and approve the request as the admin, 
then try requesting a parking pass as the user and look at, and 
approve requests as a staff member or admin.

There's still much work to do and it's not the prettiest to look at,
but the functionality is coming together.

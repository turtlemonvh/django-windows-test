django-windows-test
===================

This project is a simple test application for checking that Django works with IIS 7 on Windows Server 2008R2 with MS SQL Express 2008.  It is designed to be used as a starting point for testing that a more sophisticated Django application can work in this environment.

Where this comes from
----------------
* A guide for setting up Django on Windows (specifically using PyISAPIe on 64 bit IIS) is given in [the installation tutorial on wolf++].
* The to-do app used here is almost completely taken from [this net tuts tutorial](http://net.tutsplus.com/tutorials/python-tutorials/intro-to-django-building-a-to-do-list/) with a few changes to make it cleaner (e.g. use of django forms).
* More information about PyISAPIe was taken from [a blog post by geographika](http://geographika.co.uk/setting-up-python-on-iis7).

Installing and configuring python on target machine
-------------------
1. Get this project onto the target machine

    Create a new folder `c:\PyISAPIe` and clone the project into this folder.  [Msysgit](http://msysgit.github.com/) is a great git package for Windows if you're looking for one. 

        git clone git@github.com:turtlemonvh/django-windows-test.git

    Alternatively, you can just download the zip file and extract into this folder.

1. Download Python 2.7.3 for 64 bit architectures from [the official download site](http://www.python.org/download/).  Run the installer and accept all the default options to install.  Make sure the "Install for all users" option is checked (this should be the default setting).
 * Check your path to make sure the path to your python executable (`C:\Python27\`) and the path to the scripts folder (`C:\Python27\Scripts`) are both on your `PATH`.
1. Download `ez_setup.py` from [the setuptools site](https://pypi.python.org/pypi/setuptools#files).  Run this with python to install setuptools.
1. Install `pip` at the command line with the command `easy_install pip`
1. Create a virtual env and activate it

        virtualenv --no-site-packages ENVIRONMENT_NAME
        ENVIRONMENT_NAME\Scripts\Activate

1. Install `pywin32` for 64 bit architectures
  * Download executable from [the project website](http://sourceforge.net/projects/pywin32/files/pywin32/)
  * Install with easy_install

             easy_install \path\to\download\x.exe

1. Install `python-ldap` for 64 bit architectures
  * Download executable from [UCI's list of pre-compiled python libraries for Windows](http://www.lfd.uci.edu/~gohlke/pythonlibs/#python-ldap).
 * Install the same way as `pywin32`.

1. Install Django, the MsSQL driver package, and the LDAP wrapper package

        pip install django
        pip install django-mssql
        pip install django-auth-ldap

1. Browse to the `site-packages` folder for your installation, probably `C:\Python27\Lib\site-packages`
  * Copy all 3 DLL files from the `pywin32_system32` folder to `C:\Python27`
  * **If you skip this step you may find you have problems with MS SQL later on.**

CHECKPOINT: Check your installed packages using `pip freeze`.  Should resemble the following, with version numbers possibly changes.

    Django==1.4.5
    django-auth-ldap==1.1.3
    django-mssql==1.2
    python-ldap==2.4.9
    pywin32==218

Setting up IIS to talk to Python through PyISAPIe
-------------------
1. Download pre-compiled PyISAPIe dll from [the installation tutorial on wolf++].

  In the `c:\PyISAPIe` folder, and add the dll at `c:\PyISAPIe\PyISAPIe.dll`.
  
  There should also be a few folders in that zip file from wolf++.    Inside the `Http` directory, modify the file `Isapi.py` modify the statement modyfying the path to `os.sys.path.append('C:\inetpub\PyApp\django-windows-test\windowstest')`.  

  In the `Map` array, modify the middle portion to read `["/"     , "windowstest.settings"  ],`.    This associates your django project with the root url of this IIS web server, a bit like [Apache VirtualHosts](http://httpd.apache.org/docs/2.2/vhosts/).
  
  If you are not using Python 2.7.2 and running on a 64 bit operating system you may need to compile the executable yourself.  The tutorial also has instructions for doing that.

1. Download and install MS Visual Studio 2008 and 2010 redistributable packages

  These are needed for the DLL file downloaded / compiled in the previous step to work.

  * [Link to 2008 download page](http://www.microsoft.com/en-us/download/details.aspx?id=29)
  * [Link to 2010 download page](http://www.microsoft.com/en-us/download/details.aspx?id=5555)

1. Create directory `c:\inetpub\django` where you can add this project

1. Get the project in that directory
  You can download the zip file and unzip to that directory, or [install a flavor of git that plays nice with Windows](http://code.google.com/p/msysgit/downloads/list?q=full+installer+official+git) and clone into that directory.

1. Add a new site using the IIS Manager
  Here you will add a site and set it up to be handled by isapie.

  * Right click on the `Sites` folder in the left view pane and select the `Add Web Site...` option
      * Set name to `DjangoApp`
      * Set physical path to `c:\inetpub\django`
      * Set port to `8090` or another unused port
  * Left (select) click on the new site to get to the main options screen.
  * Under `IIS`, double click on `Handler Mappings` to option that dialog
  * In the right pane under `Actions`, select the `Add Wildcard Script Map` option
      * Set request path to `*`
      * Set executable to `c:\PyISAPIe\PyISAPIe.dll`
      * Set name to `PyISAPIe`

Setting up MS SQL
-------------------

1. [Download MS SQL Server Express 2008](http://www.microsoft.com/en-us/download/details.aspx?id=1695) and [SQL Server Express Management Studio](http://www.microsoft.com/en-us/download/details.aspx?id=7593) and install each.
1. Using the object explorer interface, create a new database for your application.  Use the default owner (usually the administrator account).  Accept all default options.
1. Create a database user to use to access your database.
  1. Expand the top level folder labeled `Security` (make sure you click on the top level and not the folder within your new database folder).
  1. Right click on `Logins` and select `New Login`.
  1. In the dialog window, create a login name for your user.
  1. Select the `SQl Server authentication` option, and enter a password.
    * Windows will prompt you for a better password if yours doesn't meet it's security requirements.
    * Note that the username and password combination you enter here is what will go in your `settings.py` for configuring database access.
  1. Select the database you created in the previous step as the default database for this user.
  1. Click `OK` to create the user.
1. Right click on the `Security` folder of the new database to create a new user.
1. Give this new user permission to create, edit, and view tables in your new database.
  1. Under the `Databases` folder, find the folder for your database and expand it.
  1. Locate the `Security` folder and expand it.
  1. Right click on `Users` and select `New User`.
  1. In the dialog box, give the user a User name (this can just be a more human-friendly version of the login username you defined in the previous step).  
  1. Click the ellipses to the right of `Login name`.
  1. In the `Select Login` dialog box, click the `Browse` button to open a dialog to browse for existing users.
  1. Click the checkbox next to the user you created previously, and click `OK` on both dialog boxes.
  1. Back in the `Database User` dialog box, check the following options under both `Owned Schemas` and `Role Members`: "db\_accessadmin, db\_datareader, db\_datawriter, db\_ddl\_admin".
1. Edit `settings.py` to use the parameters for your mssql installation

        DATABASES = {
            'default': {
            'NAME': 'dsef',
            'ENGINE': 'sqlserver_ado',
            'HOST': 'localhost',
            'USER': 'dsef_test_user',
            'PASSWORD': 'ASuperSecurePassWordToMakeWindowsHappy!',
            }
        }
  
Setting up connection to LDAP
-------------------

Setting up an ActiveDirectory server is beyond the scope of this project.  Here we assume you are connecting to an existing installation.

With this setup, each user in the targeted LDAP directory will be added as a user in your project.  No information about groups is added.  The superuser for your site (needed to access the admin) should be created separately.

1. Change the value of `AUTH_LDAP_SERVER_URI` in `settings.py` to match the location for your server.
1. Change the value of `AUTH_LDAP_USER_DN_TEMPLATE` in `settings.py`, in particular the `DSEF.private` component, to match the location for your server.
  
Getting it running
-------------------
1. Initialize the database by opening a command prompt,  `cd`ing to `c:\inetpub\django` and executing the following

        python manage.py syncdb
    
1. That should be all.

  Visit `http://localhost:8090/` in a browser to see the to do list.  Add to-do tasks to check your database connection.
  
Notes
-------------------
* If you are getting the error `You probably did a passthrough with PyISAPIe configured as an application map instead of a wildcard map` (displayed as a generic error page in IE)

  Check to make sure you defined your hander mapping for PyISAPIe as a "Wildcard Script Map" and not a "Script Map".

* If you change anything in `c:\PyISAPIe` or `c:\inetpub\django` (the application driver directory and your application directory, respectively), you may need to recycle your application pool to see these changes take effect.

  To do this, click on `Application Pools` in the left view pane of the IIS Manager, select `DjangoApp`, and click the `Recycle` task in the right view pane.

* You may want to run your site on port 80 so you don't have to type in a port number when accessing it, and you don't have to play with Windows Firewall settings to open a new port.

  * To change the ports, start the IIS Manager and click on "Sites" on the left pane.  
  * Right click on a site and select "bindings".
  * Click on the port binding you want to edit and select "Edit...".
  * Change the port number in the dialog window that pops up and click "OK" then "Close" to accept the changes and close both dialog boxes.
  * You then must click "Restart" under the "Manage Web Site" heading on the right pane of the IIS Manger for these changes to take effect.
  
!!TODO!!
-------------------
* Double check process for IIS integration with PyISAPIe to torubleshoot for possible mistakes.
* Get LDAP to play nice with IIS and not just the development server.

[the installation tutorial on wolf++]: http://blog.wolfplusplus.com/?p=272


django-windows-test
===================

This project is a simple test application for checking that Django works with IIS 7 on Windows Server 2008R2 with MS SQL Express 2008.  It is designed to be used as a starting point for testing that a more sophisticated Django application can work in this environment.

Where this comes from
----------------
* A guide for setting up Django on Windows (specifically using PyISAPIe on 64 bit IIS) is given in [the installation tutorial on wolf++].
* The to-do app used here is almost completely taken from [this net tuts tutorial](http://net.tutsplus.com/tutorials/python-tutorials/intro-to-django-building-a-to-do-list/) with a few changes to make it cleaner (e.g. use of django forms).
* More information about PyISAPIe was taken from [a blog post by geographika](http://geographika.co.uk/setting-up-python-on-iis7).

Installing and configuring python and python packages on target machine
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

_CHECKPOINT:_ Check your installed packages using `pip freeze`.  The output should resemble the following, with version numbers possibly changed.

    Django==1.4.5
    django-auth-ldap==1.1.3
    django-mssql==1.2
    python-ldap==2.4.9
    pywin32==218

Setting up IIS to talk to Python through PyISAPIe
-------------------
1. Download pre-compiled PyISAPIe dll from [the installation tutorial on wolf++].

  In the `c:\PyISAPIe` folder, and add the dll at `c:\PyISAPIe\PyISAPIe.dll`.
  
  There should also be a few folders in that zip file from wolf++.    Inside the `Http` directory, modify the file `Isapi.py` modify the statement modyfying the path to `os.sys.path.append('C:\inetpub\djangoapp\django-windows-test\windowstest')`.  

  In the `Map` array, modify the middle portion to read `["/"     , "windowstest.settings"  ],`.    This associates your django project with the root url of this IIS web server, a bit like [Apache VirtualHosts](http://httpd.apache.org/docs/2.2/vhosts/).
  
  If you are not using Python 2.7.2 and running on a 64 bit operating system you may need to compile the executable yourself.  The tutorial also has instructions for doing that.

1. Download and install MS Visual Studio 2008 and 2010 redistributable packages

  These are needed for the DLL file downloaded / compiled in the previous step to work.

  * [Link to 2008 download page](http://www.microsoft.com/en-us/download/details.aspx?id=29)
  * [Link to 2010 download page](http://www.microsoft.com/en-us/download/details.aspx?id=5555)

1. Create directory `c:\inetpub\djangoapp` where you can add this project

1. Get the project in that directory
  You can download the zip file and unzip to that directory, or [install a flavor of git that plays nice with Windows](http://code.google.com/p/msysgit/downloads/list?q=full+installer+official+git) and clone into that directory.

1. Add a new site using the IIS Manager
  Here you will add a site and set it up to be handled by python via isapi.

  * Right click on the `Sites` folder in the left view pane and select the `Add Web Site...` option
      * Set name to _DjangoApp_
      * Set physical path to `c:\inetpub\djangoapp`
      * Set port to `8090` or another unused port
  * Left (select) click on the new site to get to the main options screen.
  * Under `IIS`, double click on `Handler Mappings` to option that dialog
  * In the right pane under `Actions`, select the `Add Wildcard Script Map` option
      * Set request path to `*`
      * Set executable to `c:\PyISAPIe\PyISAPIe.dll`
      * Set name to `PyISAPIe`

1. Set the new site to run on port *80, and change the default website to run on *8090.

   You may want to run your site on port 80 so you don't have to type in a port number when accessing it and you don't have to play with Windows Firewall settings to open a new port.

  * To change the port for a website, start the IIS Manager and click on _Sites_ on the left pane.  
  * Right click on a site and select _bindings_.
  * Click on the port binding you want to edit and select _Edit..._.
  * Change the port number in the dialog window that pops up and click _OK_ then _Close_ to accept the changes and close both dialog boxes.
  * You then must click _Restart_ under the _Manage Web Site_ heading on the right pane of the IIS Manger for these changes to take effect.

_CHECKPOINT:_ You should now be able to access `http://localhost/` on the server and see a Django error page.  You can't see the home page yet because the database hasn't been configured.

If you want to check that the site works you can just use the default sqlite database included with this project.  To do this, change your `DATABASE` variable in `settings.py` to the following:

      DATABASES = {
          "default": {
              "ENGINE": "django.db.backends.sqlite3", # Add "postgresql_psycopg2", "postgresql", "mysql", "sqlite3" or "oracle".
              "NAME": "to-do.db",                       # Or path to database file if using sqlite3.
              "USER": "",                             # Not used with sqlite3.
              "PASSWORD": "",                         # Not used with sqlite3.
              "HOST": "",                             # Set to empty string for localhost. Not used with sqlite3.
              "PORT": "",                             # Set to empty string for default. Not used with sqlite3.
          }
      }


Serving static files for Django directly via IIS
-------------------
1. Make sure your `PyISAPIe` handler is defined as a `ScriptMap` and not a `Wildcard Script Map`.  A wildcard map will intercept every request for every file in all sub folders which would not allow your static files to be served.

1. Check your `Isapi.py` file (in `C:\PyISAPIe\Http\`) to make sure you have the following line in the `Map` array

        ["/media" , lambda: True        ], # exclude and passthrough

    This instructs the Isapi dll to pass off handling of requests to `/media` to the next available handler, which in our case will be the StaticFile handler.  This should be above the line in this array mapping `"/"` to your settings file.

1. Configure `settings.py` to use the following values defining the location of static and media files.

        MEDIA_ROOT = 'media/media/'
        MEDIA_URL = 'media/media/'
        STATIC_ROOT = 'media/static/'
        STATIC_URL = '/media/static/'

1. `cd` to `c:\inetpub\djangoapp\django-windows-test\windowstest` and run `python manage.py collectstatic` at the command line to collect static and media files into the target directories.
        
1. Add a Virtual Directory to the _DjangoApp_ web site in IIS Manager

    1. In the IIS Manager, right click in the top level folder _DjangoApp_.
    1. Select _Add Virtual Directory_.
    1. For the alias type `media`.
    1. For the physical path select the static root of your application (where `collectstatic` dumped the files).
    1. Click _OK_.  You should not see an additional folder under _DjangoApp_ which links to your `media` folder.

1. Set up the new virtual directory to use the `StaticFile` handler before the `PyISAPIe` handler

  Handler mappings defined at the _DjangoApp_ level for your site (i.e. the top level) are inherited for each directory of that site, including the virtual directories.  Though `PyISAPIe` should be the first handler for _DjangoApp_ as a whole, the `media` directory needs to have the `StaticFile` handler ordered first.  To fix this:

    1. In IIS Manager click on the `media` virtual directory folder to select
    1. In the center options pane under _IIS_ double click _Handler Mappings_.
    1. In the right _Actions_ pane of the _Handler Mappings_ view, click the _View Ordered List_ link.
    1. Use the arrows in the right pane of the resulting view to move the `StaticFile` handler up to the top of the list, above the `PyISAPIe` handler.
   
1. Create a new `web.config` file in `c:\inetpub\djangoapp\django-windows-test\windowstest\` with the following contents.

        <configuration>
            <system.webServer>
                <handlers>
                   <clear />
                    <add 
                        name="StaticFile" 
                        path="*" verb="*" 
                        modules="StaticFileModule,DefaultDocumentModule,DirectoryListingModule" 
                        resourceType="Either" 
                        requireAccess="Read" />
                </handlers>
                <staticContent>
                    <mimeMap fileExtension=".*" mimeType="application/octet-stream" />
                </staticContent>
            </system.webServer>
        </configuration>
     
1. Refresh the application pool for _DjangoApp_.  

_CHECKPOINT:_ You should be able to access the application's static files (e.g. try accessing `http://localhost/media/static/admin/img/icon_searchbox.png`).
      
Setting up MS SQL as the Django database
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

1. Initialize the database by opening a command prompt, `cd`ing to `c:\inetpub\djangoapp\django-windows-test\windowstest` and executing the following:

        python manage.py syncdb

_CHECKPOINT:_ You should now be able to access `http://localhost/` on the server and add items as an anonymous user.

Setting up connection to LDAP
-------------------

Setting up an ActiveDirectory server is beyond the scope of this project.  Here we assume you are connecting to an existing installation.

With this setup, each user in the targeted LDAP directory will be added as a user in your project.  No information about groups is added.  The superuser for your site (needed to access the admin) should be created separately.

1. Change the value of `AUTH_LDAP_SERVER_URI` in `settings.py` to match the location for your server.
1. Change the value of `AUTH_LDAP_USER_DN_TEMPLATE` in `settings.py`, in particular the `DSEF.private` component, to match the location for your server.

At this point we found there was still an error coming from the `python-ldap` module based off the way debug functions were structured.  Replacing the file `PYTHON_BASE_DIR\Lib\site-packages\ldap\functions.py` with the contents of `python-ldap-fix\functions_fixed.py` allowed us to connect.

This error seems to come about because somewhere the special constant `__debug__` is being manipulated in a way that causes it to behave strangely.  More details can be found in [this stackexchange post](http://stackoverflow.com/questions/15305688/conditional-debug-statement-not-executed-though-debug-is-true).  We're working on a better solution.

_CHECKPOINT:_ You should now be able to access `http://localhost/` on the server, login as one of the users in the Active Directory system you connected to, and leave to-do items as that user.
  
Notes and Tips
-------------------
* If you are getting the error `You probably did a passthrough with PyISAPIe configured as an application map instead of a wildcard map` (displayed as a generic error page in IE)

  Check to make sure you defined your hander mapping for PyISAPIe as a "Wildcard Script Map" and not a "Script Map".

* If you are having problems with the handler mappings, it may help to look at the raw configuration files used for your site to check for errors.

  In particular the following 3 configuration files are good to examine:

  1. `C:\Windows\System32\inetserv\Config\applicationHost.config` - the main configuration for IIS
  1. `C:\inetpub\djangoapp\django-windows-test\windowstest\web.config` - the main configuration file for the _djangoapp_ site
  1. `C:\inetpub\djangoapp\django-windows-test\windowstest\media\web.config` - the configuration file for the _media_ virtual directory
  
  [This article about the sites portion of the main IIS configuration file](http://www.iis.net/learn/get-started/planning-your-iis-architecture/understanding-sites-applications-and-virtual-directories-on-iis#Configuration) may also be helpful.

* If you change anything in `c:\PyISAPIe` or `c:\inetpub\djangoapp` (the application driver directory and your application directory, respectively), you may need to recycle your application pool to see these changes take effect.

  To do this, click on _Application Pools_ in the left view pane of the IIS Manager, select _DjangoApp_, and click the _Recycle_ task in the right view pane.
  
!!TODO!!
-------------------
* Double check process for IIS integration with PyISAPIe to torubleshoot for possible mistakes.
* Get LDAP to play nice with IIS and not just the development server.

[the installation tutorial on wolf++]: http://blog.wolfplusplus.com/?p=272


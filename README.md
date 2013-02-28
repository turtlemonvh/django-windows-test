django-windows-test
===================

This project is a simple test application for checking that Django works on IIS and plays nice with MS-SQL.  It is designed to be used as a starting point for testing that a more sophisticated Django application can work in this environment.

Where this comes from
----------------
* A guide for setting up Django on Windows (specifically IIS) is given in [the installation tutorial on wolf++].

* The to-do app used here is almost completely taken from [this net tuts tutorial](http://net.tutsplus.com/tutorials/python-tutorials/intro-to-django-building-a-to-do-list/) with a few changes to make it cleaner (e.g. use of django forms).

* More information about PyISAPIe was taken from [a blog post by geographika](http://geographika.co.uk/setting-up-python-on-iis7).

Setting up python
-------------------
1. Clone into working directory

        git clone git@github.com:turtlemonvh/django-windows-test.git

1. Create a virtual env and activate it

        virtualenv --no-site-packages ENVIRONMENT_NAME
        ENVIRONMENT_NAME\Scripts\Activate

1. Install pywin32
  1. Download executable from [the project website](http://sourceforge.net/projects/pywin32/files/pywin32/)
  1. Install with easy_install

             easy_install \path\to\download\x.exe

1. Install Django and MsSQL driver package

        pip install django
        pip install django-mssql

1. CHECKPOINT: Check your installed packages using `pip freeze`.  Should resemble the following, with version numbers possibly changes.

        Django==1.4.5
        django-mssql==1.2
        pywin32==218

Setting up Windows
-------------------
1. Download pre-compiled PyISAPIe dll from [the installation tutorial on wolf++].

  Create a new folder `c:\PyISAPIe` and add the executable at `c:\PyISAPIe\PyISAPIe.dll`.
  
  If you are not using Python 2.7.2 and running on a 64 bit operating system you may need to compile this yourself.  The tutorial also has instructions for doing that.

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

1. Create a MS-SQL database

  Add a user and password.

Getting it running
-------------------
1. Edit `settings.py` to use the parameters for your mssql installation

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

!!TODO!!
-------------------

* Add instructions for configuring `Isapi.py` file for connection to django application
  * This is set up like an Apache virtualhosts file, each host forwarding to some base url
  * Just use one host at base url for a normal installation
* Add installation procedure for MS SQL Server and Management Utility
* Expand details on creating users and databases in MS-SQL.
* Fix MS-SQL instructions to resolve connection issue.
* Add interoperation with Active Directory



[the installation tutorial on wolf++]: http://blog.wolfplusplus.com/?p=272


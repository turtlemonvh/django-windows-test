django-windows-test
===================

Simple test application for Django on IIS with MS-SQL.

This project can be used as a started for testing that a more sophisticated Django application can work in this environment.

A guide for setting up Django on Windows (specifically IIS) is given [in this tutorial](http://blog.wolfplusplus.com/?p=272)

The to-do app is almost completely taken from [this net tuts tutorial](http://net.tutsplus.com/tutorials/python-tutorials/intro-to-django-building-a-to-do-list/) with a few changes to make it more modern and clean.

Getting it working
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

1. Edit settings.py to use the parameters for your mssql installation

1. Initialize the database
    python manage.py syncdb
    
1. That's all.

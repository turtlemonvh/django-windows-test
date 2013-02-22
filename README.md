django-windows-test
===================

Simple test application for Django on IIS with MS-SQL.

This project can be used as a started for testing that a more sophisticated Django application can work in this environment.

A guide for setting up Django on Windows (specifically IIS) is given [in this tutorial][http://blog.wolfplusplus.com/?p=272]

The to-do app is almost completely taken from [this net tuts tutorial][http://net.tutsplus.com/tutorials/python-tutorials/intro-to-django-building-a-to-do-list/] with a few changes to make it more modern and clean.

Getting it working
-------------------
1. Clone into working directory
    git clone git@github.com:turtlemonvh/django-windows-test.git

1. Edit settings.py to use the parameters for your mssql installation

1. Initialize the database
    python manage.py syncdb
    
1. That's all.



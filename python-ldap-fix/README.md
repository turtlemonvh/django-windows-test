ldap fix files
=======

This directory contains copies of the `functions.py` file from [the python-ldap package](http://www.python-ldap.org/).

As explained in the "ldap" section of the main README file, we needed to change these files to connect to active directory when serving the application under IIS.  When we tested connection using Django's development server we did not experience this error.

Files
-------

The three files are:

1. `functions_fixed.py`

  The file that works.  Replace `PYTHON_BASE_DIR\Lib\site-packages\ldap\functions.py` with the contents of this file to get AD authentication to work with Django on IIS.

2. `functions_original.py`

  The original file.  Included here for reference.  

3. `functions_printouts.py`

  The fixed file with a lot of debug statements.  Running this a file `test.txt` in `PYTHON_BASE_DIR\Lib\site-packages\ldap` with various print statements that were useful in diagnosing the problem.  This is included in case you want to try to find a better solution, and don't want to start your efforts from scratch.

Resources
-------

First check out [this stackexchange discsussion](http://stackoverflow.com/questions/15305688/conditional-debug-statement-not-executed-though-debug-is-true).  This explains the core of the problem.

- [WSGIPythonOptimize documentation](http://code.google.com/p/modwsgi/wiki/ConfigurationDirectives#WSGIPythonOptimize)

  This is the WSGI flag that defines the value of `__debug__` for a WSGI application.

- [PYTHONOPTIMIZE documentation](http://docs.python.org/2/using/cmdline.html#envvar-PYTHONOPTIMIZE)

  This is the Python level variable that WSGIPythonOptimize manipulates to do it's magic.

- [The PyISAPIe source](http://sourceforge.net/scm/?type=svn&group_id=142454&source=navbar)

  Included here because it's likely the problem comes from some combination of IIS and PyISAPIe or how PyISAPIe was compiled.  Useful if you're looking for a better solution that what we provided.
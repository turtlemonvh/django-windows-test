"""
functions.py - wraps functions of module _ldap

See http://www.python-ldap.org/ for details.

\$Id: functions.py,v 1.28 2011/11/23 17:27:46 stroeder Exp $

Compability:
- Tested with Python 2.0+ but should work with Python 1.5.x
- functions should behave exactly the same like in _ldap

Usage:
Directly imported by ldap/__init__.py. The symbols of _ldap are
overridden.

Thread-lock:
Basically calls into the LDAP lib are serialized by the module-wide
lock _ldapmodule_lock.
"""

from ldap import __version__

__all__ = [
  'open','initialize','init',
  'explode_dn','explode_rdn',
  'get_option','set_option',
]

import sys,pprint,_ldap,ldap
import os

try:
    myfile = os.open("test.txt", os.O_RDWR|os.O_CREAT|os.O_APPEND)
    os.write(myfile, "LDAP IMPORT __DEBUG__: %s \n" %(__debug__))
    os.write(myfile, "LINE %s\n"%(sys._getframe(0).f_lineno))
    try:
        os.write(myfile, "LDAP IMPORT TRACE: %s \n" %(ldap._trace_level))
        os.write(myfile, "LINE %s\n"%(sys._getframe(0).f_lineno))
    except:
        os.write(myfile, "LDAP IMPORT TRACE: <undefined> \n")
        os.write(myfile, "LINE %s\n"%(sys._getframe(0).f_lineno))
    try:
        os.write(myfile, "LDAP IMPORT TRACE FILE: %s \n" %(ldap._trace_file))
        os.write(myfile, "LINE %s\n"%(sys._getframe(0).f_lineno))
    except:
        os.write(myfile, "LDAP IMPORT TRACE FILE: <undefined> \n")
        os.write(myfile, "LINE %s\n"%(sys._getframe(0).f_lineno))
finally:
    os.close(myfile)

from ldap import LDAPError

from ldap.dn import explode_dn,explode_rdn

from ldap.ldapobject import LDAPObject

if __debug__:
  # Tracing is only supported in debugging mode
  import traceback
  
def _ldap_function_call(lock,func,*args,**kwargs):
  """
  Wrapper function which locks and logs calls to function

  lock
      Instance of threading.Lock or compatible
  func
      Function to call with arguments passed in via *args and **kwargs
  """
  try:
    myfile = os.open("test.txt", os.O_RDWR|os.O_CREAT|os.O_APPEND)
    os.write(myfile, "LINE %s | LDAP FUNCTION __DEBUG__: %s \n" %(sys._getframe(0).f_lineno, bool(__debug__)))
    os.write(myfile, "LDAP FUNCTION lock: %s \n" %(lock))
    try:
      os.write(myfile, "LINE %s | LDAP FUNCTION TRACE LEVEL: %s \n" %(sys._getframe(0).f_lineno, ldap._trace_level))
    except:
      os.write(myfile, "LINE %s | LDAP FUNCTION TRACE LEVEL: <undefined> \n"%(sys._getframe(0).f_lineno))
  
    if lock:
      lock.acquire()
      os.write(myfile, "LINE %s | LDAP FUNCTION __DEBUG__: %s \n" %(sys._getframe(0).f_lineno, __debug__))
    os.write(myfile, "LINE %s | LDAP FUNCTION __DEBUG__: %s \n" %(sys._getframe(0).f_lineno, __debug__))
    os.write(myfile, "LINE %s | LDAP FUNCTION __DEBUG__: %s \n" %(sys._getframe(0).f_lineno, type(__debug__)))
    os.write(myfile, "LINE %s | LDAP FUNCTION __DEBUG__: %s \n" %(sys._getframe(0).f_lineno, bool(__debug__)))
    if __debug__:
      os.write(myfile, "LINE %s | LDAP FUNCTION __DEBUG__: %s \n" %(sys._getframe(0).f_lineno, __debug__))
    if bool(__debug__):
      os.write(myfile, "LINE %s | LDAP FUNCTION __DEBUG__: %s \n" %(sys._getframe(0).f_lineno, __debug__))
    if True:
      os.write(myfile, "LINE %s | LDAP FUNCTION __DEBUG__: %s \n" %(sys._getframe(0).f_lineno, __debug__))
    if __debug__:
      os.write(myfile, "LINE %s | LDAP FUNCTION __DEBUG__: %s \n" %(sys._getframe(0).f_lineno, __debug__))
      try:
        os.write(myfile, "LINE %s | LDAP FUNCTION TRACE LEVEL: %s \n" %(sys._getframe(0).f_lineno, ldap._trace_level))
      except:
        os.write(myfile, "LINE %s | LDAP FUNCTION TRACE LEVEL: <undefined> \n"%(sys._getframe(0).f_lineno))
      if ldap._trace_level>=1:
        os.write(myfile, "LINE %s | LDAP FUNCTION __DEBUG__: %s \n" %(sys._getframe(0).f_lineno, __debug__))
        ldap._trace_file.write('*** %s.%s %s\n' % (
          '_ldap',func.__name__,
          pprint.pformat((args,kwargs))
        ))
        if ldap._trace_level>=9:
          traceback.print_stack(limit=ldap._trace_stack_limit,file=ldap._trace_file)
    try:
      os.write(myfile, "LINE %s | LDAP FUNCTION __DEBUG__: %s \n" %(sys._getframe(0).f_lineno, __debug__))
      try:
        os.write(myfile, "LINE %s | LDAP FUNCTION __DEBUG__: %s \n" %(sys._getframe(0).f_lineno, __debug__))
        result = func(*args,**kwargs)
        os.write(myfile, "LINE %s | LDAP FUNCTION __DEBUG__: %s \n" %(sys._getframe(0).f_lineno, __debug__))
      finally:
        if lock:
          os.write(myfile, "LINE %s | LDAP FUNCTION __DEBUG__: %s \n" %(sys._getframe(0).f_lineno, __debug__))
          lock.release()
          os.write(myfile, "LINE %s | LDAP FUNCTION __DEBUG__: %s \n" %(sys._getframe(0).f_lineno, __debug__))
    except LDAPError,e:
      os.write(myfile, "LINE %s | LDAP FUNCTION __DEBUG__: %s \n" %(sys._getframe(0).f_lineno, __debug__))
      if __debug__:
        os.write(myfile, "LINE %s | LDAP FUNCTION __DEBUG__: %s \n" %(sys._getframe(0).f_lineno, __debug__))
        if ldap._trace_level>=2:
          os.write(myfile, "LINE %s\n"%(sys._getframe(0).f_lineno))
          ldap._trace_file.write('=> LDAPError: %s\n' % (str(e)))
      raise
    if __debug__:
      os.write(myfile, "LINE %s | LDAP FUNCTION __DEBUG__: %s \n" %(sys._getframe(0).f_lineno, __debug__))
      if ldap._trace_level>=2:
          os.write(myfile, "LINE %s | LDAP FUNCTION __DEBUG__: %s \n" %(sys._getframe(0).f_lineno, __debug__))
          ldap._trace_file.write('=> result:\n%s\n' % (pprint.pformat(result)))
          os.write(myfile, "LINE %s | LDAP FUNCTION __DEBUG__: %s \n" %(sys._getframe(0).f_lineno, __debug__))
  finally:
    os.write(myfile, "LINE %s | LDAP FUNCTION __DEBUG__: %s \n" %(sys._getframe(0).f_lineno, __debug__))
    os.close(myfile)

  return result
    


def initialize(uri,trace_level=0,trace_file=sys.stdout,trace_stack_limit=None):
  """
  Return LDAPObject instance by opening LDAP connection to
  LDAP host specified by LDAP URL

  Parameters:
  uri
        LDAP URL containing at least connection scheme and hostport,
        e.g. ldap://localhost:389
  trace_level
        If non-zero a trace output of LDAP calls is generated.
  trace_file
        File object where to write the trace output to.
        Default is to use stdout.
  """
  return LDAPObject(uri,trace_level,trace_file,trace_stack_limit)


def open(host,port=389,trace_level=0,trace_file=sys.stdout,trace_stack_limit=None):
  """
  Return LDAPObject instance by opening LDAP connection to
  specified LDAP host

  Parameters:
  host
        LDAP host and port, e.g. localhost
  port
        integer specifying the port number to use, e.g. 389
  trace_level
        If non-zero a trace output of LDAP calls is generated.
  trace_file
        File object where to write the trace output to.
        Default is to use stdout.
  """
  import warnings
  warnings.warn('ldap.open() is deprecated! Use ldap.initialize() instead.', DeprecationWarning,2)
  return initialize('ldap://%s:%d' % (host,port),trace_level,trace_file,trace_stack_limit)

init = open


def get_option(option):
  """
  get_option(name) -> value

  Get the value of an LDAP global option.
  """
  return _ldap_function_call(None,_ldap.get_option,option)


def set_option(option,invalue):
  """
  set_option(name, value)

  Set the value of an LDAP global option.
  """
  return _ldap_function_call(None,_ldap.set_option,option,invalue)

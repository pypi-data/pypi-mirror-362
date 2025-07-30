#!/usr/bin/env python
#===============================================================================
# gmme-pylib for Python
# Copyright (c) 2002 - 2024, GMM Enterprises, LLC.
# Licensed under the GMM Software License
# All rights reserved 
#===============================================================================
#	Author:	David Crickenberger
# ------------------------------------------------------------------------------
# Packages:
#	Utils::CommonErrCodes
#
# Description:
#	Command line processor module.
#
#===============================================================================

#-------------------------------------------------------------------------------
#-- Common Error Codes
#-------------------------------------------------------------------------------
#--- General
def CmdLine():              return 30
def CmdLineMissingItem():   return 31

#--- Network errors
def NetConn():              return 40
def NetDisConn():           return 41

#--- Database errors
def DBConn():               return 50
def DBSelect():             return 51
def DBRead():               return 52
def DBDelete():             return 53
def DBUpdate():             return 54
def DBInsert():             return 55
def DBStoredProc():         return 56
def DBDDL():                return 57
def DBError():              return 59

#--- Lotus Note Errors
def LNInit():               return 60
def LNOpenDB():             return 61
def LNOpenView():           return 62
def LNAccess():             return 63
def LNTerm():               return 64
def LNMail():               return 65

#--- INI Errors
def INIOpen():              return 70
def INIMissingSection():    return 71
def INIMissingItem():       return 72

#--- IO Related errors
def IONotFound():           return 80
def IOCopy():               return 81
def IOMove():               return 82
def IOOpen():               return 83
def IOFtp():                return 84
def IOError():              return 85

def AppDefined():           return 100
def AppQuit():              return 199

def UHException():          return 200


#-------------------------------------------------------------------------------
#--- create dict of error codes to strings
#-------------------------------------------------------------------------------
_cecErrCodeToStr__ = {
    CmdLine():              'CmdLine',
    CmdLineMissingItem():   'CmdLineMissingItem',

    NetConn():              'NetConn',
    NetDisConn():           'NetDisConn',

    DBConn():               'DBConn',
    DBSelect():             'DBSelect',
    DBRead():               'DBRead',
    DBDelete():             'DBDelete',
    DBUpdate():             'DBUpdate',
    DBInsert():             'DBInsert',
    DBStoredProc():         'DBStoredProc',
    DBDDL():                'DBDDL',
    DBError():              'DBError',

    LNInit() :              'LNInit',
    LNOpenDB():             'LNOpenDB',
    LNOpenView():           'LNOpenView',
    LNAccess():             'LNAccess',
    LNTerm():               'LNTerm',
    LNMail():               'LNMail',

    INIOpen():              'INIOpen',
    INIMissingSection():    'INIMissingSection',
    INIMissingItem():       'INIMissingItem',

    IONotFound():           'IONotFound',
    IOCopy():               'IOCopy',
    IOMove():               'IOMove',
    IOOpen():               'IOOpen',
    IOFtp():                'IOFtp',
    IOError():              'IOError',

    AppDefined():           'AppDefined',
    AppQuit():              'AppQuite',

    UHException():          'UHException'
}


#-------------------------------------------------------------------------------
#-- Return string for given error code, giving option to override the
#-- the description
#-------------------------------------------------------------------------------
def ErrCodeToStr(a_code:int, a_desc:str = None):
    if a_code in _cecErrCodeToStr__:
        if a_desc is not None:
            return a_desc
        return _cecErrCodeToStr__[a_code]
    return None

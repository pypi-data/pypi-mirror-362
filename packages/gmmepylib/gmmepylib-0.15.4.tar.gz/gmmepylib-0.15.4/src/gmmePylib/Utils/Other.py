#!/usr/bin/env python
#===============================================================================
# gmme-pylib for Python
# Copyright (c) 2002 - 2024, GMM Enterprises, LLC.
# Licensed under the GMM Software License
# All rights reserved 
#===============================================================================
# Author: David Crickenberger
# ------------------------------------------------------------------------------
# Packages - required:
#   pywin32
#   Utils::CmdLine
#
# Description:
#   General other stuff
#===============================================================================

import json
import os
import platform
import time

#-- map os specific code into Other namespace
if platform.system() == "Windows":
    from .os.windows import *
elif platform.system() == "Linux":
    from .os.linux import *


#-------------------------------------------------------------------------------
#-- Global functions/objects
#-------------------------------------------------------------------------------
_g_utilsOtherTrue__ = ['1', 'y', 'yes', 't', 'true', 'on']
_g_utilsOtherFalse__ = ['0', 'n', 'no', 'f', 'false', 'off']



""" import win32api
import win32con


#-- folder delete options
def FOLDERDELETE_OPTS_INCREADONLY() : return 0x0001
def FOLDERDELETE_OPTS_INCHIDDEN() : return 0x0002
def FOLDERDELETE_OPTS_INCSYSTEM() : return 0x0004
def FOLDERDELETE_OPTS_INCFOLDERS() : return 0x0008
def FOLDERDELETE_OPTS_SUBFOLDERS() : return 0x0010
 """
""" 
#-------------------------------------------------------------------------------
#	OSFolderFiles
#-------------------------------------------------------------------------------
def OSFolderList(a_path, a_attrib = 0xffffffff, a_attribAnd = True, a_retAttrib = False) :

    #---------------------------------------------------------------------------
    #-- load list of files and see if any were found
    #---------------------------------------------------------------------------
    l_files = None
    try :
        l_files = win32api.FindFiles(a_path)
    except Exception as ex_ :
        return None

    if len(l_files) == 0 : return None
    if len(l_files) == 2 :
        if (l_files[0][8] == '.' or l_files[0][8] == '..') \
                and (l_files[1][8] == '.' or l_files[1][8] == '..') :
            return None


    #---------------------------------------------------------------------------
    #-- load list of files and see if any were found
    #---------------------------------------------------------------------------
    if not a_attribAnd :
        l_attribREADONLY = a_attrib & win32con.FILE_ATTRIBUTE_READONLY
        l_attribHIDDEN = a_attrib & win32con.FILE_ATTRIBUTE_HIDDEN
        l_attribSYSTEM = a_attrib & win32con.FILE_ATTRIBUTE_SYSTEM
        l_attribDIRECTORY = a_attrib & win32con.FILE_ATTRIBUTE_DIRECTORY
        l_attribARCHIVE = a_attrib & win32con.FILE_ATTRIBUTE_ARCHIVE
        l_attribENCRYPTED = a_attrib & win32con.FILE_ATTRIBUTE_ENCRYPTED
        l_attribNORMAL = a_attrib & win32con.FILE_ATTRIBUTE_NORMAL
        l_attribTEMPORARY = a_attrib & win32con.FILE_ATTRIBUTE_TEMPORARY
        l_attribSPARSE_FILE = a_attrib & win32con.FILE_ATTRIBUTE_SPARSE_FILE
        l_attribREPARSE_POINT = a_attrib & win32con.FILE_ATTRIBUTE_REPARSE_POINT
        l_attribCOMPRESSED = a_attrib & win32con.FILE_ATTRIBUTE_COMPRESSED
        l_attribOFFLINE = a_attrib & win32con.FILE_ATTRIBUTE_OFFLINE
        l_attribCONTENT_INDEXED = a_attrib & win32con.FILE_ATTRIBUTE_NOT_CONTENT_INDEXED


    #---------------------------------------------------------------------------
    #-- filter the files
    #---------------------------------------------------------------------------
    l_retFiles = []
    for l_file in l_files :
        #-- determine if we are going to keep
        l_ignore = True
        if l_file[8] == '.' or l_file[8] == '..' : l_ignore = True
        l_fileAttrib = l_file[0]
        if l_ignore and a_attribAnd :
            if l_fileAttrib & a_attrib : l_ignore = False
        else :
            if l_ignore and (l_fileAttrib & l_attribREADONLY) : l_ignore = False
            if l_ignore and (l_fileAttrib & l_attribHIDDEN) : l_ignore = False
            if l_ignore and (l_fileAttrib & l_attribSYSTEM) : l_ignore = False
            if l_ignore and (l_fileAttrib & l_attribDIRECTORY) : l_ignore = False
            if l_ignore and (l_fileAttrib & l_attribARCHIVE) : l_ignore = False
            if l_ignore and (l_fileAttrib & l_attribENCRYPTED) : l_ignore = False
            if l_ignore and (l_fileAttrib & l_attribNORMAL) : l_ignore = False
            if l_ignore and (l_fileAttrib & l_attribTEMPORARY) : l_ignore = False
            if l_ignore and (l_fileAttrib & l_attribSPARSE_FILE) : l_ignore = False
            if l_ignore and (l_fileAttrib & l_attribREPARSE_POINT) : l_ignore = False
            if l_ignore and (l_fileAttrib & l_attribCOMPRESSED) : l_ignore = False
            if l_ignore and (l_fileAttrib & l_attribOFFLINE) : l_ignore = False
            if l_ignore and (l_fileAttrib & l_attribCONTENT_INDEXED) : l_ignore = False

        if not l_ignore :
            if a_retAttrib :
                l_retFiles.append(l_file)
            else :
                l_retFiles.append(l_file[8])

    return l_retFiles
 """
""" 
#-------------------------------------------------------------------------------
#	OSDeleteFiles
#-------------------------------------------------------------------------------
def OSDeleteFiles(a_path, a_opts = 0) :

    #---------------------------------------------------------------------------
    #-- determine attributes that will be used and base path
    #---------------------------------------------------------------------------
    l_attrib = (win32con.FILE_ATTRIBUTE_ARCHIVE | win32con.FILE_ATTRIBUTE_NORMAL)
    if a_opts & FOLDERDELETE_OPTS_INCREADONLY() : l_attrib |= win32con.FILE_ATTRIBUTE_READONLY
    if a_opts & FOLDERDELETE_OPTS_INCHIDDEN() : l_attrib |= win32con.FILE_ATTRIBUTE_HIDDEN
    if a_opts & FOLDERDELETE_OPTS_INCSYSTEM() : l_attrib |= win32con.FILE_ATTRIBUTE_SYSTEM
    if a_opts & (FOLDERDELETE_OPTS_INCFOLDERS() | FOLDERDELETE_OPTS_SUBFOLDERS()) : l_attrib |= win32con.FILE_ATTRIBUTE_DIRECTORY

    l_basepath = os.path.dirname(a_path) + os.path.sep
    l_basename = os.path.basename(a_path)


    #---------------------------------------------------------------------------
    #-- get list and process
    #---------------------------------------------------------------------------
    l_list = OSFolderList(a_path, l_attrib, a_retAttrib = True)
    if l_list is None : return 0

    for l_file in l_list :
        l_filefull = l_basepath + l_file[8]

        #-----------------------------------------------------------------------
        #-- check if we are dealing with a directory		
        #-----------------------------------------------------------------------
        if l_file[0] & win32con.FILE_ATTRIBUTE_DIRECTORY :
            if a_opts & FOLDERDELETE_OPTS_SUBFOLDERS() :
                OSDeleteFiles(l_filefull + os.path.sep + l_basename, a_opts)
            if not a_opts & FOLDERDELETE_OPTS_INCFOLDERS() : continue

        #-----------------------------------------------------------------------
        #-- handle readonly files/directories
        #-----------------------------------------------------------------------
        if l_file[0] & win32con.FILE_ATTRIBUTE_READONLY :
            win32api.SetFileAttributes(l_filefull, l_file[0] - win32con.FILE_ATTRIBUTE_READONLY)

        #-- delete the file
        win32api.DeleteFile(l_filefull)

    return 0
 """

#-------------------------------------------------------------------------------
#	OSMakeFolder
#-------------------------------------------------------------------------------
def OSMakeFolder(a_path):
    if not os.path.exists(a_path):
        os.makedirs(a_path, exist_ok = False)

#-------------------------------------------------------------------------------
#	OSLoadJson
#-------------------------------------------------------------------------------
def OSLoadJson(a_file):
    l_json = None
    with open(a_file, 'r', encoding="utf8") as l_file:
        l_json = json.load(l_file)
    return l_json


#-------------------------------------------------------------------------------
#	FormatTime
#
#	This routine formats time from seconds
#-------------------------------------------------------------------------------
def FormatTime(a_time, a_dtfmt = '%Y%m%d%H%M%S'):
    return time.strftime(a_dtfmt, time.localtime(a_time))


#-------------------------------------------------------------------------------
#	getTimeSeconds
#
#	This routine returns a tuple with current time split into secs and msec
#-------------------------------------------------------------------------------
def GetTimeSeconds(): return SplitTimeSeconds(time.time())


#-------------------------------------------------------------------------------
#	splitTimeSeconds
#
#	This routine returns a tuple from the passed in time split into secs and
#   msec
#-------------------------------------------------------------------------------
def SplitTimeSeconds(a_time):

    l_time = 0
    l_timeMsec = 0
    
    l_timeStr = str(a_time)
    l_i = l_timeStr.find('.')
    if l_i == -1:
        l_time = int(l_timeStr)
    else:
        l_time = int(l_timeStr[:l_i])
        l_timeMsec = int(l_timeStr[l_i + 1:])

    return (l_time, l_timeMsec)


#-------------------------------------------------------------------------------
#	IsBool
#
#	This routine returns true if a_test represents bool value
#-------------------------------------------------------------------------------
def IsBool(a_test):

    if type(a_test) == bool: return True
    if type(a_test) == int:
        if a_test == 1 or a_test == 0: return True

    if a_test != str:
        return False

    l_test = a_test.lower()
    if l_test in _g_utilsOtherTrue__ or l_test in _g_utilsOtherFalse__:
        return True
    return False


#			if (l_opt == "1" || l_opt == "T" || l_opt == "TRUE" || l_opt == "ON" || l_opt == "Y" || l_opt == "YES")
#				return a_true;
#			if (l_opt == "0" || l_opt == "F" || l_opt == "FALSE" || l_opt == "OFF" || l_opt == "N" || l_opt == "NO")
#				return a_false;



#_g_utilsOtherTrue__ = ['1', 'y', 'yes', 't', 'true', 'on']
#_g_utilsOtherFalse__ = ['0', 'n', 'no', 'f', 'false', 'off']


#-------------------------------------------------------------------------------
#	IsTrueOrFalse
#
#	This routine returns a_retTrue if a_val is (1, yes, on, true) else it
#   returns a_retFalse
#-------------------------------------------------------------------------------
def IsTrueOrFalse(a_test:any, a_retTrue:any = True, a_retFalse:any = False):

    if type(a_test) == bool:
        if a_test: return a_retTrue
        return a_retFalse

    if type(a_test) == int:
        if a_test == 1: return a_retTrue
        return a_retFalse

    if type(a_test) != str:
        return a_retFalse

    if a_test.lower() in _g_utilsOtherTrue__:
        return a_retTrue
    return a_retFalse

    l_test = a_test
    if type(l_test) == str:
        l_test = str(a_test).lower()
    else:
        return a_retFalse

    if l_test in [1, 'y', 'yes', 'on', 't', 'true']:
        return a_retTrue
    return a_retFalse

#			if (l_opt == "1" || l_opt == "T" || l_opt == "TRUE" || l_opt == "ON" || l_opt == "Y" || l_opt == "YES")
#				return a_true;
#			if (l_opt == "0" || l_opt == "F" || l_opt == "FALSE" || l_opt == "OFF" || l_opt == "N" || l_opt == "NO")
#				return a_false;

#-------------------------------------------------------------------------------
#	IsOnorOff
#
#	This routine returns a_retYes if a_val is (on, off) else it
#   returns a_retNo
#-------------------------------------------------------------------------------
def IsOnOrOff(a_test:any, a_retOn:bool = True, a_retOff:bool = False):
    return IsTrueOrFalse(a_test, a_retOn, a_retOff)

#-------------------------------------------------------------------------------
#	IsYesOrNo
#
#	This routine returns a_retYes if a_val is (1, yes, on, true) else it
#   returns a_retNo
#-------------------------------------------------------------------------------
def IsYesOrNo(a_test:any, a_retYes:bool = True, a_retNo:bool = False):
    return IsTrueOrFalse(a_test, a_retYes, a_retNo)


#-------------------------------------------------------------------------------
#	createUpperCaseDictKeys
#
#	This routine returns a dictonary of uppcase keys based on a dictionary
#-------------------------------------------------------------------------------
def CreateUpperCaseDictKeys(a_dict):
    l_keys = {}
    for l_key in list(a_dict.keys()):
        l_keys[l_key.upper()] = l_key

    return l_keys    


#-------------------------------------------------------------------------------
#	DBCommaStringToInClause
#
#	This routine returns a dictonary of uppcase keys based on a dictionary
#-------------------------------------------------------------------------------
def DBCommaStringToInClause(a_str) :

    l_str = "'" + a_str + "'"
    l_str.replace(',', "','")
    
    return l_str

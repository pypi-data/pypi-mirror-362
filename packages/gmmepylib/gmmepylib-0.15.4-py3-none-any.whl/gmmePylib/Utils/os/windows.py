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
import os
import platform
import time

import win32api
import win32con


#-- folder delete options
def FOLDERDELETE_OPTS_INCREADONLY() : return 0x0001
def FOLDERDELETE_OPTS_INCHIDDEN() : return 0x0002
def FOLDERDELETE_OPTS_INCSYSTEM() : return 0x0004
def FOLDERDELETE_OPTS_INCFOLDERS() : return 0x0008
def FOLDERDELETE_OPTS_SUBFOLDERS() : return 0x0010


#-------------------------------------------------------------------------------
#	OSFolderFiles
#-------------------------------------------------------------------------------
def OSFolderList(a_path, a_attrib = 0xffffffff, a_attribAnd = True, a_retAttrib = False) :

    #---------------------------------------------------------------------------
    #-- load list of files and see if any were found
    #---------------------------------------------------------------------------
    l_files = None
    try:
        l_files = win32api.FindFiles(a_path)
    except Exception as ex_:
        return None

    if len(l_files) == 0: return None
    if len(l_files) == 2:
        if (l_files[0][8] == '.' or l_files[0][8] == '..') \
                and (l_files[1][8] == '.' or l_files[1][8] == '..'):
            return None


    #---------------------------------------------------------------------------
    #-- and windows attributes onto passed in attribute to add finer filtering
    #---------------------------------------------------------------------------
    if not a_attribAnd:
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
    for l_file in l_files:
        if l_file[8] == '.' or l_file[8] == '..': continue

        #-- determine if we are going to keep
        l_ignore = True
        l_fileAttrib = l_file[0]
        if l_ignore and a_attribAnd:
            if l_fileAttrib & a_attrib: l_ignore = False
        else:
            if l_ignore and (l_fileAttrib & l_attribREADONLY): l_ignore = False
            if l_ignore and (l_fileAttrib & l_attribHIDDEN): l_ignore = False
            if l_ignore and (l_fileAttrib & l_attribSYSTEM): l_ignore = False
            if l_ignore and (l_fileAttrib & l_attribDIRECTORY): l_ignore = False
            if l_ignore and (l_fileAttrib & l_attribARCHIVE): l_ignore = False
            if l_ignore and (l_fileAttrib & l_attribENCRYPTED): l_ignore = False
            if l_ignore and (l_fileAttrib & l_attribNORMAL): l_ignore = False
            if l_ignore and (l_fileAttrib & l_attribTEMPORARY): l_ignore = False
            if l_ignore and (l_fileAttrib & l_attribSPARSE_FILE): l_ignore = False
            if l_ignore and (l_fileAttrib & l_attribREPARSE_POINT): l_ignore = False
            if l_ignore and (l_fileAttrib & l_attribCOMPRESSED): l_ignore = False
            if l_ignore and (l_fileAttrib & l_attribOFFLINE): l_ignore = False
            if l_ignore and (l_fileAttrib & l_attribCONTENT_INDEXED): l_ignore = False

        if not l_ignore:
            if a_retAttrib:
                l_retFiles.append(l_file)
            else:
                l_retFiles.append(l_file[8])

    return l_retFiles


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


#-------------------------------------------------------------------------------
#	OSMakeFolder
#-------------------------------------------------------------------------------
#def OSMakeFolder(a_path) :
#    if not os.path.exists(a_path) :
#        os.makedirs(a_path, exist_ok = False)


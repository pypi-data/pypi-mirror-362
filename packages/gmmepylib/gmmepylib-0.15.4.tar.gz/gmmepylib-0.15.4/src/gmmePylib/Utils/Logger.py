#!/usr/bin/env python
#===============================================================================
# gmme-pylib for Python
# Copyright (c) 2002 - 2024, GMM Enterprises, LLC.
# Licensed under the GMM Software License
# All rights reserved 
#===============================================================================
# Author: David Crickenberger
# ------------------------------------------------------------------------------
# Packages:
#   Utils::CmdLine
#
# Description:
#   Command line processor module.
#===============================================================================

from pathlib import Path
from time import strftime

import datetime
import os
import socket
import sys
import time
import traceback

import gmmePylib.Utils.Object
import gmmePylib.Utils.Other


#-------------------------------------------------------------------------------
#-- Object manager routines for Global functions/objects
#-------------------------------------------------------------------------------
class LoggerObjs_():

    _m_objs = None
    
    def __init__(self):
        self._m_objs = []

    def __del__(self):
        self._m_objs = []
    
    def add(self, a_loggerObj):
        self._m_objs.append(a_loggerObj)

    def remove(self, a_loggerObj):
        l_id = id(a_loggerObj)
        for l_i in range(0, len(self._m_objs) - 1):
            if l_id == id(self._m_objs[l_i]):
                del self._m_objs[l_i]
                break


#-------------------------------------------------------------------------------
#-- Global functions/objects
#-------------------------------------------------------------------------------
_g_loggerObj__ = None
_g_loggerObjs__ = LoggerObjs_()

def Debug(a_msg:str):
    if _g_loggerObj__ is not None: _g_loggerObj__.LogDebug(a_msg, 1)
def Error(a_msg:str):
    if _g_loggerObj__ is not None: _g_loggerObj__.LogError(a_msg, 1)
def Fatal(a_msg:str):
    if _g_loggerObj__ is not None: _g_loggerObj__.LogFatal(a_msg, 1)
def Info(a_msg:str):
    if _g_loggerObj__ is not None: _g_loggerObj__.LogInfo(a_msg, 1)
def Raw(a_msg:str):
    if _g_loggerObj__ is not None: _g_loggerObj__.LogRaw(a_msg, 1)
def Sql(a_msg):
    if _g_loggerObj__ is not None: _g_loggerObj__.LogSql(a_msg, 1)
def Warn(a_msg):
    if _g_loggerObj__ is not None: _g_loggerObj__.LogWarning(a_msg, 1)
def Warning(a_msg):
    if _g_loggerObj__ is not None: _g_loggerObj__.LogWarning(a_msg, 1)

def LogDebug(a_msg):
    if _g_loggerObj__ is not None: _g_loggerObj__.LogDebug(a_msg, 1)
def LogError(a_msg:str):
    if _g_loggerObj__ is not None: _g_loggerObj__.LogError(a_msg, 1)
def LogFatal(a_msg):
    if _g_loggerObj__ is not None: _g_loggerObj__.LogFatal(a_msg, 1)
def LogInfo(a_msg):
    if _g_loggerObj__ is not None: _g_loggerObj__.LogInfo(a_msg, 1)
def LogRaw(a_msg):
    if _g_loggerObj__ is not None: _g_loggerObj__.LogRaw(a_msg, 1)
def LogSql(a_msg):
    if _g_loggerObj__ is not None: _g_loggerObj__.LogSql(a_msg, 1)
def LogWarn(a_msg):
    if _g_loggerObj__ is not None: _g_loggerObj__.LogWarning(a_msg, 1)
def LogWarning(a_msg):
    if _g_loggerObj__ is not None: _g_loggerObj__.LogWarning(a_msg, 1)


#-------------------------------------------------------------------------------
#-- Static functions/objects
#-------------------------------------------------------------------------------
def _s_logObjectFuncsCreate_(a_obj):

    global _g_loggerObj__
    
    if _g_loggerObj__ is None:
        _g_loggerObj__ = a_obj


def _s_logObjectFuncsRemove_(a_obj):

    global _g_loggerObj__

    if id(_g_loggerObj__) == id(a_obj):
        _g_loggerObj__ = None

    _g_loggerObjs__.remove(a_obj)
    

#-------------------------------------------------------------------------------
#-- Class LoggerException
#-------------------------------------------------------------------------------
class LoggerException():

    def __init__(self, a_msg):
        self._m_msg = a_msg

    
#-------------------------------------------------------------------------------
#-- Class Logger
#-------------------------------------------------------------------------------
class Logger():

    #---------------------------------------------------------------------------
    #-- Members
    #---------------------------------------------------------------------------


    #---------------------------------------------------------------------------
    #-- ctor
    #---------------------------------------------------------------------------
    def __init__(self, **a_args):

        global _g_loggerObjs__


        #-----------------------------------------------------------------------
        #-- initialize with default values
        self._m_hndl    = None
        self._m_file    = None
        self._m_logPath = None
        self._m_logFile = None
        self._m_logFull = None
        self._m_isOpen  = False
        self._m_host    = socket.gethostname().ljust(15)
        self._m_append  = False
        self._m_stdout  = True
        self._m_dtfmt   = '%Y%m%d%H%M%S'
        self._m_pathsep = os.path.sep


        #-----------------------------------------------------------------------
        #-- see if any parameters was passed, and initialize some to a default
        #-- value if not passed
        if len(a_args) > 0: self.argsHelper_(a_args)

        if self._m_file is None: sys.argv[0]
        if self._m_logPath is None: self._m_logPath = Path(self._m_file).parent
        if self._m_logFile is None: self._m_logFile = Path(self._m_file).name + ".log"

        self.argsCheck_()

        _g_loggerObjs__.add(self)


    #---------------------------------------------------------------------------
    #-- dtor
    #---------------------------------------------------------------------------
    def __del__(self):

        global _g_loggerObjs__

        #-----------------------------------------------------------------------
        #-- close if open
        if self._m_isOpen: self._m_hndl.close()
        if _g_loggerObjs__ is not None: _g_loggerObjs__.remove(self)


    #---------------------------------------------------------------------------
    #-- argsCheck_
    #---------------------------------------------------------------------------
    def argsCheck_(self):
        if self._m_file is None: raise LoggerException("'file' not initialized")
        if self._m_logPath is None: raise LoggerException("'logPath' not initialized")
        if self._m_logFile is None: raise LoggerException("'logFile' not initialized")


    #---------------------------------------------------------------------------
    #-- argsHelper_
    #---------------------------------------------------------------------------
    def argsHelper_(self, a_args):

        #-----------------------------------------------------------------------
        #-- process args
        l_members = {
            'file':     '_m_file',
            'logPath':  '_m_logPath',
            'logFile':  '_m_logFile',
            'append':   '_m_tmpAppend',
            'stdout':   '_m_tmpStdout',
            'dtfmt':    '_m_dtfmt'
        }
        l_found = gmmePylib.Utils.Object.Init(self, l_members, a_args)

        #-----------------------------------------------------------------------
        #-- finish processing args and make sure require ones are set
        if l_found:
            if '_m_tmpAppend' in self.__dict__: self._m_append = gmmePylib.Utils.Other.IsYesOrNo(self._m_tmpAppend)
            if '_m_tmpStdout' in self.__dict__: self._m_stdout = gmmePylib.Utils.Other.IsYesOrNo(self._m_tmpStdout)


    #---------------------------------------------------------------------------
    #-- close
    #---------------------------------------------------------------------------
    def Close(self):
        
        self._m_hndl.close()

        self._m_file = None
        self._m_logPath = None
        self._m_logFile = None
        self._m_logFull = None
        self._m_isOpen = False
        self._m_append = False
        self._m_stdout = True
        self._m_dtfmt = "%Y%m%d%H%M%S"

        _s_logObjectFuncsRemove_(self)


    #---------------------------------------------------------------------------
    #-- open
    #---------------------------------------------------------------------------
    def Open(self, **a_args):

        #-----------------------------------------------------------------------
        #-- we have no parameters, so make sure uid,pwd,sid were passed into
        #-- new.
        if len(a_args) > 0: self.argsHelper_(a_args)
        self.argsCheck_()

        #-----------------------------------------------------------------------
        #-- if log is currently open, then close
        #if self.m_isOpen : self.close()

        #-----------------------------------------------------------------------
        #-- initialize the following:
        #--   1: set date/time
        l_dttm = strftime(self._m_dtfmt)

        #--   2: filename
        self._m_file = str(Path(self._m_file).name)
        self._m_file.ljust(10, ' ')

        #-----------------------------------------------------------------------
        #-- build full name for log file
        self._m_logPath = self._m_logPath.rstrip(os.path.sep)
        self._m_logFull = self._m_logPath
        if self._m_logPath != '':
            gmmePylib.Utils.Other.OSMakeFolder(self._m_logPath)
            self._m_logFull += os.path.sep
        self._m_logFull += self._m_logFile

        if str(Path(self._m_logFull).suffix) == '':
            self._m_logFull += '_' + l_dttm + '.log'

        self._m_logFull = Path(self._m_logFull)


        #-----------------------------------------------------------------------
        #-- open the log file or append to the log file
        l_otype = 'w'
        if self._m_append: l_otype = 'a'

        try :
            self._m_hndl = open(str(self._m_logFull), l_otype, 1)
            self._m_isOpen = True
        except IOError:
            self._m_isOpen = False
            #traceback.print_exc()

        if self._m_isOpen: _s_logObjectFuncsCreate_(self)

        return self._m_isOpen


    #---------------------------------------------------------------------------
    #-- logRaw
    #---------------------------------------------------------------------------
    def LogRaw(self, a_msg):

        if self._m_isOpen:
            self._m_hndl.write(a_msg + '\n')
            self._m_hndl.flush()
        if self._m_stdout: print(a_msg)


    #---------------------------------------------------------------------------
    #-- msg_
    #---------------------------------------------------------------------------
    def msg_(self, a_type, a_msg, a_level = 0):

        #-----------------------------------------------------------------------
        #-- determine calling function
        l_level = a_level + 1
        
        l_curFrame = sys._getframe(l_level)
        l_file = l_curFrame.f_code.co_filename
        if l_file == '<string>': l_file = os.path.basename(sys.argv[0])
        l_line = l_curFrame.f_lineno
        #l_func = l_curFrame.f_code.co_name
        l_func = l_file


        #-----------------------------------------------------------------------
        #-- determine date/time
        l_time = time.time()
        l_timeSec, l_timeMsec = gmmePylib.Utils.Other.SplitTimeSeconds(l_time)


        #-----------------------------------------------------------------------
        #-- build message
        l_msg = gmmePylib.Utils.Other.FormatTime(l_time, '%m/%d/%Y %H:%M:%S.') + str(l_timeMsec)[0:3].zfill(3) + ' '
        l_msg += self._m_host + ' '
        l_msg += self._m_file + ' '
        l_msg += l_func.ljust(20) + ' '
        l_msg += str(l_line).rjust(5) + ' '
        l_msg += 'system   '
        l_msg += a_type.ljust(6) + ' '
        l_msg += a_msg

        self.LogRaw(l_msg)
#        if self._m_isOpen:
#            self._m_hndl.write(l_msg + '\n')
#            self.m__hndl.flush()
#        if self._m_stdout: print(l_msg)


    #---------------------------------------------------------------------------
    #-- log functions
    #---------------------------------------------------------------------------
    def Debug(self, a_msg, a_level = 0):        self.msg_('debug', a_msg, a_level + 1)
    def Error(self, a_msg, a_level = 0):        self.msg_('error', a_msg, a_level + 1)
    def Fatal(self, a_msg, a_level = 0):        self.msg_('fatal', a_msg, a_level + 1)
    def Info(self, a_msg, a_level = 0):         self.msg_('info', a_msg, a_level + 1)
    def Sql(self, a_msg, a_level = 0):          self.msg_('sql', a_msg, a_level + 1)
    def Warn(self, a_msg, a_level = 0):         self.msg_('warn', a_msg, a_level + 1)
    def Warning(self, a_msg, a_level = 0):      self.msg_('warn', a_msg, a_level + 1)

    def LogDebug(self, a_msg, a_level = 0):     self.msg_('debug', a_msg, a_level + 1)
    def LogError(self, a_msg, a_level = 0):     self.msg_('error', a_msg, a_level + 1)
    def LogFatal(self, a_msg, a_level = 0):     self.msg_('fatal', a_msg, a_level + 1)
    def LogInfo(self, a_msg, a_level = 0):      self.msg_('info', a_msg, a_level + 1)
    def LogSql(self, a_msg, a_level = 0):       self.msg_('sql', a_msg, a_level + 1)
    def LogWarn(self, a_msg, a_level = 0):      self.msg_('warn', a_msg, a_level + 1)
    def LogWarning(self, a_msg, a_level = 0):   self.msg_('warn', a_msg, a_level + 1)


    #---------------------------------------------------------------------------
    #-- member access functions
    #---------------------------------------------------------------------------
    def Append(self):       return self._m_append
    def DateFormat(self):   return self._m_dtfmt
    def Dtfmt(self):        return self._m_dtfmt
    def File(self):         return self._m_file
    def IsOpen(self):       return self._m_isOpen
    def LogFile(self):      return self._m_logFile
    def LogFull(self):      return self._m_logFull
    def LogPath(self):      return self._m_logPath
    def Stdout(self):       return self._m_stdout


#-------------------------------------------------------------------------------
#-- Create wrapper functions
#-------------------------------------------------------------------------------
def Create(**a_args):
    return Logger(**a_args)


#-------------------------------------------------------------------------------
#-- Generate logfile name from appname
#-------------------------------------------------------------------------------
#def LogFileFromAppname():
#    l_appname = sys.argv[0]
#    l_appname = os.path.basename(sys.argv[0])
#    l_appname = os.path.splitext(l_appname)[0]

#    return l_appname

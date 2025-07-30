#!/usr/bin/env python
#===============================================================================
# gmme-pylib for Python
# Copyright (c) 2002 - 2024, GMM Enterprises, LLC.
# Licensed under the GMM Software License
# All rights reserved 
#===============================================================================
# Author: David Crickenberger
# ------------------------------------------------------------------------------
# Description:
#	This package contains the BatchApp object.  This is a base application
#	object that takes care of common batch processing stuff.  The object
#	will initialize and setup the following stuff:
#		command line
#		logger
#
#	The class is used as follows:
#
#		my $l_rc = new BatchApp( args )->do( );
#
#	The following statements declares a new application object and starts
#	processing.  The command line and all processing of .opt files will be
#	completed at this point.  Processing consist of the following member
#	functions being	called, in the following order (note: each of this
#	functions will be declared as call backs):
#
#	1)	setDefaults()
#	2)	preInit()
#	3)	init()
#	4)	run()
#	5)	postShutdown()
#===============================================================================

import os
import re
import sys
import time

from gmmePylib import *
#import gmmePylib.Utils.CEC
#import Utils.CmdLine
# import Utils.Mail
#import Utils.Object
#import Utils.Other

#from Utils.Logger import *


#-------------------------------------------------------------------------------
#-- globals
#-------------------------------------------------------------------------------
_gbatchapp_ = None
_gbatchapp_cmdline_ = None
_gbatchapp_dbgLevel = 0
_gbatchapp_env = ''
_gbatchapp_log = None

g_app = None
g_appCmdline = None
g_appDbgLevel = 0
g_appEnv = ''
g_appLog = None


#-------------------------------------------------------------------------------
#-- global access functions
#-------------------------------------------------------------------------------
def App() : return g_app
def AppCmdline() : return g_appCmdline
def AppDbgLevel() : return g_appDbgLevel
def AppEnv() : return g_appEnv
def AppLog() : return g_appLog


#-------------------------------------------------------------------------------
#-- Class BatchAppException
#-------------------------------------------------------------------------------
class BatchAppException(Exception):
    def __init__(self, a_rc, a_str=None, *a_args):
        super().__init__(a_args)
        self.rc = a_rc
        self.m_str = a_str

    def __str__(self):
        return 'BAE:: ErrorCode = ' + str(self.m_rc) + ('' if self.m_str == None else ', Message = ' + self.a_str)


class BatchAppQuit(Exception):
    def __init__(self, a_rc, a_str=None, *a_args):
        super().__init__(a_args)
        self.m_rc = a_rc
        self.m_str = a_str

    def __str__(self):
        return 'BAQ:: ErrorCode = ' + str(self.m_rc) + ('' if self.m_str == None else ', Message = ' + self.a_str)


#-------------------------------------------------------------------------------
#-- Class BatchApp
#-------------------------------------------------------------------------------
class BatchApp():

    #---------------------------------------------------------------------------
    #-- ctor
    #---------------------------------------------------------------------------
    def __init__(self, **a_args) :

        global g_app
        global g_appCmdline

        l_func = 'BatchApp.__init__'

        #-----------------------------------------------------------------------
        #-- initialize member with default values
        #-----------------------------------------------------------------------
        self.m_appname = None
        self.m_cmdline = None
        self.m_log = None
        self.m_logPath = None
        self.m_logFile = None
        self.m_runStartTime = 0
        self.m_runStopTime = 0
        self.m_env = None
        self.m_envReq = False
        self.m_testconn = 0
        self.m_dbgLevel = 0
        self.m_rc  = 0

        self.m_mail = None
        self.m_mailOnErr = None
        self.m_mailOnErrRegex = None

        self.m_lastErr = 0
        self.m_lastErrStr = None
        self.m_lastErrStep = None

        self.m_preInitDone = False
        self.m_setDefaultsDone = False

        self.m_funcInit = None
        self.m_funcPreInit = None
        self.m_funcPostShutDown = None
        self.m_funcRun = None
        self.m_funcSetDefaults = None

        self.m_step = None

        self.m_pData = None


        #-----------------------------------------------------------------------
        #-- process args
        #-----------------------------------------------------------------------
        l_members = {
            'PreInit': 'm_funcPreInit',
            'Init': 'm_funcInit',
            'Run': 'm_funcRun',
            'PostShutDown': 'm_funcPostShutDown',
            'SetDefaults': 'm_funcSetDefaults',
            'EnvReq': 'm_envReq',
            'EnvRequired': 'm_envReq'
        }
        Utils.Object.Init(self, l_members, a_args)

        #-----------------------------------------------------------------------
        #-- determine app name
        #-----------------------------------------------------------------------
        self.m_appname = os.path.basename(sys.argv[0])
        self.m_appname = os.path.splitext(self.m_appname)[0]

        #-----------------------------------------------------------------------
        #-- load command line stuff and call preIinit if defined
        #-----------------------------------------------------------------------
        self.m_cmdline = Utils.CmdLine.Create()
        if len(sys.argv) > 1 : self.m_cmdline.AddArgsArray(sys.argv[1:])
        g_appCmdline = self.m_cmdline

        g_app = self

    #---------------------------------------------------------------------------
    #-- do
    #---------------------------------------------------------------------------
    def Do(self, a_pData = None):

        global g_appDbgLevel
        global g_appEnv
        global g_appLog


        self.m_pData = a_pData

        #-----------------------------------------------------------------------
        #-- set run start date/time
        self.m_runStartTime = time.time()

        #-----------------------------------------------------------------------
        #-- call setDefaults / preInit
        self.m_rc = self.doStepSetDefaults_()
        self.m_rc = self.doStepPreInit_()
        if self.m_rc != 0: return self.m_rc

        #-----------------------------------------------------------------------
        #-- initialize log manager and open file
        self.m_logFile = self.m_cmdline.GetOptValue('-logfile', self.m_appname)
        self.m_logPath = self.m_cmdline.GetOptCombinedValue('-logpath', os.path.sep, '..' + os.path.sep + 'logs' + os.path.sep + self.m_appname)
        self.m_logPath = os.path.expanduser(self.m_logPath)

        self.m_log = CreateLogger(file = self.m_appname, logpath = self.m_logPath, logfile = self.m_logFile)
        self.m_log.Open()

        g_appLog = self.m_log

        #-----------------------------------------------------------------------
        #-- log command line
        l_cmdline = ''
        for l_opt in sys.argv[1:]:
            l_cmdline += l_opt + ' '
        self.m_log.Info('cmd line: ' + l_cmdline)


        #-----------------------------------------------------------------------
        #-- check for env/testconn/dbglevel options
        self.m_testconn = self.m_cmdline.IsOpt('-testconn')
        if self.m_testconn: self.m_log.Warn('Testing connections only!')

        self.m_env = self.m_cmdline.GetOptValue('-env')
        if self.m_envReq and self.m_env is None :
            self.m_log.Fatal('Missing -env option')
            print('Missing -env option');
            l_rc = -1;
        if self.m_env is not None : self.m_log.Info('Environment = ' + self.m_env)
        g_appEnv = self.m_env

        self.m_dbgLevel = self.m_cmdline.GetOptValue('-dbglevel', 0)
        if self.m_dbgLevel > 0 : self.m_log.Info('Debug Level = ' + self.m_dbgLevel)
        g_appDbgLevel = self.m_dbgLevel


        #-----------------------------------------------------------------------
        #-- check if we have a mail on error in effect
        self.m_cmdline.Dump()
        if not self.m_testconn :
            l_mailonerr = self.m_cmdline.IsOpt('-mailonerr')
            l_mailonerror = self.m_cmdline.IsOpt('-mailonerror')
            if l_mailonerr or l_mailonerror :
                #-- determine base value for mailonerror command line options
                if l_mailonerr : self.m_mailOnErr = self.m_cmdline.GetOptValue('-mailonerr')
                if l_mailonerror : self.m_mailOnErr = self.m_cmdline.GetOptValue('-mailonerror')
                if self.m_mailOnErr is None : self.m_mailOnErr = 'mailrc'

                if self.m_cmdline.IsOpt('-mailonerrregex') : self.m_mailOnErrRegex = self.m_cmdline.GetOptValue('-mailonerrregex')
                if self.m_cmdline.IsOpt('-mailonerrorregex') : self.m_mailOnErrRegex = self.m_cmdline.GetOptValue('-mailonerrorregex')

                #-- log we having mailing on error information
                self.m_mail = Utils.Mail.Create(self, self.m_mailOnErr)

                self.m_log.Info('Mail on error options:')
                self.m_log.Info('   smtp  = ' + self.m_mail.Smtp())
                self.m_log.Info('   from  = ' + self.m_mail.From())
                self.m_log.Info('   to    = ' + self.m_mail.To())
                self.m_log.Info('   cc    = ' + self.m_mail.CcFormatted())
                self.m_log.Info('   bcc   = ' + self.m_mail.BccFormatted())
                if self.m_mailOnErrRegex is not None : self.m_log.Info('   regex = ' + self.m_mailOnErrRegex)


        #-----------------------------------------------------------------------
        #-- init() and run()
        if self.m_rc == 0:
            try:
                self.m_rc = self.doStep_('init', self.m_funcInit)
                if self.m_rc == 0 :
                    self.m_rc = self.doStep_('run', self.m_funcRun)
            except BatchAppException as ex:
                self.m_rc = ex.rc
            except BatchAppQuit as ex:
                self.m_rc = ex.rc

        #-----------------------------------------------------------------------
        #-- always do postShutDown( ), and send email if that is turned on
        self.doStepPostShutDown_()
        if self.m_rc != 0 and self.m_mail is not None :
            self.Mail()
        self.m_log.Close()

        return self.m_rc


    #---------------------------------------------------------------------------
    #-- doStep_
    #---------------------------------------------------------------------------
    def doStep_(self, a_step, a_stepFunc):

        l_rc = 0

        self.m_step = a_step
        if a_stepFunc is not None: l_rc = a_stepFunc(self, self.m_pData)
        if l_rc != 0: self.m_lastErrStep = a_step

        return l_rc


    #---------------------------------------------------------------------------
    #-- doStepPostShutDown_
    #---------------------------------------------------------------------------
    def doStepPostShutDown_(self):

        self.m_step = 'postShutDown'
        if self.m_funcPostShutDown is not None: self.m_funcPostShutDown(self, self.m_pData)


    #---------------------------------------------------------------------------
    #-- doStepPreInit_
    #---------------------------------------------------------------------------
    def doStepPreInit_(self):

        self.m_step = 'preInit'
        if not self.m_preInitDone:
            l_rc = 0
            if self.m_funcPreInit is not None: l_rc = self.m_funcPreInit(self, self.m_pData)
            if l_rc != 0: return l_rc

            self.doStepSetDefaults_()
            self.m_preInitDone = True

        return 0


    #---------------------------------------------------------------------------
    #-- doStepSetDefaults_
    #---------------------------------------------------------------------------
    def doStepSetDefaults_(self):

        self.m_step = 'setDefaults'
        if not self.m_setDefaultsDone:
            if self.m_funcSetDefaults is not None: l_rc = self.m_funcSetDefaults(self, self.m_pData)
            self.m_setDefaultsDone = True

        return 0


    #---------------------------------------------------------------------------
    #-- Mail
    #---------------------------------------------------------------------------
    def Mail(self) :

        #-----------------------------------------------------------------------
        #-- see if we are going to mail based on rc and regex
        if self.m_mailOnErrRegex is not None :
            if re.match(self.m_mailOnErrRegex, str(self.m_rc)) is None : return


        #-----------------------------------------------------------------------
        #-- create subst dictionary
        l_subst = {
            'APP_NAME' : self.m_appname,
            'APP_LOGFILE' : self.m_log.LogFull(),
            'APP_RC' : str(self.m_rc),
            'APP_RCSTR' : Utils.CEC.ErrCodeToStr(self.m_rc),
            'APP_LASTERR' : self.m_lastErr,
            'APP_LASTERRSTR' : self.m_lastErrStr,
            'APP_LASTERRSTEP' : self.m_lastErrStep,
            'APP_RUNDT' : Utils.Other.FormatTime(self.m_runStartTime, '%Y-%m-%d %H:%M:%S'),
            'APP_FAILEDDT' : Utils.Other.FormatTime(time.time(), '%Y-%m-%d %H:%M:%S')
        }


        #-----------------------------------------------------------------------
        #-- build text for message
        if self.m_mail.Text() is None :
            l_rcstr = Utils.CEC.ErrCodeToStr(self.m_rc)
            if l_rcstr is not None : l_rcstr = ' (' + l_rcstr + ')'

            l_text = ''
            l_text += '===============================================================================================\n'
            l_text += 'Error as occured in application: ' + self.m_appname + '\n'
            l_text += '===============================================================================================\n'
            l_text += 'Return Code: ' + str(self.m_rc) + l_rcstr + '\n\n'
            l_text += 'Log file: ' + self.m_log.LogFull() + '\n\n'
            l_text += 'Last Error Step: ' + self.m_lastErrStep + '\n'
            l_text += 'Last Error Code: ' + self.m_lastErr + '\n'
            l_text += 'Last Error Desc:\n' + self.m_lastErrStr + '\n'
            self.m_mail.Text(l_text)

        self.m_mail.Send(l_subst)


    #---------------------------------------------------------------------------
    #-- member access functions
    #---------------------------------------------------------------------------
    def Appname(self) : return self.m_appname
    def CmdLine(self) : return self.m_cmdline
    def Env(self) : return self.m_env
    def EnvReq(self) : return self.m_envReq
    def Log(self) : return self.m_log
    def LogPath(self) : return self.m_logPath
    def LogFile(self) : return self.m_logFile
    def RunStartTime(self, a_dtfmt = '%Y%m%d%H%M%S') : return Utils.Other.FormatTime(self.m_runStartTime, a_dtfmt)
    def RunStopTime(self, a_dtfmt = '%Y%m%d%H%M%S') : return Utils.Other.FormatTime(self.m_runStopTime, a_dtfmt)
    def TestConn(self) : return self.m_testconn


    #---------------------------------------------------------------------------
    #-- member command line access functions
    #---------------------------------------------------------------------------
    def GetDBLogon(self, **a_argv) : return self.m_cmdline.GetDBLogon(**a_argv)
    def GetOptValue(self, *a_argv) : return self.m_cmdline.GetOptValue(*a_argv)
    def GetOptCombinedValue(self, *a_argv) : return self.m_cmdline.GetOptCombinedValue(*a_argv)
    def GetPathOpt(self, *a_argv) : return self.m_cmdline.GetPathOpt(*a_argv)
    def IsOpt(self, a_opt) : return self.m_cmdline.IsOpt(a_opt)
    #def loadCmdlineFromHash(self, **a_argv) : return return shift->{m_cmdline}->loadFromHash( @_ ); }


    #---------------------------------------------------------------------------
    #-- logger line access functions
    #---------------------------------------------------------------------------
    def LogDebug(self, a_msg) : self.m_log.LogDebug(a_msg, 1)
    def LogFatal(self, a_msg) : self.m_log.LogFatal(a_msg, 1)
    def LogInfo(self, a_msg) : self.m_log.LogInfo(a_msg, 1)
    def LogRaw(self, a_msg) : self.m_log.LogRaw(a_msg)
    def LogSql(self, a_msg) : self.m_log.LogSql(a_msg, 1)
    def LogWarn(self, a_msg) : self.m_log.LogWarn(a_msg, 1)
    def LogWarning(self, a_msg) : self.m_log.LogWarn(a_msg, 1)


    #---------------------------------------------------------------------------
    #-- helper access functions
    #---------------------------------------------------------------------------
    def LogFatalAndReturn(self, a_msg, a_ret):
        self.m_log.LogFatal(a_msg, 1)
        return a_ret

    def GetOptValueErrorNone(self, a_opt, a_msg):
        l_opt = self.m_cmdline.GetOptValue(a_opt)
        if l_opt == None:
            self.m_log.LogFatal(a_msg, 1)
            raise BatchAppException(Utils.CEC.CmdLineMissingItem())
        return l_opt
#        return a_app.LogFatalAndReturn('Missing or no value for -sync option !!!!', Utils.CEC.CmdLineMissingItem())
#self.m_cmdline.GetOptValue


#-------------------------------------------------------------------------------
#-- Create wrapper functions
#-------------------------------------------------------------------------------
def CreateBatchApp(**a_argv) :
    return BatchApp(**a_argv)


#===============================================================================
# Self test of module
#===============================================================================
if __name__ == "__main__" :

    l_rcregex = '(60)'
    l_matchgrp = None

    l_rc = 20
    l_match = re.match(l_rcregex, str(l_rc))
    if l_match is not None : l_matchgrp = l_match.groups()

    l_rc = 60
    l_match = re.match(l_rcregex, str(l_rc))
    if l_match is not None : l_matchgrp = l_match.groups()

    l_rc = 0

    def testInit() :
        print("Inside testInit()...")
        return 0
    def testPreInit() :
        print("Inside testPreInit()...")
        return 0
    def testPostShutDown() :
        print("Inside testPostShutDown()...")
        return 0
    def testRun() :
        print("Inside testRun()...")
        return 0
    def testSetDefaults() :
        print("Inside testSetDefaults()...")
        return 0

    #-- test app
    l_app = BatchApp(PreInit=testPreInit, Init=testInit, Run=testRun, SetDefaults=testSetDefaults)
#        'PostShutDown' : testPostShutDown,
    l_app.Do()
    l_rc = None


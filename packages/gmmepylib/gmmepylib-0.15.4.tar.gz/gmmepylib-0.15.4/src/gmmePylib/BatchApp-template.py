#!/usr/bin/env python
#===============================================================================
# gmme-pylib for Python
# Copyright (c) 2002 - 2023, GMM Enterprises, LLC.
# Licensed under the GMM Software License
# All rights reserved 
#===============================================================================
#   Author:	David Crickenberger
# ------------------------------------------------------------------------------
#
#   Desc:   Template main .py file for using GMME stuff
#
#   Required PIP:
#       pip install importlib
#       pip install pywin32
#===============================================================================
#===============================================================================
import os
import sys
import time

#-------------------------------------------------------------------------------
#-- bring GMME Lib stuff into root import root
import importlib.util
l_gmmelib = '.\\GMME'
if not importlib.util.find_spec('GMME'):
    l_gmmelib = l_gmmelib if 'GMMEPythonLib' not in os.environ else os.environ.get('GMMEPythonLib')
sys.path.append(l_gmmelib)
from BatchApp import *


#-------------------------------------------------------------------------------
#-- doSetDefaults_()
#-------------------------------------------------------------------------------
def doSetDefaults_(a_app, a_pData):
    return 0

#-------------------------------------------------------------------------------
#-- doPreInit_()
#-------------------------------------------------------------------------------
def doPreInit_(a_app, a_pData):
    a_app.LogInfo('Pre-Initialization - beg:')
    a_app.LogInfo('Pre-Initialization - end:')
    return 0

#-------------------------------------------------------------------------------
#-- doInit_()
#-------------------------------------------------------------------------------
def doInit_(a_app, a_pData):
    a_app.LogInfo('Initialization - beg:')
    a_app.LogInfo('Initialization - end:')
    return 0

#-------------------------------------------------------------------------------
#-- doRun_()
#-------------------------------------------------------------------------------
def doRun_(a_app, a_pData):
    a_app.LogInfo('Run - beg:')
    a_app.LogInfo('Run - end:')
    return 0

#-------------------------------------------------------------------------------
#-- doPostShutdown_()
#-------------------------------------------------------------------------------
def doPostShutdown_(a_app, a_pData):
    return 0


#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#--
#-- main process
#--
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
g_app_ = CreateBatchApp(PreInit=doPreInit_, Init=doInit_, Run=doRun_, SetDefaults=doSetDefaults_, PostShutdown=doPostShutdown_)
l_rc = g_app_.Do()
sys.exit(l_rc)

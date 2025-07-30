#!/usr/bin/env python
#===============================================================================
# gmme-pylib for Python
# Copyright (c) 2002 - 2023, GMM Enterprises, LLC.
# Licensed under the GMM Software License
# All rights reserved 
#===============================================================================
#	Author:	David Crickenberger
# ------------------------------------------------------------------------------
#	Packages:
#		Utils::CmdLine
#
# 	Description:
#		Command line processor module.
#
#===============================================================================
# $Log: $
#===============================================================================
import gmmePylib.Utils.CmdLine
import gmmePylib.Utils.Other


#-------------------------------------------------------------------------------
#-- globals
#-------------------------------------------------------------------------------
g_dbgOn = False


#-------------------------------------------------------------------------------
#-- 
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
#-- init: initial object members from dict object
#-------------------------------------------------------------------------------
def Init(a_obj, a_members, a_args, a_valueAsStr = False):

    #---------------------------------------------------------------------------
    #-- produce a list of uppercase keys to map parameters back using case
    #-- insenstive values and then process a_args
    l_members = gmmePylib.Utils.Other.CreateUpperCaseDictKeys(a_members)

    l_found = False
    for l_arg in list(a_args.keys()):
        l_argu = l_arg.upper()
        if l_argu in l_members:
            l_value = a_args[l_arg]
            a_obj.__dict__[a_members[l_members[l_arg.upper()]]] = l_value
            l_found = True

    return l_found


#-------------------------------------------------------------------------------
#-- init: initial object members from dict object
#-------------------------------------------------------------------------------
def InitWithCmdLine(a_obj, a_members, a_cmdline, a_args = None) :

    #---------------------------------------------------------------------------
    #-- debug stuff
    #if g_dbgOn :
    #    print('DBG-Utils.Object.initWithCmdLine == args - beg:')
    #    print('DBG-a_obj -- beg:')
    #    print(dump(a_obj))
    #    print('DBG-a_obj -- end:')
    #    #if a_members is not None :
    #    #    print('DBG ===========================================')
    #    #    print('DBG-a_members -- beg:')
    #    #    pprint.pprint(a_members)
    #    #    print('DBG-a_members -- end:')
    #    print('DBG ===========================================')
    #    print('DBG-a_cmdline -- beg:')
    #    print(dump(a_cmdline))
    #    print('DBG-a_cmdline -- end:')
    #    #print('DBG ===========================================')
    #    #print('DBG-a_args -- beg:')
    #    #print(Dumper( @a_args );
    #    #print('DBG-a_args -- end:')
    #    print('DBG-Utils::Object::initWithCmdLine == args - end:')


    #---------------------------------------------------------------------------
    #-- 1st call default init object and see if cmdline was returned
    l_found = False
    l_obj = None

    if a_members is not None:
        if len(a_members) > 0:
            l_found = Init(a_obj, a_members, a_args)

    if a_args is not None :
        if isinstance(a_args[0], gmmePylib.Utils.CmdLine):
            l_obj = a_args[0]

    if l_obj is None :
        if '_obj' in a_cmdline : l_obj = a_cmdline['_obj']

    if l_obj is None : return l_found        


    #---------------------------------------------------------------------------
    #-- 2nd determine base and process command line options
    l_base = '-' + a_cmdline['_base']
    for l_key in list(a_cmdline.keys()) :
        #-----------------------------------------------------------------------
        #-- determine key, type and opt values
        if l_key == '_obj' or l_key == '_base' : continue

        l_keyt = a_cmdline[l_key]['t']
        l_keyv = a_cmdline[l_key]['v']

        if 'k' in a_cmdline[l_key] :
            l_opt = l_base + a_cmdline[l_key]['k']
        else :
            l_opt = l_base + l_key
        l_optFound = l_obj.IsOpt(l_opt)
        if l_optFound : l_found = True


        #-----------------------------------------------------------------------
        #-- process based on cmdline key type
        if l_keyt == gmmePylib.Utils.CmdLine.ISOPT() :
            a_obj.__dict__[l_keyv] = l_optFound
            continue

        if not l_optFound : continue

        #-- the next set of calls to cmdline use the current objects members
        #-- as default value.  make sure it exists
        l_defValue = None
        if l_keyv in a_obj.__dict__ : l_defValue = a_obj.__dict__[l_keyv]

        if l_keyt == gmmePylib.Utils.CmdLine.GETOPTVALUE() or l_keyt == gmmePylib.Utils.CmdLine.GETOPTVALUEDEF() :
            if 'd' in a_cmdline[l_key] : l_defValue = a_cmdline[l_key]['d']
            a_obj.__dict__[l_keyv] = l_obj.GetOptValue(l_opt, l_defValue)
            continue

        if l_keyt == gmmePylib.Utils.CmdLine.GETPATHOPT() :
            a_obj.__dict__[l_keyv] = l_obj.GetPathOpt(l_opt, l_defValue)
            continue

        #-- process dblogon stuff
        if l_keyt != gmmePylib.Utils.CmdLine.GETDBLOGON() : continue

        l_keyvc = a_cmdline[l_key]['vc']
        l_keyvn = a_cmdline[l_key]['vn']
        l_keyvp = a_cmdline[l_key]['vp']
        l_keyvu = a_cmdline[l_key]['vu']
        
        l_dblogon = l_obj.GetDBLogon(l_opt)
        l_tmp = l_dblogon[0].lower()
        if l_tmp in ['ado', 'db2', 'mysql', 'odbc', 'oracle'] :
            if len(l_dblogon) == 2 :
                a_obj.__dict__[l_keyvc] = l_dblogon[1]
            else :
                a_obj.__dict__[l_keyvu] = l_dblogon[1]
                a_obj.__dict__[l_keyvp] = l_dblogon[2]
                a_obj.__dict__[l_keyvc] = l_dblogon[3]
        else :
            #-- old format
            a_obj.__dict__[l_keyvu] = l_dblogon[1]
            a_obj.__dict__[l_keyvp] = l_dblogon[2]
            a_obj.__dict__[l_keyvc] = l_dblogon[3]

    return l_found

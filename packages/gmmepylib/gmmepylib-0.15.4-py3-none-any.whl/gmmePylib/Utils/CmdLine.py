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
#	Utils::CmdLine
#
# Description:
#	Command line processor module.
#===============================================================================

from pathlib import Path

import errno
import os
import random
import re


#-------------------------------------------------------------------------------
#-- Simulate Constants
#-------------------------------------------------------------------------------
def GETDBLOGON():       return 1
def GETOPTVALUE():      return 2
def GETOPTVALUEDEF():   return 3
def GETPATHOPT():       return 4
def ISOPT():            return 5
def ISOPT_SETON():      return 5
def ISOPT_SETOFF():     return 6


#-------------------------------------------------------------------------------
#-- static functions
#-------------------------------------------------------------------------------
def _s_dumpAddArgsParameters_(a_dbgfunc:str, a_argv):
    print(a_dbgfunc + " -- beg:")
    print(a_dbgfunc + " :: cwd => " + os.getcwd())
    print(a_dbgfunc + " :: type(a_argv) => " + str(type(a_argv)))
    print(a_dbgfunc + " :: a_argv -- beg:")
    print(a_argv)
    print(a_dbgfunc + " :: a_argv -- end:")
    print(a_dbgfunc + " -- end:")


#-------------------------------------------------------------------------------
#-- Class CmdLineException
#-------------------------------------------------------------------------------
class CmdLineException():
    _m_msg:str = None

    def __init__(self, a_msg:str):
        self._m_msg = a_msg


#-------------------------------------------------------------------------------
#-- Class CmdLine
#-------------------------------------------------------------------------------
class CmdLine():
    #---------------------------------------------------------------------------
    #-- Members
    #---------------------------------------------------------------------------
    _m_dbgOn:bool = False
    _m_isInit:bool = False
    _m_opts = {}


    #---------------------------------------------------------------------------
    #-- ctor
    #---------------------------------------------------------------------------
    def __init__(self, a_dbgOn:bool = False):
        self._m_isInit = True
        self._m_dbgOn = a_dbgOn


    #---------------------------------------------------------------------------
    #-- AddArgs
    #---------------------------------------------------------------------------
    def AddArgs(self, a_argv:any):

        l_dbgfunc = "DBG-Utils.CmdLine.AddArgs"
        if self._m_dbgOn: _s_dumpAddArgsParameters_(l_dbgfunc, a_argv)

        #-----------------------------------------------------------------------
        #-- call correct AddXXXX method
        if isinstance(a_argv, str):
            self.AddArgsLine(a_argv)
        elif isinstance(a_argv, list):
            if len(a_argv) > 0:
                self.AddArgsArray(a_argv)
        else:
            raise CmdLineException("'a_argv' type not supported")


    #---------------------------------------------------------------------------
    #-- AddArgsArray
    #---------------------------------------------------------------------------
    def AddArgsArray(self, a_argv:list):

        l_dbgfunc = "DBG-Utils.CmdLine.AddArgsArray"
        if self._m_dbgOn: _s_dumpAddArgsParameters_(l_dbgfunc, a_argv)

        #-----------------------------------------------------------------------
        #-- process
        l_i = 0
        while l_i < len(a_argv) :
            #-------------------------------------------------------------------
            #-- pull option
            l_arg = a_argv[l_i]
            if l_arg[0] == '-' or l_arg[0] == '/' :
                l_opt = l_arg
                l_val = None

                if (l_i + 1 ) < len(a_argv) :
                    #-- make sure next value is not an option
                    l_arg = a_argv[l_i + 1]
                    if len(l_arg) == 0 or (l_arg[0] != '-' and l_arg[0] != '/' and l_arg[0] != '@'):
                        #-- we have a value with the option
                        l_val = l_arg
                        l_i = l_i + 1

                #---------------------------------------------------------------
                #-- add item to list
                l_opt, l_tags = self.checkOptForTags_(l_opt.upper())
                self._m_opts[l_opt] = {"val": self.subEnv_(l_val), "tags": l_tags}
            elif (l_arg[0] == '@') :
                self.AddArgsFile(self.subEnv_(l_arg[1:], True))

            l_i = l_i + 1

        self._m_isInit = 1


    #---------------------------------------------------------------------------
    #-- AddArgsFile
    #---------------------------------------------------------------------------
    def AddArgsFile(self, a_file:str):

        l_dbgfunc = "DBG-Utils.CmdLine.AddArgsFile"

        l_file = Path(a_file).expanduser()
        

        #-----------------------------------------------------------------------
        #-- dbg stuff
        if self._m_dbgOn:
            print(l_dbgfunc + " :: cwd => " + os.getcwd())
            print(l_dbgfunc + " :: file => " + str(l_file))

        #-----------------------------------------------------------------------
        #-- make sure file exists
        if not l_file.exists():
            if self._m_dbgOn: print(l_dbgfunc + " :: ERROR !!! FILE DOES NOT EXISTS !!!")
            raise FileNotFoundError(errno.ENOENT,
                                    os.strerror(errno.ENOENT),
                                    "OPT file could not be found: " + str(l_file) + " [cwd = " + os.getcwd() + "]")

        #-----------------------------------------------------------------------
        #-- open file and process
        if self._m_dbgOn: print(l_dbgfunc + " :: opening file => " + str(l_file))

        with l_file.open() as l_optfile:
            for l_line in l_optfile:
                #-- strip newline and see if we have comments
                l_line = l_line.rstrip().lstrip()
                l_lineComment = False
                if len(l_line) > 0:
                    if l_line[0] == '#' or l_line[0] == ':':
                        l_lineComment = True
                    elif len(l_line) > 2:
                        if l_line[0] == '/' and l_line[1] == '/':
                            l_lineComment = True
    
                    if not l_lineComment: self.AddArgsLine(l_line)

        self._m_isInit = True

        if self._m_dbgOn:
            print(l_dbgfunc + " :: opening file == dump - beg:")
            self.Dump()
            print(l_dbgfunc + " :: opening file == dump - end:")


    #---------------------------------------------------------------------------
    #-- AddArgsLine
    #---------------------------------------------------------------------------
    def AddArgsLine(self, a_line:str):

        l_dbgfunc = "DBG-Utils.CmdLine.AddArgsLine"
        if self._m_dbgOn: print(l_dbgfunc + ":: line = " + a_line)

        #-----------------------------------------------------------------------
        #-- process
        l_array = []

        l_splitCh = ' '
        l_line = a_line
        while (len(l_line) > 0):
            #-------------------------------------------------------------------
            #-- split based on current split character
            l_split = l_line.split(l_splitCh, 1)
            l_array.append(l_split[0])

            #-------------------------------------------------------------------
            #-- stirp spaces and determine next split character
            if len(l_split) == 1:
                l_tmp = ''
            else:
                l_tmp = l_split[1].rstrip()
                l_splitCh = ' ';
                if l_tmp != '':
                    if l_tmp[0] == '"' or l_tmp[0] == "'":
                        l_splitCh = l_tmp[0]
                        l_tmp = l_tmp[1:]

            l_line = l_tmp

        self.AddArgsArray(l_array)


    #---------------------------------------------------------------------------
    #-- Dump
    #---------------------------------------------------------------------------
    def Dump(self):

        l_dbgfunc = "DBG-Utils.CmdLine.Dump"

        if not self._m_isInit:
            print(l_dbgfunc + ":: nothing exists...")
            return
        
        #-----------------------------------------------------------------------
        #-- dump contents
        print(l_dbgfunc + " -- beg:")
        l_opts = list(self._m_opts.keys())
        l_opts.sort()
        for l_opt in l_opts:
            l_val, l_tags = (self._m_opts[l_opt]['val'], self._m_opts[l_opt]['tags'])
            if l_val is None:           l_val = '<none>'
            elif l_val == '':           l_val = '<empty string>'
            else:
                if len(l_tags) > 0:     l_val = 'X' * random.sample(range(10,20),1)[0]
            print('   ' + l_opt + ' == [' + l_val + ']')
        print(l_dbgfunc + " -- end:")


    #---------------------------------------------------------------------------
    #-- GetOptCombinedValue
    #---------------------------------------------------------------------------
    def GetOptCombinedValue(self, a_opt:str, a_sep:str = os.path.sep, a_def:any = None):

        if not self._m_isInit: return None

        #-----------------------------------------------------------------------
        #-- see if option value exists
        l_val = self.GetOptValue(a_opt, a_def)
        if l_val is None: return None

        #-----------------------------------------------------------------------
        #-- pull initial option, then see if 2nd option exists
        l_val2 = self.GetOptValue(a_opt.upper() + '2')
        if l_val2 is not None:
            if a_sep is not None:
                if l_val[-1] != a_sep:
                    l_val = l_val + a_sep
                l_val = l_val + l_val2

        return l_val


    #---------------------------------------------------------------------------
    #-- GetDBLogon
    #---------------------------------------------------------------------------
    def GetDBLogon(self, a_opt:str):

        if not self._m_isInit: return None

        #-----------------------------------------------------------------------
        #-- see if option value exists
        l_opt = self.GetOptValue(a_opt)
        if l_opt is None: return None


        #-----------------------------------------------------------------------
        #-- see if we are working with one of the new formats
        l_tmpOpt = l_opt.upper()
        if l_tmpOpt.startswith('ADO'):
            if l_opt[3] == '@':
                #-- we have a dnsless connect string
                l_conn = l_opt[4:]
                return ['ado', l_conn]
            return None
        elif l_tmpOpt.startswith('DB2'):
            if l_opt[3] == '@':
                l_conn = l_opt[4:]
                return ['db2', l_conn]
            return None
        elif l_tmpOpt.startswith('MYSQL'):
            l_conn = l_opt[6:].split(',', 4)
            return ['mysql', l_conn[0], l_conn[1], l_conn[2], l_conn[3]]
        elif l_tmpOpt.startswith('ORA'):
            l_typeLen = 4
            if l_tmpOpt.startswith('ORACLE'): l_typeLen = 7
            
            l_opt1 = l_opt[l_typeLen:].split('/', 2)
            l_opt2 = l_opt1[1].split('@', 2)
            
            return ['oracle', l_opt1[0], l_opt2[0], l_opt2[1]]
        elif l_tmpOpt.startswith('ODBC'):
            if l_opt[4] == '@':
                l_conn = l_opt[5:]
                return ['odbc', l_conn]
            
            l_conn = l_opt.split(',', 4)
            return ['odbc', l_conn[0], l_conn[1], l_conn[2], l_conn[3]]


        #----------------------------------------------------------------------------
        # see if working with oracle or ODBC/MYSQL format
        if l_opt.find('/') > -1 and l_opt.find('@') > -1:
            #-- oracle
            l_opt1 = l_opt.split('/', 2)
            l_opt2 = l_opt1[1].split('@', 2)
            
            return [l_opt1[0], l_opt2[0], l_opt2[1]]
        elif l_opt.find(',') > -1:
            l_conn = l_opt.split(',', 4)
            return [l_conn[0], l_conn[1], l_conn[2], l_conn[3]]

        return None


    #---------------------------------------------------------------------------
    #-- GgetOptValue
    #---------------------------------------------------------------------------
    def GetOptValue(self, a_opt:str, a_def:str = None):

        if not self._m_isInit: return None

        #-----------------------------------------------------------------------
        #-- convert to uppercase and see it it exists
        l_val = None

        l_opt = a_opt.upper()
        if l_opt in self._m_opts: l_val = self._m_opts[l_opt]['val']

        if l_val is not None:
            if l_val != '': return l_val
        
        #-----------------------------------------------------------------------
        #-- see if default passed in
        if a_def is not None: return a_def
        
        return None


    #---------------------------------------------------------------------------
    #-- getPathOpt
    #---------------------------------------------------------------------------
    def GetPathOpt(self, a_opt:str, a_defValue:str = None, a_allowSub:bool = None, a_subValue:str = None):

        if not self._m_isInit: return None

        #-----------------------------------------------------------------------
        #-- see if value exists
        l_str = a_defValue
        l_val = self.GetOptValue(a_opt)
        if l_val is not None:
            #-------------------------------------------------------------------
            #-- save value and see if substitution is allowed
            l_str = l_val
            if a_allowSub is not None:
                if (a_allowSub == True) and (a_subValue is not None):
                    l_i = l_str.find('%')
                    if l_i > -1:
                        l_str2 = l_str
                        if l_i > 0 : l_str = l_str2[0:l_i-1]
                        l_str = l_str + a_subValue
                        l_str = l_str + l_str2[l_i:]

        #-----------------------------------------------------------------------
        #-- make sure their is '\' on end of string
        if (l_str is not None) and l_str != '':
            l_sep = os.path.sep
#            if not l_str.endswith(l_sep) :
            if l_str[-1] != l_sep:
                l_str = l_str + l_sep
                l_str = os.path.expanduser(l_str)

        return l_str


    #---------------------------------------------------------------------------
    #-- IsOpt
    #---------------------------------------------------------------------------
    def IsOpt(self, a_opt:str):

        if not self._m_isInit: return None

        if a_opt.upper() not in self._m_opts:
            return False

        return True


    #---------------------------------------------------------------------------
    #-- checkOptForTags_
    #---------------------------------------------------------------------------
    def checkOptForTags_(self, a_opt:str):
        l_opt = a_opt
        l_tags = []
        l_split = re.split("(^.*)(\\#\\{(.*)\\}$)", a_opt)
        if len(l_split) > 1:
            l_opt = l_split[1]
            l_tagsTmp = re.split("[ ,\\:\\|]", l_split[3])
            for l_tag in l_tagsTmp:
                l_tags.append("HIDE" if l_tag == "HIDE" or l_tag == "HIDDEN" or l_tag == "SECRET" else l_tag)

        return l_opt, l_tags


    #---------------------------------------------------------------------------
    #-- subEnv_
    #---------------------------------------------------------------------------
    def subEnv_(self, a_str:str, a_isPath:bool = False):
        #-----------------------------------------------------------------------
        #-- see if anything to check
        if a_str is None: return None
        if len(a_str) == 0: return ''

        l_str = a_str

        #-----------------------------------------------------------------------
        #-- see if we are going to sub the opt with environment values
        l_p1 = 0
        l_p2 = 0
        l_envSub = ""

        while l_str.find('${') > -1:
            l_p1 = l_str.find('${')
            l_p2 = l_str.find('}', l_p1 + 2 )
            l_envSub = l_str[(l_p1 + 2):l_p2].upper()
            l_str = l_str[:l_p1] + os.environ.get(l_envSub, "") + l_str[(l_p2 + 1):]

        return l_str
#        return {"val": l_str, "hide": l_hide, "path": a_isPath}


##-------------------------------------------------------------------------------
##	loadFromHash
##
##	This routine will load command line options based on values in a hash that
##	contains a command line option and a control hash.
##
##	Each key entry in the hash consist of a hash set has following keys:
##		t =>	the type of function (GETDBLOGON, GETOPTVALUE, etc)
##   	v =>	reference to where value should be placed
##		vu =>	username ref for GETDBLOGON
##		vp =>	password ref for GETDBLOGON
##		vc =>	connection ref for GETDBLOGON
##		vn =>	db name ref from GETDBLOGON
##-------------------------------------------------------------------------------
#sub loadFromHash
#{
#	my $self = shift;
#	my $a_opts = shift;
#	my $a_base = shift;
#
#
#	my $l_base = '-'.$a_base;
#	foreach my $l_key ( keys %{$a_opts} )
#	{
#		my $l_opt = $l_base.$l_key;
#		if ( $a_opts->{$l_key}->{t} == ISOPT )
#		{
#			${$a_opts->{$l_key}->{v}} = $self->isOpt( $l_opt );
#		}
#		elsif ( $a_opts->{$l_key}->{t} == ISOPT_SETOFF )
#		{
#			${$a_opts->{$l_key}->{v}} = ( $self->isOpt( $l_opt ) == 0 );
#		}
#		elsif ( $self->isOpt( $l_opt ) )
#		{
#			if ( $a_opts->{$l_key}->{t} == GETDBLOGON )
#			{
#				my ( $l_u, $l_p, $l_c, $l_n ) = $self->getDBLogon( $l_opt );
#				${$a_opts->{$l_key}->{vu}} = $l_u;
#				${$a_opts->{$l_key}->{vp}} = $l_p;
#				${$a_opts->{$l_key}->{vc}} = $l_c;
#				${$a_opts->{$l_key}->{vn}} = $l_n;
#			}
#			elsif ( $a_opts->{$l_key}->{t} == GETOPTVALUE )
#			{
#				${$a_opts->{$l_key}->{v}} = $self->getOptValue( $l_opt, ${$a_opts->{$l_key}->{v}} );
#			}
#			elsif ( $a_opts->{$l_key}->{t} == GETPATHOPT )
#			{
#				${$a_opts->{$l_key}->{v}} = $self->getPathOpt( $l_opt, ${$a_opts->{$l_key}->{v}} );
#			}
#		}
#	}
#}


#-------------------------------------------------------------------------------
#-- Create wrapper functions
#-------------------------------------------------------------------------------
def Create(a_dbgOn:bool = False):
    return CmdLine(a_dbgOn)

def CreateDbgOn():
    return CmdLine(True)

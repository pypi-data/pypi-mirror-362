#!/usr/bin/env python
#===============================================================================
# gmme-pylib for Python
# Copyright (c) 2002 - 2024, GMM Enterprises, LLC.
# Licensed under the GMM Software License
# All rights reserved 
#===============================================================================
# Author:	David Crickenberger
# ------------------------------------------------------------------------------
# Packages:
#	Utils.Mail
#
# Description:
#	Command line processor module.
#===============================================================================

import gmmePylib.Utils
#.CmdLine
#import gmmePylib.Utils.Other

#-- import modules need for mail
import smtplib
from email.mime.text import MIMEText


#-------------------------------------------------------------------------------
#-- Class Mail
#-------------------------------------------------------------------------------
class Mail() :

    #---------------------------------------------------------------------------
    #-- Members
    #---------------------------------------------------------------------------
    m_app = None

    m_smtp = None
    m_from = None
    m_subj = None
    m_to = None
    m_cc = None
    m_bcc = None
    m_text = None
    m_textfile = None
    m_priority = None

    m_dbgLevel = 0;

    m_tab = ''


    #---------------------------------------------------------------------------
    #-- ctor
    #---------------------------------------------------------------------------
    def __init__(self, a_app, a_base) :

        m_app = a_app

        #---------------------------------------------------------------------------
        #-- initialize new options
        l_cmdline = {
            '_obj': a_app.CmdLine(),
            '_base': a_base,
            'smtp': {'t': gmmePylib.Utils.CmdLine.GETOPTVALUE(), 'v' : 'm_smtp'},
            'from': {'t': gmmePylib.Utils.CmdLine.GETOPTVALUE(), 'v' : 'm_from'},
            'subj': {'t': gmmePylib.Utils.CmdLine.GETOPTVALUE(), 'v' : 'm_subj'},
            'subject': {'t': gmmePylib.Utils.CmdLine.GETOPTVALUE(), 'v' : 'm_subj'},
            'to': {'t': gmmePylib.Utils.CmdLine.GETOPTVALUE(), 'v' : 'm_to'},
            'cc': {'t': gmmePylib.Utils.CmdLine.GETOPTVALUE(), 'v' : 'm_cc'},
            'bcc': {'t': gmmePylib.Utils.CmdLine.GETOPTVALUE(), 'v' : 'm_bcc'},
            'text': {'t': gmmePylib.Utils.CmdLine.GETOPTVALUE(), 'v' : 'm_text'},
            'textfile': {'t': gmmePylib.Utils.CmdLine.GETOPTVALUE(), 'v' : 'm_textfile'},
            'txt': {'t' : gmmePylib.Utils.CmdLine.GETOPTVALUE(), 'v' : 'm_text'},
            'txtfile': {'t' : gmmePylib.Utils.CmdLine.GETOPTVALUE(), 'v' : 'm_textfile'},
            'priority': {'t' : gmmePylib.Utils.CmdLine.GETOPTVALUE(), 'v' : 'm_priority'},
            'dbglevel': {'t' : gmmePylib.Utils.CmdLine.GETOPTVALUE(), 'v' : 'm_dbgLevel'}
        }
        gmmePylib.Utils.Object.InitWithCmdLine(self, None, l_cmdline);


    #---------------------------------------------------------------------------
    #-- Send
    #---------------------------------------------------------------------------
    def Send(self, a_substitute = None) :

        #-- see if we have any substitutions in body and subject
        l_subj = self.SubjFormatted('')
        l_body = self.TextFormatted('')
        if a_substitute is not None :
            l_subj = doSubstitute_(l_subj, a_substitute)
            l_body = doSubstitute_(l_body, a_substitute)

        #-- prepare the message
        l_msg = MIMEText(l_body)
        l_msg['Subject'] = l_subj
        l_msg['From'] = self.m_from
        l_msg['To'] = self.m_to
        if self.m_cc is not None : l_msg['CC'] = self.m_cc
        if self.m_bcc is not None : l_msg['BCC'] = self.m_bcc

        #-- send message
        l_smtp = smtplib.SMTP()
        l_smtp.sendmail(self.m_from, self.m_to, l_msg.as_string())
        l_smtp.quit()
#	if ( $l_rc < 0 )
#	{
#		$self->{m_app}->log( )->fatal( "Error in Mail::Sender::Close()->code = $l_rc" );
#		$self->{m_app}->log( )->fatal( "Error in Mail::Sender::Close()->msg  = ".$Mail::Sender::Error );
#		return 1;
#	}

        #-- log that email was done
        self.m_app.Log().Info(self.m_tab + '----------------------------------------')
        self.m_app.Log().Info(self.m_tab + 'Email-To  : ' + self.m_to)
        if self.m_cc is not None : self.m_app.Log().Info(self.m_tab + '      Cc  : ' + self.m_cc)
        if self.m_bcc is not None : self.m_app.Log().Info(self.m_tab + '      Bcc  : ' + self.m_bcc)
        self.m_app.Log().Info(self.m_tab + '      Subj: ' + l_subj)
        self.m_app.Log().Info(self.m_tab + '----------------------------------------')


    #---------------------------------------------------------------------------
    #-- member access functions
    #---------------------------------------------------------------------------
    def Smtp(self, a_smtp = None) :
        if a_smtp is not None : self.m_smtp = a_smtp
        return self.m_smtp

    def From(self, a_from = None) :
        if a_from is not None : self.m_from = a_from
        return self.m_from

    def Subj(self, a_subj = None) :
        if a_subj is not None : self.m_subj = a_subj
        return self.m_subj
    def SubjFormatted(self, a_none = '<none>') :
        if self.m_subj is None : return a_none
        return self.m_subj

    def Subject(self, a_subj = None) :
        if a_subj is not None : self.m_subj = a_subj
        return self.m_subj
    def SubjectFormatted(self, a_none = '<none>') :
        if self.m_subj is None : return a_none
        return self.m_subj

    def To(self, a_to = None) :
        if a_to is not None : self.m_to = a_to
        return self.m_to

    def Cc(self, a_cc = None) :
        if a_cc is not None : self.m_cc = a_cc
        return self.m_cc
    def CcFormatted(self, a_none = '<none>') :
        if self.m_cc is None : return a_none
        return self.m_cc

    def Bcc(self, a_bcc = None) :
        if a_bcc is not None : self.m_bcc = a_bcc
        return self.m_bcc
    def BccFormatted(self, a_none = '<none>') :
        if self.m_bcc is None : return a_none
        return self.m_bcc

    def Priority(self, a_priority = None) :
        if a_priority is not None : self.m_priority = a_priority
        return self.m_priority

    def Tab(self, a_tab = None) :
        if a_tab is not None : self.m_tab = a_tab
        return self.m_tab

    def Text(self, a_text = None) :
        if a_text is not None : self.m_text = a_text
        return self.m_text
    def TextFormatted(self, a_none = '<none>') :
        if self.m_text is None : return a_none
        return self.m_text

    def TextFile(self, a_textFile = None) :
        if a_textFile is not None : self.m_textFile = a_textFile
        return self.m_textFile

    def Txt(self, a_text = None) :
        if a_text is not None : self.m_text = a_text
        return self.m_text

    def TxtFile(self, a_textFile = None) :
        if a_textFile is not None : self.m_textFile = a_textFile
        return self.m_textFile


#-------------------------------------------------------------------------------
#-- other module functions
#-------------------------------------------------------------------------------
def doSubstitute_(a_str, a_substitute) :

    #---------------------------------------------------------------------------
    #-- determine if we have anything to substitute
    l_retStr = a_str
    l_subKeys = gmmePylib.Utils.Other.CreateUpperCaseDictKeys(a_substitute)

    l_pos1 = l_retStr.find('@@', l_pos1)
    while l_pos1 > -1 :
        l_pos2 = l_retStr.find('@@', l_pos1 + 2)
        if l_pos2 == -1 : break

        l_sub = l_retStr[(l_pos1 + 2):(l_pos2 - l_pos1 - 2)].upper()
        if l_sub in l_subKeys :
            l_val = a_substitute[l_subKeys[l_sub]]
            l_retStr = l_retStr[:l_pos1] + l_val + l_retStr[(l_pos2 + 2):]

        l_pos1 = l_retStr.find('@@', l_pos1)

    return l_retStr


#-------------------------------------------------------------------------------
#-- Create wrapper functions
#-------------------------------------------------------------------------------
def Create(a_app:str, a_base:str):
    return Mail(a_app, a_base)

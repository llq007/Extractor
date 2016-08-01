#!usr/bin/env python                                        #
#-*- coding: utf-8 -*-                                      #
#-----------------------------------------------------------#
#burpExtender/  extractor.py version 0.10                   #
#Author: linglingqi  (2016.07.28)                           #
#-----------------------------------------------------------#

from burp import IBurpExtender
from burp import ITab
from burp import IHttpListener
from burp import IHttpRequestResponse

from javax import swing
from java.awt import BorderLayout
from java.awt import Dimension
from java.awt.event import ItemListener

import re
import urllib
import urllib2

class BurpExtender(IBurpExtender,ITab,IHttpListener,ItemListener):
    
    # implement IBurpExtender
    def registerExtenderCallbacks(self,callbacks):
        self._callbacks=callbacks
        self._helpes=callbacks.getHelpers()
        self._callbacks.setExtensionName("Extractor")

        #build UI
        self._jPanel=swing.JPanel()
        self._jCheckEnableExtract=swing.JCheckBox('Enable Extract Information:')
        self._jCheckGoogleEngineUrls=swing.JCheckBox('Extract links from google')
        self._jCheckBaiduEngineUrls=swing.JCheckBox('Extract links from baidu')
        self._jCheckLinkDomains=swing.JCheckBox('Extract domain only from google or baidu searched links')
        self._jCheckExtractEmail=swing.JCheckBox('Extract E-mail:')
        self._jCheckFixedDomain=swing.JCheckBox('Fixed domain')
        self._jTextFieldFixedDomain=swing.JTextField('')
        self._jTextFieldFixedDomain.setPreferredSize(Dimension(200,27))
        self._jCheckCustomerRegex=swing.JCheckBox('Customer Regex:')
        self._jComboBoxCustomerRegex=swing.JComboBox(['<a href="([^/].[^"<>()]+?)"','<a target="_blank" href="(.[^"<>]*?)"','<a href="(.[^"<>]*?)" target="_blank">','//(.[^/"<>]*?)/','[\/>]([a-zA-Z0-9]+\.[a-zA-Z0-9]+\.[a-zA-Z0-9.]*?)[\/<]','\\b[a-zA-Z0-9<>/._%+-]+@[a-zA-Z0-9<>/.-]+\.[a-zA-Z<>/]{2,8}\\b','\\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}\\b'],editable=True)
        self._jComboBoxCustomerRegex.setPreferredSize(Dimension(350,27))
        self._jComboBoxCustomerRegex.selectedIndex=-1
        tmpBoxVertical=swing.Box.createVerticalBox()
        tmpBoxVertical.add(self._jCheckEnableExtract)
        tmpBoxVertical.add(swing.Box.createVerticalStrut(15))
        tmpBoxVertical.add(self._jCheckGoogleEngineUrls)
        tmpBoxVertical.add(swing.Box.createVerticalStrut(15))
        tmpBoxVertical.add(self._jCheckBaiduEngineUrls)
        tmpBoxVertical.add(swing.Box.createVerticalStrut(15))
        tmpBoxVertical.add(self._jCheckLinkDomains)
        tmpBoxHorizontal1=swing.Box.createHorizontalBox()
        tmpBoxHorizontal1.add(tmpBoxVertical)
        
        tmpBoxHorizontal2=swing.Box.createHorizontalBox()
        tmpBoxHorizontal2.add(self._jCheckExtractEmail)
        tmpBoxHorizontal2.add(swing.Box.createHorizontalStrut(20))
        tmpBoxHorizontal2.add(self._jCheckFixedDomain)
        tmpBoxHorizontal2.add(swing.Box.createHorizontalStrut(5))
        tmpBoxHorizontal2.add(self._jTextFieldFixedDomain)
        
        tmpBoxHorizontal3=swing.Box.createHorizontalBox()
        tmpBoxHorizontal3.add(self._jCheckCustomerRegex)
        tmpBoxHorizontal3.add(swing.Box.createHorizontalStrut(5))
        tmpBoxHorizontal3.add(self._jComboBoxCustomerRegex)
   
        boxVertical=swing.Box.createVerticalBox()
        boxVertical.add(swing.Box.createVerticalStrut(10))
        boxVertical.add(tmpBoxHorizontal1)
        boxVertical.add(swing.Box.createVerticalStrut(10))
        boxVertical.add(tmpBoxHorizontal2)
        boxVertical.add(swing.Box.createVerticalStrut(10))
        boxVertical.add(tmpBoxHorizontal3)
        boxHorizontal=swing.Box.createHorizontalBox()
        boxHorizontal.add(swing.Box.createHorizontalStrut(10))
        boxHorizontal.add(boxVertical)
        self._jPanel.add(boxHorizontal,BorderLayout.NORTH)
         
        self._jCheckGoogleEngineUrls.setEnabled(False)
        self._jCheckBaiduEngineUrls.setEnabled(False)
        self._jCheckLinkDomains.setEnabled(False)
        self._jCheckExtractEmail.setEnabled(False)
        self._jCheckFixedDomain.setEnabled(False)
        self._jTextFieldFixedDomain.setEnabled(False)
        self._jCheckCustomerRegex.setEnabled(False)
        self._jComboBoxCustomerRegex.setEnabled(False)
        
        self._jCheckEnableExtract.addItemListener(self)
        self._jCheckGoogleEngineUrls.addItemListener(self)
        self._jCheckBaiduEngineUrls.addItemListener(self)
        self._jCheckExtractEmail.addItemListener(self)
        self._callbacks.addSuiteTab(self)
        self._callbacks.registerHttpListener(self)
        
        return

    def itemStateChanged(self,e):
        if self._jCheckEnableExtract.isSelected():
            self._jCheckGoogleEngineUrls.setEnabled(True)
            self._jCheckBaiduEngineUrls.setEnabled(True)
            self._jCheckExtractEmail.setEnabled(True)
            self._jCheckCustomerRegex.setEnabled(True)
            self._jComboBoxCustomerRegex.setEnabled(True)
        else:
            self._jCheckGoogleEngineUrls.setEnabled(False)
            self._jCheckGoogleEngineUrls.setSelected(False)
            self._jCheckBaiduEngineUrls.setEnabled(False)
            self._jCheckBaiduEngineUrls.setSelected(False)
            self._jCheckLinkDomains.setEnabled(False)
            self._jCheckLinkDomains.setSelected(False)
            self._jCheckExtractEmail.setEnabled(False)
            self._jCheckExtractEmail.setSelected(False)
            self._jCheckFixedDomain.setEnabled(False)
            self._jCheckFixedDomain.setSelected(False)
            self._jTextFieldFixedDomain.setEnabled(False)
            self._jCheckCustomerRegex.setEnabled(False)
            self._jCheckCustomerRegex.setSelected(False)
            self._jComboBoxCustomerRegex.setEnabled(False)
            
        if self._jCheckGoogleEngineUrls.isSelected() or self._jCheckBaiduEngineUrls.isSelected():
            self._jCheckLinkDomains.setEnabled(True)
        else:
            self._jCheckLinkDomains.setEnabled(False)
            
        if self._jCheckExtractEmail.isSelected():
            self._jCheckFixedDomain.setEnabled(True)
            self._jTextFieldFixedDomain.setEnabled(True)
        else:
            self._jCheckFixedDomain.setEnabled(False)
            self._jTextFieldFixedDomain.setEnabled(False) 

        return
    
    # implement IHttpListener
    def processHttpMessage(self,toolFlag,messageIsRequest,messageInfo):
        try:
            if self._jCheckEnableExtract.isSelected():
                #callback tools (repeater or intruder or spider or proxy)
                if toolFlag==64 or toolFlag==32 or toolFlag==8 or toolFlag==4: 
                    if not messageIsRequest:
                        bytesResponse=messageInfo.getResponse()
                        analyzedResponse=self._helpes.analyzeResponse(bytesResponse)
                        bytesBody=bytesResponse[analyzedResponse.getBodyOffset():]
                        stringsBody=bytesBody.tostring()
                        
                        #extract links from google search results
                        if self._jCheckGoogleEngineUrls.isSelected():
                            patternUrls=re.compile(r'<a href="(.[^"<>()]+?)"')
                            urls=re.findall(patternUrls, stringsBody)
                            urlsNonrepetition=list(set(urls))
                            urlsNonrepetition.sort(key=urls.index)
                            domains=[]
                            for url in urlsNonrepetition:
                                posFlag=url.lower().find("=http")
                                if self._jCheckLinkDomains.isSelected():
                                    #extract domain with regex
                                    domains+=re.findall(r'//(.[^/]*?)/', url)
                                else:
                                    if posFlag>=0 and url.find("url?")>=0:
                                        url=url.replace("&amp;","&")
                                        print urllib.unquote_plus(url[posFlag+1:])
                                    elif url.startswith("http"):
                                        url=url.replace("&amp;","&")
                                        print urllib.unquote_plus(url)
                            #print extracted domain
                            domainNonrepetition=list(set(domains))
                            domainNonrepetition.sort(key=domains.index)
                            for domain in domainNonrepetition:
                                print domain                                

                        #extract links from baidu search results
                        if self._jCheckBaiduEngineUrls.isSelected():
                            patternUrls=re.compile(r'<a target="_blank" href="(.[^"<>]*?)"|<a href="(.[^"<>]*?)" target="_blank">')
                            urls=re.findall(patternUrls,stringsBody)
                            urlsNonrepetition=list(set(urls))
                            urlsNonrepetition.sort(key=urls.index)
                            domains=[]
                            for urlTuple in urlsNonrepetition:
                                if len(urlTuple[0])>0:
                                    url=urlTuple[0]
                                elif len(urlTuple[1])>0:
                                    url=urlTuple[1]
                                if url.find("?url=")>=0:
                                    responseMessage=getUnRedirectUrl(url)
                                    if not isinstance(responseMessage,(str,int)):
                                        getUrl=responseMessage['Location']
                                        if self._jCheckLinkDomains.isSelected():
                                            #extract domain with regex
                                            domains+=re.findall(r'//(.[^/]*?)/', getUrl)
                                        else:    
                                            print urllib.unquote_plus(getUrl)
                            #print extracted domain
                            domainNonrepetition=list(set(domains))
                            domainNonrepetition.sort(key=domains.index)
                            for domain in domainNonrepetition:
                                print domain
                                
                        #extract Email from html
                        if self._jCheckExtractEmail.isSelected():
                            patternEmails=re.compile(r'\b[a-zA-Z0-9<>/._%+-]+@[a-zA-Z0-9<>/.-]+\.[a-zA-Z<>/]{2,8}\b')
                            emails=re.findall(patternEmails, stringsBody)
                            emailsNonrepetition=list(set(emails))
                            emailsNonrepetition.sort(key=emails.index)
                            getEmails=[]
                            for email in emailsNonrepetition:
                                delStrs=re.findall(r'<(.*?)>',email)
                                for delStr in delStrs:
                                    email=email.replace("<"+delStr+">",'')
                                tmpEmail=re.search(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}\b',email)
                                if tmpEmail is not None:
                                    if self._jCheckFixedDomain.isSelected() and len(self._jTextFieldFixedDomain.getText())>0:
                                        if tmpEmail.group(0).find(self._jTextFieldFixedDomain.getText())>=0:
                                            getEmails.append(tmpEmail.group(0))
                                    else:
                                        getEmails.append(tmpEmail.group(0))
                            for email in list(set(getEmails)):
                                print email

                        #ectract string with defined regex
                        if self._jCheckCustomerRegex.isSelected():
                            patternStrings=re.compile(r'%s'%(str(self._jComboBoxCustomerRegex.getSelectedItem())))
                            getStrings=re.findall(patternStrings, stringsBody)
                            getStringsNonrepetition=list(set(getStrings))
                            getStringsNonrepetition.sort(key=getStrings.index)
                            for getString in getStringsNonrepetition:
                                print getString
        except Exception,e:
            if isinstance(e,str):
                if len(e)>0:
                    print e
            elif e is not None:
                print e
        return

    #implement ITab
    def getTabCaption(self):
        return "Extractor"
    
    def getUiComponent(self):
        return self._jPanel
    
    
class RedirctHandler(urllib2.HTTPRedirectHandler):
    """docstring for RedirctHandler
    """
    def http_error_301(self, req, fp, code, msg, headers):
        pass
    def http_error_302(self, req, fp, code, msg, headers):
        pass

def getUnRedirectUrl(url,timeout=10):
    req = urllib2.Request(url)
    debug_handler = urllib2.HTTPHandler(debuglevel = 0)
    opener = urllib2.build_opener(debug_handler, RedirctHandler)

    html = None
    response = None
    try:
        response = opener.open(url,timeout=timeout)
        html = response.read()
    except urllib2.URLError as e:
        if hasattr(e, 'headers'):
            error_info = e.headers
        elif hasattr(e, 'reason'):
            error_info = e.reason
    finally:
        if response:
            response.close()
    if html:
        return html
    else:
        return error_info

#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------
Authors :
Created by Daniel Zaťovič (P4r4doX)
Special thanks to iPhoneV8 for providing original plists from 4S
---------------------------------------------------------------------
About :
Using this plugin you can change your name directly from Siri
---------------------------------------------------------------------
Usage :
Call me <new name>
Change my <first|nick|last> name to <new name>
My name
---------------------------------------------------------------------
Instalation :
Just create folder called "callMe" in your plugins directory, and place 
this file into it. Then add "callMe" to your plugins.conf
---------------------------------------------------------------------
IMPORTANT :
You MUST download the newest version of SiriServerCore.
---------------------------------------------------------------------
Changelog :
v1.0 (th March 2012) - initial release
"""

from plugin import *
from siriObjects.baseObjects import ObjectIsCommand
from siriObjects.contactObjects import ABPersonSearch, ABPersonSearchCompleted, ABPerson, Person
from siriObjects.systemObjects import DomainObjectRetrieve, DomainObjectRetrieveCompleted, \
     DomainObjectUpdate, DomainObjectUpdateCompleted, DomainObjectCommit, DomainObjectCommitCompleted

res = {
'success': 
    {'de-DE': u"Ok, ich nenne Dich \ "{0} \" von jetzt an.", #translate this to German
     'en-GB': u"Ok, I'll call you \"{0}\" from now on."
    },
'specType': 
    {'de-DE': u"Ok, Dein {0} ist \ "{1} \" von jetzt an.", #translate this to German
     'en-GB': u"Ok, your {0} will be \"{1}\" from now on."
    },
'names': 
    {'de-DE': u"I'm not translated to German !", #translate this to German
     'en-GB': u"Vorname : {0}\nNickname : {1}"
    },
}

class callMe(Plugin):
    
    def changeName(self, nameType, value):      
      meSearch = ABPersonSearch(self.refId)
      meSearch.me = True
      meSearch.scope = "Local"
      
      answer = self.getResponseForRequest(meSearch)
      
      if ObjectIsCommand(answer, ABPersonSearchCompleted):
	results = ABPersonSearchCompleted(answer)
	results = results.results[0]
      else:
	raise StopPluginExecution("Unknown response: {0}".format(answer))
      
      mePerson = ABPerson()
      mePerson.identifier = results.identifier
      
      domainRetrieve = DomainObjectRetrieve(self.refId)
      domainRetrieve.identifiers = [mePerson]
      
      domainAnswer = self.getResponseForRequest(domainRetrieve)
      
      if not ObjectIsCommand(domainAnswer, DomainObjectRetrieveCompleted):
	raise StopPluginExecution("Unknown response: {0}".format(domainAnswer))      

      domainUpdate = DomainObjectUpdate(self.refId)
      domainUpdate.identifier = mePerson
      
      newName = ABPerson()
      
      if nameType in ["nick", "nick name"]:
	newName.nickName = value
      if nameType in ["firstName", "first name"]:
	newName.firstName = value
      if nameType in ["lastName", "last name"]:
	newName.lastName = value
      
      domainUpdate.setFields = newName
      
      updateAnswer = self.getResponseForRequest(domainUpdate)
      
      if not ObjectIsCommand(updateAnswer, DomainObjectUpdateCompleted):
	raise StopPluginExecution("Unknown response: {0}".format(updateAnswer))
      
      domainCommit = DomainObjectCommit(self.refId)
      domainCommit.identifier = mePerson
      
      commitAnswer = self.getResponseForRequest(domainCommit)
      
      if not ObjectIsCommand(commitAnswer, DomainObjectCommitCompleted):
	raise StopPluginExecution("Unknown response: {0}".format(commitAnswer))
      
    
    @register("de-DE", "ändere meinen (?P<type>vornamen|Nachnamen|nick|nick name)?( to )(?P<changeName>[\w ]+)")
    def changeUserName(self, speech, language, regex):
      newNameType = regex.group("type")
      newNameValue = regex.group("changeName").strip().title()
      self.changeName(newNameType, newNameValue)
      self.say(res["specType"][language].format(newNameType, newNameValue))
      self.complete_request()
    
    
    @register("de-DE", "(nenne mich | Mein Name ist | Ich bin) (?P<name>[\w ]+)")
    def callMe(self, speech, language, regex):
      name = regex.group('name').strip().title()
      self.changeName("nick", name)      
      self.say(res["success"][language].format(name))
      self.complete_request()    
    
    @register("en-GB", "(.*my.*names.*)")
    @register("de-DE", "(.*meine.*namen.*)")
    def myName(self, speech, language):
      names = res["names"][language].format(self.assistant.firstName.decode("utf-8"), self.assistant.nickName.decode("utf-8"))
      self.say(names)
      self.complete_request()
    
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      

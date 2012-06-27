#!/usr/bin/python
# -*- coding: utf-8 -*-
#by Daniel "P4r4doX" Zaťovič and a little by Jimmy Kane
#Edited by boeaja
import re
from plugin import *
import urllib2 
from xml.dom.minidom import parseString

#You can choose your own BOT here : http://pandorabots.com/botmaster/en/~1ce90ef1ac87f6dc9dce531~/mostactive
# EVE English
#botID_en = "a9481f8c7e347656"

#SIRI 
botID_en="ae8206713e34cb2e"

# A.L.I.C.E German
botID_de = "d227fbf14e34d947"


def askBOT(botID,input,language):	
	#convert symbols to HEX
        print  botID
        try:        
            input = input.replace(' ', '%20')
            input = input.replace('?', '%3F')
            input = input.replace('$', '%24')
            input = input.replace('+', '%2B')
            input = input.replace(',', '%2C')
            input = input.replace('/', '%2F')
            input = input.replace(':', '%3A') 
            input = input.replace(';', '%3B') 
            input = input.replace('=', '%3D') 
            input = input.replace('@', '%40')	
            file = urllib2.urlopen('http://www.pandorabots.com/pandora/talk-xml?botid=%s&input=%s' % (botID, input))	
            data = file.read()	
            file.close()	
            dom = parseString(data)	
            xmlTag = dom.getElementsByTagName('that')[0].toxml()	
            xmlData=xmlTag.replace('<that>','').replace('</that>','')
            #convert symbols
            xmlData = xmlData.replace('&quot;', '"')
            xmlData = xmlData.replace('&lt;', '<')
            xmlData = xmlData.replace('&gt;', '>')
            xmlData = xmlData.replace('&amp;', '&')
            xmlData = xmlData.replace('<br>', ' ')
            xmlData = xmlData.replace('Eve.', 'Siri.')
            return xmlData
        except:
            if language == 'de-DE':           
                return 'Entschuldigung?'
            else:
                return 'Sorry can you say that again, please ?'
            
def respond(self,botID, input,language):
    if input == 'Stop':
        
        if language == 'de-DE':           
            self.say(u"Gut, danke {0}".format(self.user_name()))                    
        else:
            self.say(u"Nice to chat with you, see you next time {0}".format(self.user_name()))        
            
    else:
        answer = self.say(askBOT(botID,input,language))      
        
    self.complete_request()   
                              
class chatBOT(Plugin):


    @register("en-US", "(.*)")
    @register("en-GB", "(.*)")    
    @register("de-DE", "(.*)")
    def BOT_Message(self, speech, language,regex):
        if language == 'en-US':
            answer = regex.group(regex.lastindex).strip()
            respond(self, botID_en ,answer,language)
        if language == 'en-GB':            
            answer = regex.group(regex.lastindex).strip()
            respond(self,botID_en, answer,language)            
        if language == 'de-DE':            
            answer = regex.group(regex.lastindex).strip()
            respond(self,botID_de, answer,language)
        self.complete_request()

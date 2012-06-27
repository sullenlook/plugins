#!/usr/bin/python
# -*- coding: utf-8 -*-
# v1.2 Get earthquake data by Mike (gaVRos) Pissanos
# Map added by rotastrain
# Usage: all earthquake / all quake will display 50 most recentely reported earthquakes
#        find earthquake in (country or region)
#        for more info see: http://www.emsc-csem.org/service/rss/rss.php?typ=emsc

import urllib
import xml.dom.minidom
import random
import re
from xml.dom.minidom import Node

from plugin import *
from siriObjects.answerObjects import AnswerSnippet, AnswerObject, AnswerObjectLine
from siriObjects.systemObjects import GetRequestOrigin
from siriObjects.uiObjects import AddViews, AssistantUtteranceView
from siriObjects.mapObjects import SiriLocation, SiriMapItem, SiriMapItemSnippet

class EquakePlugin(Plugin):

     @register("de-DE", "(finde|suche|wo).* (Erdbeben | Erdbeben | Erdbeben in).* (.*)")
     @register("en-GB", "(find|show|where).* (earthquake|quake|earthquakes in).* (.*)")
     def quakesearch(self, speech, language, regex):
		searchString = regex.group(regex.lastindex).strip()
		gefunden = 0;
		html = urllib.urlopen("http://www.emsc-csem.org/service/rss/rss.php?typ=emsc").read()
		dom = xml.dom.minidom.parseString(html)	
                self.say("Überprüfung meiner Quellen...")
		for node in dom.getElementsByTagName('item'):
			sendtitle = node.getElementsByTagName('title')
                        sendtime = node.getElementsByTagName('emsc:time')
                        sendlat = node.getElementsByTagName('geo:lat')
                        sendlong = node.getElementsByTagName('geo:long')
                        sendmag = node.getElementsByTagName('emsc:magnitude')                        
			sendeinfo = sendtitle[0].firstChild.data + '\n' + sendtime[0].firstChild.data			
			if re.match(".*"+searchString+".*", sendeinfo, re.IGNORECASE):
				gefunden = 1;
				# self.say(sendeinfo, (' '))			
				view = AddViews(self.refId, dialogPhase="Completion")
				the_header = "Epicenter: " + sendtitle[0].firstChild.data
				Location=SiriLocation(the_header,"","","","","",sendlat[0].firstChild.data,sendlong[0].firstChild.data)
				mapsnippet = SiriMapItemSnippet(items=[SiriMapItem(the_header, Location)])
				view.views = [AssistantUtteranceView(text=sendeinfo, dialogIdentifier="Map"), mapsnippet]
				self.sendRequestWithoutAnswer(view)
		if gefunden == 0:
			self.say(u"Sorry, ich fand keine Erdbeben fuer \""+searchString+"\"")
		self.complete_request()
		
     @register("de-DE", ".*alle .*erdbeben.*|.*alle .*beben.*")
     @register("en-GB", ".*all .*earthquake.*|.*all .*quake.*")
     def quakeall(self, speech, language, regex):
		html = urllib.urlopen("http://www.emsc-csem.org/service/rss/rss.php?typ=emsc").read()
		dom = xml.dom.minidom.parseString(html)	
                self.say("Hier ist die neueste Seismologie Bericht...")
                sendeinfo = ''
                for node in dom.getElementsByTagName('item'):
                        sendtitle = node.getElementsByTagName('title')
                        sendtime = node.getElementsByTagName('emsc:time')
                        sendeinfo = sendeinfo + sendtitle[0].firstChild.data + sendtime[0].firstChild.data + '\n' + '\n'
                        view = AddViews(self.refId, dialogPhase="Completion")
                        ImageAnswer = AnswerObject(title='Realtime earthquake report:',lines=[AnswerObjectLine(sendeinfo)])
                        view1 = AnswerSnippet(answers=[ImageAnswer])
                        view.views = [view1]
                self.sendRequestWithoutAnswer(view)
                self.complete_request()

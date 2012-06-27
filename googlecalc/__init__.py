#!/usr/bin/python
# -*- coding: utf-8 -*-
# Google units calculator v1.0
# by Mike Pissanos (gaVRos) 
#    Usage: simply say Convert or Calculate X to Y
#    Examples: 
#             Convert 70 ferinheight to celsius 
#             Convert 1 euro to dollars
#             Convert 1 tablespoon to teaspoons
#             Calculate 30 divided by 10   


import re
import urllib2, urllib
import json

from plugin import *
from plugin import __criteria_key__

from siriObjects.uiObjects import AddViews
from siriObjects.answerObjects import AnswerSnippet, AnswerObject, AnswerObjectLine

class UnitsConverter(Plugin):
    
    @register("de-DE", "(umwandeln | berechnen)* ([\w ]+)")
    @register("en-GB", "(convert|calculate)* ([\w ]+)")
    def defineword(self, speech, language, regex):
        Title = regex.group(regex.lastindex)
        Query = urllib.quote_plus(Title.encode("utf-8"))
        SearchURL = u'http://www.google.com/ig/calculator?q=' + str(Query)
        try:
            result = urllib2.urlopen(SearchURL).read().decode("utf-8", "ignore")
            result = re.sub("([a-z]+):", '"\\1" :', result)
            result = json.loads(result)
            ConvA = result['lhs']
            ConvB = result['rhs'] 
            self.say("Das habe ich gefunden..." '\n' +str(ConvA) + " gleich, " +str(ConvB))
            self.complete_request()
        except (urllib2.URLError):
            self.say("Sorry, aber eine Verbindung zum Google-Rechner konnte nicht hergestellt werden.")
            self.complete_request()

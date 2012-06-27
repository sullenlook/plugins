#!/usr/bin/python
# -*- coding: utf-8 -*-
#by Joh Gerna

import webbrowser 
from plugin import *


class webrowser(Plugin):
    

    @register("de-DE", "(.*Öffnen. * Website.*)|(.*Durchsuche. * Website.*)|(.*Suche. * Webseite.*)")
    def st_hello(self, speech, language):
            answer = self.ask("Welche Website soll ich durchsuchen?")
	    answer2 = self.ask("Willstn %s in einem neuen Tab oder einem neuen Fenster oeffnet?"%(answer))
            if answer2 == "New tab" :
                webbrowser.open_new_tab("http://www.%s" %(answer))
                self.say("%s wurde auf Ihrem Computer erfolgreich geoeffnet" %(answer))
                self.complete_request()
            else : next
            if answer2 == "Neues Fenster" :
                webbrowser.open("http://www.%s" %(answer))
                self.say("%s wurde auf Ihrem Computer erfolgreich geoeffnet" %(answer))
                self.complete_request()
            else : 
                self.say("Ich muss Sie falsch verstanden haben, sorry, bitte versuchen Sie es erneut.")
                self.complete_request()
            self.complete_request()


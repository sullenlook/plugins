#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import urllib2, urllib
import json
from plugin import *
from plugin import __criteria_key__
from siriObjects.uiObjects import AddViews
from siriObjects.answerObjects import AnswerSnippet, AnswerObject, AnswerObjectLine
import pprint
from random import randint
import os, random

mps = {
	'ps':
	{	1:"abc",
		2:"troll",
		3:"f7u12",
		4:"4chan",
		5:"9gag",
		6:"narwhal",
		7:"cats"
	},
	'qs':
	{ 
	1:"Wie ist die korrekte Schreibweise '':\n1: meem\n2: meme\n3: mimi\n4: maymay",
	2:"Wie ist die richtige Aussprache von meme: 1, 2, 3 or 4",
	3:"'Newfags cant Triforce ist ein Ausdruck, um Neulinge auf der Website zu testen, \n1: reddit\n2: tumblr\n3: facebook\n4: 4chan",
	4:"Woher kommen die meisten Wut Comics / Gesichter :\n1: reddit\n2: tumblr\n3: facebook\n4: 9gag",
	5:"Welche Website wird am meisten gehasst von reddit und 4chan?",
	6:"Wann wird der Narwal Speck?",
	7:"Hat CATS gesagt:\n1: All of your bases belong to us\n2: All your base are belong to us\n3: All of you're bases are belong to us\n4: All of you're base belong to us"
	},
	'sqs':
	{ 
	1:"Welche ist die korrekte Schreibweise von meme: 1, 2, 3 or 4?",
	2:"Welche ist die richtige Aussprache des Wortes: 1: may may. 2: me me. 3: meme or 4: my my?",
	3:"'Newfags cant Triforce ist ein Ausdruck, um Neulinge auf der Website zu testen, 1, red dit. 2, tumblr. 3, facebook or 4, 4chan?",
	4:"Woher kommen die meisten Wut Comics / Gesichter: 1, reddit. 2, tumblr. 3, facebook or 4, 9gag?",
	5:"Welche Website wird am meisten gehasst von reddit und 4chan?",
	6:"Wann wird der Narwal Speck?",
	7:"Hat CATS gesagt:\n1: All of your bases belong to us\n2: All your base are belong to us\n3: All of you're bases are belong to us\n4: All of you're base belong to us?"
	},
	'ans':
	{
	1:"2",
	2:"3",
	3:"4",
	4:"1",
	5:"9gag",
	6:"midnight",
	7:"2"
	}
}

class priv(Plugin):
	@register("de-DE", "testlauf")
	def authtest(self, speech, language, regex):
		if self.assistant_id() == "[6CF4E775-2DB0-4C99-A5D8-DB1B35EEDE00":
			self.say("Zugelassen!")
		else:
			self.say("Netter Versuch, Newfag...","Netter Versuch Newfag.")
			ans = self.ask(u"  ▲\n▲ ▲","Ich wette, Du schaffst es nicht").lower()
			if ans != "op ist eine Schwuchtel" and ans != "new fag" and ans != "newfag":
				view = AddViews(self.refId, dialogPhase="Completion")
				ImageAnswer = AnswerObject(title=str("Trolololololololololololololololololololololololololololol"),lines=[AnswerObjectLine(image="http://harryj.co.uk/t.gif")])
				view1 = AnswerSnippet(answers=[ImageAnswer])
				view.views = [view1]
				self.sendRequestWithoutAnswer(view)
				answer = None
				filename = "./plugins/priv/cat.txt"
				file = open(filename, 'r')
				file_size = os.stat(filename)[6]
				while answer != "Yes" and answer != "Yeah":
					lnum = random.randint(0, file_size-1)
					file.seek((file.tell()+lnum)%file_size)
					file.readline()
					line=file.readline()
					self.say("Cat fact number "+str(lnum)+":\n"+str(line).rstrip('\n'))
					answer = self.ask("Did you know that?")
			view = AddViews(self.refId, dialogPhase="Completion")
			ImageAnswer = AnswerObject(title=str(""),lines=[AnswerObjectLine(image="http://harryj.co.uk/b.gif")])
			view1 = AnswerSnippet(answers=[ImageAnswer])
			view.views = [view1]
			self.sendRequestWithoutAnswer(view)
		self.complete_request()

	@register("de-DE",".*(quiz|game)(.*(?P<level>[1-9]))?")
	def memequiz(self,speech,language,regex):
		gameDone = False
		if regex.group('level'):
			level = int(regex.group('level'))
		else:
			level = 1
		if level != 1:
			passwordAttempt = self.ask("Wie lautet das Passwort fuer Level "+str(level)+"?")
			while passwordAttempt.lower() != mps['ps'][level]:
				self.say("Incorrect.")
				passwordAttempt = self.ask("Wie lautet das Passwort fuer Level "+str(level)+"?")
		self.say(u"Starte level "+str(level))
		ans = "NONE"
		while gameDone == False:
			while ans.lower() != mps['ans'][level]:
				ans = self.ask(mps['qs'][level],mps['sqs'][level])
			self.say("Korrekt!")
			if level != 1: self.say("Der Code wird auf dieses level zurueck gesetzt '"+str(mps['ps'][level])+"'")
			ans = "NONE"
			level = level +1
			if level >7:
				self.say("Du hast Gewonnen!!!!")
				gameDone = True
		self.complete_request()


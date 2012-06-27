#!/usr/bin/env python
# encoding: utf-8
"""
Basic Directions and Traffic
Created by Javik
"""
import re
import urllib2, urllib
import json

from plugin import *

from siriObjects.baseObjects import AceObject, ClientBoundCommand, ObjectIsCommand, RequestCompleted
from siriObjects.systemObjects import *
from siriObjects.uiObjects import *
from siriObjects.localsearchObjects import MapItem, ShowMapPoints

class basicDirections(Plugin):
    @register("de-DE", "Wie geht es nach (?P<location>[\w ]+?)$")
    @register("en-GB", "(How do|Direct|Directions)( I| Me)?( get| go)? to (the |a )?( neareast| closest)?(?P<location>[\w ]+?)$")
    def directions(self, speech, language, regex):
       searchlocation = regex.group('location')
       Title = searchlocation   
       Query = urllib.quote_plus(str(Title.encode("utf-8")))
       googleurl = "http://maps.googleapis.com/maps/api/geocode/json?address={0}&sensor=true&language=en".format(Query)
       jsonString = urllib2.urlopen(googleurl, timeout=20).read()
       response = json.loads(jsonString)
       if (response['status'] == 'OK') and (len(response['results'])):
         for result in response['results']:
             label = "{0}".format(Title.title())
             latitude=result['geometry']['location']['lat']
             longitude=result['geometry']['location']['lng']
             city=result['address_components'][0]['long_name']
             state=result['address_components'][2]['short_name']
             country=result['address_components'][3]['short_name']
       else:
              self.say("Leider koennen Richtungen nur Straßennamen gegeben werden bis jetzt.")
              self.conplete_request()
       code = 0
       Loc = Location(self.refId)
       Loc.street = ""
       Loc.countryCode = country
       Loc.city = city
       Loc.latitude = latitude
       Loc.stateCode = state
       Loc.longitude = longitude
       Map = MapItem(self.refId)
       Map.detailType = "ADDRESS_ITEM"
       Map.label = label
       Map.location = Loc
       Source = MapItem(self.refId)
       Source.detailType = "CURRENT_LOCATION"
       ShowPoints = ShowMapPoints(self.refId)
       ShowPoints.showTraffic = False  
       ShowPoints.showDirections = True
       ShowPoints.regionOfInterestRadiusInMiles = "10.0"
       ShowPoints.itemDestination = Map
       ShowPoints.itemSource = Source
       AddViews = UIAddViews(self.refId)
       AddViews.dialogPhase = "Summary"
       AssistantUtteranceView = UIAssistantUtteranceView()
       AssistantUtteranceView.dialogIdentifier = "LocationSearch#foundLocationForDirections"
       AssistantUtteranceView.speakableText = "Hier ist der Weg nach {0}:".format(label)
       AssistantUtteranceView.text = "Hier ist der Weg nach {0}:".format(label)
       AddViews.views = [(AssistantUtteranceView)]
       AddViews.scrollToTop = False
       AddViews.callbacks = [ResultCallback([ShowPoints], code)]
       callback = [ResultCallback([AddViews])]
       self.complete_request(callbacks=[ResultCallback([AddViews], code)])

class Traffic(Plugin):
    
    @register("de-DE", ".*Verkehr nach (in | auf) (?P<location>[\w ]+?)$")
    @register("en-GB", ".*traffic (like )?(in|on|near) (?P<location>[\w ]+?)$")
    def traffic(self, speech, language, regex):
       searchlocation = regex.group('location')
       Title = searchlocation   
       Query = urllib.quote_plus(str(Title.encode("utf-8")))
       googleurl = "http://maps.googleapis.com/maps/api/geocode/json?address={0}&sensor=true&language=en".format(Query)
       jsonString = urllib2.urlopen(googleurl, timeout=20).read()
       response = json.loads(jsonString)
       if (response['status'] == 'OK') and (len(response['results'])):
         for result in response['results']:
             label = "{0}".format(Title.title())
             latitude=result['geometry']['location']['lat']
             longitude=result['geometry']['location']['lng']
             city=result['address_components'][0]['long_name']
             state=result['address_components'][2]['short_name']
             country=result['address_components'][3]['short_name']
       code = 0
       Loc = Location(self.refId)
       Loc.street = ""
       Loc.countryCode = country
       Loc.city = city
       Loc.latitude = latitude
       Loc.stateCode = state
       Loc.longitude = longitude
       Map = MapItem(self.refId)
       Map.detailType = "ADDRESS_ITEM"
       Map.label = label
       Map.location = Loc
       Source = MapItem(self.refId)
       Source.detailType = "CURRENT_LOCATION"
       ShowPoints = ShowMapPoints(self.refId)
       ShowPoints.showTraffic = True  
       ShowPoints.showDirections = False
       ShowPoints.regionOfInterestRadiusInMiles = "10.0"
       ShowPoints.itemDestination = Map
       ShowPoints.itemSource = Source
       AddViews = UIAddViews(self.refId)
       AddViews.dialogPhase = "Summary"
       AssistantUtteranceView = UIAssistantUtteranceView()
       AssistantUtteranceView.dialogIdentifier = "LocationSearch#foundLocationForTraffic"
       AssistantUtteranceView.speakableText = "Hier \ 's der Verkehr:"
       AssistantUtteranceView.text = "Hier \ 's der Verkehr:"
       AddViews.views = [(AssistantUtteranceView)]
       AddViews.scrollToTop = False
       AddViews.callbacks = [ResultCallback([ShowPoints], code)]
       callback = [ResultCallback([AddViews])]
       self.complete_request(callbacks=[ResultCallback([AddViews], code)])

    @register("de-DE", ".*Verkehr wie")
    @register("en-GB", ".*traffic")
    def trafficSelf(self, speech, language, regex):
       mapGetLocation = self.getCurrentLocation(force_reload=True,accuracy=GetRequestOrigin.desiredAccuracyBest)
       latitude= mapGetLocation.latitude
       longitude= mapGetLocation.longitude
       label = "Your location"
       code = 0
       Loc = Location(self.refId)
       Loc.street = ""
       Loc.countryCode = "DE"
       Loc.city = ""
       Loc.latitude = latitude
       Loc.stateCode = ""
       Loc.longitude = longitude
       Map = MapItem(self.refId)
       Map.detailType = "ADDRESS_ITEM"
       Map.label = label
       Map.location = Loc
       Source = MapItem(self.refId)
       Source.detailType = "CURRENT_LOCATION"
       ShowPoints = ShowMapPoints(self.refId)
       ShowPoints.showTraffic = True  
       ShowPoints.showDirections = False
       ShowPoints.regionOfInterestRadiusInMiles = "10.0"
       ShowPoints.itemDestination = Map
       ShowPoints.itemSource = Source
       AddViews = UIAddViews(self.refId)
       AddViews.dialogPhase = "Summary"
       AssistantUtteranceView = UIAssistantUtteranceView()
       AssistantUtteranceView.dialogIdentifier = "LocationSearch#foundLocationForTraffic"
       AssistantUtteranceView.speakableText = "Hier \ 's der Verkehr:"
       AssistantUtteranceView.text = "Hier \ 's der Verkehr:"
       AddViews.views = [(AssistantUtteranceView)]
       AddViews.scrollToTop = False
       AddViews.callbacks = [ResultCallback([ShowPoints], code)]
       callback = [ResultCallback([AddViews])]
       self.complete_request(callbacks=[ResultCallback([AddViews], code)])

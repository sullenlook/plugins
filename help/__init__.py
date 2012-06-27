#!/usr/bin/python
# -*- coding: utf-8 -*-
# Original by Joh Gerna thanks for help to john-dev
# Updated by Mike Pissanos (gaVRoS) for SiriServerCore
# Further updated by Cristian Asenjo (apu95) for better commands list

# CONFIGURATION
# - Write the absolute path of the folder you store your plugins in.
# - Write the name of the folder for the helpPlugin
# - If you don't want to show a message for plugins that are missing help messages, change
#   the value of displayMissingHelpMessage from True to False
myPluginsFolder = "/home/ec2-user/SiriServerCore/plugins/"
helpPluginFolder = "help"
displayMissingHelpMessage = True

import re,os

config_file="plugins.conf"
pluginPath="plugins"
from plugin import *
tline_answer = ''
pluginsList = {}

# The following three lines allow you to import plugins from your plugins folder
import os, sys, inspect
if myPluginsFolder not in sys.path:
    sys.path.insert(0, myPluginsFolder)

# Go through each plugin in the plugins list (plugins.conf) and store the name and class
# reference in the loadedPlugins dictionary
with open(config_file, "r") as fh:
    for line in fh:
        line = line.strip()
        if line.startswith("#") or line == "" or line == helpPluginFolder:
            continue
        try:
            # The following three lines are used to import the plugin that is fetched 
            # in the previous for loop
            module = __import__(line)
            class_ = getattr(module, line)
            loadedPlugin = class_()
            
            pluginsList[line] = loadedPlugin

        except:
            print "**HelpPlugin message: Could not load plugin: " + line + "**"

# Appends the help messages from the classes in the pluginsList dictionary to the answer
# returned by the main class
def loadMessages(language):

    global tline_answer
    for name, plugin in pluginsList.iteritems():
        try:
            helpMessages = plugin.getHelp(language)
            tline_answer = tline_answer + "Commands for " + name + ":" + "\n"
            
            for message in helpMessages:
                tline_answer = tline_answer + '-' + message + '\n'

            tline_answer = tline_answer + '\n'
        except AttributeError:
            if displayMissingHelpMessage:
                tline_answer = tline_answer + name + " does not have help messages available\n\n"


class help(Plugin):

    messagesLoaded = False
    
    @register("de-DE", "(Hilfe)|(Befehle)")
    @register("en-GB", "(Help)|(Commands)")
    def help(self, speech, language):
        
        # Have we loaded our messages? This runs only once.
        if not self.messagesLoaded:
            loadMessages(language)
            self.messagesLoaded = True

        if language == 'de-DE':
            self.say("Das sind die Befehle die in Deiner Sprache verfügbar sind:")
            self.say("".join(tline_answer ),' ')
        else:
            self.say("Here are the available commands:")
            self.say(tline_answer ,' ')
        self.complete_request()


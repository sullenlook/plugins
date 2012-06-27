#!/usr/bin/python
# -*- coding: utf-8 -*-

from plugin import *
import bluetoothGerät

class bluetoof(Plugin):
               
    @register("de-DE", ".*Suche. * Bluetooth.*")
    def blootoof(self, speech, language):
        port = 1
        self.say("Suche jetzt nach Bluetooth-Geraeten, bitte warten...")
        nearby_devices = bluetooth.discover_devices(lookup_names = True)
        self.say("Habe %d Geraete gefunden!" % len(nearby_devices))
        for addr, name in nearby_devices:           
            self.say("Das Gerät, das ich gefunden habe, ist - %s" % (name))
            answer = self.ask("Jetzt mit dem  Geraet verbinden?")
            if answer == "Ja" :
                self.say("Verbinde, bitte warten...")
                sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
                sock.connect((addr, port))
                self.say("Geraet erfolgreich mit dem Computer verbunden!")
                #Insert your code here
                self.complete_request()
            else : self.say("Okay, Trennen vom Bluetooth")
            self.complete_request()
            
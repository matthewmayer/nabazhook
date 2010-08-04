#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Nabaztag python API
by Ricardo Varela <phobeo@gmail.com>

This module wraps up the Nabaztag API
based on Nabaztag API 2.0
(see http://api.nabaztag.com/docs/home.html)
"""

import random
import urllib
from xml.dom.minidom import parseString

"""
Encapsulate the TTS voice ids
"""

class TTSVoices:
    # french
    FR_1 = 'julie22k',
    FR_2 = 'claire22s',
    FR_3 = 'caroline22k',
    FR_4 = 'bruno22k',
    
    # english
    EN_1 = 'graham22s',
    EN_2 = 'lucy22s',
    EN_3 = 'heather22k',
    EN_4 = 'ryan22k',
    EN_5 = 'aaron22s',
    EN_6 = 'laura22s' 

"""
Encapsulate a choreography
"""
class Choreography:
    tempo = ''
    commands = []
    
    def __init__(self, tempo='10'):
        self.tempo = tempo
    
    def addEarCommand(self, heure, side, angle, direction):
        """ add a new ear movement command to the choreography """
        # parameter check
        badParam = ''
        if not heure >= 0:
            badParam = 'heure'
        elif not (side == Choreography.EAR_LEFT or side == Choreography.EAR_RIGHT):
            badParam = 'side'
        elif not angle >=0 and angle <=180:
            badParam = 'angle'
        elif not (direction == Choreography.EAR_BACK or direction == Choreography.EAR_FRONT):
            badParam = 'direction'
            
        if badParam != '':
            raise ValueError, "Invalid parameter in ear command (%s)" % badParam
        else:
            self.commands.append(self.buildEarCommand(heure, side, angle, direction))
    
    def buildEarCommand(self, heure, side, angle, direction):
        """ return a string with the API representation of the command """
        return "%s,motor,%s,%s,0,%s" % (heure, side, angle, direction)
    
    def addLedCommand(self, heure, led, r, g, b):
        """ add a new led command to the choreography """
        # parameter check
        badParam = ''
        if not heure >= 0:
            badParam = 'heure'
        elif not (led == Choreography.LED_BOTTOM or led == Choreography.LED_LEFT or led == Choreography.LED_MIDDLE or led == Choreography.LED_RIGHT or led == Choreography.LED_TOP):
            badParam = 'led'
        elif not (r >=0 and r <=255):
            badParam = 'r'
        elif not (g >=0 and g <=255):
            badParam = 'g'
        elif not (b >=0 and b <=255):
            badParam = 'b'
            
        if badParam != '':
            raise ValueError, "Invalid parameter in ear command (%s)" % badParam
        else:
            self.commands.append(self.buildLedCommand(heure, led, r, g, b))
    
    def buildLedCommand(self, heure, led, r, g, b):
        """ return a string with the API representation of the command """
        return "%s,led,%s,%s,%s,%s" % (heure, led, r, g, b)
    
    def buildChoreography(self):
        """ returns a string with the API representation for this whole choreography """
        if len(self.commands) == 0:
            raise ValueError, "can't build an empty choreography"
        else:
            choreography = "%s" % self.tempo
            for command in self.commands:
                choreography += ",%s" % command
            return choreography
    
    # some useful constants
    # for ear commands
    EAR_LEFT = 1
    EAR_RIGHT = 0
    EAR_BACK = 1
    EAR_FRONT = 0
    # for led commands
    LED_BOTTOM = 0
    LED_LEFT = 1
    LED_MIDDLE = 2
    LED_RIGHT = 3
    LED_TOP = 4 

class Nabaztag:
    base_uri = 'http://api.nabaztag.com/vl/FR/api.jsp?'
    options = {}
    default_voice = TTSVoices.EN_6

    def __init__(self, sn, token, key=''):
        self.options['sn'] = sn
        self.options['token'] = token
        self.options['key'] = key

    def _get(self, **kwargs):
        """Fetches uri to API with given arguments"""
        options = {}
        options.update(self.options)
        options.update(kwargs)

        print self.base_uri + urllib.urlencode(options)
        try: 
            fread = urllib.urlopen(self.base_uri, urllib.urlencode(options))
        except IOError, e:
            # print error if any 
            print "Error: %s" % e
        else: 
            # or if not, print the response
            response = fread.read()
            # raw print for debugging
            print response
            # TODO: add some nicer printing here

    def sendMessage(self, idmessage):
        """Sends a message in the library or uploaded mp3"""
        print self._get(idmessage=idmessage)

    def say(self, text, voice=default_voice, speed='', pitch=''):
        """Says a message using optional voicename"""
        return self._get(tts=text, voice=voice, speed=speed, pitch=pitch)

    def play(self, urls):
        """Plays remote mp3s using given single url or list of urls"""
        if isinstance(urls, str): urls = (urls,)
        return self._get(urlList='|'.join(urls))
    
    def doChoreography(self, choreography):
        """Does the choreography specified in the given instance of the Choreography class """
        if isinstance(choreography, Choreography): 
            return self._get(chor=choreography.buildChoreography())
        else:
            raise TypeException, "Invalid parameter in doChoreography (%s)" % choreography    


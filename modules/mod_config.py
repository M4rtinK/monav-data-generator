#!/usr/bin/python
#----------------------------------------------------------------------------
# Configuration options
#
# Rename this file to mod_config.py to use it
#----------------------------------------------------------------------------
# Copyright 2007-2008, Oliver White
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#---------------------------------------------------------------------------
from base_module import ranaModule
import os #TODO: testing import, remove this
from time import clock
from configobj import ConfigObj

def getModule(m,d):
  return(config(m,d))

class config(ranaModule):
  """Handle configuration, options, and setup"""
  def __init__(self, m, d):
    ranaModule.__init__(self, m, d)
    self.userConfigPath = 'user_config.conf'
    self.userConfig = None

  def firstTime(self):

    self.set('userConfig', None) # zero the user config in case there were values stored from the last time

    # load the user config file

    self.parseUserConfig(self.userConfigPath)

    # Option: load a GPX replay
#    m = self.m.get('replayGpx', None)
#    if(m != None):
#      m.load('track.gpx')

    # Option: set your start position
    self.set("pos", (49.2, 16.616667)) # Brno
    #self.set("centred", False)  # don't keep the map centred on the start position
    #  self.set("pos_source", "default")

    # Option: set the initial view
    # WARNING: this locks to these coordinates, unless set to false
    # self.set("centreOn", False)
    
    # Option: set the map tiles
    # osma, mapnik, etc - see mod_mapTiles for list
    # currently: gmap,gsat,mapnik,osma,cycle,pyrender,localhost
    # NOTE: cycle map seems to be missing some z14 tiles
    self.set('layer',"osma")


    # Option: whether to centre on your position
    #self.set('centred', False)


      #m.load('Znaim-Wien.gpx')
      #m.load('znojmo-brno.gpx')

    # Option: True => draw circles for debuging of the track drawing mechanism optimalization
    #self.set('debugCircles', False)
    # Option: Number of threads for batch-downloading tiles
    self.set('maxBatchThreads', 5)
    # Option: Folder for storing downloaded tile images (there should be a slash at the end)
    self.set('tileFolder', 'cache/images/')
    # Option: Folder for storing POI file representations (there should be a slash at the end)
    self.set('POIFolder', 'data/poi/')
    # this sets the number of threads for bach tile download
    # even values of 10 can lead to 3000+ open sockets on a fast internet connection
    # handle with care :)
    self.set('maxDlThreads', 5)
    # this sets the number of threads used for determining the size of the batch (from http headers)
    # NOTE: even though we are downloading only the headers,
    # for a few tousand tiles this can be an unrivila amount of data
    # (so use this with caution on metered connections)
    self.set('maxSizeThreads', 20)

    # Google API key
    self.set('googleAPIKey', 'ABQIAAAAv84YYgTIjdezewgb8xl5_xTKlax5G-CAZlpGqFgXfh-jq3S0yRS6XLrXE9CkHPS6KDCig4gHvHK3lw')



  def parseUserConfig(self, path):
    """Par user created configuration file."""

    config = ConfigObj(path)

    self.userConfig = config

#    self.set('userConfig', config.dict.copy())
##    print config['cycle']['OSD']['speed']
##    self.m.get('showOSD')
#    print self.get('userConfig', None)





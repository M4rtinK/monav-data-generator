#!/usr/bin/python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Sample of a modRana device-specific module.
# It is a basic modRana module, that has some special features
# and is loaded only on the correpsponding device.
#----------------------------------------------------------------------------
# Copyright 2010, Martin Kolman
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
from base_device_module import deviceModule

# NOTE: use the device_ prefix when naming the module

def getModule(m,d,i):
  return(device_example(m,d,i))

class device_example(deviceModule):
  """A sample modRana device-specific module"""
  
  def __init__(self, m, d, i):
    deviceModule.__init__(self, m, d, i)

  def getDeviceIDString(self):
    return "n9"

  def getDeviceName(self):
    return "Nokia N9 or N950"

  def getWinWH(self):
    """N9/N950 screen resolution"""
    return ((854,480))

  def startInFullscreen(self):
    """
    non-fullscreen mode just draw some weird toolbar & status-bar
    on Harmattan
    """
    return True

  def fullscreenOnly(self):
    """
    basically no need to
    """
    return True

  def screenBlankingControlSupported(self):
    # TODO: screen blanking support
    return False

  def getLocationType(self):
    return "qt_mobility"

  def hasButtons(self):
    # TODO: support for volume buttons
    return False


  # ** LOCATION **

  def handlesLocation(self):
    """using Qt Mobility"""
    return False

  def startLocation(self):
    pass

  def stopLocation(self):
    pass


  # ** PATHS **

  # NOTE: basically the same as on
  # maemo 5 on the N900

  def getTracklogFolderPath(self):
    return "/home/user/MyDocs/tracklogs"

  def getMapFolderPath(self):
    return "/home/user/MyDocs/.maps/"

  def getPOIFolderPath(self):
    return "/home/user/MyDocs/.maps"

  def getLogFolderPath(self):
    return "/home/user/MyDocs/modrana_debug_logs/"

  def needsQuitButton(self):
    """No need for a separate Quit button thanks to Swipe UI"""
    return False

if(__name__ == "__main__"):
  a = device_example({}, {})
  a.update()
  a.update()
  a.update()
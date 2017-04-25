#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#     Copyright (C) 2015 Tim Ker
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import xbmcaddon
import xbmcgui
import xbmc
import sys
import subprocess
import os

addon = xbmcaddon.Addon()
addon_name = addon.getAddonInfo('name')
addon_path = addon.getAddonInfo('path')


def ensurePath():
	 binPath = '/opt/vc/bin'
	 paths = os.environ["PATH"].split(os.pathsep)
	 if binPath not in paths:
		 os.environ["PATH"] += os.pathsep + binPath     
     
class Screensaver(xbmcgui.WindowXMLDialog):

    class ExitMonitor(xbmc.Monitor):

        def __init__(self, exit_callback):
            self.exit_callback = exit_callback

        def onScreensaverDeactivated(self):
            self.exit_callback()

    def onInit(self):
        self.log('onInit')
        ensurePath()
        subprocess.Popen(['vcgencmd', 'display_power', '0'])
        self.set_cpu_governor('powersave')
        self.set_led(1, 'none', 1)
        self.exit_monitor = self.ExitMonitor(self.exit)

    def exit(self):
        self.abort_requested = True
        self.exit_monitor = None
        subprocess.Popen(['vcgencmd', 'display_power', '1'])
        self.set_cpu_governor('ondemand')
        self.set_led(1, 'input')
        self.log('exit')
        self.close()
        
    def set_cpu_governor(self, governor):
        self.write('/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor', governor)

    def set_led(self, index, trigger, value=-1):
        self.write('/sys/class/leds/led%d/trigger' % index, trigger)
        if value >= 0:
            self.write('/sys/class/leds/led%d/brightness' % index, str(value))

    def write(self, file, content):
        fd = os.open(file, os.O_WRONLY)                                                                                    
        os.write(fd, content)                                                                                                                                                
        os.close(fd)                                                                                                                                                          
        del fd                                                                                                                                                                
        

    def log(self, msg):
        xbmc.log(u'pimon hdmi screensaver: %s' % msg)


if __name__ == '__main__':
    screensaver = Screensaver(
        'script-%s-main.xml' % addon_name,
        addon_path,
        'default',
    )
    screensaver.doModal()
    del screensaver
    sys.modules.clear()

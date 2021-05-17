# coding=utf-8
from __future__ import absolute_import

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin
import board
import adafruit_dht
from Device import Device
import time

class ClimatemonitorPlugin(octoprint.plugin.SettingsPlugin,
                           octoprint.plugin.AssetPlugin,
                           octoprint.plugin.TemplatePlugin,
						   octoprint.plugin.StartupPlugin):

	
	def on_startup(self):
		self.devices = []
		for k in self._settings.get(["sensors"]).keys():
			kwargs = dict(self._settings.get(['sensors',k]))
			self.devices.append(
				Device(**kwargs)
			)
		

	def on_after_startup(self):
		self._logger.info(f"CLIMATE LOG: {self._settings.get([])}")

	##~~ SettingsPlugin mixin

	def get_settings_defaults(self):
		return {
			"active_sensors": ["ambient", "enclosure"],
			"sensors": {
				"enclosure":{
					"data_pin": 4,
					"reads_per_min": 5
				},
				"ambient":{
					"data_pin": 11,
					"reads_per_min": 2
				}
			},
			"use_celsius":True,
			"notifications": {
				"temp_delta":False,
				"humidity_delta":False
			}
		}


	# def get_template_vars(self):
	# 	return {
	# 		"ambient_sensor_data_pin_number": self._settings.get(["ambient_sensor_data_pin_number"]),
	# 		"enclosure_sensor_data_pin_number": self._settings.get(["enclosure_sensor_data_pin_number"]),
	# 		"updates_per_min":  self._settings.get(["updates_per_min"])
	# 	}


	def get_template_configs(self):
		return [
			dict(type="navbar", custom_bindings=False),
			dict(type="settings", custom_bindings=False)
		]
		

	##~~ AssetPlugin mixin

	def get_assets(self):
		# Define your plugin's asset files to automatically include in the
		# core UI here.
		return dict(
			js=["js/ClimateMonitor.js"],
			css=["css/ClimateMonitor.css"],
			less=["less/ClimateMonitor.less"]
		)

	##~~ Softwareupdate hook

	def get_update_information(self):
		# Define the configuration for your plugin to use with the Software Update
		# Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
		# for details.
		return dict(
			ClimateMonitor=dict(
				displayName="Climatemonitor Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="Conor-Carmichael",
				repo="OctoPrint-Climatemonitor",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/Conor-Carmichael/OctoPrint-Climatemonitor/archive/{target_version}.zip"
			)
		)


	## Sensor reading fns 
	def _read_sensor(self):
		# h/t https://www.piddlerintheroot.com/dht22/
		try:
			if self._devices_init_done :
				readings = {
					"ambient": {
						"temperature": self.ambient_device.temperature,
						"humidity": self.ambient_device.temperature
					},
					"enclosure": {
						"temperature": self.enclosure_device.temperature,
						"humidity": self.enclosure_device.temperature
					},
					"errors": "None"
				}
			else:
				raise RuntimeError("Devices not yet initialized.")
				
		except Exception as error:
			self._logger.info(f"Device reading error: {str(error)}")
			readings = {"errors": str(error)}
		finally:
			return readings





# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Climatemonitor Plugin"

# Starting with OctoPrint 1.4.0 OctoPrint will also support to run under Python 3 in addition to the deprecated
# Python 2. New plugins should make sure to run under both versions for now. Uncomment one of the following
# compatibility flags according to what Python versions your plugin supports!
#__plugin_pythoncompat__ = ">=2.7,<3" # only python 2
__plugin_pythoncompat__ = ">=3,<4" # only python 3
#__plugin_pythoncompat__ = ">=2.7,<4" # python 2 and 3

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = ClimatemonitorPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}


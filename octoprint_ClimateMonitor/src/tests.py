from octoprint_ClimateMonitor.src.utils import *
from octoprint_ClimateMonitor.src.Device import Device
from octoprint_ClimateMonitor import ClimatemonitorPlugin



def test_c_to_f():
    assert convert_c_to_f(-10) == 14
    assert convert_c_to_f(0) == 32.0 
    assert convert_c_to_f(32) == 89.6
    

def test_f_to_c():
    assert convert_f_to_c(32) == 0


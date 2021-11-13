import win32api as win32
import win32con
import sys
import re
x = 0
args=sys.argv[1].lower()
rotation_val=0
m = re.search("(?<=^-rotate=)\S+", args)    # Use non-white character wildcard instead of d decimal
if (m != None):
    #print m.group(0)
    if ((m.group(0) == "180")):
        rotation_val=win32con.DMDO_180
    elif((m.group(0) == "90")):
        rotation_val=win32con.DMDO_270
    elif ((m.group(0) == "270")):   
        rotation_val=win32con.DMDO_90
    else:
        rotation_val=win32con.DMDO_DEFAULT

device = win32.EnumDisplayDevices(None,x)
dm = win32.EnumDisplaySettings(device.DeviceName,win32con.ENUM_CURRENT_SETTINGS)
if((dm.DisplayOrientation + rotation_val)%2==1):
    dm.PelsWidth, dm.PelsHeight = dm.PelsHeight, dm.PelsWidth   
dm.DisplayOrientation = rotation_val

win32.ChangeDisplaySettingsEx(device.DeviceName,dm)
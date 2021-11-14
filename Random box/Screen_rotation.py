#API to interact with win32
#https://mhammond.github.io/pywin32/win32api.html
#http://timgolden.me.uk/pywin32-docs/contents.html
import win32api as win32

#Win32 constants
#https://github.com/SublimeText/Pywin32/blob/master/lib/x32/win32/lib/win32con.py
import win32con

import sys

#Regular expressions (pattern matching search for strings)
import re


#Display device number
x = 0


#Get arguments passed to the script, as a string
args=sys.argv[1].lower()

rotation_val=0


#Matches argument string to a pattern and extracts rotation value.
#Returns a search object, m.group(0) gives the entire search result.
m = re.search("(?<=^-rotate=)\S+", args)    # Use non-white character wildcard instead of d decimal


#The pattern matching would return None if there were no matches
if (m != None):
    #win32con.DMDO_? are the constants related to screen rotation.
    #0º (default) = int(0)
    #90º = 1
    #180º = 2
    #270º = 3
    if ((m.group(0) == "180")):
        rotation_val=win32con.DMDO_180
    elif((m.group(0) == "90")):
        rotation_val=win32con.DMDO_270
    elif ((m.group(0) == "270")):   
        rotation_val=win32con.DMDO_90
    else:
        rotation_val=win32con.DMDO_DEFAULT


#Get info on device (used to get DeviceName)
device = win32.EnumDisplayDevices(None,x)
'''EnumDisplayDevices(Device = None, DevNum = 0)
        Gives info on a display device.
        
        Device  string   Name of the device. None will search by DevNum.
        DevNum  int      Index of the device (starts at 0).
        
        Returns a PyDISPLAY_DEVICE object:
            Methods     Clear       Reset all members of the structure
            
            Properties  Size            int     Size of structure
                        DeviceName      str     At most 32 chars
                        DeviceString    str     At most 128 chars
                        StateFlags      int     win32con.DISPLAY_DEVICE_ indicating current device status
                        DeviceID        str     At most 128 chars
                        DeviceKey       str     At most 128 chars
'''


#Get device settings in a PyDEVMODE object
dm = win32.EnumDisplaySettings(device.DeviceName,win32con.ENUM_CURRENT_SETTINGS)
'''EnumDisplaySettings(DeviceName = None, ModeNum = 0)
        Lists settings for the specified device.
        
        DeviceName  string  Name of device (from EnumDisplayDevices). None for default display device.
        ModeNum     int     Index of setting:
                                 0  Default (???)
                                -1  win32con.ENUM_CURRENT_SETTINGS
                                -2  win32con.ENUM_REGISTRY_SETTINGS
        
        Returns a PyDEVMODE object:
            Methods     Clear       Reset all members of the structure
            Properties  Size                int     Size of structure
                        DeviceName          str     At most 32 chars
                        Position_x          int     Position relative to desktop
                        Position_y          int     Position relative to desktop
                        DisplayOrientation  int     DMDO_DEFAULT,DMDO_90, DMDO_180, DMDO_270 or 0, 1, 2, 3
                        DisplayFrequency    int     Display refresh rate
                        Other display properties:
                        DisplayFixedOutput  int     ??? DMDFO_DEFAULT, DMDFO_CENTER, DMDFO_STRETCH
                        LogPixels           int     Pixels per inch
                        BitsPerPel          int     Color resolution in bits per pixel
                        PelsWidth           int     Pixel width of display
                        PelsHeight          int     Pixel height of display
                        DisplayFlags        int     ??? Combination of DM_GRAYSCALE and DM_INTERLACED
                        DitherType          int     win32con.DMDITHER*
                        DriverData          str     Driver data
                        There are more printer-related properties.
'''


#Changing shape of display if it turns into a vertical one (90º or 270º)
if((dm.DisplayOrientation + rotation_val)%2==1):
    dm.PelsWidth, dm.PelsHeight = dm.PelsHeight, dm.PelsWidth


#Change the rotation value in the PyDEVMODE object
dm.DisplayOrientation = rotation_val


#Pass PyDEVMODE object to set settings for device
win32.ChangeDisplaySettingsEx(device.DeviceName,dm)
'''ChangeDisplaySettingsEx(DeviceName = None, DevMode = None)
        Changes settings for the display device.
        
        DeviceName  string              Name of device (from EnumDisplayDevices). None for default display device.
        DevMode     PyDEVMODE object    A PyDEVMODE object with settings (from EnumDisplaySettings). None for default.
        
        Returns status int:
            DISP_CHANGE_SUCCESSFUL = 0
            DISP_CHANGE_RESTART = 1
            DISP_CHANGE_FAILED = -1
            DISP_CHANGE_BADMODE = -2
            DISP_CHANGE_NOTUPDATED = -3
            DISP_CHANGE_BADFLAGS = -4
            DISP_CHANGE_BADPARAM = -5
            DISP_CHANGE_BADDUALVIEW = -6
'''
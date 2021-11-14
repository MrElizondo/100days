import win32api as win32
import win32con
import os


n = 0
try:
    device = win32.EnumDisplayDevices(None,n)
except:
    print('Device number not found.')
    os.system('pause')
    quit()

settings = win32.EnumDisplaySettings(device.DeviceName, win32con.ENUM_CURRENT_SETTINGS)

old_orientation = settings.DisplayOrientation

if old_orientation == win32con.DMDO_DEFAULT:
    settings.DisplayOrientation = win32con.DMDO_270
else:
    settings.DisplayOrientation = win32con.DMDO_DEFAULT

if old_orientation != win32con.DMDO_180:
    settings.PelsWidth, settings.PelsHeight = settings.PelsHeight, settings.PelsWidth

success = win32.ChangeDisplaySettingsEx(device.DeviceName, settings)

if success == win32con.DISP_CHANGE_SUCCESSFUL:
    print('Screen successfully rotated.')
else:
    print('There was an error:', success)

os.system('pause')

'''Error codes:
    DISP_CHANGE_SUCCESSFUL = 0
    DISP_CHANGE_RESTART = 1
    DISP_CHANGE_FAILED = -1
    DISP_CHANGE_BADMODE = -2
    DISP_CHANGE_NOTUPDATED = -3
    DISP_CHANGE_BADFLAGS = -4
    DISP_CHANGE_BADPARAM = -5
    DISP_CHANGE_BADDUALVIEW = -6
'''
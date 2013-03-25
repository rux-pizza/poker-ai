import platform

if platform.system() == "Darwin":
	import screencap_mac_quartz as cap
elif platform.system() == "Windows":
	import screencap_windows_wxpython as cap
else:#Linux most probably
	import screencap_windows_wxpython as cap
#Milou love classes
ScreenCapture = cap.ScreenCapture
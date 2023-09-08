import platform

play_command = None
default_libpath = None

system = platform.system()
release = platform.release()
machine = platform.machine()
uname = platform.uname()

print("System:" + system)
print("Release:" + release)
print("Machine:" + machine)
print("Uname:" + str(uname))

if system == "Darwin":
	from cross_record import AudiostreamSource
	play_command ="play -q"
	default_libpath = '../lib/mac/libnyumaya.dylib'

elif system == "Linux":
	from record import AudiostreamSource
	play_command = "aplay"
	if(machine == "x86_64"):
		default_libpath = "../../lib/linux_x86_64/libnyumaya_premium.so.3.1.0"

	elif(machine == "armv6l"):
		default_libpath = '../../lib/rpi/armv6/libnyumaya_premium.so.3.1.0'

	#Pi3 says it's armv7 although its armv8
	elif(machine == "armv7l"):
		default_libpath = '../../lib/rpi/armv8/libnyumaya_premium.so.3.1.0'

	elif(machine == "aarch64"):
		default_libpath = '../../lib/rpi/aarch64/libnyumaya_premium.so.3.1.0'

	else:
		print("Machine not supported")
		print("Please setup a match for your machine in python/src/auto_platform.py")

elif system == "Windows":
	print("Windows is currently not supported")

else:
	print("Your OS is currently not supported")



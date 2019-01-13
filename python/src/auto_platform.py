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
	play_command ="play -q"
	
	from cross_record import AudiostreamSource
	default_libpath = '../lib/mac/libnyumaya.dylib'
	
elif system == "Linux":
	from record import AudiostreamSource
	play_command = "aplay"
	if(machine == "x86_64"):
		default_libpath = '../lib/linux/libnyumaya.so'
	elif(machine == "armv6l"):
		default_libpath = '../lib/rpi/armv6/libnyumaya.so'
	elif(machine == "armv7l"):
		default_libpath = '../lib/rpi/armv7/libnyumaya.so'
	else:
		print("Machine not supported")
		
elif system == "Windows":
	print("Windows is currently not supported")

else:
	print("Your OS is currently not supported")



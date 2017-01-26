import os, time, sys
folder = 'static/images'
second_time = 86400 #1 day

while(True):
	time.sleep(60)
	now = time.time()
	for subdir, dirs, files in os.walk(folder):
	    for file in files:
	    	path_file = os.path.join(subdir, file)
	    	if "fractal" in file:
				if os.stat(path_file).st_mtime < now - second_time:
					os.remove(path_file)


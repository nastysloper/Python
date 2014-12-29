import subprocess

print "start"
# subprocess.call("./powdiddy.sh", shell=True)
# don't need shell=True if first line of shell script is path to shell
subprocess.call("./powdiddy.sh")
print "end"
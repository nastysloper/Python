import subprocess
import os
import sys
# import path

class cd:
  """Context manager for changing the current working directory"""
  def __init__(self, newPath):
    self.newPath = newPath

  def __enter__(self):
    self.savedPath = os.getcwd()
    os.chdir(self.newPath)

  def __exit__(self, etype, value, traceback):
    os.chdir(self.savedPath)

repos = ['bt', 'cadence', 'puppetry']
for repo in repos:
  print "Updating the following repo: %s" % repo
  with cd(repo):
    # get current dir
    current = os.path.abspath('.')
    print "current dir is %s" % current
    subprocess.call("ls")
    task = subprocess.Popen(['git', 'status', '--porcelain'], stdout=subprocess.PIPE)
    flag = False
    for l in task.stdout.readlines():
      flag = True
      print "This file is not committed\n  %s" % l.split()[1]

    if flag:
      print("Please commit, checkout, or stash your changes.")
    else:
      print "No changes here!"

print "current dir is %s" % os.getcwd()
print "exiting!"

sys.exit()


# else:
#   print "pull"
#   fetch = subprocess.Popen(['git', 'fetch'])
#   fetch.communicate([0])
#   merge = subprocess.Popen(['git', 'merge', '--ff-only'])
#   fetch.communicate([0])

print "\nNow running cd"
print "we are in %s" % current
# current = os.getcwd()
# returns back to current directory
with cd("/Users/richvogt/Code"):
  subprocess.call("ls")

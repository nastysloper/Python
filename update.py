import subprocess
import os
import sys
import time
import re

def checkout(file):
  print "in checkout"
  subprocess.call(['git', 'checkout', '--', file])

def unstage(file):
  subprocess.call(['git', 'reset', 'HEAD', file])

def stash(file):
  subprocess.call(['git', 'stash'])

def add(file):
  subprocess.Popen(['git', 'add', file])
  print "%s added / updated." % file

def commit(file):
  print "Please enter a commit message:"
  message = raw_input()
  subprocess.call(['git', 'commit', '-m', message])

def add(file):
  subprocess.call(['git', 'add', file])

def manage_untracked_file(file):
  subprocess.call(['git', 'add', file])
  print "%s added to the staging area." % file
  while True:
    print "do you want to (c) commit this file or (s) stash it?"
    print "enter (u) if you would like to undo this change."
    command = raw_input()
    if command in {'c', 's', 'u'}:
      break
    print "\nI don't recognize %s\n\n" % command
  options = {
    "s" : stash,
    "c" : commit,
    "u" : checkout
  }
  options[command](file)

def manage_untracked_changes(file):
  while True:
    print "This file has unstaged changes: %s" % file
    print "Do you want to (a) add or (c) checkout these changes?"
    command = raw_input()
    if command in {'a', 'c'}:
      break
    print "I don't recognize %s\n\n" % command
  options = {
    "a" : add,
    "c" : checkout
  }
  options[command](file)
  manage_staged(file)

def manage_staged(file):
  while True:
    print "this file is added to the staging area but not committed: %s" % file
    print "do you want to (c) commit, (u) unstage, or (s) stash this file?"
    command = raw_input()
    if command in {'c', 'u', 's'}:
      break
    print "I don't recognize %s\n\n" % command
  options = {
    "s" : stash,
    "c" : commit,
    "u" : unstage
  }
  options[command](file)

status = subprocess.Popen(['git', 'status', '--porcelain', '-b'], stdout=subprocess.PIPE)
for l in status.stdout.readlines():
  result = re.search('\[ahead.*\]', l)
  if result:
    print "Your branch is ahead of origin => %s" % result.group()
    time.sleep(.5)
    sys.exit()

task = subprocess.Popen(['git', 'status', '--porcelain'], stdout=subprocess.PIPE)
flag = False
for l in task.stdout.readlines():
  flag = True
  status = l.split()[0]
  file = l.split()[1]
  print status
  if status == "A":
    manage_staged(file)
  elif status in {'M', 'MM'}:
    print "this file has changes: %s\n" % file
    manage_untracked_changes(file)
  elif status == "??":
    print "This file is untracked: %s\n" % file
    print "Do you want to (i) ignore this file or do you want git to (t) track it?"
    command = raw_input()
    if command == 't':
      manage_untracked_file(file)
  elif status == "AM":
    manage_untracked_changes(file)
    manage_staged(file)
  elif status == "AA":
    # AA is unmerged path. Exiting to let user examine diff.
    subprocess.call(['git', 'status'])
    time.sleep(.5)
    sys.exit()
    
print "pull"
subprocess.call(['git', 'fetch'])
subprocess.call(['git', 'merge', '--ff-only'])

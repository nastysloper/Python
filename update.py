import subprocess
import os
import sys

def checkout(file):
  print "in checkout"
  co = subprocess.Popen(['git', 'checkout', '--', file], stdout=subprocess.PIPE)
  co.communicate()

def unstage(file):
  co = subprocess.Popen(['git', 'reset', 'HEAD', file],)
  co.communicate()
  print "%s unstaged." % file

def stash(file):
  stash = subprocess.Popen(['git', 'stash'])
  stash.communicate()

def commit(file):
  print "Please enter a commit message:"
  message = raw_input()
  commit = subprocess.Popen(['git', 'commit', '-m', message])
  commit.communicate()

def add(file):
  add = subprocess.Popen(['git', 'add', file])
  add.communicate()
  # print "%s added / updated." % file
  print "yes, stashed %s" % file

def commit(file):
  print "yes, commit %s" % file

def add(file):
  add = subprocess.Popen(['git', 'add', file], stdout=subprocess.PIPE)
  add.communicate()
  print "%s added / updated." % file

def manage_untracked_file(file):
  add = subprocess.Popen(['git', 'add', file], stdout=subprocess.PIPE)
  add.communicate()
  print "%s added to the staging area." % file
  print "do you want to (c) commit this file or (s) stash it?"
  print "enter (u) if you would like to undo this change."
  command = raw_input()
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

status = subprocess.Popen(['git', 'status', '-sb'], stdout=subprocess.PIPE)
for l in status.stdout.readlines():
  print l.split()

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
  elif status == "??":
    print "This file is untracked: %s\n" % file
    print("Do you want to (i) ignore this file or do you want git to (t) track it?")
    command = raw_input()
    if command == 't':
      manage_untracked_file(file)
  elif status == "AM":
    manage_untracked_changes(file)
    manage_staged(file)
  elif status == "AA":
    # AA is unmerged path. Exiting to let user examine diff.
    status = subprocess.Popen(['git', 'status'])
    sys.exit()
    
# print "No changes here!"
# print "pull"
# fetch = subprocess.Popen(['git', 'fetch'])
# fetch.communicate([0])
# merge = subprocess.Popen(['git', 'merge', '--ff-only'])
# fetch.communicate([0])

print "exiting!"

# sys.exit()
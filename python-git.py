from git import *

repo = Repo("/Users/richvogt/Code/python")
assert repo.bare == False

# dirty means untracked files present?
status = repo.is_dirty()
if status == True:
  print status
else:
  print("Not true")

untracked_files = repo.untracked
print untracked_files


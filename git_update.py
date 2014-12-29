#!/usr/bin/python

import subprocess

subprocess.call(["git", "branch", "-a"])
subprocess.call(["git", "status"])

print("That's all...")

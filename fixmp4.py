import os
import re
import subprocess

rootdir = "tmp/"
regex = re.compile(r"\d*\.mp4")



for root, dirs, files in os.walk(rootdir):
  for file in files:
    if regex.match(file):
        rawCommand = 'cd {} && towebm {}'
        command = rawCommand.format(root, file)
        subprocess.run(command,shell=True)
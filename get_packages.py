import subprocess as sp

cmd = 'pip freeze'
packages = str(sp.check_output(cmd, shell=True), 'utf-8')[0:-1]
file = open('packages.txt', 'w')
file.write(packages)
file.close()

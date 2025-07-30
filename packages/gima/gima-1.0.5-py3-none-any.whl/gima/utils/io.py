'''
Created on Jul 15, 2025

@author: ahypki
'''
from utils.Logger import Logger
import subprocess
from utils.regex import firstGroup

def linux_cmd(cmd, workingDir = None, printImmediatelly = False):
    if printImmediatelly:
        Logger.logDebug("linux cmd: " + cmd);
    result = []
    s = subprocess.Popen(cmd, cwd = workingDir, shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    for line in s.stdout.readlines():
        strLine = str(line).rstrip()
#         if printImmediatelly is False:
        result.append(firstGroup(strLine, 'b\'(.*)\\\\n\''))
#         else:
        if printImmediatelly:
            print(firstGroup(strLine, 'b\'(.*)\\\\n\''))
    return result
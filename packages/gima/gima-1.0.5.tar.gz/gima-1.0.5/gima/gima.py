'''
Created on Jul 10, 2025

@author: ahypki
'''
import os
from sys import path
import sys

from db.Database import Database
from git.GitRepo import GitRepo
from utils.args import getArgString, isArgPresent
from git.Settings import Settings
from utils.Logger import Logger


database = Database()

def prompt(gitRepo, readCommand = False):
    path = gitRepo.getPath()
    status = None
    if gitRepo.isClean():
        status = Logger.GREEN + 'clean' + Logger.ENDC
    else:
        status = Logger.WARNING + gitRepo.statusShort() + Logger.ENDC 
    
    prompt = Settings.PREFIX_LINE\
            + Logger.BLUE + 'gim > ' + Logger.ENDC \
            + ('[' + (status).rjust(18, " ") + '] ' if status is not None else '') \
            + Logger.BLUE + str(path) + Logger.ENDC \
            + ' > '
    if readCommand:
        print(prompt, end = '', flush = True)
        return sys.stdin.readline().strip()
    else:
        Logger.logInfo(prompt, printLogLevel = False)

def printUsage():
    Logger.logInfo(Logger.BLUE + 'gim usage:' + Logger.ENDC, printLogLevel=False)
    Logger.logInfo('\t{} - prints summary'.format((Logger.GREEN + '--summary' + Logger.ENDC).rjust(18, ' ')), printLogLevel=False)
    Logger.logInfo('\t{} - interactively make a commit'.format((Logger.GREEN + '--commit [--group ... --path ...]' + Logger.ENDC).rjust(18, ' ')), printLogLevel=False)
    Logger.logInfo('\t\t{} - add file(s) by id, idFrom-idTo or using wildcard pattern'.format((Logger.GREEN + 'a pattern' + Logger.ENDC).ljust(18, ' ')), printLogLevel=False)
    Logger.logInfo('\t\t{} - ignore file(s) by id, idFrom-idTo or using wildcard pattern'.format((Logger.GREEN + 'i pattern' + Logger.ENDC).ljust(18, ' ')), printLogLevel=False)
    Logger.logInfo('\t\t{} - commit'.format((Logger.GREEN + 'c' + Logger.ENDC).ljust(18, ' ')), printLogLevel=False)
    Logger.logInfo('\t\t{} - commit and then push'.format((Logger.GREEN + 'cp' + Logger.ENDC).ljust(18, ' ')), printLogLevel=False)
    Logger.logInfo('\t\t{} - push only'.format((Logger.GREEN + 'push' + Logger.ENDC).ljust(18, ' ')), printLogLevel=False)
    Logger.logInfo('\t\t{} - pull only'.format((Logger.GREEN + 'pull' + Logger.ENDC).ljust(18, ' ')), printLogLevel=False)
    Logger.logInfo('\t\t{} - go to the next repository'.format((Logger.GREEN + 'n' + Logger.ENDC).ljust(18, ' ')), printLogLevel=False)
    Logger.logInfo('\t\t{} - quit'.format((Logger.GREEN + 'q' + Logger.ENDC).ljust(18, ' ')), printLogLevel=False)
    Logger.logInfo('\t{} - scans for git repos in the current folder or in the folder specified with --param'.format((Logger.GREEN + '--scan [--path ...]' + Logger.ENDC).rjust(18, ' ')), printLogLevel=False)
    
def commitOneRepo(repo):
    while True:
        Logger.logInfo(Settings.SEPARATOR_NEXT_REPO, printLogLevel= False)
        gitRepo = GitRepo(repo)
        if gitRepo.isGitRepo():
            items, size = gitRepo.status()
            if (len(items) > 0):
                cmd = prompt(gitRepo, True)
                
                if cmd.startswith('cp '):
                    msg = cmd[2:].strip()
                    gitRepo.commit(msg)
                    gitRepo.push()
                elif cmd.startswith('c '):
                    msg = cmd[2:].strip()
                    gitRepo.commit(msg)
                elif cmd.startswith('a '):
                    if size > Settings.MAX_COMMIT_BYTES:
                        Logger.logWarn('Already added {} MB in this commit, skipping'.format(str(size / 1_000_000)))
                    else:
                        pattern = cmd[1:].strip()
                        gitRepo.add(pattern)
                elif cmd.startswith('i '):
                    pattern = cmd[1:].strip()
                    gitRepo.ignore(pattern)
                elif cmd.startswith('push'):
                    gitRepo.push()
                elif cmd.startswith('pull'):
                    gitRepo.pull()
                elif cmd.startswith('l'):
                    pass
                elif cmd.startswith('n'):
                    break
                elif cmd.startswith('q'):
                    # break checking other repos
                    return True
                else:
                    Logger.logError('Unknown command: {}'.format(cmd))
            else:
                prompt(gitRepo)
                break
        else:
            # not a git repo
            Logger.logError("Not a git repo in {}".format(repo))
            break
        
def commit():
    if isArgPresent("path"):
        commitOneRepo(getArgString("path", None))
    else:
        for repo in database.iterateRepos(getArgString('group', None)):
            if (os.path.exists(repo)):
                if commitOneRepo(repo):
                    break

def scan():
    currentDir = os.getcwd()
    if getArgString('path', None) is not None:
        currentDir = getArgString('path', None)
        
    foldersSkip = []
    foldersCountAll = 0
    foldersCountIgnored = 0
    foldersCountGitRepos = 0
    
    Logger.logInfo('Scanning {}...'.format(currentDir))
        
    for subdir, dirs, files in os.walk(currentDir):
        subdir = str(subdir)
        
        # statistics
        foldersCountAll += 1
        if (foldersCountAll == 100
            or foldersCountAll == 1000 
            or foldersCountAll % 10000 == 0):
            Logger.logInfo("{} folders scanned, {} ignored, {} already tracking".format(foldersCountAll, foldersCountIgnored, foldersCountGitRepos))
        
        # check if folder was checked already
        skip = False
        for ign in foldersSkip:
            if subdir.startswith(ign):
                # logDebug('Already checked ' + subdir)
                skip = True
                break
        if skip:
            continue
                    
        # check if the folder is ignored in the database
        if database.isIgnored(subdir):
            gitRepo = GitRepo(subdir)
            if gitRepo.isGitRepo():
                foldersSkip.append(subdir)
                foldersCountIgnored += 1
            # logDebug('Ignored in database ' + subdir)
            continue
            
        gitRepo = GitRepo(subdir)
        if gitRepo.isGitRepo():
            subdir = str(gitRepo.getPath())
            if subdir not in foldersSkip and not database.isRepoPresent(subdir):
            #     logInfo("Git repo in {} is ignored".format(subdir))
            # else:
                Logger.logInfo("{} > [A]dd/[I]gnore/ignore [R]ecursivelly/[S]kip for now".format(Logger.BLUE + subdir + Logger.ENDC))
                cmd = sys.stdin.readline().strip()
                if cmd.lower() == "a":
                    database.addRepo(subdir)
                elif cmd.lower() == "i":
                    database.ignore(subdir)
                elif cmd.lower() == "r":
                    database.ignoreAll(subdir)
                elif cmd.lower() == "s":
                    pass
            else:
                foldersCountGitRepos += 1

            foldersSkip.append(str(subdir))
    Logger.logInfo("{} folders scanned, {} ignored, {} already tracking".format(foldersCountAll, foldersCountIgnored, foldersCountGitRepos))
    
if __name__ == '__main__':
    if isArgPresent('verbose'):
        DEBUG = True
    
    if (isArgPresent('summary')):
        database.printSummary(None)
    elif (isArgPresent('ignore')):
        database.ignore(getArgString('ignore', None))
    elif (isArgPresent('ignore-all')):
        database.ignoreAll(getArgString('ignore-all', None))
    elif (isArgPresent('commit')):
        commit()
    elif (isArgPresent('scan')):
        scan()
    else:
        printUsage()
        
    Logger.logInfo('Finished!')
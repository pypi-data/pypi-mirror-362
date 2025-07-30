'''
Created on Jul 10, 2025

@author: ahypki
'''

class Logger:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    
    DEBUG = False
    INFO = True
    
    def logDebug(msg, printLogLevel = True, printNewLine = True):  # @NoSelf
        if Logger.DEBUG:
            print(("DEBUG " if printLogLevel else '') 
                  + str(msg), 
                  end = ('\n' if printNewLine else ''))
    
    def logInfo(msg, printLogLevel = True, printNewLine = True):  # @NoSelf
        if Logger.INFO:
            print(("INFO  " if printLogLevel else '') 
                  + str(msg), 
                  end = ('\n' if printNewLine else ''))
        
    def logWarn(msg, printLogLevel = True, printNewLine = True):  # @NoSelf
        print(("WARN  " if printLogLevel else '') 
              + str(msg), 
              end = ('\n' if printNewLine else ''))
    
    def logError(msg, printLogLevel = True, printNewLine = True):  # @NoSelf
        print(("ERROR " if printLogLevel else '') 
              + str(msg), 
              end = ('\n' if printNewLine else ''))

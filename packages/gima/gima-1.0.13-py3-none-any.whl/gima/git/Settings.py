'''
Created on Jul 15, 2025

@author: ahypki
'''

class Settings(object):
    '''
    classdocs
    '''

    MAX_COMMIT_BYTES = 5_000_000
    
    SEPARATOR_NEXT_REPO = '############################################################'
    PREFIX_LINE = "# "

    def __init__(self, params):
        '''
        Constructor
        '''
        
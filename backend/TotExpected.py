from infofile import infos
from keyTranslate import keyTranslate

def TotExpected(dataKey):
    """
    Function which returns the total number of generated Monte Carlo events for a given data
    set.
    """

    newDataKey = keyTranslate[dataKey] # look up ATLAS key name

    return infos[newDataKey]["xsec"] * 10.064 * 1000 

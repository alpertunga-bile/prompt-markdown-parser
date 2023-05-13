from subprocess import call
from os import name

def ClearTerminal():
    call('cls' if name=='nt' else 'clear', shell=True)

def MainOperationComplete(text, state):
    volcab = ['parse', 'clear', 'cls', 'create', 'civitai', 'train', 'evaluate', 'exit', 'generate']
    results = [x for x in volcab if x.startswith(text)] + [None]
    return results[state]

def Clamp(number, min, max):
    number = number if number > min else min
    number = number if number < max else max

    return number

def CreatorOperationComplete(text, state):
    volcab = ['enhance', 'prune', 'frequency', 'clear', 'cls', 'exit']
    results = [x for x in volcab if x.startswith(text)] + [None]
    return results[state]

def CreatorNSFWComplete(text, state):
    volcab = ['none', 'soft', 'mature', 'x']
    results = [x for x in volcab if x.startswith(text)] + [None]
    return results[state]

def CreatorSortComplete(text, state):
    volcab = ['most_reactions', 'most_comments', 'newest']
    results = [x for x in volcab if x.startswith(text)] + [None]
    return results[state]

def CreatorPeriodComplete(text, state):
    volcab = ['allTime', 'year', 'month', "week", "day"]
    results = [x for x in volcab if x.startswith(text)] + [None]
    return results[state]

def ParserOperationComplete(text, state):
    vocab = ['allParse', 'exit', 'parse']
    results = [x for x in vocab if x.startswith(text)] + [None]
    return results[state]

def YesNoComplete(text, state):
    vocab = ['yes', 'no']
    results = [x for x in vocab if x.startswith(text)] + [None]
    return results[state]

def GenerateOrSetComplete(text, state):
    vocab = ['generate', 'set', 'exit', 'clear', 'cls', 'print']
    results = [x for x in vocab if x.startswith(text)] + [None]
    return results[state]

def SelectVariableToSet(text, state):
    vocab = ['minLength', 'maxLength', 'doSample', 'earlyStop', 'recursiveLevel', 'selfRecursive']
    results = [x for x in vocab if x.startswith(text)] + [None]
    return results[state]
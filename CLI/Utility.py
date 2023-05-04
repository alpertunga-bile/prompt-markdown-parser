from subprocess import call
from os import name

def ClearTerminal():
    call('cls' if name=='nt' else 'clear', shell=True)

def MainOperationComplete(text, state):
    volcab = ['parse', 'clear', 'cls', 'create', 'train', 'evaluate', 'exit', 'generate']
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
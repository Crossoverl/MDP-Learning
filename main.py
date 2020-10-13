import sys
import copy

def readData():
    dataFile = open(sys.argv[3], 'r')
    data = dict()
    for line in dataFile.readlines():
        string = str(line)
        space = string.find(" ")
        state = string[0:space]
        string = string.replace(')', '')
        data[state] = string[space:].rsplit("(")
    if len(data) != numStates:
        print("Number of states in file does not match state number given")
        exit()
    for state in data:
        ind = 0
        for elem in data[state]:
            elem = elem.strip()
            data[state][ind] = elem
            ind += 1
    return data

def parseAction(markovDP, state, data):
    actionData = list()
    newAction = markovDP[state][data].rsplit(" ")
    actionData.append(int(newAction[0][1:]))
    actionData.append(int(newAction[1][1:]))
    actionData.append(float(newAction[2]))
    return actionData

def getMax(jValues, state):
    indexMax = list(jValues[state].keys())[0]
    for key in jValues[state].keys():
        if jValues[state][indexMax] < jValues[state][key]:
            indexMax = key
    return indexMax

def valueIteration(markovDP):
    jValues = dict()
    for s in range(1, numStates + 1):
        jValues[s] = dict()
    prevJValues = copy.deepcopy(jValues)
    for i in range(20):
        print("After iteration ", (i+1), ":", sep = '')
        for s in range(1, numStates + 1):
            state = str(s)
            state = "s" + state
            reward = int(markovDP[state][0])
            for k in range(1, numActions + 1):
                sum = 0
                data = 1
                kExists = False
                while True:
                    if data >= len(markovDP[state]):
                        break
                    actionData = parseAction(markovDP, state, data)
                    if actionData[0] != k:
                        data += 1
                        continue
                    kExists = True
                    if not prevJValues[actionData[1]]:
                        data += 1
                        continue
                    else:
                        sum += actionData[2] * prevJValues[actionData[1]][getMax(prevJValues, actionData[1])]
                    data += 1
                if kExists:
                    jValues[s][k] = reward + (gamma * sum)
            optA = getMax(jValues, s)
            jValue = jValues[s][optA]
            print("(s", s, " a", optA, " {:0.4f}".format(jValue), ") ", sep = '', end = '')
        print("\n", end = '')
        prevJValues = copy.deepcopy(jValues)

if len(sys.argv) < 5 or len(sys.argv) > 5:
    print("Please execute script with exactly 4 arguments in order of number of states, number of actions, input file, and discount value")
    sys.exit()
    
numStates = int(sys.argv[1])
numActions = int(sys.argv[2])
gamma = float(sys.argv[4]) # 0.9 in example 1

mDP = readData()

valueIteration(mDP)



















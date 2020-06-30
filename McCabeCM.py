import re
import os
import sys

folder = ""

if(len(sys.argv) > 1):
    folder = sys.argv[1]

extention = ""

if(len(sys.argv) > 2):
    extention = sys.argv[2]

recursiveley = True

if(len(sys.argv) > 3):
    if(sys.argv[3] == '/nr'):
        recursiveley = False
    if(sys.argv[3] == '/r'):
        recursiveley = True


interestingComplexity = 0

makeErrors = False
if(len(sys.argv) > 4):
    if(sys.argv[4].isnumeric()):
        interestingComplexity = int(sys.argv[4])
    else:
        if(sys.argv[4] == '/err'):
            makeErrors = True
        elif(sys.argv[4] == '/nerr'):
            makeErrors = False

if(len(sys.argv) > 5):
    if (sys.argv[5] == '/err'):
        makeErrors = True
    elif (sys.argv[5] == '/nerr'):
        makeErrors = False

filenames = []

if(recursiveley):
    for root, subdirs, files in os.walk(folder):
        for filename in files:
            filenames.append(root + '\\' + filename)
else:
    filenames = [(folder + '\\' + el) for el in os.listdir(folder)]


suitableFiles = []

for filename in filenames:
    if(filename[-len(extention):] == extention):
        suitableFiles.append(filename)

expression = r"[\w\d<>:\[\]]+[*]{0,1} [\w\d:]+\((?:[\w\d<>:*\[\]]+ [\w\d<>:*\[\]]+(?:,[ \n]*){0,1})*\)[\n]*[ ]*\{"
keywords = [r"for", r"while", r"do", r"if", r"[&]{2}", r"[|]{2}", r"switch", r"throw", r"catch", r"goto"]
complexityTresholds = [-1, 5, 10, 20, 10000000000]
nestingTresholds = [-1, 3, 3, 5, 100000000000]
warningIndex = 2
errorIndex = 3
recomendations = ["", "are very good", "are recommended to rewrite", "you must rewrite later", "you must rewrite now"]

errorText = '#error "This method is too complex to read! Reconstruct it"'
warningText = '#warning "This method is complex to read! Maybe it is good to reconstruct it'

results = {}
for filename in suitableFiles:
    file = open(filename, 'r', encoding='utf-8')
    data = file.read()
    #print("\n\n\nFrom file " + filename)
    data = data.replace("\n" + warningText + "\n", "")
    data = data.replace("\n" + errorText + "\n", "")


    #([\w\d<>:\[\]]+[*]{0,1} [*]{0,1}[\w\d<>:\[\]]+(,[ \n]){0,1})*
    methods = re.split(expression, data)
    names = re.findall(expression, data)
    resultData = ""
    if(len(methods) > 0):
        resultData = methods[0]
    for i in range(1, len(methods)):
        method = methods[i]
        complexity = 1
        currentNesting = 0
        nesting = 0

        for l in method:
            if(l == '{'):
                currentNesting += 1
            if(l == '}'):
                currentNesting -= 1
            if(currentNesting > nesting):
                nesting = currentNesting

        

        for keyword in keywords:
            complexity += len(re.findall(keyword, method))
            #print("--------------------NEW METHOD--------------------------")
            #print(method)
            #print(re.findall(keyword, method))
        results[names[i-1]] = {"complexity" : complexity, "nesting" : nesting}
        if(makeErrors):
            if (complexity > complexityTresholds[errorIndex]):
                resultData += "\n" + errorText + "\n"
            elif(complexity > complexityTresholds[warningIndex]):
                resultData += "\n" + warningText + "\n"
        resultData += names[i-1]
        resultData += methods[i]

    file.close()
    writeFile = open(filename, 'w', encoding='utf-8')
    writeFile.write(resultData)
    writeFile.close()


listedMethods = []

for i in range(1, len(complexityTresholds)):
    if(complexityTresholds[i] > interestingComplexity):
        print('\n\nMethods that ' + recomendations[i] + '\n')
        for methodname in results.keys():
            if(methodname not in listedMethods):
                if(results[methodname]["complexity"] <= complexityTresholds[i]
                        and results[methodname]["complexity"] > interestingComplexity
                        and results[methodname]["nesting"] <= nestingTresholds[i]):
                    listedMethods.append(methodname)
                    if(methodname[-2] == '\n'):
                        print(methodname[:-2] + ' [' + str(results[methodname]["complexity"]) + "] {" + str(results[methodname]["nesting"]) + "}")
                    else:
                        print(methodname[:-1] + ' [' + str(results[methodname]["complexity"]) + "] {" + str(results[methodname]["nesting"]) + "}")
#print(suitableFiles)

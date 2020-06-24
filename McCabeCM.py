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
if(len(sys.argv) > 4):
    interestingComplexity = int(sys.argv[4])

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

expression = r"[\w\d<>:\[\]]+[*]{0,1} [\w\d:]+\((?:[\w\d<>:*\[\]]+ [\w\d<>:*\[\]]+(?:,[ \n]*){0,1})*\)[\n]*\{"
keywords = [r"for", r"while", r"do", r"if", r"[&]{2}", r"[|]{2}", r"switch", r"throw", r"catch", r"goto"]

results = {}
for filename in suitableFiles:
    file = open(filename, 'r', encoding='utf-8')
    data = file.read()
    #print("\n\n\nFrom file " + filename)


    #([\w\d<>:\[\]]+[*]{0,1} [*]{0,1}[\w\d<>:\[\]]+(,[ \n]){0,1})*
    methods = re.split(expression, data)
    names = re.findall(expression, data)


    for i in range(1, len(methods)):
        method = methods[i]
        complexity = 1
        for keyword in keywords:
            complexity += len(re.findall(keyword, method))
            #print("--------------------NEW METHOD--------------------------")
            #print(method)
            #print(re.findall(keyword, method))
        results[names[i-1]] = complexity


            #print("complexity = " + str(results[methodname]) + "\n")

    file.close()

tresholds = [-1, 5, 10, 20, 10000000000]
recomendations = ["", "are very good", "are recommended to rewrite", "you must rewrite later", "you must rewrite now"]

for i in range(1, len(tresholds)):
    if(tresholds[i] > interestingComplexity):
        print('\n\nMethods that ' + recomendations[i] + '\n')
        for methodname in results.keys():
            if(tresholds[i-1] < results[methodname] <= tresholds[i] and results[methodname] > interestingComplexity):
                if(methodname[-2] == '\n'):
                    print(methodname[:-2] + ' [' + str(results[methodname]) + "]")
                else:
                    print(methodname[:-1] + ' [' + str(results[methodname]) + ']')
#print(suitableFiles)

import tree
import fileinput
import sys
import re
import pprint


input = fileinput.input()
att = 0
trainData = []
attributes = []
numberAtt = 0
data = 0
for line in input:
    if "%" not in line and att == 1:
        data = line.strip("\n").split(",")
        trainData.append(data)
        numberAtt = len(data)
    if "@attribute" in line:
        raw_line = re.sub('\s+', '', line)
        raw_list = raw_line.replace("@attribute", "").strip("}").split("{")
        attributes.append(raw_list[0])
    if "@data" in line:
        att = 1



class Node:
    value = ""
    children = []
    
    def __init__(self, val, dic):
        self.value = val
        if(isinstance(dic, dict)):
            self.children = dic.keys()
            


def recursivePrint(dicTree, depth=0, prefix=""):
    if isinstance(dicTree, dict):
        for ele in dicTree:
            if isinstance(dicTree[ele], dict):
                if ele in attributes:
                    prefix = ele
                else:
                    print(" "* depth+ prefix + ": " + ele)
                depth += 1
                recursivePrint(dicTree[ele], depth, prefix)
            else:
                print(" "* depth+ prefix + ": " + ele)
                print("  "*depth + "ANSWER: "+  dicTree[ele])
        depth -= 1

def main():
    targetAtt = attributes[len(attributes)-1]
    #print(targetAtt)
    #print(trainData)
    #print(attributes)
    defaultVal = "empty"
    dicTree = tree.Tree(trainData, targetAtt, defaultVal, attributes)
    print(dicTree)
    recursivePrint(dicTree)

main()

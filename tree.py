

import math


def calvalCount(sets,attIndex):
    valCount={}
    for s in sets:
       
        if s[attIndex] in valCount:
            valCount[s[attIndex]] += 1
        else:
            valCount[s[attIndex]]  = 1
    return valCount
        
def calEntropy(sets,attValues,targetAtt):
     from math import log2
     entropy=0.0
     col=0
     valCount={}
     for record in attValues:
        if (targetAtt == record):
            break
        ++col
     for s in sets:
        if ((s[col])  not in valCount):
            valCount[s[col]] = 1
        else:
            valCount[s[col]]  += 1     
         
         
     
          #print(results)
     for key in valCount.keys():
         p=float(valCount[key]/len(sets))
         entropy=entropy+(-p*log2(p))
     #print('first entropy',entropy)    
     return entropy

        
def calGain(attValues,sets,targetAtt,att):
    valCount = {}
    subentropy=0.0
    attEntropy = 0.0
    attIndex = attValues.index(att)
    
    parentEntropy=calEntropy(sets,attValues,targetAtt)
    
    valCount=calvalCount(sets,attIndex)
  
    
   
    for key in valCount.keys():
       
        attData= [s for s in sets if s[attIndex] == key]
       
        subEntropy= calEntropy(attData,attValues,targetAtt)
        
        tempP=valCount[key] / sum(valCount.values())
        attEntropy=attEntropy+ (tempP * subEntropy)
        #print(attEntropy)
        
    infoGain=parentEntropy-attEntropy
    #print('info',infoGain)    
    return infoGain

#choosing the best attribute for spliting the tree based on the highest gain
def getBestAtt(data,attributes, targetAtt):
    bestAtt = attributes[0]
    highestGain = 0;
    
    for att in attributes:
        
            tempGain = calGain(attributes,data, targetAtt,att)
        
            if tempGain > highestGain:
            
                highestGain = tempGain
           # print(highestGain)
                bestAtt = att
    #print(bestAtt)       
    return bestAtt

#a function to return the sub records based on the bestAtt
def getAttValueSamples(sets, attributes, value,bestAtt):
    
    samples = []
    index = attributes.index(bestAtt)
    #print(index)
    for record in sets:
        if (record[index] == value):
            newRecord = []
            
            
            for i in range(0,len(record)):
                if(i != index):
                    newRecord.append(record[i])
                    
            samples.append(newRecord)
           # print(samples)
    return samples

def calDefault(sets,targetAtt,attributes):
    targetIndex=attributes.index(targetAtt)
    maximum = 0
    valCount=calvalCount(sets,targetIndex)
    for key in valCount.keys():
        if valCount[key]>maximum:
            maximum = valCount[key]
            major = key
    return major


  
    
 
   
#constructing the tree based on ID3 algorithm

def Tree(data,targetAtt,default,attributes):

    
    data = data[:]
    
    targetIndex=attributes.index(targetAtt)
    
    targetvals = [record[targetIndex] for record in data]
    targetlen=len(targetvals)
  
    #calculating the default value of target Attribute for the all sets or subsets
    defaultVal=calDefault(data,targetAtt,attributes)
   
    if len(data)==0 :#the set or data is empty
        return defaultVal
    if len(attributes) - 1 <= 0:#no attributes left returns most frequent target value of the records
        return defaultVal
       
    elif  len(targetvals)==targetvals.count(targetvals[0]):#the target labels are the same for all records
        leafLabel=targetvals[0]
        return leafLabel
        #print(leafLabel)
    #constructing the tree or subtrees
    
    else:
        #choosing the attribute with highest information gain
        bestAtt = getBestAtt(data, attributes, targetAtt)
        #print(bestAtt)


        #saving nodes of tree in a dictionary
        tree = {bestAtt:{}}
        #collecting the values of best attribute
        values = []
    
        i = attributes.index(bestAtt)
        for record in data:
            if record[i] not in values:
               values.append(record[i])
        
        for value in values:
            #choosing the records with the each corresponding values of best attribute
            sets = getAttValueSamples(data,attributes,value,bestAtt)

            #removing the best att from the list of attributes for not choosing again in this recursion
            newList = attributes[:]
            newList.remove(bestAtt)

            #calling tree recursively to make subtrees based on the parent nodes
            subtree = Tree(sets, targetAtt,default,newList)

            #saving subtree in the tree dictionary
            tree[bestAtt][value] = subtree
    
    return tree

import sys
import json

def scanIDs (array) :
    sample_dict = {}
    temp = array[0].split(' ')
    sample_dict['action'] = temp[0]
    sample_dict ['type'] = temp[1][:temp[1].find('(')]
    sample_dict['subtype'] = temp[1][temp[1].find('(')+1:temp[1].find(')')]
    #sample_dict['data'] = dict(array[2].split(' '))
    print(array[2][array[2].find('-'):].split(' '))
    return sample_dict

def extractBlock (FileData):
    array = []
    for lines in FileData:
        array.append(lines.lstrip('\t').rstrip('\n'))
        if (lines.find(';') >= 0 ) :
            break
    return array

#def GenHashmap (array):

FileData = open ('sample.txt', 'r')

temp = extractBlock(FileData)
print (temp)
print (scanIDs (temp))
temp = extractBlock(FileData)
print (temp)

#json_str = json.dumps(array)
#print(json.dumps(json_str, indent=4))
#print (json_str)

'''with open('data.json','w') as outfile:
    json.dump(json_str, outfile)

print(json.dumps(json_str, indent=4))'''

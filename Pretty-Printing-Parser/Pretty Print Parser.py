import sys
import json
import pdb

class Parser:
    state = ''
    substate = ''
    action = []
    Type = []
    key = []
    value = []
    subtype = []
    data = {}
    curlystack = []
    stack = []
    output = {}
    threshold = 1
    def initialize (self):
        self.state = 'action'
    def reset (self):
        self.state = ''
        self.substate = ''
        self.action = []
        self.Type = []
        self.key = []
        self.value = []
        self.subtype = []
        self.data = {}
        self.curlystack = []
        self.stack = []
        self.threshold = 1

    def updatedict (self, hashmap, key, value):
        #print ('%s %s' %(key,value))
        if key in hashmap:
            if type(hashmap[key]) is not type([]):
                hashmap[key] = [hashmap[key]]
                hashmap[key].append(value)
            else:
                hashmap[key].append(value)
        else:
            hashmap[key] = value

    def processline(self,line):
        if self.state == 'action' :
            if line == ' ':
                self.state = 'type'
            elif line != '\n':
                self.action.append(line)
        elif self.state == 'type' :
            if line == '(':
                self.stack.append(line)
                self.state = 'subtype'
            else:
                self.Type.append(line)
        elif self.state == 'subtype' :
            if line ==')':
                if (''.join(self.subtype) == 'cassette'):
                    self.threshold = 2
                else:
                    self.threshold = 1
            if line == '{':
                self.curlystack.append(line)
                if len(self.curlystack) >= self.threshold:
                    self.state = 'data'
                    self.substate = 'key'
            elif line != ')' and line != '\n':
                self.subtype.append(line)
        elif self.state == 'data' :
            #print(''.join(self.key),''.join(self.value))
            if self.substate == 'key':
                if line == ' ' and len(self.key) != 0:
                    self.substate = 'value'
                elif "\n" not in line:
                    if line!= '-' and line != ' ':
                        if line == '}':
                            if len(self.curlystack) != 0:
                                self.curlystack.pop()
                            self.key = []
                            self.value = []
                        elif line == ';':
                            #pdb.set_trace()
                            self.updatedict(self.output,'action',''.join(self.action))
                            self.updatedict(self.output,'type',''.join(self.Type))
                            self.updatedict(self.output,'subtype',''.join(self.subtype))
                            self.updatedict(self.output,'data',self.data)
                            self.reset()
                            self.state = 'action'
                        elif line != '\t' and line != '{':
                            self.key.append(line)

            elif self.substate == 'value':
                #pdb.set_trace()
                if line == '{':
                    self.curlystack.append(line)
                elif line == '}' and len(self.curlystack) != 0:
                    self.curlystack.pop()
                elif line == '}' and len(self.curlystack) < self.threshold:
                    self.curlystack.pop()
                    #self.data[str(''.join(self.key))] = str(''.join(self.value))
                    self.updatedict(self.data,str(''.join(self.key)),str(''.join(self.value)))
                    self.key = []
                    self.value = []
                elif line == '\n':
                    #self.data[str(''.join(self.key))] = str(''.join(self.value))
                    self.updatedict(self.data,str(''.join(self.key)),str(''.join(self.value)))
                    self.key = []
                    self.value = []
                    self.substate = 'key'
                else:
                    self.value.append(line)

if __name__ == '__main__' :
    FileData = open ('sample.txt', 'r')
    test = Parser()
    test.initialize()
    line = FileData.readline(1)
    while (line):
        test.processline(line)
        line = FileData.readline(1)
    print (test.output)
    with open('data.json','w') as outfile:
        json.dump(test.output, outfile)

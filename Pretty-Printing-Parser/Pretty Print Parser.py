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
        self.threshold = 1

###################################################
#   Function to update values to the dictionary
###################################################
    def updatedict (self, hashmap, key, value):
        if key in hashmap:                              #Check if the key is already in the dictionary
            if type(hashmap[key]) is not type([]):      #Resolve collisions --> Convert it into a list
                hashmap[key] = [hashmap[key]]
                hashmap[key].append(value)
            else:
                hashmap[key].append(value)
        else:
            hashmap[key] = value                       #Add key,value pair to the dictionary

###################################################
#   Action State : Detect action keywords
###################################################

    def Action (self,line):
        if line == ' ':
            self.state = 'type'
        elif line != '\n':
            self.action.append(line)

###################################################
#   Type State : Detect type keywords
###################################################

    def _Type (self,line):
        if line == '(':
            self.state = 'subtype'
        else:
            self.Type.append(line)

###################################################
#   Subtype State : Detect Subtype keywords
###################################################
    def Subtype (self,line):
        if line ==')':
            if (''.join(self.subtype) == 'cassette'):
                self.threshold = 2              # Detect two curly braces for cassette type or else one
            else:
                self.threshold = 1
        if line == '{':
            self.curlystack.append(line)        # Maintain a stack for curly braces, push and pop when detecting code blocks
            if len(self.curlystack) >= self.threshold:
                self.state = 'data'
                self.substate = 'key'
        elif line != ')' and line != '\n':      # Discard escape sequences and braces
            self.subtype.append(line)

###################################################
#   Data State : Build keys for the dictionary
###################################################

    def Data_key (self,line):
        if line == ' ' and len(self.key) != 0:  # Identify spaces between key and value
            self.substate = 'value'
        elif "\n" not in line:
            if line!= '-' and line != ' ':      # Discard escape sequences and spaces
                if line == '}':
                    if len(self.curlystack) != 0:
                        self.curlystack.pop()
                    self.key = []
                    self.value = []
                elif line == ';':               # Update dictionary values at the end of code block
                    #pdb.set_trace()
                    self.updatedict(self.output,'action',''.join(self.action))
                    self.updatedict(self.output,'type',''.join(self.Type))
                    self.updatedict(self.output,'subtype',''.join(self.subtype))
                    self.updatedict(self.output,'data',self.data)
                    self.reset()
                    self.state = 'action'
                elif line != '\t' and line != '{':
                    self.key.append(line)       # Stream characters to build the key

###################################################
#   Data State : Build values for the dictionary
###################################################

    def Data_value(self,line):
        #pdb.set_trace()
        if line == '{':
            self.curlystack.append(line)
        elif line == '}' and len(self.curlystack) != 0:
            self.curlystack.pop()
        elif line == '}' and len(self.curlystack) < self.threshold:
            self.curlystack.pop()
            self.updatedict(self.data,str(''.join(self.key)),str(''.join(self.value))) # Update key, value pair to dictionary at end of block
            self.key = []
            self.value = []
        elif line == '\n':
            self.updatedict(self.data,str(''.join(self.key)),str(''.join(self.value))) # Update key, value pair to dictionary at end of line
            self.key = []
            self.value = []
            self.substate = 'key'
        else:
            self.value.append(line)             # Stream characters to build the value

    def processline(self,line):
        if self.state == 'action' :
            self.Action(line)
        elif self.state == 'type' :
            self._Type(line)
        elif self.state == 'subtype' :
            self.Subtype(line)
        elif self.state == 'data' :
            if self.substate == 'key':
                self.Data_key(line)
            elif self.substate == 'value':
                self.Data_value(line)

if __name__ == '__main__' :
    FileData = open ('sample.txt', 'r')
    test = Parser()                       # Instantiate the class
    test.initialize()
    line = FileData.readline(1)         # Read the file character by character
    while (line):
        test.processline(line)
        line = FileData.readline(1)
    print (test.output)
    with open('data.json','w') as outfile:   # Dump the output to a json file
        json.dump(test.output, outfile)

#!/usr/bin/env python
import math

DEBUG = False

LEFT  = 0
RIGHT = 1
PLUS  = 2
MINUS = 3
IN    = 4
OUT   = 5
LOOP  = 6
BACK  = 7


def change_mem_index(obj, change):
    obj.memoryIndex += change
    if obj.memoryIndex not in obj.memory:
        obj.memory[obj.memoryIndex] = 0

def func_left(obj):
    change_mem_index(obj, -1)
    obj.programCounter += 1

def func_right(obj):
    change_mem_index(obj, 1)
    obj.programCounter += 1  

def func_plus(obj):
    obj.setCell( (obj.getCell() + 1) & 0xFF)
    obj.programCounter += 1

def func_minus(obj):
    obj.setCell((obj.getCell() - 1) & 0xFF)
    obj.programCounter += 1

def func_in(obj):
    obj.setCell(obj.getNextInputByte())
    obj.programCounter += 1
    
def func_out(obj):
    obj.output += chr(obj.getCell())
    obj.programCounter += 1
    
def func_loop(obj):
    if (obj.getCell() == 0):
        obj.programCounter = obj.program[obj.programCounter + 1]
    obj.programCounter += 2
    
def func_back(obj):
    if (obj.getCell() != 0):
        obj.programCounter = obj.program[obj.programCounter + 1]
    obj.programCounter += 2   

FUNCS = [ func_left, func_right, func_plus, func_minus, func_in, func_out, func_loop, func_back ]

class BrainFuckProgram():
    def __init__(self,code):
        self.code = code

        self.programCounter = 0
        self.inputIndex = 0
        self.output = ""

        self.memory = {0:0,1:0}
        self.memoryIndex = 0
        self.minMemoryWrite = self.memoryIndex
        self.maxMemoryWrite = self.memoryIndex
        self.program = self.compile()
        self.programlen = len(self.program)

    def run(self):
        while(self.step()):
            #if not :
            pass
        print("Done.")
        print(bf.output)

    def step(self):
        """ program step """
        try: 
            FUNCS[self.program[self.programCounter]](self)
            return True
        except IndexError:
            return False


    def getCell(self):
        return self.memory[self.memoryIndex]


    def setCell(self, value):
        self.memory[self.memoryIndex] = value
        self.minMemoryWrite = min((self.memoryIndex, self.minMemoryWrite))
        self.maxMemoryWrite = max((self.memoryIndex, self.maxMemoryWrite))

    def getNextInputByte(self):
        if self.inputIndex == len(self.program):
            return 0
        else:
            self.inputIndex += 1
            return self.program[self.inputIndex]

    def compile(self):
        #  #  Takes the program and returns an array of numeric opcodes and jump targets.
        print("Compiling")
        result = []
        openBracketIndices = []
        for i in [i for i in self.code if i in '<>+-,.[]']:
            if i ==  '<':  op = LEFT
            elif i ==  '>':  op = RIGHT
            elif i ==  '+':  op = PLUS
            elif i ==  '-':  op = MINUS
            elif i ==  ',':  op = IN
            elif i ==  '.':  op = OUT
            elif i ==  '[':  op = LOOP
            elif i ==  ']':  op = BACK
            result.append(op)
        
            #  Add jump targets
            if (op == LOOP):
                openBracketIndices.append(len(result) - 1)
                result.append(-1)  #  Placeholder
            elif (op == BACK):
                if (len(openBracketIndices) == 0):
                    exit("Mismatched brackets: extra right bracket")
                index = openBracketIndices.pop()
                result[index + 1] = len(result) - 1
                result.append(index)
            
        if (len(openBracketIndices) > 0):
            exit("Mismatched brackets: extra left bracket")
        print("Done compiling.")
        return result



##  check for a file to parse
import sys
if len(sys.argv) <2:
    exit("Please provide the filename to parse")
else:
    filename = sys.argv[-1]
    code = open(filename, 'r').read().replace('\r','').replace('\n', '')

print("Loaded code: {}".format(code))
bf = BrainFuckProgram(code)
print("Instructions: {}".format(len(bf.program)))
print("Running...")
bf.run()
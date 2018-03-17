#!/usr/bin/env python

LEFT  = 0
RIGHT = 1
PLUS  = 2
MINUS = 3
IN    = 4
OUT   = 5
LOOP  = 6
BACK  = 7
import sys
sys.setcheckinterval(100000000)

class BrainFuckProgram():
    def __init__(self,code):
        self.FUNCS = [ self.func_left, self.func_right, self.func_plus, self.func_minus, self.func_in, self.func_out, self.func_loop, self.func_back ]

        self.code = code

        self.programCounter = 0
        self.inputIndex = 0
        self.output = ""

        # initialize 30k memory cells
        self.defmemory()
        self.memoryIndex = 0

        #self.minMemoryWrite = self.memoryIndex
        #self.maxMemoryWrite = self.memoryIndex
        self.program = self.compile()

    def defmemory(self):
        self.memory = []
        for i in range(30000):
            self.memory.append(0)
    
    def run(self):
        step = self.step
        while(True):
            step()

    def step(self):
        """ program step """
        try: 
            self.FUNCS[self.program[self.programCounter]]()
            return True
        except IndexError:
            print("Done.")
            #print(bf.output)
            sys.stdout.write('\n')
            sys.stdout.flush()
            exit()

    def func_left(self):
        self.memoryIndex -= 1
        self.programCounter += 1

    def func_right(self):
        self.memoryIndex += 1
        self.programCounter += 1  

    def func_plus(self):
        self.setCell((self.getCell() + 1) % 256 )
        self.programCounter += 1

    def func_minus(self):
        self.setCell((self.getCell() - 1) % 256 )

        self.programCounter += 1

    def func_in(self):
        self.setCell(self.getNextInputByte())
        self.programCounter += 1
        
    def func_out(self):
        sys.stdout.write(chr(self.getCell()))
        self.programCounter += 1
        
    def func_loop(self):
        if self.getCell() == 0:
            self.programCounter = self.program[self.programCounter + 1]
        self.programCounter += 2
        
    def func_back(self):
        if (self.getCell() != 0):
            self.programCounter = self.program[self.programCounter + 1]
        self.programCounter += 2   

    def getCell(self):
        return self.memory[self.memoryIndex]

    def setCell(self, value):
        self.memory[self.memoryIndex] = value

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
print("Loaded code from {}".format(filename))
bf = BrainFuckProgram(code)
print("Instructions: {}".format(len(bf.program)))
print("Running...")
bf.run()
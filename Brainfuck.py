# Scott Ouellette
# Brainfuck interpreter w/ optimizations

import sys as s
import time,re


def parser(code):
    open_brack = [] # contains indexes of open brackets that are found
    loop  = {} # dictionary mapping idx of open brackets to closed ones

    for index,cell in enumerate(code):
        if cell == "[":
            open_brack.append(index)
        elif cell == "]":
            try:
                #if ']' is found get index of innermost 
                #'[' and add a key:value to the loop hash in the form of
                #(index of innermost '['):(index of innermost ']')
                begin = open_brack.pop()
                loop[begin] = index
            except IndexError:
                raise ValueError, "Too many ]'s"
    #if the stack of [s isnt empty then we have an issue!
    if open_brack != []:
        raise ValueError, "Too many ['s"
    else:
        return loop

def evaluate(code):
    global pointer
    global primitive_count
    # build up locations of '[' and ']' by running parser
    loop  = parser(code)
    # program counter to 0
    pc = 0
    # a stack to store the pc for loops
    programCounter_stack = []

    while pc < len(code):

        instruction = code[pc]

        if instruction == "+" or instruction == "-":
            #print "PLUS OR MINUS"
            primitive_count = 1
            # while peeking at next cell and checking for the same primitive
            while instruction == code[pc + 1]:
                #print "Instruction%d : " % pc ,instruction
                primitive_count += 1
                instruction = code[pc + 1]
                pc+=1

            if "+" in instruction:
                #print "Found group of %d plusses." % primitive_count
                incrementCell(primitive_count)
            elif "-" in instruction:
                #print "Found group of %d minuses." % primitive_count
                decrementCell(primitive_count)

        if instruction == "[":
            # enter loop
            if Prog[pointer] > 0:
                programCounter_stack.append(pc)
            else: # else go to the end of the block
                pc = loop[pc]

        elif instruction == "]":
            # jump back where you came from!
            pc = programCounter_stack.pop() - 1

        # if current instruction in within the primitive hash, then run its respective method
        if instruction in primitive_hash:
            apply(primitive_hash[instruction])
          
        pc += 1

def reset():
    global pointer, Prog
    pointer = 0
    Prog = [0]*10000

def prevCell():
    global pointer
    # <
    if pointer <= 0:
        raise ValueError, "< Out of Cell Range!"
    else:
        #go to previous cell
        pointer -= 1

def nextCell():
    global pointer
    # >
    if pointer >= 10000 - 1:
        raise ValueError, "> Out of Cell Range!"
    else:
        #go to next cell
        pointer += 1

def incrementCell(plus):
    global pointer
    p = plus
    # +
    #increment value of current cell by 1
    Prog[pointer] = (Prog[pointer] + p)

def decrementCell(minus):
    global pointer
    # -
    m = minus
    #decrement value of current cell by 1
    Prog[pointer] = (Prog[pointer] - m)

def output():
    global pointer
    # .
    # write value of current cell to stdout
    s.stdout.write(chr(Prog[pointer]))

def input_():
    global pointer
    # .
    #read user input
    c = ord(s.stdin.read(1)) #ord returns the ascii value of the given input
    if c != 26:
        Prog[pointer] = c

def ignore():
    # [^\+\-\[\]\<\>\.\,]
    # treat unknown characters as comments
    pass


#Start timing the program
start_time = time.time()

#Simulate potential cells of program with a list of size 1000
Prog = [0]*10000

#Pointer to the current cell being interpreted
pointer = 0

#map characters found in brainfuck to their respective functions
comment = re.compile('[^\+\-\[\]\<\>\.\,]')

primitive_hash = { 
    "." : output, 
    "," : input_ , 
    "<" : prevCell, 
    ">" : nextCell,
    comment : ignore
    #"+" : incrementCell, 
    #"-" : decrementCell
}

for input_file in s.argv[1:]:
    with open(input_file, "r") as f:
        code = f.read()
    evaluate(code)

print("\n--- %s seconds ---" % (time.time() - start_time))
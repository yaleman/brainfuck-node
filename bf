#!/usr/local/bin/node

"use strict";
var DEBUG = false;
var instance = null;

// Opcodes
var LEFT  = 0,
    RIGHT = 1,
    PLUS  = 2,
    MINUS = 3,
    IN    = 4,
    OUT   = 5,
    LOOP  = 6,
    BACK  = 7;

function step() {
	try{
		switch (program[programCounter]) {
			case LEFT:
				memoryIndex--;
				programCounter++;
				break;
			case RIGHT:
				memoryIndex++;
				programCounter++;
				break;
			case PLUS:
				setCell((getCell() + 1) & 0xFF);
				programCounter++;
				break;
			case MINUS:
				setCell((getCell() - 1) & 0xFF);
				programCounter++;
				break;
			case IN:
				setCell(getNextInputByte());
				programCounter++;
				break;
			case OUT:
				output += String.fromCharCode(getCell());
				programCounter++;
				break;
			case LOOP:
				if (getCell() == 0)
					programCounter = program[programCounter + 1];
				programCounter += 2;
				break;
			case BACK:
				if (getCell() != 0)
					programCounter = program[programCounter + 1];
				programCounter += 2;
				break;
			default:
				throw "We're done! Or you suck.";
			} 
		} catch(err) {
		console.log("Output:");
		console.log(output);
		process.exit();
		}
	//steps++;
	}

// Helper functions
function getCell() {
	if (memory[memoryIndex] === undefined)
		memory[memoryIndex] = 0;
	return memory[memoryIndex];
}

function setCell(value) {
	memory[memoryIndex] = value;
	minMemoryWrite = Math.min(memoryIndex, minMemoryWrite);
	maxMemoryWrite = Math.max(memoryIndex, maxMemoryWrite);
}

function getNextInputByte() {
	if (inputIndex == input.length)
		return 0;
	else if (input.charCodeAt(inputIndex) >= 256)
		throw "Error: Input has character code greater than 255";
	else
		return input.charCodeAt(inputIndex++);
}

function compile(str) {
// Takes the program and returns an array of numeric opcodes and jump targets.
	var result = [];
	var openBracketIndices = [];
	for (var i = 0; i < str.length; i++) {
		var op;
		switch (str.charAt(i)) {
			case '<':  op = LEFT;   break;
			case '>':  op = RIGHT;  break;
			case '+':  op = PLUS;   break;
			case '-':  op = MINUS;  break;
			case ',':  op = IN;     break;
			case '.':  op = OUT;    break;
			case '[':  op = LOOP;   break;
			case ']':  op = BACK;   break;
			default:   op = -1;     break;
		}
		if (op != -1)
			result.push(op);
		
		// Add jump targets
		if (op == LOOP) {
			openBracketIndices.push(result.length - 1);
			result.push(-1);  // Placeholder
		} else if (op == BACK) {
			if (openBracketIndices.length == 0)
				throw "Mismatched brackets: extra right bracket";
			var index = openBracketIndices.pop();
			result[index + 1] = result.length - 1;
			result.push(index);
		}
	}
	if (openBracketIndices.length > 0)
		throw "Mismatched brackets: extra left bracket";
	return result;
}

var programCounter = 0;
var inputIndex = 0;
var output = "";

var memory = [];
var memoryIndex = 0;
var minMemoryWrite = memoryIndex;
var maxMemoryWrite = memoryIndex;

// check for a file to parse
if(process.argv.length != 3){
	console.log("Please provide the filename to parse")
	process.exit();
} 
else {
	// fs library for reading files
	var fs = require('fs');
	var filename = process.argv[2];
	// read the file synchronously because we can wait
	var code = fs.readFileSync( filename ).toString().replace(/\r?\n|\r/g, '');
	if(DEBUG){
		console.log("Loaded code from file '"+filename+"':")
		console.log(code);
	}
}	

if(DEBUG){console.log("Compiling code to opcodes...")}

const program = compile(code);

if(DEBUG){
	console.log("Program length: "+code.length)
	console.log("running script")
	}

while(true){
	step();
}

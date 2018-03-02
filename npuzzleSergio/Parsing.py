#!/usr/bin/python3

class Parsing():

	def __init__(self, file):
		self.parse(file)
	
	def parse(self, file):
		import utils
		
		lineI = 0
		self.puzzle = []
		for line in file:
			splittedLine = line.split()

			hashtagInMiddle = False
			wordHashtagI = None
			indexComment = None
			try:
				for word in splittedLine:
					if '#' in word:
						if word.index('#') == 0:
							indexComment = splittedLine.index(word)
						else:
							indexComment = splittedLine.index(word) + 1
							wordHashtagI = word.index('#')
							hashtagInMiddle = True
						if indexComment == 0:
							splittedLine = None
						pass
			except:
				indexComment = None
			
			if splittedLine == None or all(splitLine.isspace() for splitLine in splittedLine):
				continue

			splittedLine = splittedLine[:indexComment]
			if hashtagInMiddle:
				splittedLine[len(splittedLine) - 1] = splittedLine[len(splittedLine) - 1][:wordHashtagI]
			if lineI == 0:
				if len(splittedLine) > 1:
					utils.printError(utils.Errors.FORMAT_FILE)
				try:
					self.puzzleSize = int(splittedLine[0])
				except:
					utils.printError(utils.Errors.FORMAT_FILE)
			else:
				if len(splittedLine) != self.puzzleSize:
					utils.printError(utils.Errors.FORMAT_FILE)
				wordI = 0
				for word in splittedLine:
					try:
						self.puzzle.append(int(splittedLine[wordI]))
						wordI += 1
					except:
						utils.printError(utils.Errors.FORMAT_FILE)

			lineI += 1
		
		if len(self.puzzle) != self.puzzleSize * self.puzzleSize:
			utils.printError(utils.Errors.FORMAT_FILE)
		
		for nb in range(0, self.puzzleSize * self.puzzleSize - 1):
			if self.puzzle.count(nb) != 1:
				utils.printError(utils.Errors.FORMAT_FILE)
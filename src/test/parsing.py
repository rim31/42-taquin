import sys


class Parsing():

	def __init__(self, file):
		self.parse(file)
	
	def parse(self, file):
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
					sys.exit('error on file format')
				try:
					self.puzzleSize = int(splittedLine[0])
				except:
					sys.exit('error on file format')
			else:
				if len(splittedLine) != self.puzzleSize:
					sys.exit('error on file format')
				wordI = 0
				for word in splittedLine:
					try:
						self.puzzle.append(int(splittedLine[wordI]))
						wordI += 1
					except:
						sys.exit('error on file format')

			lineI += 1
		
		if len(self.puzzle) != self.puzzleSize * self.puzzleSize:
			sys.exit('error on puzzle format')
		
		for nb in range(0, self.puzzleSize * self.puzzleSize - 1):
			if self.puzzle.count(nb) != 1:
				sys.exit('error on puzzle format')

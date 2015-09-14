import re
import sys

if(len(sys.argv)  < 2):
	print "Usage: python parser.py source.pvm"
else:
	singlekeywords = '(LDC_[0-9]+|LDA_[0-9]+|LDL_[0-9]+|STL_[0-9]+|LDV|LDXA|STO|PRNI|PRNB|PRNL|INPI|INPB|ADD|SUB|MUL|DIV|REM|CEQ|CNE|CGT|CLT|CLE|CGE|NEG|AND|OR|NOT|ANEW|NOP|ISLET|LOW|INC|DEC)'
	doublekeywords = '(LDC|LDA|PRNS|DSP|BRN|BZE|NOP|LDL|STL|BGT|BLT|JR|BNE|BEQ|INPC|PRNC)'


	leading = re.compile('^[ \t]*[0-9]+[ \t]*')
	blank = re.compile('[ \t]*\n?') 
	comment = re.compile('([ \t]*)(;(.|[0-9])*)+[ \t]*\n')
	halt = re.compile('[ \t]*[0-9]+[ \t]*(HALT)([ \t]*;.+)?[ \t]*\n?')
	singleC = re.compile('[ \t]*-?[0-9]+[ \t]*(' + singlekeywords + ')([ \t]*;(.|[0-9])+)?[ \t]*\n')
	double = re.compile('[ \t]*[0-9]+[ \t]*(' + doublekeywords + ' )[ \t]*-?[0-9]+([ \t]*;(.|[0-9])*)?[ \t]*\n')
	squote = re.compile('[ \t]*[0-9]+[ \t]*(' + doublekeywords + '[ \t]*\'.*\')+([ \t]*;(.|[0-9])*)?[ \t]*\n')
	dquote = re.compile('[ \t]*[0-9]+[ \t]*(' + doublekeywords + '[ \t]*\".*\")+([ \t]*;(.|[0-9])*)?[ \t]*\n')

	filename = str(sys.argv[1])

	fileLine = 1
	lineNum = 0
	prevLineNum =0

	source = open(filename, 'r')
	output = ""

	Error = False

	for line in source:
		blankCheck = False
		if(double.match(line) or squote.match(line) or dquote.match(line)):
			lineNum += 2
			#output += "--"
		elif(halt.match(line) or singleC.match(line)):
			lineNum += 1
			#output += "- "
		elif(comment.match(line)):
			#output += "  "
			#line number stays the same
			pass
		elif(blank.match(line)):
			#dont write blank lines
			blankCheck = True
		else:
			Error = True
			print "ERROR Line " + str(fileLine) + ": " + line,

		if(lineNum == prevLineNum):
			if(blankCheck):
				pass
			else:
				output += re.sub(leading,"",line)
		else:
			output += str(prevLineNum).rjust(4) + "   " + re.sub(leading,"",line,1)

		prevLineNum = lineNum
		fileLine += 1

	source.close()

	#print(output)
	if(Error):
		print "Line numbers not changed due to error(s)!"
	else:
		source = open(filename,'w')
		source.write(output)
		source.close()
		print "Line numbers re-calculated."

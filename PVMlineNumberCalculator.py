import re
import sys

singlekeywords = '(LDV|LDXA|STO|PRNI|PRNB|PRNL|INPI|INPB|ADD|SUB|MUL|DIV|REM|CEQ|CNE|CGT|CLT|CLE|CGE|NEG|AND|OR|NOT|ANEW|NOP|ISLET|LOW|INC|DEC)'
doublekeywords = '(LDC(_[0-9])*|LDA(_[0-9])*|PRNS|DSP|BRN|BZE|NOP|LDL(_[0-9])*|STL(_[0-9])*|BGT|BLT|JR|BNE|BEQ|INPC|PRNC)'


leading = re.compile('[ ]*[0-9]+ [ ]*')

blank = re.compile('[ ]*\n') 
comment = re.compile('([ ]*)(;.*)+[ ]*\n')
halt = re.compile('[ ]*[0-9]+ [ ]*(HALT)[ ]*\n?')
singleC = re.compile('[ ]*[0-9]+ [ ]*(' + singlekeywords + ')( [ ]*;.+)?[ ]*\n')
double = re.compile('[ ]*[0-9]+ [ ]*(' + doublekeywords + ' )[ ]*[0-9]+( [ ]*;.*)?[ ]*\n')
squote = re.compile('[ ]*[0-9]+ [ ]*(' + doublekeywords + ' [ ]*\'.*\')+( [ ]*;.*)?[ ]*\n')
dquote = re.compile('[ ]*[0-9]+ [ ]*(' + doublekeywords + ' [ ]*\".*\")+( [ ]*;.*)?[ ]*\n')

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

if(Error):
	print "Line numbers not changed due to error(s)!"
else:
	source = open(filename,'w')
	source.write(output)
	source.close()
	print "Line numbers re-calculated."
#Basic script to remove unused lines from the code, spaces at the EOL...
import os
import re
import sys
directory = '.'
nbOfFiles = 0
nbOfLines = 0
nbOfEmptyLines = 0
nbOfChars = 0
for filename in os.listdir(directory):
	if os.path.isfile(directory + "/" + filename):
		if filename.endswith('.py'):
			print(filename)
			f = open (filename, 'r')
			data = f.read()
			data = re.sub(' +\n', '\n', data)
			data = re.sub('\n\n', '\n', data)
			#Fix missing empty line before definition.
			pattern = re.compile(r'[\w\:\.\W]\n(	+)((def)|(class))')
			for m in re.finditer(pattern, data):
				strToReplace = m.group(0)
				newStr = strToReplace.replace("\n","\n\n")
				data = data.replace(strToReplace, newStr)
			pattern = re.compile(r'	*#[\w :\.]+\n\n')
			#Fix line between comment and defintion.
			for m in re.finditer(pattern, data):
				strToReplace = m.group(0)
				newStr = strToReplace.replace("\n\n","\n")
				newStr = '\n' + newStr
				data = data.replace(strToReplace, newStr)
			#Fix missing points at the end of the comment.
			pattern = re.compile(r'	*#[\w :\.]*[\w]\n')
			for m in re.finditer(pattern, data):
				strToReplace = m.group(0)
				newStr = strToReplace.replace("\n",".\n")
				data = data.replace(strToReplace, newStr)
			f.close()
			f = open (filename, 'w')
			f.write(data)
			f.close()
print("_______________________________________________")
print("Task successfully finished!")
print("_______________________________________________")

#Basic program to get some stats about the code.
import os
import sys
directory = '.'
nbOfFiles = 0
nbOfLines = 0
nbOfEmptyLines = 0
nbOfChars = 0
for filename in os.listdir(directory):
	if os.path.isfile(directory + "/" + filename):
		if filename.endswith('.py') and not filename in sys.argv[0]:
			print(filename)
			nbOfFiles +=1
			with open(filename, 'r') as myfile:
  				data = myfile.read()
  				nbOfChars += len(data)
  				lines = data.split('\n')
  				for l in lines:
  					nbOfLines += 1
  					if len(l) < 1:
  						nbOfEmptyLines += 1
print("_______________________________________________")
print("Nombre de fichiers: " + str(nbOfFiles))
print("Nombre de caracteres: " + str(nbOfChars))
print("Nombre de lignes: " + str(nbOfLines))
print("Nombre de lignes vide: " + str(nbOfEmptyLines))
print("_______________________________________________")

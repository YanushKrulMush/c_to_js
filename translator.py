import myParser

file = open("test.c", "r")
p = myParser.parse(file.read())
resultFile = open("result.js", "w")
print(p)
resultFile.write(p)
    
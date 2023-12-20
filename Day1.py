"""
Challenge - read in file, find first and last digits in each row, add them, add all numbers

PseudoCode
    - Read in file
    - Parse new line
    - Find all digits
    - Add first and last
    - Add to list
    - Add all
"""
import re

"""
HELPERS
"""

"""
Find digits in line
"""
def findAllDigits(inputLine):
    """
    Function that takes a string input and returns tuples of all digits and their indices
    """
    intList = []
    i = 0
    for c in inputLine:
        if c.isdigit():
            intList.append((int(c),i))
        i = i + 1
    return intList


def findTextNumbers(inputLine):
    """
    Function that takes a string input and returns tuples of all non-overlapping strings of digit words and their indices
    """
    textNumbers = []
    for match in re.finditer("one", inputLine):
        textNumbers.append((1,match.start()))
    for match in re.finditer("two", inputLine):
        textNumbers.append((2,match.start()))
    for match in re.finditer("three", inputLine):
        textNumbers.append((3,match.start()))
    for match in re.finditer("four", inputLine):
        textNumbers.append((4,match.start()))
    for match in re.finditer("five", inputLine):
        textNumbers.append((5,match.start()))
    for match in re.finditer("six", inputLine):
        textNumbers.append((6,match.start()))
    for match in re.finditer("seven", inputLine):
        textNumbers.append((7,match.start()))
    for match in re.finditer("eight", inputLine):
        textNumbers.append((8,match.start()))
    for match in re.finditer("nine", inputLine):
        textNumbers.append((9,match.start()))
    return textNumbers

f = open("Day1Input.txt")
runningSum = 0

for l in f:
    lineInts = []
    lineInts = findAllDigits(l)
    
    textNumList = []
    textNumList = findTextNumbers(l)

    for p in textNumList:
        lineInts.append(p)
    
    lineInts.sort(key = lambda x: x[1]) 

    lenLineInts = len(lineInts)
    lineSum = ""  
    if lenLineInts == 0:
        print("No ints found in this line - should this ever happen?")
    elif lenLineInts == 1:
        lineSum = str(lineInts[0][0]) + str(lineInts[0][0])
    else:
        lineSum = str(lineInts[0][0]) + str(lineInts[lenLineInts-1][0])
    print(lineSum)
    
    runningSum = runningSum + int(lineSum)

print(runningSum)









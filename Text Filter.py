import re
import os
# This script loads the source data, switches the text to lowercase, organizes it as a single line, and removes
# numbers, punctuation, some special characters and excessive whitespace
filtering = "mineral"
current_path = os.path.abspath("")
abspath = current_path + "/" + filtering + ".txt"

f = open(abspath, "r")
txt = f.read()

txt = txt.lower()
txt = txt.replace('\n', ' ')
txt = txt.replace('(', '')
txt = txt.replace(')', '')

txt = re.sub('\d|[^(\w|\s)]', '', txt)  # sub everything that is a digit "\d" or not letter, underscore, or whitespace

k = 0
while txt.find('  ') >= 0:
    k = k+1
    txt = re.sub('\s\s', ' ', txt)  # removing multiple whitespaces
if txt[0] == ' ':
    txt = txt[1:]
print('Resulting text:\n', txt)

abspath = current_path + "/" + filtering + " filtered.txt"

g = open(abspath, "w+")
g.write(txt)

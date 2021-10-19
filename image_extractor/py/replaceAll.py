from timer import timer
import csv
from multiprocessing import Pool, cpu_count


#string = "geeks for geeks geeks geeks geeks"
#print(string.replace("g", "#"))
 

f1=open("/Users/a-5156/DeepShared/Turnkey/input/example_names.txt", "r", encoding='utf8') #todo : absolute
f2=open("/Users/a-5156/DeepShared/Turnkey/output/3x5K_out.txt", "w")

def replaceSpaceAndNewLine():
    for line in f1:
        return line.replace('%@_@%', '|').replace('_@%@_', '\n')

print(replaceSpaceAndNewLine())

f1.close()
f2.close()







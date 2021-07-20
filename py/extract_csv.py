from timer import timer
import csv
from multiprocessing import Pool, cpu_count
import timeit


inputFilePath = "/Users/a-5156/DeepShared/Turnkey/output/3x5K_1.txt"
outputFilePath = "/Users/a-5156/DeepShared/Turnkey/output/MainFilePiped_out.csv"


def timer(number, repeat):
    def wrapper(func):
        runs = timeit.repeat(func, number=number, repeat=repeat)
        print(func.__name__ , ' : ' , sum(runs) / len(runs))
    return wrapper     

#todo: so replacing open("u.item", encoding="utf-8") with open('u.item', encoding = "ISO-8859-1") will solve the problem.
f1=open(inputFilePath, "r", newline='') #todo : absolute , encoding='utf8'
f2=open(outputFilePath, "w")

#self = {'file' : "/Users/a-5156/DeepShared/Turnkey/output/3x5K_1.txt"}

def read_file():
    with open("/Users/a-5156/DeepShared/Turnkey/output/3x5K_1.txt", 'r') as f:
        data = [row for row in csv.reader(f.read().replace('%@_@%', '|').replace('_@%@_', '\n').splitlines(), dialect=csv.excel, delimiter='\n')]
        #print(data)
    return data

def replaceSpaceAndNewLine():
    data1 = []
    for line in f1:
        x = line.replace('%@_@%', '|').replace('_@%@_', '\n').splitlines()
        y = list(filter(None, x))
        data1.append(y)
        #print('line : ', y)
        return data1

theData = replaceSpaceAndNewLine() #read_file()
#print(theData)

def getBytesFromHexa(hexa):
    return bytes.fromhex(hexa)

def getDecodedFromArabic(data):
    return data.decode('iso-8859-6')

def putToListForCSV(data):
    c = [data.splitlines()]
    print(c[0])

def doAllConversions(hexaRow):
    binaryRow = getBytesFromHexa(hexaRow)
    isoToUTF = getDecodedFromArabic(binaryRow)
    newLineReplaced = isoToUTF.replace('\n:', '').replace('\r\n', ':')
    print('aaaa')
    #putToListForCSV(newLineReplaced)
    return newLineReplaced

#%@_@% space _@%@_ new record
@timer(1,1)
def main():
        writer = csv.writer(f2, delimiter='|', quoting=csv.QUOTE_NONE, lineterminator='\n',escapechar='~')
        #writer.writerow(['col_1', 'col_2', 'col_3', 'col_4', 'col_5', 'col_6', 'col_7'])
        writer.writerow(['|TAG:', '|TAG_VALUE_1:', 'TAG_VALUE_2'])
        nonEmptyData = list(filter(None, theData))[0]
        totalLength = len(nonEmptyData)
        #writer.writerow(nonEmptyData)  
        print('lenght : ', totalLength)    
        for i in range(0, totalLength):
            row = nonEmptyData[i]
            splitted = row.split('|')
            #print('i val : ', i, '\nrow::::::::: ', splitted)
            #print(nonEmptyData)

            #c1 = splitted[0]
            #c2 = splitted[1]
            #c3 = splitted[2]
            #c4 = splitted[3]
            #c5 = splitted[4]
            c6 = doAllConversions(splitted[5])
            #c7 = splitted[6]

            #joined = [c1, c2, c3, c4, c5, c6, c7]
            writer.writerow([c6]) #write joined

f1.close()
f2.close()







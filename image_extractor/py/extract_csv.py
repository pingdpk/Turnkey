import csv
import timeit


inputFilePath = "/Users/a-5156/DeepShared/Turnkey/output/3x5K_1.txt"
outputFilePath = "/Users/a-5156/DeepShared/Turnkey/output/MainFilePiped_out.csv"


def timer(number, repeat):
    def wrapper(func):
        runs = timeit.repeat(func, number=number, repeat=repeat)
        print(func.__name__ , ' : ' , sum(runs) / len(runs))
    return wrapper     

f1=open(inputFilePath, "r", newline='') 
f2=open(outputFilePath, "w")

#self = {'file' : "/DeepShared/Turnkey/output/3x5K_1.txt"}

def read_file():
    with open("/Users/a-5156/DeepShared/Turnkey/output/3x5K_1.txt", 'r') as f:
        data = [row for row in csv.reader(f.read().replace('%@_@%', '|').replace('_@%@_', '\n').splitlines(), dialect=csv.excel, delimiter='\n')]
    return data

def replaceSpaceAndNewLine():
    replacedData = []
    for line in f1:
        splitted = line.replace('%@_@%', '|').replace('_@%@_', '\n').splitlines()
        replacedData.append(list(filter(None, splitted)))
        return replacedData

def getBytesFromHexa(hexa):
    return bytes.fromhex(hexa)

def getDecodedFromArabic(data):
    return data.decode('iso-8859-6')

def putToListForCSV(data):
    c = [data.splitlines()]
    print(c[0])

def doAllConversions(ref_num, hexaRow):
    binaryRow = getBytesFromHexa(hexaRow)
    isoToUTF = getDecodedFromArabic(binaryRow)
    newLineReplaced = isoToUTF.replace('\n:', ref_num+':').replace('\r\n', ':')
    return newLineReplaced.split(':')

@timer(1,1)
def main():
        writer = csv.writer(f2, delimiter='|', quoting=csv.QUOTE_NONE, lineterminator='\n',escapechar='~')
        writer.writerow(['TXN_REFERENCE_NUMBER', 'TAG', 'TAG_VALUE_1', 'TAG_VALUE_2'])
        nonEmptyData = list(filter(None, replaceSpaceAndNewLine()))[0]
        totalLength = len(nonEmptyData)
        print('No. of records in raw file : ', totalLength)    
        for i in range(0, totalLength):
            row = nonEmptyData[i]
            splitted = row.split('|')
            c1 = splitted[0]
            #c2 = splitted[1]
            #c3 = splitted[2]
            #c4 = splitted[3]
            #c5 = splitted[4]
            c6 = doAllConversions(c1, splitted[5])
            #c7 = splitted[6]

            #joined = [c1, c2, c3, c4, c5, c6, c7]
            writer.writerow(c6) #write joined

f1.close()
f2.close()

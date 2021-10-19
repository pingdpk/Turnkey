# @Program   : Image Extractor 
# @Usage     : To extract image content and then to convert to human readable table format
# @Auther    : Deepak Edakkott
# @Date      : 22nd July 2021
# @Version   : v3.0 (Multi-processing integrated)


import timeit
from multiprocessing.pool import Pool

inputFilePath = "/Users/a-5156/DeepShared/Turnkey/output/3x5K_1.txt"
outputFilePath = "/Users/a-5156/DeepShared/Turnkey/output/MainFilePiped_out.csv"
#inputFilePath = "/DeepShared/Turnkey/input/hexadecimal_inputfile_provided.txt"
#outputFilePath = "/DeepShared/Turnkey/output/image_extractor.csv"
inputDelimiter_space = ''
inputDelimiter_newLine = '' #move to helperConfig file


def timer(number, repeat):
    def wrapper(func):
        runs = timeit.repeat(func, number=number, repeat=repeat)
        print(func.__name__ , ' : ' , sum(runs) / len(runs))
    return wrapper     

f1=open(inputFilePath, "r") 
f2=open(outputFilePath, "w")
convertedLine=''


def getBytesFromHexa(hexa):
    return bytes.fromhex(hexa)

def getDecodedFromArabic(data):
    return data.decode('iso-8859-6')


def doAllConversions(ref_num, hexaRow):
    binaryRow = getBytesFromHexa(hexaRow)
    isoToUTF = getDecodedFromArabic(binaryRow)
    newLineReplaced = isoToUTF.replace('\r\n', '|').replace('|:', '\n'+ref_num+':').replace('|', ':')
    return newLineReplaced

def getConvertedLine(line):
    converted = ''
    if line.rstrip():
        actualData = line.split('%@_@%')
        ref_num = actualData[0]
        requiredContent = actualData[5]
        converted = doAllConversions(ref_num, requiredContent)
    return converted

fullFile = f1.read()
replacedData = []
splitted = fullFile.replace('\n','').split('_@%@_')
print(len(splitted)-1)

def doImageExtraction(line):
    global convertedLine
    convertedLine += getConvertedLine(line)

#Main here
@timer(1,1)
def main():
    if __name__ == '__main__':
        with Pool() as pool:
            pool.starmap(doImageExtraction, [(line) for line in splitted])


output = 'TXN_REFERENCE_NUMBER:TAG:TAG_VALUE_1:TAG_VALUE_2'
output += convertedLine
f2.write(output) #if content then write else error

f1.close
f2.close


# Required for Windows:
if __name__ == '__main__':
    main()
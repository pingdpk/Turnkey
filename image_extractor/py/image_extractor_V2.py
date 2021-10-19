# @Program   : Image Extractor
# @Usage     : To extract image content and then to convert to human readable format
# @Auther    : Deepak Edakkott
# @Date      : 22nd July 2021
# @Version   : v2.0


import timeit


inputFilePath = "/DeepShared/Turnkey/input/hexadecimal_inputfile_provided.txt"
outputFilePath = "/DeepShared/Turnkey/output/image_extractor.csv"


def timer(number, repeat):
    def wrapper(func):
        runs = timeit.repeat(func, number=number, repeat=repeat)
        print(func.__name__ , ' : ' , sum(runs) / len(runs))
    return wrapper     

f1=open(inputFilePath, "r") 
f2=open(outputFilePath, "w")


def getBytesFromHexa(hexa):
    return bytes.fromhex(hexa)

def getDecodedFromArabic(data):
    return data.decode('iso-8859-6')


def doAllConversions(ref_num, hexaRow):
    binaryRow = getBytesFromHexa(hexaRow)
    isoToUTF = getDecodedFromArabic(binaryRow)
    newLineReplaced = isoToUTF.replace('\r\n', '|').replace('|:', '\n'+ref_num+':').replace('|', ':')
    return newLineReplaced


fullFile = f1.read()
replacedData = []
splitted = fullFile.replace('\n','').split('_@%@_')
print(len(splitted)-1)

#Main here
@timer(1,1)
def main():
    output = 'TXN_REFERENCE_NUMBER:TAG:TAG_VALUE_1:TAG_VALUE_2'
    for line in splitted:
        if line.rstrip():
            actualData = line.split('%@_@%')
            ref_num = actualData[0]
            requiredContent = actualData[5]
            converted = doAllConversions(ref_num, requiredContent)
            output += converted

    f2.write(output)

f1.close
f2.close
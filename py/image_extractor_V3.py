# @Program   : Image Extractor
# @Usage     : To extract image content and then to convert to human readable table format
# @Auther    : Deepak Edakkott
# @Date      : 16th Aug 2021
# @Version   : v3.0


import timeit
from datetime import datetime


# ------- These can be change if required ------->>>

#inputFilePath = "/DeepShared/Turnkey/input/hexadecimal_inputfile_provided.txt"
#outputFilePath = "/DeepShared/Turnkey/output/image_extractor.csv"

inputFilePath = "/Users/a-5156/DeepShared/Turnkey/output/3x5K_1.txt"
outputFilePath = "/Users/a-5156/DeepShared/Turnkey/output/MainFilePiped_out.csv"

inputFile_space = '%@_@%'
inputFile_newLine = '_@%@_'
# output delimter : should provide a character which will not be already present in the input file
output_delimiter = '|' 

# column names : Should not change format/position/add/remove. You can change name/spelling/capitalize..
column_names = 'uti' + output_delimiter                     #column heading 1
column_names += 'msg_type' + output_delimiter               #column heading 2
column_names += 'msg_fmt' + output_delimiter                #column heading 3
column_names += 'instance' + output_delimiter               #column heading 4
column_names += 'msg_size' + output_delimiter               #column heading 5
column_names += 'create_datetime' + output_delimiter        #column heading 6
column_names += 'TXN_REFERENCE_NUMBER' + output_delimiter   #column heading 7
column_names += 'TAG' + output_delimiter                    #column heading 8
column_names += 'TAG_VALUE_1' + output_delimiter            #column heading 9
column_names += 'TAG_VALUE_2' + output_delimiter            #column heading 10
column_names += 'TAG_VALUE_3' + output_delimiter            #column heading 11
column_names += 'TAG_VALUE_4' + output_delimiter            #column heading 12
column_names += 'TAG_VALUE_5' + output_delimiter            #column heading 13

# ------- These can be change if required -------<<<

process_start_time = str(datetime.now())
process_total_time_taken = ''


f1=open(inputFilePath, "r") 
f2=open(outputFilePath, "w")


def timer(number, repeat):
    def wrapper(func):
        runs = timeit.repeat(func, number=number, repeat=repeat)
        global process_total_time_taken 
        process_total_time_taken = str(sum(runs) / len(runs))
    return wrapper     



def getBytesFromHexa(hexa):
    return bytes.fromhex(hexa)


def getDecodedFromArabic(data):
    return data.decode('iso-8859-6')



def makeFirstSevenColumns(actualData):
    firstSevenColumns = actualData[0] + '|'     #column 1
    firstSevenColumns += actualData[1] + '|'    #column 2
    firstSevenColumns += actualData[2] + '|'    #column 3
    firstSevenColumns += actualData[3] + '|'    #column 4
    firstSevenColumns += actualData[4] + '|'    #column 5
    firstSevenColumns += actualData[6] + '|'    #column 6
    firstSevenColumns += actualData[0] + '|'    #column 7
    return firstSevenColumns



def doAllConversions(actualData):
    firstSevenColumns = makeFirstSevenColumns(actualData)
    hexaContent = actualData[5]
    
    binaryRow = getBytesFromHexa(hexaContent)
    isoToUTF = getDecodedFromArabic(binaryRow)
    
    # column 8 to last column are created and first seven columns included to it, here
    return isoToUTF.replace('\r\n', '~~')\
                                .replace('~~:', '###')\
                                .replace(':', output_delimiter)\
                                .replace('~~', output_delimiter)\
                                .replace('###', '\n' + firstSevenColumns)



fullFile = f1.read()
replacedData = []
splitted = fullFile.replace('\n','').split(inputFile_newLine)
#print(len(splitted)-1)



@timer(1,1)
def main():
    output = column_names
    for line in splitted:
        if line.rstrip():
            actualData = line.split(inputFile_space)
            converted = doAllConversions(actualData)
            output += converted

    f2.write(output)



f1.close
f2.close



process_end_time = str(datetime.now())
process_total_time_taken



print('Start time : ' + process_start_time + \
        '\nEnd time : ' + process_end_time + \
        '\nTotal time taken : ' + process_total_time_taken)
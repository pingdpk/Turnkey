# @Program   : Image Extractor
# @Usage     : To extract image content and then to convert to human readable table format
# @Auther    : Deepak Edakkott
# @Date      : 16th Aug 2021
# @Version   : v4.0


import timeit
from datetime import datetime
import argparse
import os
import logging


# ------- These can be change if required ------->>>
# base_path is used to create required directories (log, processed, etc)
# if base_path is empty or no permission, current path of `this program` will take as base_path
base_path = '' 
processed_dir_name = 'processed'
not_processed_dir_name = 'unprocessed'
log_dir_name = 'log'
output_dir_name = 'output'

input_file_space = '%@_@%'
input_file_new_line = '_@%@_'
# output delimter : should provide a character which will not be already present in the input file
output_delimiter = '|' 
output_file_extension = '.csv'
log_file_name = 'image_extractor.log'

no_error = True

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
column_names += 'TAG_VALUE_5'                               #column heading 13
# ------- These can be change if required -------<<<



# ------- Get file name from given path ---------->>>>
def getFileName(filePath):
    return os.path.basename(filePath)
# ------- Get file name from given path ----------<<<<


# ------- Getting arguments -------->>>
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help = "Input file path", required=True)
args = parser.parse_args()
inputFilePath = args.input
# ------- Getting arguments --------<<<


# ------- Logging ------->>>>
logDir = os.path.join(base_path, log_dir_name) #with user given path
if not base_path or not os.access(logDir, os.W_OK): 
    base_path = os.path.dirname(os.path.realpath(__file__))
    logDir = os.path.join(base_path, log_dir_name) #with current directory path
if not os.path.exists(logDir):
    os.makedirs(logDir)

logging.basicConfig(filename=os.path.join(logDir, log_file_name), level=logging.DEBUG, 
                    format=getFileName(inputFilePath) + ' | %(asctime)s | %(levelname)s | %(name)s | %(message)s')
logger = logging.getLogger(__name__)
# ------- Logging -------<<<<<


# ------- Time taken for processing file --------->>>>
process_start_time = str(datetime.now())
time_key = datetime.now().strftime("%Y%m%d%H%M%S")
process_total_time_taken = ''

def timer(number, repeat):
    def wrapper(func):
        runs = timeit.repeat(func, number=number, repeat=repeat)
        global process_total_time_taken 
        process_total_time_taken = str(sum(runs) / len(runs))
    return wrapper     
# ------- Time taken for processing file ---------<<<<



# ------- Make 'output' directory ------->>>>
outputDir = os.path.join(base_path, output_dir_name) #with user given path
if not base_path or not os.access(outputDir, os.W_OK): 
    base_path = os.path.dirname(os.path.realpath(__file__))
    outputDir = os.path.join(base_path, output_dir_name) #with current directory path
if not os.path.exists(outputDir):
    os.makedirs(outputDir)
# ------- Make 'output' directory -------<<<<<



# ------- Make 'processed' directory ------->>>>
processedDir = os.path.join(base_path, processed_dir_name) #with user given path
if not base_path or not os.access(processedDir, os.W_OK): 
    base_path = os.path.dirname(os.path.realpath(__file__))
    processedDir = os.path.join(base_path, processed_dir_name) #with current directory path
if not os.path.exists(processedDir):
    os.makedirs(processedDir)
# ------- Make 'processed' directory -------<<<<<


# ------- Make 'unprocessed' directory ------->>>>
def getUnProcessedDir():
    global base_path
    unProcessedDir = os.path.join(base_path, not_processed_dir_name) #with user given path
    if not base_path or not os.access(unProcessedDir, os.W_OK): 
        base_path = os.path.dirname(os.path.realpath(__file__))
        unProcessedDir = os.path.join(base_path, not_processed_dir_name) #with current directory path
    if not os.path.exists(unProcessedDir):
        os.makedirs(unProcessedDir)
    return unProcessedDir
# ------- Make 'unprocessed' directory -------<<<<<



# ------- Open input & output files ------->>>>
outputFilePath = os.path.join(outputDir, \
                getFileName(inputFilePath).replace('.', '_')  \
                + '__out_' \
                + time_key \
                + output_file_extension)

f1=open(inputFilePath, "r") 
f2=open(outputFilePath, "w")
# ------- Open input & output files -------<<<<





# -------- Actual file execution starts from here -------
fullFile = f1.read()
replacedData = []
splitted = fullFile.replace('\n','').split(input_file_new_line)
total_number_of_records = str(len(splitted)-1)


def getBytesFromHexa(hexa):
    return bytes.fromhex(hexa)


def getDecodedFromArabic(data):
    return data.decode('iso-8859-6')


def makeFirstSevenColumns(actualData):
    firstSevenColumns = actualData[0] + output_delimiter     #column 1
    firstSevenColumns += actualData[1] + output_delimiter    #column 2
    firstSevenColumns += actualData[2] + output_delimiter    #column 3
    firstSevenColumns += actualData[3] + output_delimiter    #column 4
    firstSevenColumns += actualData[4] + output_delimiter    #column 5
    firstSevenColumns += actualData[6] + output_delimiter    #column 6
    firstSevenColumns += actualData[0] + output_delimiter    #column 7
    return firstSevenColumns


def doAllConversions(actualData):
    firstSevenColumns = makeFirstSevenColumns(actualData)
    hexaContent = actualData[5]
    
    binaryRow = getBytesFromHexa(hexaContent)
    isoToUTF = getDecodedFromArabic(binaryRow)

    # move return to above
    # get full line
    # count number of delimiter 
    # make it 12
    # if didn't worked... put in array, set pipe 12
    # End of each line should have \x0a\x0d
    
    # column 8 to last column are created and first seven columns included to it, here
    singleRecordArr = (isoToUTF.replace('\r\n', '^^^^^^^^^^~~')\
                                .replace('~~:', '###')\
                                .replace(':', output_delimiter)\
                                .replace('~~', output_delimiter)\
                                .replace('###', '\n#~#' + firstSevenColumns)).split('#~#')

    print(' --- ' + str(len(singleRecordArr))) 
    print(' --- ' + str(singleRecordArr[0]) + ' | ' + str(singleRecordArr[3].count('|')))
    return ''.join(singleRecordArr)


@timer(1,1)
def main():
    output = column_names
    try:
        for line in splitted:
            if line.rstrip():
                actualData = line.split(input_file_space)
                converted = doAllConversions(actualData)
                output += converted

        f2.write(output)
    except Exception as e:
        global no_error
        no_error = False
        err_msg = 'Error : Some problem happened.'
        err_msg += ' The input file will be moved to the `' + not_processed_dir_name
        err_msg += '` directory. Please try running this file manually | Exception ::: '
        err_msg += str(e)
        print(err_msg)
        logger.error(err_msg)
        os.replace(inputFilePath, os.path.join(getUnProcessedDir(), getFileName(inputFilePath)))
        

f1.close
f2.close


# -------- Move executed files to 'processed' directory --------->>>>
if os.path.isfile(inputFilePath):
    os.replace(inputFilePath, os.path.join(processedDir, getFileName(inputFilePath)))
    logger.info('The file has been processed successfully and moved to `' + processed_dir_name \
            + '` directory | Output file : ' + getFileName(outputFilePath) \
            + ' | Time taken: ' + process_total_time_taken \
            + ' seconds | No. of records in file: ' + total_number_of_records)
# -------- Move executed files to 'processed' directory ---------<<<<

# Print process details (for manual run)
if no_error:
    process_end_time = str(datetime.now())
    print('\nNo. of records found in file : ' + total_number_of_records)
    print('\nInput file : ' + inputFilePath)
    print('Output file : ' + outputFilePath)
    print('\nStart time : ' + process_start_time + \
            '\nEnd time : ' + process_end_time + \
            '\nTotal time taken : ' + process_total_time_taken)

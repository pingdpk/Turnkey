# @Program   : Image Extractor
# @Usage     : To extract image content and then to convert to human readable table format
# @Auther    : Deepak Edakkott
# @Date      : 26th Aug 2021
# @Version   : v8.0


import timeit
from datetime import datetime
import argparse
import os
import logging
import traceback


# ------- Configurable values ------->>>>>>>>>>>>
# base_path : Used to create required directories (log, processed, etc)
#             if base_path is empty or no permission, current path of `this program` will take as base_path
base_path = '' 
processed_dir_name = 'processed'
not_processed_dir_name = 'unprocessed'
log_dir_name = 'log'
output_dir_name = 'output'

# Delimiter for space and new line in the input file (change this if your input file has different delimiters)
input_file_space = '%@_@%'
input_file_new_line = '_@%@_'

# output delimter : should provide a character which will not be already present in the input file
output_delimiter = '|' 
LF_char = '\\x0a\\x0d'
output_file_extension = '.csv'
output_time_format = '%Y%m%d%H%M%S'

# log_file_format : Automatically the file name will change periodically (each month), so that you can delete unwanted previous logs easily.
log_file_format = datetime.now().strftime('image_extractor' + '_%B%Y.log') 

has_error = False

# decimal_points : How many digits you want to see in the time (seconds)
decimal_points = '{:.6f}'

# keys for getting transaction ID
key1_for_txn = '20'
key2_for_txn = '21'

# For logging
total_number_of_records = 0

# column names : Should not change format/position/add/remove. You can change name/spelling/capitalize..
column_headers = 'uti' + output_delimiter                     #column heading 1
column_headers += 'msg_type' + output_delimiter               #column heading 2
column_headers += 'msg_fmt' + output_delimiter                #column heading 3
column_headers += 'instance' + output_delimiter               #column heading 4
column_headers += 'msg_size' + output_delimiter               #column heading 5
column_headers += 'create_datetime' + output_delimiter        #column heading 6
column_headers += 'TXN_REFERENCE_NUMBER' + output_delimiter   #column heading 7
column_headers += 'TAG' + output_delimiter                    #column heading 8
column_headers += 'TAG_VALUE_1' + output_delimiter            #column heading 9
column_headers += 'TAG_VALUE_2' + output_delimiter            #column heading 10
column_headers += 'TAG_VALUE_3' + output_delimiter            #column heading 11
column_headers += 'TAG_VALUE_4' + output_delimiter            #column heading 12
column_headers += 'TAG_VALUE_5' + output_delimiter            #column heading 13
# ------- Configurable values -------<<<<<<<<<<<<



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

logging.basicConfig(filename=os.path.join(logDir, log_file_format), 
                    level=logging.DEBUG, 
                    format=getFileName(inputFilePath) + ' | %(asctime)s | %(levelname)s | %(name)s | %(message)s')
logger = logging.getLogger(__name__)

# logger.propagate : Set this to False to stop logging (if you found logging is not at all required)
logger.propagate = True
# ------- Logging -------<<<<<


# ------- Time taken for processing file --------->>>>
process_start_time = str(datetime.now())
time_key = datetime.now().strftime(output_time_format)
process_total_time_taken = ''

def timer(number, repeat):
    def wrapper(func):
        runs = timeit.repeat(func, number=number, repeat=repeat)
        global process_total_time_taken 
        process_total_time_taken = str(decimal_points.format(sum(runs) / len(runs)))
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
# ------- Open input & output files -------<<<<


# ------- Close opened file ---------->>>>>>
def closeOpenedFile(f):
    if not f.closed:
        f.close()
# ------- Close opened file ----------<<<<<<


# ------- Common Error Message Format ----------->>>>>>
def getCommonErrorMsg(dirName, err):
        err_msg = 'Error : Some problem happened.'
        err_msg += ' The input file will be moved to the `' + dirName
        err_msg += '` directory. Please try running this file manually'
        err_msg += '| Exception ::: ' + str(err)
        return err_msg

# -------- Actual file execution starts from here -------
def chunked_read(textFile, separator):
    collector = []
    N = len(separator)
    separator_list = [c for c in separator]
    while True:
        char = textFile.read(1) 
        if not char: 
            if collector: 
                yield ''.join(collector)
            break # Nothing more to do

        collector.append(char) 

        if collector[-N:] == separator_list: 
            yield ''.join(collector[:-N])
            collector = []


def getBytesFromHexa(hexa):
    return bytes.fromhex(hexa)


def getDecodedFromArabic(data):
    return data.decode('iso-8859-6')


def makefirstColumns(actualData):
    firstColumns = actualData[0] + output_delimiter     #column 1
    firstColumns += actualData[1] + output_delimiter    #column 2
    firstColumns += actualData[2] + output_delimiter    #column 3
    firstColumns += actualData[3] + output_delimiter    #column 4
    firstColumns += actualData[4] + output_delimiter    #column 5
    firstColumns += actualData[6] + output_delimiter    #column 6
    return firstColumns


def doAllConversions(actualData):
    firstColumns = makefirstColumns(actualData)
    hexaContent = actualData[5]
    binaryRow = getBytesFromHexa(hexaContent)
    decodedRecord = getDecodedFromArabic(binaryRow)
    decodedRecord = (decodedRecord.replace('\r\n', '~~')\
                                .replace('~~:', '\n')\
                                .replace(':', output_delimiter)\
                                .replace('~~', output_delimiter))

    key_txn = ''
    res_lines = []
    for line in decodedRecord.splitlines():
        if(len(line) != 0):
            data = line.split(output_delimiter)
            if data[0] == key1_for_txn or data[0] == key2_for_txn:
                key_txn = data[1]
            res_lines.append(firstColumns + key_txn + output_delimiter + line + LF_char)

    return '\n' + '\n'.join(res_lines)


@timer(1,1)
def main():
    output = column_headers
    try:
        with open(inputFilePath, 'r') as inputTextFile:
            for line in chunked_read(inputTextFile, input_file_new_line):
                if line.rstrip():
                    global total_number_of_records
                    total_number_of_records += 1
                    actualData = line.split(input_file_space)
                    converted = doAllConversions(actualData)
                    output += converted

                    with open(outputFilePath, 'a') as outputTextFile:
                        outputTextFile.write(output)
                    closeOpenedFile(outputTextFile)

        closeOpenedFile(inputTextFile)
        
    except Exception as e:
        closeOpenedFile(outputTextFile)
        global has_error
        has_error = True
        err_msg = getCommonErrorMsg(not_processed_dir_name, e)
        print(err_msg)
        logger.error(err_msg)
        print(traceback.format_exc())
        os.replace(inputFilePath, os.path.join(getUnProcessedDir(), getFileName(inputFilePath)))
        

# -------- Move executed files to 'processed' directory --------->>>>
if os.path.isfile(inputFilePath):
    try:
        os.replace(inputFilePath, os.path.join(processedDir, getFileName(inputFilePath)))
        logger.info('The file has been processed successfully and moved to `' + processed_dir_name \
                    + '` directory | Output file : ' + getFileName(outputFilePath) \
                    + ' | Time taken: ' + process_total_time_taken \
                    + ' seconds | No. of records in file: ' + str(total_number_of_records))
    except Exception as e:
        has_error = True
        err_msg = getCommonErrorMsg(processedDir, e)
        print(err_msg)
        logger.error(err_msg)
        print(traceback.format_exc())

# -------- Move executed files to 'processed' directory ---------<<<<


# Print process details (for manual run)
if not has_error:
    process_end_time = str(datetime.now())
    print('\nNo. of records found in file : ' + str(total_number_of_records))
    print('\nInput file : ' + inputFilePath)
    print('Output file : ' + outputFilePath)
    print('\nStart time : ' + process_start_time + \
            '\nEnd time : ' + process_end_time + \
            '\nTotal time taken : ' + process_total_time_taken + ' seconds')

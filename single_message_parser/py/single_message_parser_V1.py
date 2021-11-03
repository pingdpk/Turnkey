#! /usr/bin/env python3

# @Program   : Single message parser
# @Usage     : To extract binary content and then to convert to human readable table format
# @Auther    : Deepak Edakkott
# @Date      : 17th Oct 2021
# @Version   : v1


import timeit
from datetime import datetime
import argparse
import os
import logging
import traceback
import codecs


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
input_latin = 'iso-8859-6'
input_file_codec = 'iso-8859-6' #'iso-8859-6' # #'Latin-1' #

# output delimter : should provide a character which will not be already present in the input file
output_delimiter = '|'
LF_char = '' # You may provide (will show at the end of each line in the output)
output_file_extension = '.csv'
output_time_format = '%Y%m%d%H%M%S'
output_file_codec = 'utf-8'

# log_file_format : Automatically the file name will change periodically (each month), so that you can delete unwanted previous logs easily.
log_file_format = datetime.now().strftime('single_message_parser' + '_%B%Y.log')

has_error = False

# decimal_points : How many digits you want to see in the time (seconds)
decimal_points = '{:.6f}'

# keys for getting transaction ID
key1_for_txn = '20'
key2_for_txn = '21'

# For logging
total_lines = 0
current_line_num = 0

# column names : Should not change format/position/add/remove. You can change name/spelling/capitalize..
column_headers = 'uti' + output_delimiter                     #column heading 1
column_headers += 'msg_type' + output_delimiter               #column heading 2
column_headers += 'msg_fmt' + output_delimiter                #column heading 3
column_headers += 'instance' + output_delimiter               #column heading 4
column_headers += 'row_number' + output_delimiter             #column heading 5
column_headers += 'msg_tag' + output_delimiter                #column heading 6
column_headers += 'msg_value' + output_delimiter              #column heading 7
column_headers += 'create_datetime'                           #column heading 8
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


# ------- Get number of lines in a file ------------>>>>
def file_len(fname):
    x = os.system("wc -l " + fname)
    return x
# ------- Get number of lines in a file ------------<<<<<<<    


# ------- Common Error Message Format ----------->>>>>>
def getCommonErrorMsg(dirName, err):
        err_msg = '\nError : Some problem happened.'
        err_msg += ' The input file will be moved to the `' + dirName
        err_msg += '` directory. Please try running this file manually'
        err_msg += '| Exception ::: ' + str(err)
        return err_msg

def getDecodedFromArabic(data):
    return data.decode(input_latin)

def convertArrayToText(data):
    global total_lines
    #print("-----\n")
    c = 0
    for i in data:
        #print(str(c) + ") "+ i)
        c += 1
    #print("\n-----")

    row = data[0] + output_delimiter
    row += data[1] + output_delimiter
    row += data[2] + output_delimiter
    row += data[3] + output_delimiter
    row += data[4] + output_delimiter
    row += data[5] + output_delimiter
    row += data[6] + output_delimiter
    i = 7
    for val in data:
        if(i==len(data)-1):
            row += data[i] 
    row += (data[len(data)-1]).replace('_@%@_', '') #you may remove this replace
    total_lines = len(data) + 1
    return row

@timer(1,1)
def main():
    global total_lines
    with codecs.open(outputFilePath, "a", output_file_codec) as outputTextFile:
        outputTextFile.write(column_headers)
    closeOpenedFile(outputTextFile)

    try:
        with codecs.open(inputFilePath, 'r', input_file_codec) as inputTextFile:

            allLines = inputTextFile.readlines()
            fullFileSingleLine = "".join([line.strip() for line in allLines])
            #print(fullFileSingleLine)

            if fullFileSingleLine.rstrip():
                actualData = fullFileSingleLine.split(input_file_space)
                converted = convertArrayToText(actualData)
                #print(actualData)
                #print(converted)

                with codecs.open(outputFilePath, "a", output_file_codec) as outputTextFile:
                    outputTextFile.write("\n" + converted)
                closeOpenedFile(outputTextFile)

        if LF_char:
            with codecs.open(outputFilePath, "a", output_file_codec) as outputTextFile:
                outputTextFile.write(LF_char)
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
                    + ' seconds | No. of records in file: ' + str(total_lines))
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
    print('\nNo. of lines found in file : ' + str(total_lines))
    print('\nInput file : ' + inputFilePath)
    print('Output file : ' + outputFilePath)
    print('\nStart time : ' + process_start_time + \
            '\nEnd time : ' + process_end_time + \
            '\nTotal time taken : ' + process_total_time_taken + ' seconds')

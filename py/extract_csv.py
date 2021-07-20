from timer import timer
import csv
from multiprocessing import Pool, cpu_count

f1=open("/Users/a-5156/DeepShared/Turnkey/output/3x5K_1.txt", "r", newline='') #todo : absolute , encoding='utf8'
f2=open("/Users/a-5156/DeepShared/Turnkey/output/3x5K_out.csv", "w")

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



#%@_@% space _@%@_ new record
@timer(1,1)
def main():
        #print(1)
        # reader = csv.reader(theData, dialect=csv.excel, delimiter='|')   
        # writer = csv.writer(f2, dialect=csv.excel, delimiter='\n', quotechar='"', quoting=csv.QUOTE_ALL)
        # for row in reader:
        #     #print(row)
        #     writer.writerow(row)

        # for row in theData:
        #     print(8)
        #     print(row)
    
    #with open(f2, 'a') as outcsv:   
    #configure writer to write standard csv file
        writer = csv.writer(f2, delimiter='|', quoting=csv.QUOTE_NONE, lineterminator='\n')
        writer.writerow(['col_1', 'col_2', 'col_3', 'col_4', 'col_5', 'col_6', 'col_7'])
        #for item in theData:
            #print(item)   
            #writer.writerow([item])
        #print(theData)  
        nonEmptyData = list(filter(None, theData))[0]
        totalLength = len(nonEmptyData)
        #writer.writerow(nonEmptyData)  
        print('lenght : ', totalLength)    
        for i in range(0, totalLength):
            row = nonEmptyData[i]
            splitted = row.split('|')
            print('i val : ', i, '\nrow::::::::: ', splitted)
            #print(nonEmptyData)
            c1 = splitted[0]
            c2 = splitted[1]
            c3 = splitted[2]
            c4 = splitted[3]
            c5 = splitted[4]
            c6 = splitted[5]
            c7 = splitted[6]
            joined = [c1, c2, c3, c4, c5, c6, c7]
            writer.writerow(joined)

f1.close()
f2.close()







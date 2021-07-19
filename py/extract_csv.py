from timer import timer
import csv
from multiprocessing import Pool, cpu_count

f1=open("/Users/a-5156/DeepShared/Turnkey/output/3x5K_1.txt", "r", newline='') #todo : absolute , encoding='utf8'
f2=open("/Users/a-5156/DeepShared/Turnkey/output/3x5K_out.txt", "w")

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
        data1.append(x)
        #print(x)
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
        writer = csv.writer(f2, delimiter='|', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        writer.writerow(['number', 'text', 'number'])
        #for item in theData:
            #print(item)   
            #writer.writerow([item])
        for i in range(0, len(theData[0])):
            print(theData[0][i])
            writer.writerow(theData[0][i])

f1.close()
f2.close()







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

theData = [['abc|123', 'def|456', ''], []] #replaceSpaceAndNewLine() #read_file()
#print(theData)



#%@_@% space _@%@_ new record
@timer(1,1)
def main():
        writer = csv.writer(f2, delimiter='|', quoting=csv.QUOTE_NONE, lineterminator='\n')
        writer.writerow(['number', 'text', 'number'])
        nonEmptyData = list(filter(None, theData))[0]
        totalLength = len(nonEmptyData)
        #writer.writerow(nonEmptyData)  
        print('nonEmpty : ', nonEmptyData)
        print('lenght : ', totalLength)    
        for i in range(0, totalLength):
            row = nonEmptyData[i]
            splitted = row.split('|')
            print('i val : ', i, '\nrow::::::::: ', splitted)
            #print(nonEmptyData)
            # c1 = splitted[0]
            # c2 = splitted[1]
            # c3 = splitted[2]
            # c4 = splitted[3]
            # c5 = splitted[4]
            # c6 = splitted[5]
            #c7 = splitted[6]
            #joined = [c1, c2, c3, c4, c5, c6, c7]
            writer.writerow(splitted)

f1.close()
f2.close()







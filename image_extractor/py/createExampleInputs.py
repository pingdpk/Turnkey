#../input/bulk_3Records.txt
#../input/example_names.txt
inputF = "../input/bulk_3Records.txt"
outputF = "../output/3x5K_1.txt"
f1=open(inputF, "r", encoding='utf8') 
f2=open(outputF, "a", encoding='utf8')

s=f1.read()

n=int(input("enter how many times you want the file multiplied: "))
data = ''
for i in range(n):
    i+=1
    data += s

f2.write(data)

print('\ninput file : ', inputF)
print('output file : ', outputF)

f1.close()
f2.close()

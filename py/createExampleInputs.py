#../input/bulk_3Records.txt
#../input/example_names.txt
inputF = "../input/example_names.txt"
outputF = "../output/3x5K_1.txt"
f1=open(inputF, "r", encoding='utf8') 
f2=open(outputF, "w", encoding='utf8')

s=f1.read()

n=int(input("enter how many times you want the file multiplied: "))
for i in range(n):
    i+=1
    f2.write(s)

print('\ninput file : ', inputF)
print('output file : ', outputF)

f1.close()
f2.close()

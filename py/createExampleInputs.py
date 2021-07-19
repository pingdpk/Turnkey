#../input/bulk_3Records.txt
#../input/example_names.txt
f1=open("../input/bulk_3Records.txt", "r", encoding='utf8') 
f2=open("../output/3x5K_1.txt", "w", encoding='utf8')

s=f1.read()

n=int(input("enter how many times you want the file multiplied: "))
for i in range(n):
    i+=1
    f2.write(s)

f1.close()
f2.close()

Z=input()
Y=0
X=''
for x in Z:
 if x.isalpha():X+=x.lower()if Y%2 else x.upper();Y+=1
 else:X+=x
print(X)
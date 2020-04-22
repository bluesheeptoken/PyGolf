V=input
n=int(V())
Z=float('inf')
Y=0
for i in range(n):
 q,v=[int(j)for j in V().split()]
 if q*v<Z:Z=q*v;Y=i+1
print(Y)